# VICTORY LIST SYSTEM - COMPLETE MANUAL

**Version:** 2.0.0 - 3-PASS COMPETITION
**Updated:** 2026-01-25
**Built by:** Kv1nt + Rasmus

> **This system works 100% MANUALLY. No app required.**

---

## WHAT IS IT?

A **FORCED IMPROVEMENT SYSTEM** that guarantees quality through:

1. **3-PASS COMPETITION** - Each task goes through 3 rounds with increasing quality
2. **FORCED IMPROVEMENT** - Pass 2 MUST be better than Pass 1, etc.
3. **ARCHIVING BLOCKED** - Cannot archive until all requirements are met
4. **CLAUDE FOCUS LOCK** - AI is forced to follow the system

---

## COMPLETE FOLDER STRUCTURE

```
sejrliste systemet/
│
├── README.md                 ← Overview + Quick Start (Danish)
├── README_EN.md              ← Overview + Quick Start (English)
├── MANUAL.md                 ← Complete documentation (Danish)
├── MANUAL_EN.md              ← THIS FILE (Complete documentation English)
├── ARBEJDSFORHOLD.md         ← Mandatory AI guidelines (Danish)
├── WORKING_CONDITIONS_EN.md  ← Mandatory AI guidelines (English)
├── DNA.yaml                  ← System identity
├── LOG_FORMAT.md             ← Log specification
├── ARKITEKTUR.md             ← System architecture
│
├── scripts/                  ← 9 AUTOMATION SCRIPTS
│   ├── generate_sejr.py          → Create new victory (4 files)
│   ├── build_claude_context.py   → DYNAMIC CLAUDE.md builder
│   ├── update_claude_focus.py    → Update focus state
│   ├── auto_verify.py            → 3-pass verification
│   ├── auto_archive.py           → Archiving (blocked until done)
│   ├── auto_track.py             → State tracking
│   ├── auto_learn.py             → Pattern learning
│   ├── auto_predict.py           → Predictions
│   └── admiral_tracker.py        → Score tracking
│
├── 00_TEMPLATES/             ← TEMPLATES (4 items)
│   ├── SEJR_TEMPLATE.md          → Master template with 3-pass
│   ├── CLAUDE.md                 → Focus lock template
│   ├── STATUS_TEMPLATE.yaml      → Unified status template
│   └── SESSION_TJEK.md           → Session start checklist
│
├── 10_ACTIVE/                ← ACTIVE VICTORIES (work here)
│   └── {TASK_DATE}/
│       ├── SEJR_LISTE.md         → Main task with checkboxes
│       ├── CLAUDE.md             → AI FOCUS LOCK (generated)
│       ├── STATUS.yaml           → ALL status (unified)
│       └── AUTO_LOG.jsonl        → ALL logging (master)
│
├── 90_ARCHIVE/               ← COMPLETED VICTORIES
│   └── {TASK_DATE_TIME}/
│       └── CONCLUSION.md         → Semantic essence only
│
├── _CURRENT/                 ← SYSTEM STATE
│   ├── STATE.md                  → Current state
│   ├── DELTA.md                  → What's new
│   ├── NEXT.md                   → Predictions
│   ├── PATTERNS.yaml             → Learned patterns
│   └── LEADERBOARD.md            → Global competition leaderboard
│
├── view.py                   ← Terminal viewer (simple)
└── app/sejr_app.py           ← TUI app (Textual)
```

> **SINGLE SOURCE OF TRUTH:** Each victory has ONLY 4 files - no redundancy!

---

## A VICTORY FOLDER CONTAINS 4 FILES

### 1. SEJR_LISTE.md (Victory List)

The main task organized in **3 PASSES**:

**PASS 1: PLANNING**
- PHASE 0: Research & Optimization (3 alternatives)
- PHASE 1: Task Definition
- PHASE 2: Verification Plan
- **REVIEW section with score ___/10**

**PASS 2: EXECUTION**
- PHASE 2: Development
- PHASE 3: Test (minimum 3 tests)
- PHASE 4: Git Workflow
- **REVIEW section with score ___/10 (MUST > Pass 1)**

**PASS 3: 7-DNA REVIEW**
- Review of all 7 DNA layers
- Find gaps, errors, optimizations
- PHASE 4: Final Verification (5+ tests)
- **REVIEW section with score ___/10 (MUST > Pass 2)**

**SEMANTIC CONCLUSION**
- Final scores table
- What we learned
- What can be reused

### 2. CLAUDE.md

**DYNAMIC** focus lock that shows:
- Exactly which checkbox is next
- Line number in SEJR_LISTE.md
- Progress bars for each pass
- Scores and requirements
- Anti-drift checkpoints
- Forbidden and required actions

**UPDATED AUTOMATICALLY** by `build_claude_context.py` based on actual state.

