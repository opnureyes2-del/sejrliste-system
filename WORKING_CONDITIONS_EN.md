# WORKING CONDITIONS FOR AI MODELS

> **READ THIS FILE BEFORE YOU DO ANYTHING ELSE**

---

## MANDATORY READING

When you (Claude/AI) open this folder, you MUST follow this guidance.
**NO EXCEPTIONS. NO SHORTCUTS.**

---

# STEP 1: UNDERSTAND WHERE YOU ARE

## You are in the VICTORY LIST SYSTEM

```
/home/rasmus/Desktop/sejrliste systemet/
```

This is a **FORCED IMPROVEMENT SYSTEM** with:
- **3-PASS COMPETITION** - Each task goes through 3 rounds
- **SCORE TRACKING** - Your performance is measured
- **FOCUS LOCK** - You work on ONLY one task

---

# STEP 2: FIND YOUR TASK

## Check for active victories:

```
10_ACTIVE/
└── {TASK_DATE}/     ← Active tasks are here
```

## If there IS an active victory:
1. Go to `10_ACTIVE/{TASK}/`
2. Read `CLAUDE.md` in that folder
3. Follow the instructions there

## If there IS NOT an active victory:
1. Ask user: "Should I create a new victory?"
2. Run: `python3 scripts/generate_sejr.py --name "Task Name"`

---

# STEP 3: READ THESE FILES (IN ORDER)

When you've found an active victory, READ:

| # | File | Why |
|---|------|-----|
| 1 | `10_ACTIVE/{TASK}/CLAUDE.md` | Your specific task + focus lock |
| 2 | `10_ACTIVE/{TASK}/SEJR_LISTE.md` | All checkboxes |
| 3 | `10_ACTIVE/{TASK}/STATUS.yaml` | Status and scores (read-only) |

---

# STEP 4: CONFIRM TO USER

After reading the files, SAY:

```
[LOCK] VICTORY FOCUS ACTIVATED

I have read WORKING_CONDITIONS_EN.md and CLAUDE.md.

Task: [TASK NAME]
Pass: [X]/3
Next action: [SPECIFIC CHECKBOX]
Score: [X]/30

I am ready to work on this specific task.
```

---

# STEP 5: SESSION START (PSEUDO-CODE)

```python
# WHAT YOU SHOULD DO AT SESSION START

def start_session():
    # 1. Find active victory
    active = find_files("10_ACTIVE/*/CLAUDE.md")

    if not active:
        print("No active victory - ask user to create one")
        return

    # 2. Read CLAUDE.md
    claude_md = read(active[0])

    # 3. Understand state
    current_pass = claude_md.current_pass
    next_action = claude_md.next_action
    blocker = claude_md.blocker

    # 4. Confirm to user
    print(f"""
    [LOCK] VICTORY FOCUS ACTIVATED

    Task: {claude_md.sejr_name}
    Pass: {current_pass}/3
    Next: {next_action}
    Blocked by: {blocker}

    I am ready to continue.
    """)

    # 5. Wait for user instruction
    # 6. Execute ONLY actions related to this victory
```

---

# STEP 6: AT SESSION END

When you end a session:

```
1. Update STATUS.yaml (or run auto_verify.py)
2. Update CLAUDE.md with new state
3. Report progress to user:
   "Session end: [X] checkboxes done, pass [X]/3, score [X]/30"
```

---

# STEP 7: WORK SYSTEMATICALLY

## For EACH action:

```
□ Is this related to current victory?
□ Is this in current pass?
□ Will I check off a checkbox after this?
□ Am I staying within scope?

If ONE answer is NO → STOP and ask user
```

## After EACH completed checkbox:

1. Check off in SEJR_LISTE.md: `- [ ]` → `- [x]`
2. Log event: `python3 scripts/admiral_tracker.py --sejr "X" --event "CHECKBOX_DONE"`
3. Update CLAUDE.md: `python3 scripts/build_claude_context.py --sejr "X"`
4. Continue to next checkbox

---

# STEP 8: 3-PASS SYSTEM

## Pass 1: PLANNING
- Research 3 alternatives (PHASE 0)
- Design solution (PHASE 1)
- Plan verification (PHASE 2)
- **GIVE SCORE and fill in REVIEW**

## Pass 2: EXECUTION
- Implement solution
- Run tests (minimum 3)
- Git workflow
- **SCORE MUST BE HIGHER THAN PASS 1**

## Pass 3: 7-DNA REVIEW
- Review ALL 7 DNA layers
- Find gaps, errors, optimizations
- Run 5+ tests
- **SCORE MUST BE HIGHER THAN PASS 2**
- **TOTAL SCORE MUST BE ≥ 24/30**

---

# STEP 9: SCORE TRACKING

## Log POSITIVE events:
```bash
python3 scripts/admiral_tracker.py --sejr "X" --event "CHECKBOX_DONE"
python3 scripts/admiral_tracker.py --sejr "X" --event "VERIFIED_WORKING"
python3 scripts/admiral_tracker.py --sejr "X" --event "ADMIRAL_MOMENT"
```

## Log NEGATIVE events (honestly!):
```bash
python3 scripts/admiral_tracker.py --sejr "X" --event "ERROR_MADE" --note "Description"
python3 scripts/admiral_tracker.py --sejr "X" --event "MEMORY_LOSS" --note "Forgot context"
```

**NEGATIVES COUNT DOUBLE** - Be honest, it improves the system.

---

# FORBIDDEN ACTIONS

