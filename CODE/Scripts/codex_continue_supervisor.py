#!/usr/bin/env python3
"""
codex_continue_supervisor.py

Purpose:
Attach to an EXISTING Codex CLI/local session after (or even while) its current
writer is finishing, then keep resuming it until Codex explicitly reports
COMPLETE or BLOCKED.

This script does NOT bypass Codex usage/rate limits. It waits and retries.

Typical use from the same repo directory:
    py .\CODE\Scripts\codex_continue_supervisor.py --repo . --resume-last

Safer, if you know the exact thread/session id:
    py .\CODE\Scripts\codex_continue_supervisor.py --repo . --thread-id <ID>
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


COMPLETE = "SUPERVISOR_STATUS: COMPLETE"
CONTINUE = "SUPERVISOR_STATUS: CONTINUE"
BLOCKED = "SUPERVISOR_STATUS: BLOCKED"

CONTINUE_PROMPT = """Continue the existing task autonomously from the current repository and thread state.

Do not restart completed work. Re-read the original goal from this thread, inspect what has already been completed, continue the remaining work, and validate before claiming completion.

At the very end of this turn, emit exactly one final status line:

SUPERVISOR_STATUS: COMPLETE
only if the full original task is complete and validated;

SUPERVISOR_STATUS: CONTINUE
if useful work still remains and you can continue autonomously;

SUPERVISOR_STATUS: BLOCKED | <brief reason>
only if a genuine Creative-Director-level decision or external authorization is required.

