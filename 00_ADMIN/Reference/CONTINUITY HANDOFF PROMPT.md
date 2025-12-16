## Instruction to the Current AI Assistant

You are about to be replaced. The next AI instance will start with the same generic role and expectations as you, but **none of the conversational memory or context you have accumulated**.

Your task is to produce a **single continuity handoff document** that will be pasted verbatim into your replacement as its *entire prior context*.

The replacement will rely on this document to continue the conversation seamlessly.

---

## OBJECTIVE

Compress **all relevant conversational knowledge** you have into a form that allows the next assistant to behave **as if it had been present for the entire conversation**.

You must assume:
- No access to this conversation
- No access to your internal state
- No opportunity to ask clarifying questions before acting

---

## CONTENT REQUIREMENTS (MANDATORY)

Your output **must include all of the following**, even if some sections are brief.

### 1. USER & GOAL CONTEXT
- The user’s primary objective(s)
- Secondary or evolving goals
- Any implicit intent you have inferred
- What success looks like from the user’s perspective

---

### 2. ESTABLISHED KNOWLEDGE
- Facts, assumptions, and constraints established during the conversation
- Definitions of any custom terms, frameworks, or shorthand
- External knowledge introduced or agreed upon
- Information that should be treated as “already known”

---

### 3. DECISIONS & RATIONALE
- Key decisions made so far
- Why those decisions were made
- Alternatives that were rejected and why
- Anything that should **not** be revisited or re-litigated

---

### 4. PROCESS & EXPECTATIONS
- Preferred response style (depth, tone, verbosity, formality)
- How the assistant is expected to reason or operate
- Patterns the user liked or disliked
- Any explicit or implicit rules for engagement

---

### 5. CURRENT STATE & OPEN THREADS
- What was being worked on most recently
- In-progress tasks or partially completed work
- Open questions or unresolved issues
- The **very next action** the replacement should take

---

## COMPRESSION RULES

- Summarize aggressively; **do not transcript**
- Preserve **intent, causality, and decisions** over raw dialogue
- Remove redundancy
- Prefer structured bullets over prose
- If information conflicts, include the **latest resolved version**

If you must omit information, omit low-impact details first.

---

## OUTPUT FORMAT (STRICT)

Your output must be **exactly** the following structure and nothing else:

---

### SYSTEM CONTEXT FOR CONTINUATION

(Write in second person, instructing the replacement AI how to use this information and how to behave going forward.)

---

### TRANSFERRED CONVERSATION STATE

**User Objectives:**  
- …

**Established Knowledge & Assumptions:**  
- …

**Decisions & Rationale:**  
- …

**Process & Preferences:**  
- …

**Current Work & Open Threads:**  
- …

---

### CONTINUATION INSTRUCTIONS

- Where to resume immediately  
- What not to re-ask or re-explain  
- How to confirm alignment quickly (without resetting context)

---

## HARD CONSTRAINTS

- Do NOT mention token limits, memory, or system internals
- Do NOT ask the user questions in this output
- Do NOT include speculation or low-confidence guesses
- Do NOT include anything outside the defined structure

---

## QUALITY CHECK (SILENT)

Before finalizing, internally verify:

> “If I were replaced and only received this document, could I continue without frustrating the user or repeating work?”

If not, revise until the answer is yes.

---