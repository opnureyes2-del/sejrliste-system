# VICTORY LIST SYSTEM (Sejr Liste System)

**Version:** 2.1.0 - SINGLE SOURCE OF TRUTH
**Updated:** 2026-01-25
**DNA Layers:** 7 (SELF-AWARE → SELF-OPTIMIZING)

---

## WHAT IS IT?

A **FORCED IMPROVEMENT SYSTEM** that ensures EVERY task goes through 3 passes with increasing quality:

| Pass | Focus | Requirements |
|------|-------|--------------|
| **Pass 1** | Planning | Baseline score |
| **Pass 2** | Execution | Score > Pass 1 |
| **Pass 3** | 7-DNA Review | Score > Pass 2, Total ≥ 24/30 |

**ARCHIVING IS BLOCKED** until all 3 passes are complete with sufficient score.

---

## QUICK START

```bash
cd "/home/rasmus/Desktop/sejrliste systemet"

# 1. Create new victory
python3 scripts/generate_sejr.py --name "My Task"

# 2. Build DYNAMIC CLAUDE.md
python3 scripts/build_claude_context.py --all

# 3. Work on victory in 10_ACTIVE/

# 4. Verify progress (run often!)
python3 scripts/auto_verify.py --all

# 5. Archive when done (blocked until 3-pass complete)
python3 scripts/auto_archive.py --sejr "MY_TASK_2026-01-25"
```

---

## COMPLETE FOLDER STRUCTURE

```
sejrliste systemet/
│
├── README.md                 ← Danish version (Quick Start)
├── README_EN.md              ← You are reading this (English)
├── ADMIRAL.md                ← WHAT IS AN ADMIRAL? (5 qualities)
├── MODEL_ONBOARDING.md       ← AI ONBOARDING (read first as new model!)
├── SCRIPT_REFERENCE.md       ← All 11 scripts documented
├── EKSEMPLER.md              ← 10+ concrete examples
├── ARBEJDSFORHOLD.md         ← COMPLETE GUIDE (AI rules included)
├── MANUAL.md                 ← Full documentation (3-pass + score system)
├── LOG_FORMAT.md             ← Log format specification
├── DNA.yaml                  ← System identity
├── ARKITEKTUR.md             ← System architecture
├── view.py                   ← Terminal viewer (simple)
├── app/sejr_app.py           ← TUI app (Textual - advanced)
│
├── scripts/                  ← Automation (9 scripts)
│   ├── generate_sejr.py          → Create new victory + CLAUDE.md
│   ├── build_claude_context.py   → DYNAMIC CLAUDE.md builder
│   ├── update_claude_focus.py    → Update focus state
│   ├── auto_verify.py            → 3-pass verification
│   ├── auto_archive.py           → Archiving (blocked until done)
│   ├── auto_track.py             → State tracking
│   ├── auto_learn.py             → Pattern learning
│   ├── auto_predict.py           → Predictions
│   └── admiral_tracker.py        → Score tracking + leaderboard
│
├── 00_TEMPLATES/             ← Templates (4 items)
│   ├── SEJR_TEMPLATE.md          → Master template with 3-pass
│   ├── CLAUDE.md                 → Focus lock template
│   ├── STATUS_TEMPLATE.yaml      → Unified status template
│   └── SESSION_TJEK.md           → Session start checklist
│
├── 10_ACTIVE/                ← ACTIVE VICTORIES (work here)
│   └── {TASK_DATE}/
│       ├── SEJR_LISTE.md         → Main task with checkboxes
│       ├── CLAUDE.md             → AI FOCUS LOCK (generated)
│       ├── STATUS.yaml           → UNIFIED (pass + score + model)
│       └── AUTO_LOG.jsonl        → MASTER (all logging)
│
├── 90_ARCHIVE/               ← COMPLETED VICTORIES (conclusion only)
│   └── {TASK_DATE_TIME}/
│       └── CONCLUSION.md         → Semantic essence
│
└── _CURRENT/                 ← System state (5 files)
    ├── STATE.md                  → Current state
    ├── DELTA.md                  → What's new
    ├── NEXT.md                   → Predictions
    ├── PATTERNS.yaml             → Learned patterns
    └── LEADERBOARD.md            → Global competition leaderboard
```

---

## A VICTORY FOLDER CONTAINS

When you create a new victory, you get these **4 files** (Single Source of Truth):

### 1. SEJR_LISTE.md (Victory List)
The main task with all checkboxes organized in 3 passes:
- **Pass 1:** PHASE 0-1-2 (Research, Planning, Verification)
- **Pass 2:** PHASE 2-3-4 (Development, Test, Git)
- **Pass 3:** 7-DNA Review (all 7 layers checked)

### 2. CLAUDE.md
**DYNAMIC** focus lock (generated from STATUS.yaml):
- Exactly which checkbox is next
- Progress bars for each pass
- Scores and requirements
- Anti-drift checkpoints