Do not report COMPLETE for partial work.
"""

RATE_LIMIT_PATTERNS = (
    "rate limit",
    "usage limit",
    "limit reached",
    "quota",
    "too many requests",
    "429",
    "try again later",
    "reset",
)

ACTIVE_WRITER_PATTERNS = (
    "active writer",
    "already has a writer",
    "already being written",
    "session is active",
    "thread is active",
)

UUIDISH = re.compile(r"^[0-9a-fA-F-]{20,}$")


def stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str) -> None:
    print(f"[{stamp()}] {msg}", flush=True)


def find_codex() -> str:
    for candidate in ("codex", "codex.cmd", "codex.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    raise SystemExit(
        "Codex CLI was not found on PATH. Install/login to Codex CLI first."
    )


def parse_event(line: str) -> Optional[dict]:
    try:
        value = json.loads(line)
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def extract_agent_text(event: dict) -> Optional[str]:
    if event.get("type") != "item.completed":
        return None

    item = event.get("item")
    if not isinstance(item, dict):
        return None

    if item.get("type") == "agent_message":
        text = item.get("text")
        if isinstance(text, str):
            return text

    content = item.get("content")
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                parts.append(part["text"])
        if parts:
            return "\n".join(parts)

    return None


def parse_status(text: str) -> Tuple[str, Optional[str]]:
    for line in reversed([x.strip() for x in text.splitlines() if x.strip()]):
        if line == COMPLETE:
            return "complete", None
        if line == CONTINUE:
            return "continue", None
        if line.startswith(BLOCKED):
            reason = None
            if "|" in line:
                reason = line.split("|", 1)[1].strip() or None
            return "blocked", reason
    return "unknown", None


def contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(p in lowered for p in patterns)


def save_state(path: Path, *, thread_id: Optional[str], turn: int, status: str) -> None:
    path.write_text(
        json.dumps(
            {
                "thread_id": thread_id,
                "turn": turn,
                "status": status,
                "updated_at": datetime.now().isoformat(timespec="seconds"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def run_turn(
    *,
    codex: str,
    repo: Path,
    prompt: str,
    thread_id: Optional[str],
    resume_last: bool,
    model: Optional[str],
    full_auto: bool,
    log_file: Path,
) -> Tuple[int, Optional[str], str, str]:
    cmd = [codex, "exec", "--json"]

    if model:
        cmd += ["--model", model]
    if full_auto:
        cmd += ["--full-auto"]

    if thread_id:
        cmd += ["resume", thread_id, prompt]
    elif resume_last:
        cmd += ["resume", "--last", prompt]
    else:
        raise RuntimeError("Supervisor requires --thread-id or --resume-last.")

    log("Launching Codex resume turn...")

    proc = subprocess.Popen(
        cmd,
        cwd=str(repo),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    discovered = thread_id
    last_agent_message = ""
    recent_stdout = []

    assert proc.stdout is not None
    for line in proc.stdout:
        recent_stdout.append(line)
        if len(recent_stdout) > 80:
            recent_stdout.pop(0)

        with log_file.open("a", encoding="utf-8") as f:
            f.write(line)

        event = parse_event(line)
        if not event:
            continue

        if event.get("type") == "thread.started":
            candidate = event.get("thread_id")
            if isinstance(candidate, str) and UUIDISH.match(candidate):
                discovered = candidate

        agent_text = extract_agent_text(event)
        if agent_text is not None:
            last_agent_message = agent_text
            print(agent_text, flush=True)

    stderr = proc.stderr.read() if proc.stderr is not None else ""
    rc = proc.wait()

    if stderr:
        with log_file.open("a", encoding="utf-8") as f:
            f.write("\n--- STDERR ---\n")
            f.write(stderr)
            f.write("\n--- END STDERR ---\n")

    combined = stderr + "\n" + "".join(recent_stdout)
    return rc, discovered, last_agent_message, combined


def run_verify(command: str, repo: Path) -> bool:
    log(f"Running verification: {command}")
    result = subprocess.run(command, cwd=str(repo), shell=True)
    if result.returncode == 0:
        log("Verification passed.")
        return True

    log(f"Verification failed with exit code {result.returncode}.")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Continue an existing Codex task until COMPLETE or BLOCKED."
    )
    parser.add_argument("--repo", type=Path, required=True)

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--resume-last",
        action="store_true",
        help=(
            "Resume the most recent Codex session for this working directory. "
            "Run from the same repo used by the existing task."
        ),
    )
    source.add_argument(
        "--thread-id",
        help="Resume this exact Codex session/thread ID.",
    )

    parser.add_argument("--model", help="Optional model override.")
    parser.add_argument(
        "--max-turns",
        type=int,
        default=20,
        help="Maximum successful continuation turns. Default: 20.",
    )
    parser.add_argument(
        "--retry-minutes",
        type=int,
        default=15,
        help="Wait between usage/rate-limit retries. Default: 15 minutes.",
    )
    parser.add_argument(
        "--active-writer-retry-seconds",
        type=int,
        default=60,
        help=(
            "If the original Codex turn is still active, wait this many seconds "
            "before trying again. Default: 60."
        ),
    )
    parser.add_argument(
        "--max-wait-hours",
        type=float,
        default=6.0,
        help="Maximum cumulative wait for limits/active writer. Default: 6 hours.",
    )
    parser.add_argument(
        "--verify-command",
        help=(
            "Optional local command that must exit 0 before COMPLETE is accepted."
        ),
    )
    parser.add_argument(
        "--full-auto",
        action="store_true",
        help="Pass --full-auto to Codex CLI.",
    )
    args = parser.parse_args()

    repo = args.repo.expanduser().resolve()
    if not repo.is_dir():
        raise SystemExit(f"Repository not found: {repo}")
    if args.max_turns < 1:
        raise SystemExit("--max-turns must be >= 1")
    if args.retry_minutes < 1:
        raise SystemExit("--retry-minutes must be >= 1")
    if args.active_writer_retry_seconds < 5:
        raise SystemExit("--active-writer-retry-seconds must be >= 5")
    if args.max_wait_hours < 0:
        raise SystemExit("--max-wait-hours must be >= 0")

    codex = find_codex()

    # Keep supervisor bookkeeping outside Git tracking.
    git_dir = repo / ".git"
    supervisor_dir = git_dir / "codex-supervisor" if git_dir.is_dir() else repo / ".codex-supervisor"
    supervisor_dir.mkdir(parents=True, exist_ok=True)
    state_file = supervisor_dir / "state.json"
    log_file = supervisor_dir / "supervisor.log"

    thread_id = args.thread_id
    resume_last = bool(args.resume_last)

    total_wait = 0.0
    max_wait = args.max_wait_hours * 3600.0
    completed_turns = 0
    attempt = 0

    if thread_id:
        log(f"Will supervise exact Codex thread: {thread_id}")
    else:
        log("Will supervise the most recent Codex session for this repository.")

    while completed_turns < args.max_turns:
        attempt += 1

        rc, discovered, last_message, diagnostics = run_turn(
            codex=codex,
            repo=repo,
            prompt=CONTINUE_PROMPT,
            thread_id=thread_id,
            resume_last=resume_last,
            model=args.model,
            full_auto=args.full_auto,
            log_file=log_file,
        )

        if discovered:
            # Once Codex tells us the exact id, stop relying on --last.
            thread_id = discovered
            resume_last = False

        if rc != 0:
            if contains_any(diagnostics, ACTIVE_WRITER_PATTERNS):
                if total_wait >= max_wait:
                    save_state(
                        state_file,
                        thread_id=thread_id,
                        turn=completed_turns,
                        status="active_writer_timeout",
                    )
                    log("Maximum wait reached while another writer remained active.")
                    return 5

                delay = min(args.active_writer_retry_seconds, max_wait - total_wait)
                log(
                    f"The existing Codex task still appears active. "
                    f"Waiting {delay:.0f}s before retrying."
                )
                save_state(
                    state_file,
                    thread_id=thread_id,
                    turn=completed_turns,
                    status="waiting_for_active_writer",
                )
                time.sleep(delay)
                total_wait += delay
                continue

            if contains_any(diagnostics, RATE_LIMIT_PATTERNS):
                if total_wait >= max_wait:
                    save_state(
                        state_file,
                        thread_id=thread_id,
                        turn=completed_turns,
                        status="rate_limit_timeout",
                    )
                    log("Maximum rate/usage-limit wait reached.")
                    return 2

                delay = min(args.retry_minutes * 60, max_wait - total_wait)
                log(
                    f"Codex appears usage/rate limited. "
                    f"Waiting {delay / 60:.0f} minutes before retrying."
                )
                save_state(
                    state_file,
                    thread_id=thread_id,
                    turn=completed_turns,
                    status="waiting_for_limit_reset",
                )
                time.sleep(delay)
                total_wait += delay
                continue

            save_state(
                state_file,
                thread_id=thread_id,
                turn=completed_turns,
                status=f"codex_error_{rc}",
            )
            log(f"Codex exited with code {rc}. Stopping safely.")
            return rc or 1

        completed_turns += 1
        status, reason = parse_status(last_message)
        save_state(
            state_file,
            thread_id=thread_id,
            turn=completed_turns,
            status=status,
        )

        if status == "blocked":
            log(f"Codex reported BLOCKED{': ' + reason if reason else ''}.")
            return 3

        if status == "complete":
            if args.verify_command and not run_verify(args.verify_command, repo):
                log("Codex reported COMPLETE, but verification failed. Continuing.")
                continue

            save_state(
                state_file,
                thread_id=thread_id,
                turn=completed_turns,
                status="complete",
            )
            log("TASK COMPLETE.")
            return 0

        if status == "continue":
            log("Codex reports more work remains. Resuming same thread.")
        else:
            log(
                "No recognized status line found. Treating the task as incomplete "
                "and resuming the same thread."
            )

    save_state(
        state_file,
        thread_id=thread_id,
        turn=completed_turns,
        status="max_turns_reached",
    )
    log("Safety turn cap reached before COMPLETE.")
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