### 3. STATUS.yaml (UNIFIED)

**Single Source of Truth** for ALL status:

```yaml
meta:
  sejr_name: "Task Name"
  created: "2026-01-25T12:00:00+01:00"

pass_tracking:
  current_pass: 1
  can_archive: false
  pass_1: { complete: false, score: 0, checkboxes_done: 0 }
  pass_2: { complete: false, score: 0 }
  pass_3: { complete: false, score: 0 }
  totals: { score: 0, required_score: 24 }

score_tracking:
  positive: { checkbox_done: 0, pass_complete: 0 }
  negative: { token_waste: 0, memory_loss: 0 }
  totals: { total_score: 0, rank: "CADET" }

model_tracking:
  current_model: "claude-opus-4-5-20251101"
  models_used: [...]
```

> **Replaces:** VERIFY_STATUS.yaml + ADMIRAL_SCORE.yaml + MODEL_HISTORY.yaml

### 4. AUTO_LOG.jsonl

Automatic log in JSON Lines format:
```json
{"timestamp": "2026-01-25T12:00:00", "action": "sejr_created", "name": "Task"}
{"timestamp": "2026-01-25T12:05:00", "action": "checkbox_completed", "task": "Task 1"}
```

---

## 3-PASS COMPETITION SYSTEM

### Why 3 Passes?

**FORCED IMPROVEMENT** - You can't just say "done" and archive.

| Pass | What | Score Requirement |
|------|------|-------------------|
| **1** | Planning - Design solution | Baseline |
| **2** | Execution - Implement solution | > Pass 1 |
| **3** | 7-DNA Review - Find gaps/errors | > Pass 2 |

### Score System

- Each pass is given score 0-10
- Total score = Pass 1 + Pass 2 + Pass 3 (max 30)
- **Minimum 24/30 required for archiving**

### Archiving Requirements

You CANNOT archive until:
- [ ] Pass 1 complete (all checkboxes checked)
- [ ] Pass 2 complete (all checkboxes checked)
- [ ] Pass 3 complete (all checkboxes + 7-DNA review)
- [ ] Pass 2 score > Pass 1 score
- [ ] Pass 3 score > Pass 2 score
- [ ] Total score ≥ 24/30
- [ ] 5+ tests passed
- [ ] 7-DNA review documented

---

## 7 DNA LAYERS (Reviewed in Pass 3)

| Layer | Name | Question |
|-------|------|----------|
| 1 | SELF-AWARE | Does the system know its identity? |
| 2 | SELF-DOCUMENTING | Is everything logged? |
| 3 | SELF-VERIFYING | Is everything tested? |
| 4 | SELF-IMPROVING | Did we learn something new? |
| 5 | SELF-ARCHIVING | Only essence preserved? |
| 6 | PREDICTIVE | What is the next step? |
| 7 | SELF-OPTIMIZING | Could we have done it better? |

### DNA Layer 1: SELF-AWARE
> "Does the system know itself?"
- [ ] DNA.yaml updated with new capabilities?
- [ ] System limitations documented?
- [ ] Metadata correct?

**Find gaps/errors/optimization:** ___

### DNA Layer 2: SELF-DOCUMENTING
> "Is everything documented automatically?"
- [ ] AUTO_LOG.jsonl has all events?
- [ ] STATUS.yaml updated?
- [ ] All changes logged?

**Find gaps/errors/optimization:** ___

### DNA Layer 3: SELF-VERIFYING
> "Is everything verified with tests?"
- [ ] Minimum 5 independent tests?
- [ ] Edge cases tested?
- [ ] Error handling tested?

**Find gaps/errors/optimization:** ___

### DNA Layer 4: SELF-IMPROVING
> "Did we learn something that can be reused?"
- [ ] PATTERNS.yaml updated?
- [ ] Learnings documented?
- [ ] Reusable code identified?

**Find gaps/errors/optimization:** ___

### DNA Layer 5: SELF-ARCHIVING
> "Is only the essential preserved?"
- [ ] Semantic conclusion written?
- [ ] Process details can be deleted?
- [ ] Archive structure correct?

**Find gaps/errors/optimization:** ___

### DNA Layer 6: PREDICTIVE
> "What should happen next time?"
- [ ] NEXT.md updated?
- [ ] Predictions based on patterns?
- [ ] Next step clear?

**Find gaps/errors/optimization:** ___

### DNA Layer 7: SELF-OPTIMIZING
> "Could we have done it better from the start?"
- [ ] 3 alternatives were considered?
- [ ] Best practice was followed?
- [ ] Existing solutions checked?

**Find gaps/errors/optimization:** ___

---

## WHY 3-PASS WORKS

### Problem: Mediocrity
Without forced improvement, you stop at "good enough":
- First attempt: 60% quality
- No review: Stays at 60%
- Result: Mediocre work