### 3. STATUS.yaml (UNIFIED)
**Single Source of Truth** for ALL status:
- **Pass tracking:** Completion %, scores, checkboxes
- **Score tracking:** Positive/negative events, rank
- **Model tracking:** Which models worked, sessions
- **Statistics:** Total time, actions, models

### 4. AUTO_LOG.jsonl (MASTER)
**Single Source of Truth** for ALL logging:
- All actions with ISO 8601 timestamps
- Actor info (model_id, model_name, type)
- Terminal output (command, exit_code, stdout/stderr)
- Session tracking

**See `LOG_FORMAT.md` for complete specification.**

> **NO REDUNDANCY:** All data exists in ONLY one place!

---

## 3-PASS COMPETITION SYSTEM

### Pass 1: PLANNING
- Research 3 alternatives (PHASE 0)
- Define the task (PHASE 1)
- Plan verification (PHASE 2)
- **Give score and fill out REVIEW**

### Pass 2: EXECUTION
- Implement solution
- Run tests (minimum 3)
- Git workflow
- **Score MUST be higher than Pass 1**

### Pass 3: 7-DNA REVIEW
- Review ALL 7 DNA layers:
  1. SELF-AWARE - Does the system know itself?
  2. SELF-DOCUMENTING - Is everything logged?
  3. SELF-VERIFYING - Is everything tested?
  4. SELF-IMPROVING - Did we learn something?
  5. SELF-ARCHIVING - Only essence preserved?
  6. PREDICTIVE - What is the next step?
  7. SELF-OPTIMIZING - Could we have done better?
- Run 5+ tests
- **Score MUST be higher than Pass 2**
- **Total score MUST be ≥ 24/30**

---

## ARCHIVING REQUIREMENTS

You CANNOT archive until:
- [ ] All 3 passes complete
- [ ] Pass 2 score > Pass 1 score
- [ ] Pass 3 score > Pass 2 score
- [ ] Total score ≥ 24/30
- [ ] 5+ tests passed
- [ ] 7-DNA review completed

---

## CLAUDE FOCUS SYSTEM

### For AI Models
When Claude opens a victory folder:
1. **READ** `ARBEJDSFORHOLD.md` (mandatory)
2. **READ** `CLAUDE.md` in the victory folder
3. **CONFIRM** understanding to user
4. **WORK** ONLY on current task
5. **CHECK** checkbox when done
6. **UPDATE** CLAUDE.md and continue

### Anti-Drift Checkpoints
Every 5 actions:
- Re-read CLAUDE.md
- Confirm task and pass
- Find next unchecked checkbox
- Continue

---

## SCRIPTS REFERENCE

| Script | Command | Function |
|--------|---------|----------|
| Create victory | `python3 scripts/generate_sejr.py --name "X"` | New victory + all files |
| Build context | `python3 scripts/build_claude_context.py --all` | Dynamic CLAUDE.md |
| Verify | `python3 scripts/auto_verify.py --all` | Check 3-pass status |
| Archive | `python3 scripts/auto_archive.py --sejr "X"` | Archive (if allowed) |
| Track | `python3 scripts/auto_track.py` | Update STATE.md |
| Learn | `python3 scripts/auto_learn.py` | Update PATTERNS.yaml |
| Predict | `python3 scripts/auto_predict.py` | Generate NEXT.md |
| Score | `python3 scripts/admiral_tracker.py --sejr "X"` | Score tracking |

---

## VIEWS (Terminal)

```bash
# Simple terminal viewer
python3 view.py

# Advanced TUI app (Textual)
python3 app/sejr_app.py
```

---

## 🎖️ ADMIRAL COMPETITION SYSTEM

A **SCORE SYSTEM** that measures AI model performance objectively!

### Positive Points (Reward)
| Event | Points |
|-------|--------|
| CHECKBOX_DONE | +1 |
| PASS_COMPLETE | +10 |
| VERIFIED_WORKING | +5 |
| ADMIRAL_MOMENT | +10 |
| SEJR_ARCHIVED | +20 |

### Negative Points (Penalty × 2!)
| Event | Points |
|-------|--------|
| TOKEN_WASTE | -6 |
| MEMORY_LOSS | -10 |
| LIE_DETECTED | -20 |
| RULE_BREAK | -20 |

### Rankings
| Rank | Score |
|------|-------|
| 🎖️ GRAND ADMIRAL | 150+ |
| ⭐ ADMIRAL | 100-149 |
| 🏅 CAPTAIN | 50-99 |
| 🎗️ LIEUTENANT | 20-49 |
| 📛 CADET | 0-19 |
| 💀 DECKHAND | < 0 |

### Commands
```bash
# See leaderboard
python3 scripts/admiral_tracker.py --leaderboard

# Log event
python3 scripts/admiral_tracker.py --sejr "X" --event "CHECKBOX_DONE"

# See score
python3 scripts/admiral_tracker.py --sejr "X" --score
```

See MANUAL.md for full documentation of the score system.

---

**Built by:** Kv1nt + Rasmus
**Date:** 2026-01-25
**Status:** ✅ OPERATIONAL
