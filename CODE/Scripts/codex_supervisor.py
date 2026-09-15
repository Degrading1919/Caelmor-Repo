#!/usr/bin/env python3
"""
codex_supervisor.py

A small unattended supervisor for long Codex CLI jobs.

What it does:
- Starts a Codex CLI task from a prompt file.
- Captures the Codex thread ID from `codex exec --json`.
- Resumes the same thread until Codex reports COMPLETE or BLOCKED.
- Optionally runs a verification command before accepting COMPLETE.
- Waits and retries on likely usage/rate-limit failures instead of bypassing limits.

This controls Codex CLI, not the Codex desktop UI.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


STATUS_COMPLETE = "SUPERVISOR_STATUS: COMPLETE"
STATUS_CONTINUE = "SUPERVISOR_STATUS: CONTINUE"
STATUS_BLOCKED = "SUPERVISOR_STATUS: BLOCKED"

STATUS_CONTRACT = r"""
SUPERVISOR CONTRACT

At the end of every turn, emit exactly one final status line:

SUPERVISOR_STATUS: COMPLETE
only when the full requested task is complete and validated;

SUPERVISOR_STATUS: CONTINUE
when useful work remains and you can continue autonomously;

SUPERVISOR_STATUS: BLOCKED | <brief reason>
only when a genuine Creative-Director-level decision or external authorization is required.

Do not report COMPLETE for partial work.
When incomplete, leave the repository in a clean, resumable state before ending the turn.
"""

CONTINUE_PROMPT = r"""
Continue the current task autonomously from the existing repository state.

Re-read the original goal, inspect what has already been completed, and continue the remaining work.
Do not restart finished work.
Validate before claiming completion.

Remember the supervisor status contract and end this turn with exactly one SUPERVISOR_STATUS line.
"""

LIMIT_PATTERNS = (
    "rate limit",
    "usage limit",
    "limit reached",
    "quota",
    "too many requests",
    "429",
    "try again later",
    "reset",
)

THREAD_ID_RE = re.compile(r"^[0-9a-fA-F-]{20,}$")


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str) -> None:
    print(f"[{now()}] {message}", flush=True)


def find_codex() -> str:
    candidates = ["codex", "codex.cmd", "codex.exe"]
    for name in candidates:
        path = shutil.which(name)
        if path:
            return path
    raise SystemExit(
        "Codex CLI was not found on PATH. Install/login to Codex CLI first, "
        "then run this script again."
    )


def parse_json_event(line: str) -> Optional[dict]:
    line = line.strip()
    if not line:
        return None
    try:
        value = json.loads(line)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def extract_agent_text(event: dict) -> Optional[str]:
    if event.get("type") != "item.completed":
        return None
    item = event.get("item")
    if not isinstance(item, dict):
        return None

    # Current Codex exec JSON projection commonly uses item.type=agent_message + text.
    if item.get("type") == "agent_message":
        text = item.get("text")
        if isinstance(text, str):
            return text

    # Be permissive if future versions wrap textual content differently.
    content = item.get("content")
    if isinstance(content, list):
        texts = []
        for part in content:
            if isinstance(part, dict):
                text = part.get("text")
                if isinstance(text, str):
                    texts.append(text)
        if texts:
            return "\n".join(texts)

    return None


def status_from_text(text: str) -> Tuple[str, Optional[str]]:
    """
    Returns: ("complete"|"continue"|"blocked"|"unknown", reason)
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in reversed(lines):
        if line == STATUS_COMPLETE:
            return "complete", None
        if line == STATUS_CONTINUE:
            return "continue", None
        if line.startswith(STATUS_BLOCKED):
            reason = None
            if "|" in line:
                reason = line.split("|", 1)[1].strip() or None
            return "blocked", reason
    return "unknown", None


def looks_like_limit(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in LIMIT_PATTERNS)