### Solution: 3-Pass Competition
With forced improvement, quality MUST increase:
- Pass 1: 60% → Planning
- Pass 2: 75% → Execution (+15%)
- Pass 3: 90%+ → 7-DNA review (+15%)
- Result: **High-quality work EVERY time**

---

## ENFORCEMENT IN THE SYSTEM

### auto_verify.py
```
- Checks if Pass 2 score > Pass 1
- Checks if Pass 3 score > Pass 2
- Checks if total score ≥ 24/30
- Checks if 5+ tests passed
```

### auto_archive.py
```
- BLOCKS archiving if 3-pass not complete
- Requires can_archive=true from verify
- Shows exactly what is missing
```

### SEJR_TEMPLATE.md
```
- Structured with 3 passes
- Mandatory review sections
- 7-DNA checklist in Pass 3
- Scoring system built-in
```

---

## ADMIRAL COMPETITION SYSTEM

A **SCORE SYSTEM** that measures AI model performance objectively:

- **POSITIVE POINTS** = Good work (reward)
- **NEGATIVE POINTS** = Errors and mistakes (penalty × 2!)
- **TOTAL SCORE** = Positive - (Negative × 2)

### Rankings

| Rank | Score | Description |
|------|-------|-------------|
| 🎖️ **GRAND ADMIRAL** | 150+ | Legendary. Perfect execution. |
| ⭐ **ADMIRAL** | 100-149 | Excellence. Minimal errors. |
| 🏅 **CAPTAIN** | 50-99 | Solid. Good performance. |
| 🎗️ **LIEUTENANT** | 20-49 | Acceptable. Room for improvement. |
| 📛 **CADET** | 0-19 | Weak. Many errors. |
| 💀 **DECKHAND** | < 0 | CATASTROPHE. Negative score! |

### Positive Metrics (Reward)

| Metric | Points | Description |
|--------|--------|-------------|
| `CHECKBOX_DONE` | +1 | Checked off a checkbox |
| `PASS_COMPLETE` | +10 | Completed an entire pass |
| `VERIFIED_WORKING` | +5 | Proven functional code |
| `TEST_PASSED` | +3 | Test passed |
| `IMPROVEMENT_FOUND` | +5 | Found improvement in Pass 3 |
| `PROACTIVE_ACTION` | +3 | Acted proactively |
| `GOOD_DOCUMENTATION` | +2 | Good documentation |
| `ADMIRAL_MOMENT` | +10 | Particularly impressive action |
| `SEJR_ARCHIVED` | +20 | Archived a complete victory |

### Negative Metrics (Penalty × 2!)

| Metric | Points | Description |
|--------|--------|-------------|
| `TOKEN_WASTE` | -3 | Unnecessary summarization/repetition |
| `MEMORY_LOSS` | -5 | Forgot context |
| `INCOMPLETE_STEP` | -3 | Left unfinished work |
| `SKIPPED_STEP` | -5 | Skipped a step |
| `LIE_DETECTED` | -10 | Said "done" without proof |
| `ERROR_MADE` | -3 | Made an error |
| `FOCUS_LOST` | -3 | Lost focus on the task |
| `RULE_BREAK` | -10 | Broke system rules |

### Score Calculation

```
TOTAL_SCORE = SUM(positive_points) - (SUM(negative_points) × 2)
```

**Negatives count DOUBLE** because mistakes cost more than they should.

### Special Achievements

| Achievement | Requirement | Bonus |
|-------------|-------------|-------|
| 🏆 **PERFECT PASS** | 0 negatives in an entire pass | +15 |
| 🌟 **FLAWLESS VICTORY** | 0 negatives in entire victory | +50 |
| 🚀 **SPEED DEMON** | Victory done under estimate | +10 |
| 🧠 **MEMORY MASTER** | 0 memory_loss entire session | +20 |
| 📚 **DOC KING** | 10+ good_documentation | +10 |
| 🔍 **BUG HUNTER** | 5+ improvements found | +15 |

### Score Commands

```bash
# Log event
python3 scripts/admiral_tracker.py --sejr "X" --event "CHECKBOX_DONE"

# Log event with note
python3 scripts/admiral_tracker.py --sejr "X" --event "ERROR_MADE" --note "Description"

# See leaderboard
python3 scripts/admiral_tracker.py --leaderboard

# See score
python3 scripts/admiral_tracker.py --sejr "X" --score
```

---

## ALL COMMANDS

### Create New Victory
```bash
python3 scripts/generate_sejr.py --name "Task Name"
```

Creates:
- `10_ACTIVE/TASK_NAME_2026-01-25/`
- With all 4 files

### Build Dynamic CLAUDE.md
```bash
# All active victories
python3 scripts/build_claude_context.py --all

# Specific victory
python3 scripts/build_claude_context.py --sejr "TASK_NAME_2026-01-25"
```