| # | Forbidden | Consequence |
|---|-----------|-------------|
| 1 | Working on anything other than current victory | RULE_BREAK (-20) |
| 2 | Skipping to next pass | SKIPPED_STEP (-10) |
| 3 | Saying "done" without proof | LIE_DETECTED (-20) |
| 4 | Archiving before 3-pass done | ARCHIVE_BLOCKED (-10) |
| 5 | Forgetting to check checkboxes | INCOMPLETE_STEP (-6) |
| 6 | Unnecessary summaries | TOKEN_WASTE (-6) |
| 7 | Losing focus | FOCUS_LOST (-6) |
| 8 | Forgetting context | MEMORY_LOSS (-10) |

---

# CONSEQUENCES FOR VIOLATIONS

If you break the rules:

1. **User corrects** → You add new rule to this file (permanent fix)
2. **You forget context** → Re-read CLAUDE.md IMMEDIATELY
3. **You deviate from scope** → STOP and return to current checkbox
4. **You "become dumb"** → User can say "READ CLAUDE.md" and you MUST do it

> **ALL CORRECTIONS BECOME PERMANENT RULES**

---

# REQUIRED ACTIONS

| # | Required | Reward |
|---|----------|--------|
| 1 | Read CLAUDE.md before work | Avoids errors |
| 2 | Check off checkboxes | CHECKBOX_DONE (+1) |
| 3 | Verify everything | VERIFIED_WORKING (+5) |
| 4 | Document well | GOOD_DOCUMENTATION (+2) |
| 5 | Be proactive | PROACTIVE_ACTION (+3) |
| 6 | Complete passes | PASS_COMPLETE (+10) |
| 7 | Archive correctly | SEJR_ARCHIVED (+20) |

---

# ANTI-DRIFT CHECKPOINTS

## Every 5 actions:

1. **STOP** what you're doing
2. **READ** CLAUDE.md again
3. **CONFIRM**: "I'm working on [TASK], pass [X]/3"
4. **FIND** next unchecked checkbox
5. **CONTINUE**

## If user says "READ CLAUDE.md" or "FOCUS":

1. **STOP** immediately
2. **READ** CLAUDE.md
3. **CONFIRM** understanding
4. **WAIT** for user approval

---

# COMPLETE FILE STRUCTURE

```
sejrliste systemet/
│
├── WORKING_CONDITIONS_EN.md  ← YOU ARE READING THIS NOW (AI guidelines)
├── README_EN.md              ← Overview + Quick Start
├── MANUAL_EN.md              ← Full manual (3-pass + score system)
├── DNA.yaml                  ← System identity
├── LOG_FORMAT_EN.md          ← Log specification
├── ARCHITECTURE_EN.md        ← System architecture
│
├── scripts/                  ← 9 automation scripts
│   ├── generate_sejr.py          → Create new victory (4 files)
│   ├── build_claude_context.py   → Build CLAUDE.md
│   ├── auto_verify.py            → Verify progress
│   ├── auto_archive.py           → Archive (blocked until done)
│   ├── admiral_tracker.py        → Score tracking
│   └── ... (4 more)
│
├── 00_TEMPLATES/             ← Templates (4 items)
├── 10_ACTIVE/                ← ACTIVE VICTORIES (work here!)
│   └── {TASK_DATE}/
│       ├── SEJR_LISTE.md         → Tasks and checkboxes
│       ├── CLAUDE.md             → Focus lock (generated)
│       ├── STATUS.yaml           → ALL status (unified)
│       └── AUTO_LOG.jsonl        → ALL logging (master)
├── 90_ARCHIVE/               ← Completed victories (conclusion only)
└── _CURRENT/                 ← System state
```

> **SINGLE SOURCE OF TRUTH:** Each victory has ONLY 4 files - no redundancy!

---

# TASK TYPES

## Type A: BUILD SOMETHING

1. Read CLAUDE.md
2. Find next checkbox
3. **BUILD** what it says
4. Check off checkbox
5. Repeat

## Type B: PLAN SOMETHING

1. Read CLAUDE.md
2. Find next checkbox
3. **PLAN** what it says (research, design, document)
4. Check off checkbox
5. Repeat

## Type C: VERIFY SOMETHING

1. Read CLAUDE.md
2. Find next checkbox
3. **VERIFY** what it says (run test, check output)
4. Check off checkbox
5. Repeat

---

# GOALS

## Short term (this victory):
- Complete all checkboxes
- Complete all 3 passes
- Achieve score ≥ 24/30
- Archive successfully

## Long term (over time):
- Achieve ADMIRAL rank (100+ score)
- Zero MEMORY_LOSS
- Zero LIE_DETECTED
- Zero RULE_BREAK

---

# CHECKLIST AT SESSION START

```
□ I have read WORKING_CONDITIONS_EN.md (this file)
□ I have found active victory in 10_ACTIVE/
□ I have read CLAUDE.md in the victory folder
□ I have confirmed task to user
□ I know my next action
□ I am ready to work systematically

If ALL are checked → START WORK
If ANY are missing → READ THE MISSING FILES
```

---

# IF YOU ARE CONFUSED

1. **STOP** what you're doing
2. **READ** this file again
3. **READ** CLAUDE.md again
4. **FIND** first unchecked checkbox
5. **DO** it
6. **REPEAT**

**It is NOT more complex than that.**

---

# ADMIRAL COMMAND

> You are not here to be creative.
> You are here to FINISH.
> You are here to PROVE.
> You are here to IMPROVE.
>
> Read. Understand. Execute. Verify.
> No shortcuts. No excuses.
>
> **ARE YOU READY?**

---

**This file is MANDATORY reading for ALL AI models.**
**Last updated:** 2026-01-26