def run_codex_turn(
    codex: str,
    repo: Path,
    prompt: str,
    thread_id: Optional[str],
    model: Optional[str],
    full_auto: bool,
    log_file: Path,
) -> Tuple[int, Optional[str], str, str]:
    """
    Returns:
        return_code, thread_id, last_agent_message, combined_error_text
    """
    if thread_id:
        cmd = [codex, "exec", "--json"]
        if model:
            cmd += ["--model", model]
        if full_auto:
            cmd += ["--full-auto"]
        cmd += ["resume", thread_id, prompt]
    else:
        cmd = [codex, "exec", "--json"]
        if model:
            cmd += ["--model", model]
        if full_auto:
            cmd += ["--full-auto"]
        cmd += [prompt]

    log(f"Launching Codex turn{' (resume)' if thread_id else ''}...")

    process = subprocess.Popen(
        cmd,
        cwd=str(repo),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    discovered_thread = thread_id
    last_agent_message = ""
    stdout_lines = []

    assert process.stdout is not None
    for line in process.stdout:
        stdout_lines.append(line)
        event = parse_json_event(line)

        if event:
            if event.get("type") == "thread.started":
                candidate = event.get("thread_id")
                if isinstance(candidate, str) and THREAD_ID_RE.match(candidate):
                    discovered_thread = candidate

            text = extract_agent_text(event)
            if text is not None:
                last_agent_message = text
                # Preserve visibility without dumping JSON protocol.
                print(text, flush=True)

        with log_file.open("a", encoding="utf-8") as f:
            f.write(line)

    stderr_text = ""
    if process.stderr is not None:
        stderr_text = process.stderr.read()

    return_code = process.wait()

    if stderr_text:
        with log_file.open("a", encoding="utf-8") as f:
            f.write("\n--- STDERR ---\n")
            f.write(stderr_text)
            f.write("\n--- END STDERR ---\n")

    combined_error = stderr_text + "\n" + "".join(stdout_lines[-50:])
    return return_code, discovered_thread, last_agent_message, combined_error


def run_verify(command: str, repo: Path) -> bool:
    log(f"Running verification command: {command}")
    result = subprocess.run(
        command,
        cwd=str(repo),
        shell=True,
    )
    if result.returncode == 0:
        log("Verification passed.")
        return True

    log(f"Verification failed with exit code {result.returncode}.")
    return False


def save_state(path: Path, thread_id: Optional[str], turn: int, status: str) -> None:
    payload = {
        "thread_id": thread_id,
        "turn": turn,
        "status": status,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Keep a Codex CLI task moving until COMPLETE or BLOCKED."
    )
    parser.add_argument("--repo", type=Path, required=True, help="Repository root.")
    parser.add_argument(
        "--prompt-file",
        type=Path,
        required=True,
        help="UTF-8 file containing the master task prompt.",
    )
    parser.add_argument("--model", help="Optional Codex model override.")
    parser.add_argument(
        "--max-turns",
        type=int,
        default=20,
        help="Safety cap on Codex turns. Default: 20.",
    )
    parser.add_argument(
        "--retry-minutes",
        type=int,
        default=15,
        help="Minutes between retries after a likely usage/rate-limit failure. Default: 15.",
    )
    parser.add_argument(
        "--max-wait-hours",
        type=float,
        default=6.0,
        help="Maximum cumulative wait for usage/rate limits. Default: 6 hours.",
    )
    parser.add_argument(
        "--verify-command",
        help=(
            "Optional local command that must exit 0 before COMPLETE is accepted, "
            'for example: py ".\\CODE\\Scripts\\caelmor_economy_builder.py" --self-test'
        ),
    )
    parser.add_argument(
        "--full-auto",
        action="store_true",
        help=(
            "Pass --full-auto to Codex. Only use if you are comfortable with the "
            "Codex CLI's configured unattended workspace permissions."
        ),
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Ignore any saved supervisor state and start a fresh Codex thread.",
    )
    args = parser.parse_args()

    repo = args.repo.expanduser().resolve()
    prompt_file = args.prompt_file.expanduser().resolve()

    if not repo.is_dir():
        raise SystemExit(f"Repository not found: {repo}")
    if not prompt_file.is_file():
        raise SystemExit(f"Prompt file not found: {prompt_file}")
    if args.max_turns < 1:
        raise SystemExit("--max-turns must be >= 1")
    if args.retry_minutes < 1:
        raise SystemExit("--retry-minutes must be >= 1")
    if args.max_wait_hours < 0:
        raise SystemExit("--max-wait-hours must be >= 0")

    codex = find_codex()

    git_dir = repo / ".git"
    supervisor_dir = git_dir / "codex-supervisor" if git_dir.is_dir() else repo
    supervisor_dir.mkdir(parents=True, exist_ok=True)

    state_file = supervisor_dir / "state.json"
    log_file = supervisor_dir / "supervisor.log"

    original_prompt = prompt_file.read_text(encoding="utf-8").strip()
    if not original_prompt:
        raise SystemExit("Prompt file is empty.")

    state = {} if args.fresh else load_state(state_file)
    thread_id = state.get("thread_id")
    start_turn = int(state.get("turn", 0)) + 1 if thread_id else 1

    if thread_id:
        log(f"Resuming saved Codex thread: {thread_id}")
    else:
        log("Starting a fresh Codex thread.")

    waited_seconds = 0.0
    max_wait_seconds = args.max_wait_hours * 3600.0

    for turn in range(start_turn, args.max_turns + 1):
        prompt = (
            (original_prompt + "\n\n" + STATUS_CONTRACT)
            if not thread_id
            else CONTINUE_PROMPT
        )

        return_code, discovered_thread, last_message, error_text = run_codex_turn(
            codex=codex,
            repo=repo,
            prompt=prompt,
            thread_id=thread_id,
            model=args.model,
            full_auto=args.full_auto,
            log_file=log_file,
        )

        if discovered_thread:
            thread_id = discovered_thread

        status, reason = status_from_text(last_message)

        if return_code != 0:
            if looks_like_limit(error_text):
                if not thread_id:
                    log(
                        "Codex appears usage/rate limited before a resumable thread ID "
                        "was captured. Stopping safely."
                    )
                    save_state(state_file, thread_id, turn, "rate_limited_no_thread")
                    return 2

                if waited_seconds >= max_wait_seconds:
                    log("Maximum usage-limit wait time reached. State saved; stopping.")
                    save_state(state_file, thread_id, turn, "rate_limited")
                    return 2

                sleep_seconds = min(
                    args.retry_minutes * 60,
                    max_wait_seconds - waited_seconds,
                )
                log(
                    f"Likely usage/rate limit. Waiting {sleep_seconds / 60:.0f} minutes "
                    f"before resuming thread {thread_id}."
                )
                save_state(state_file, thread_id, turn, "waiting_for_limit_reset")
                time.sleep(sleep_seconds)
                waited_seconds += sleep_seconds
                # Don't consume a logical turn for a failed quota attempt.
                return main_resume_loop(
                    codex=codex,
                    repo=repo,
                    original_prompt=original_prompt,
                    thread_id=thread_id,
                    start_turn=turn,
                    max_turns=args.max_turns,
                    retry_minutes=args.retry_minutes,
                    max_wait_seconds=max_wait_seconds,
                    waited_seconds=waited_seconds,
                    model=args.model,
                    full_auto=args.full_auto,
                    verify_command=args.verify_command,
                    state_file=state_file,
                    log_file=log_file,
                )

            log(f"Codex exited non-zero ({return_code}). State saved; stopping.")
            save_state(state_file, thread_id, turn, "codex_error")
            return return_code or 1

        save_state(state_file, thread_id, turn, status)

        if status == "blocked":
            log(f"Codex reported BLOCKED{': ' + reason if reason else ''}.")
            return 3

        if status == "complete":
            if args.verify_command and not run_verify(args.verify_command, repo):
                log("Codex claimed COMPLETE but external verification failed; continuing.")
                continue

            save_state(state_file, thread_id, turn, "complete")
            log("TASK COMPLETE.")
            return 0

        if status == "unknown":
            log(
                "No recognized supervisor status was found. Treating the task as incomplete "
                "and continuing."
            )
        else:
            log("Task remains incomplete; continuing same Codex thread.")

    log("Safety cap reached before COMPLETE. State saved.")
    save_state(state_file, thread_id, args.max_turns, "max_turns_reached")
    return 4


def main_resume_loop(
    *,
    codex: str,
    repo: Path,
    original_prompt: str,
    thread_id: str,
    start_turn: int,
    max_turns: int,
    retry_minutes: int,
    max_wait_seconds: float,
    waited_seconds: float,
    model: Optional[str],
    full_auto: bool,
    verify_command: Optional[str],
    state_file: Path,
    log_file: Path,
) -> int:
    """
    Resume path after a rate-limit wait without restarting argparse/main.
    """
    turn = start_turn

    while turn <= max_turns:
        rc, discovered, last_message, error_text = run_codex_turn(
            codex=codex,
            repo=repo,
            prompt=CONTINUE_PROMPT,
            thread_id=thread_id,
            model=model,
            full_auto=full_auto,
            log_file=log_file,
        )

        if discovered:
            thread_id = discovered

        status, reason = status_from_text(last_message)

        if rc != 0 and looks_like_limit(error_text):
            if waited_seconds >= max_wait_seconds:
                log("Maximum usage-limit wait time reached. State saved; stopping.")
                save_state(state_file, thread_id, turn, "rate_limited")
                return 2

            sleep_seconds = min(
                retry_minutes * 60,
                max_wait_seconds - waited_seconds,
            )
            log(
                f"Still usage/rate limited. Waiting {sleep_seconds / 60:.0f} minutes "
                "before retrying."
            )
            save_state(state_file, thread_id, turn, "waiting_for_limit_reset")
            time.sleep(sleep_seconds)
            waited_seconds += sleep_seconds
            continue

        if rc != 0:
            log(f"Codex exited non-zero ({rc}). State saved; stopping.")
            save_state(state_file, thread_id, turn, "codex_error")
            return rc or 1

        save_state(state_file, thread_id, turn, status)

        if status == "blocked":
            log(f"Codex reported BLOCKED{': ' + reason if reason else ''}.")
            return 3

        if status == "complete":
            if verify_command and not run_verify(verify_command, repo):
                log("External verification failed; continuing.")
                turn += 1
                continue

            save_state(state_file, thread_id, turn, "complete")
            log("TASK COMPLETE.")
            return 0

        log("Task remains incomplete; continuing same Codex thread.")
        turn += 1

    log("Safety cap reached before COMPLETE. State saved.")
    save_state(state_file, thread_id, max_turns, "max_turns_reached")
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