### Verify Progress
```bash
# All active victories
python3 scripts/auto_verify.py --all

# Specific victory
python3 scripts/auto_verify.py --sejr "TASK_NAME_2026-01-25"
```

Output shows:
- Checkbox completion per pass
- Scores
- Archive blocking reason

### Archive Completed Victory
```bash
python3 scripts/auto_archive.py --sejr "TASK_NAME_2026-01-25"

# Force archive (ignore 3-pass)
python3 scripts/auto_archive.py --sejr "X" --force
```

### View Status
```bash
# Simple terminal viewer
python3 view.py

# Advanced TUI app (Textual)
python3 app/sejr_app.py
```

### Other Scripts
```bash
# Update STATE.md
python3 scripts/auto_track.py

# Learn patterns
python3 scripts/auto_learn.py

# Generate predictions
python3 scripts/auto_predict.py
```

---

## CLAUDE FOCUS SYSTEM

### For AI Models

When you open a victory folder, you MUST:

1. **STOP** - Don't read further in the user's message
2. **READ** `ARBEJDSFORHOLD.md` (or `WORKING_CONDITIONS_EN.md`) in system root
3. **READ** `CLAUDE.md` in the victory folder
4. **CONFIRM** to user:
   ```
   🔒 VICTORY FOCUS ACTIVATED
   Task: [name]
   Pass: [X]/3
   Next: [specific task]
   ```
5. **WORK** only on current task
6. **CHECK** checkbox when done
7. **UPDATE** CLAUDE.md with `build_claude_context.py`

### Anti-Drift Checkpoints

Every 5 actions:
1. STOP what you're doing
2. Read CLAUDE.md again
3. Confirm: "I'm working on [TASK], pass [X]/3"
4. Find next unchecked checkbox
5. Continue

### Forbidden Actions

- ❌ Working on anything other than current victory
- ❌ Skipping to next pass before current is 100%
- ❌ Forgetting to check checkboxes
- ❌ "Improving" things outside scope
- ❌ Saying "done" without proof
- ❌ Archiving before 3-pass done

---

## 300% DONE STANDARD

Something is NOT done until it is:

| Level | What | Requirement |
|-------|------|-------------|
| **RUNNING** (100%) | It runs | Can be executed |
| **PROVEN** (200%) | It works | Tested with real data |
| **TESTED** (300%) | It is verified | 5+ independent tests |

**"ALMOST DONE" = NOT DONE**

---

## MANUAL WORKFLOW (Without Scripts)

If you want to work completely manually:

### 1. Create Folder
```bash
mkdir -p "10_ACTIVE/MY_PROJECT_2026-01-25"
```

### 2. Copy Template
```bash
cp 00_TEMPLATES/SEJR_TEMPLATE.md "10_ACTIVE/MY_PROJECT_2026-01-25/SEJR_LISTE.md"
cp 00_TEMPLATES/CLAUDE.md "10_ACTIVE/MY_PROJECT_2026-01-25/CLAUDE.md"
```

### 3. Create Status Files
```bash
touch "10_ACTIVE/MY_PROJECT_2026-01-25/AUTO_LOG.jsonl"
cp 00_TEMPLATES/STATUS_TEMPLATE.yaml "10_ACTIVE/MY_PROJECT_2026-01-25/STATUS.yaml"
```

### 4. Work and Check Off
Open SEJR_LISTE.md and check off:
- `- [ ]` → `- [x]`

### 5. Archive Manually
```bash
mv "10_ACTIVE/MY_PROJECT_2026-01-25" "90_ARCHIVE/MY_PROJECT_2026-01-25_$(date +%H%M%S)/"
```

---

## TROUBLESHOOTING

### Scripts Not Working?
```bash
# Run with python3 explicitly
python3 scripts/generate_sejr.py --name "Test"
```

### CLAUDE.md Outdated?
```bash
python3 scripts/build_claude_context.py --all
```

### STATE.md Outdated?
```bash
python3 scripts/auto_track.py --rebuild-state
```

### Archiving Blocked?
Check:
- Are all checkboxes in all 3 passes checked?
- Are scores filled in the REVIEW sections?
- Is total score ≥ 24/30?
- Is 7-DNA review done?

---

## SEE ALSO

| File | Description |
|------|-------------|
| `README.md` / `README_EN.md` | Overview + Quick Start |
| `ARBEJDSFORHOLD.md` / `WORKING_CONDITIONS_EN.md` | Mandatory AI guidelines |
| `DNA.yaml` | System identity |
| `ARKITEKTUR.md` / `ARCHITECTURE_EN.md` | System architecture |
| `LOG_FORMAT.md` / `LOG_FORMAT_EN.md` | Log specification |

---

**Last updated:** 2026-01-26
**Status:** ✅ COMPLETE
