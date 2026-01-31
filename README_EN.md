# VICTORY LIST SYSTEM (Sejr Liste System)

**Version:** 3.0.0 - UNIFIED CROSS-DEVICE APP
**Updated:** 2026-01-31
**DNA Layers:** 7 (SELF-AWARE → SELF-OPTIMIZING)
**Built by:** Kv1nt + Rasmus

---

## WHAT IS IT?

A **FORCED IMPROVEMENT SYSTEM** with 3 interfaces (desktop, web, terminal) that ensures EVERY task goes through 3 passes with increasing quality — and the system LEARNS from EVERY completed task.

| Pass | Focus | Requirements |
|------|-------|--------------|
| **Pass 1** | Planning | Baseline score |
| **Pass 2** | Execution | Score > Pass 1 |
| **Pass 3** | 7-DNA Review | Score > Pass 2, Total >= 24/30 |

**ARCHIVING IS BLOCKED** until all 3 passes are complete with sufficient score.

---

## ACCESS — 6 WAYS TO USE THE SYSTEM

### 1. Desktop App (GTK4 Native)
```bash
# Double-click "Sejrliste" on desktop
# Or:
python3 masterpiece_en.py   # English
python3 masterpiece.py       # Danish
```
- Full GNOME integration with Libadwaita
- Sidebar navigation, real-time updates
- 7 DNA layer visualization

### 2. Web App (Browser)
```
http://localhost:8501
```
- Auto-starts at login (systemd service)
- 5 pages: Active Projects, Archive, New Project, Statistics, Settings
- Run scripts directly from UI

### 3. Phone (Tailscale HTTPS)
```
https://rog.tailc9c1c5.ts.net
```
- Secure connection via Tailscale mesh VPN
- Same web app as localhost
- Works EVERYWHERE (not just local WiFi)

### 4. Phone (Local WiFi)
```
http://10.168.6.233:8501
```
- Direct access on same network
- QR code: `bash scripts/show_phone_url.sh`

### 5. Terminal Dashboard
```bash
sejrliste                          # Global command — full system status
bash scripts/sejr_dashboard.sh     # Detailed enforcement dashboard
```

### 6. TUI App (Textual)
```bash
python3 app/sejr_app.py
```
- Steam-style terminal interface
- Keyboard-driven (j/k navigation, Enter to open)
- Real-time file monitoring

---

## QUICK START

```bash
cd "/home/rasmus/Desktop/sejrliste systemet"

# 1. Create new victory
python3 scripts/generate_sejr.py --name "My Task" --goal "What we're building" --tech "Python"

# 2. Work on victory in 10_ACTIVE/

# 3. Verify progress (run often!)
python3 scripts/auto_verify.py --all

# 4. Archive when done (blocked until 3-pass complete)
python3 scripts/auto_archive.py --sejr "MY_TASK_2026-01-31"

# 5. Check system status
sejrliste
```

---

## A VICTORY FOLDER CONTAINS

When you create a new victory, you get these **5 files** (Single Source of Truth):

### 1. PROJECT_BRIEF.md
> READ THIS FIRST. 30 seconds. Complete understanding.
- Goal, success criteria, scope, technology

### 2. SEJR_LISTE.md (Victory List)
The main task with all checkboxes organized in 3 passes:
- **Pass 1:** PHASE 0-1-2 (Research, Planning, Verification)
- **Pass 2:** PHASE 2-3-4 (Development, Test, Git)
- **Pass 3:** 7-DNA Review (all 7 layers checked)

### 3. CLAUDE.md
**DYNAMIC** focus lock (generated + pattern-injected):
- Exactly which checkbox is next
- Top 5 learned patterns from PATTERNS.json
- Anti-drift checkpoints

### 4. STATUS.yaml (UNIFIED)
**Single Source of Truth** for ALL status:
- **Pass tracking:** Completion %, scores, checkboxes
- **Score tracking:** Positive/negative events, rank
- **Model tracking:** Which models worked, sessions

### 5. AUTO_LOG.jsonl (MASTER)
**Single Source of Truth** for ALL logging:
- All actions with ISO 8601 timestamps
- Actor info (model_id, type)
- Session tracking

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
  1. SELF-AWARE — Does the system know itself?
  2. SELF-DOCUMENTING — Is everything logged?
  3. SELF-VERIFYING — Is everything tested?
  4. SELF-IMPROVING — Did we learn something?
  5. SELF-ARCHIVING — Only essence preserved?
  6. PREDICTIVE — What is the next step?
  7. SELF-OPTIMIZING — Could we have done better?
- Run 5+ tests
- **Score MUST be higher than Pass 2**
- **Total score MUST be >= 24/30**

---

## LEARNING SYSTEM (FEEDBACK LOOP)

```
Victory COMPLETE
    |
    v
auto_archive.py → moves to 90_ARCHIVE/
    |
    v
auto_learn.py → scans ALL archived victories
    |           → identifies patterns, bugs, workflows
    |           → stores in PATTERNS.json (52 patterns, growing)
    v
generate_sejr.py → reads top-5 patterns
    |             → injects into new CLAUDE.md as "LEARNED WISDOM"
    |             → tracks applied_count for fair rotation
    v
NEW VICTORY starts with KNOWLEDGE from ALL previous victories
```

**Cron job:** Daily learning at 08:00 (regardless of new victories)

---

## FOLDER STRUCTURE

```
sejrliste systemet/
|
|-- masterpiece.py              # GTK4 desktop app (Danish)
|-- masterpiece_en.py           # GTK4 desktop app (English)
|-- web_app.py                  # Streamlit web app (Danish)
|-- web_app_en.py               # Streamlit web app (English)
|-- start-web.sh                # Wrapper for systemd service
|-- enforcement_engine.py       # Quality enforcement
|-- intro_integration.py        # INTRO folder integration
|-- sejr                        # Global launcher (dashboard)
|-- DNA.yaml                    # System DNA configuration (7 layers)
|
|-- app/                        # TUI terminal app
|   |-- sejr_app.py             # Main TUI (Textual, Steam-style)
|   |-- model_router.py         # AI model routing (ModelType enum)
|   |-- widgets/                # UI components
|   |-- models/                 # Model handler
|   |-- utils/                  # Utilities
|   +-- tests/                  # Test suite (77 tests)
|
|-- scripts/                    # 22 automation scripts + shell scripts
|-- docs/                       # 20 documentation files (DK + EN)
|
|-- pages/                      # Streamlit web pages
|   |-- 1_Aktiv_Sejr.py
|   |-- 2_Arkiv.py
|   |-- 3_Ny_Sejr.py
|   |-- 4_Statistik.py
|   +-- 5_Indstillinger.py
|
|-- 00_TEMPLATES/               # Templates (5 items)
|-- 10_ACTIVE/                  # Active victories (work here)
|-- 90_ARCHIVE/                 # Archived victories (31, 100% Grand Admiral)
|-- _CURRENT/                   # System state (live status, patterns, leaderboard)
|-- DROP_HER/                   # Drop zone (drag-and-drop victory creation)
|-- assets/                     # Icons and graphics
+-- _unused/                    # Inactive code (gitignored)
```

---

## DOCUMENTATION (docs/)

| File | Content |
|------|---------|
| `README.md` | This file — complete overview (root) |
| `docs/MANUAL.md` | Full documentation (3-pass + score) |
| `docs/ADMIRAL.md` | What is an Admiral? (5 qualities) |
| `docs/MODEL_ONBOARDING.md` | AI onboarding (read first as new model) |
| `docs/SCRIPT_REFERENCE.md` | All scripts documented |
| `docs/EKSEMPLER.md` | 10+ concrete examples |
| `docs/ARBEJDSFORHOLD.md` | Complete guide (AI rules) |
| `docs/ARKITEKTUR.md` | System architecture |
| `docs/LOG_FORMAT.md` | Log format specification |
| `docs/PREVENTION_RULES.md` | Prevention rules |
| `docs/INCOMPLETE_CHECK.md` | Incompleteness check |

All documents available in both Danish and English (*_EN.md) in the `docs/` folder.

---

## INFRASTRUCTURE

### Automatic
- **systemd service:** `sejrliste-web.service` — auto-start Streamlit at login
- **Cron 07:55:** Daily health check + repair (52 checks, 12 categories)
- **Cron 08:00:** Daily pattern learning

### Tailscale
- **Desktop ROG:** 100.86.106.42
- **Phone Pixel 9 Pro:** 100.84.174.88
- **HTTPS:** https://rog.tailc9c1c5.ts.net (via Tailscale Serve)
- **Account:** opnureyes2@gmail.com

### Desktop
- **Launcher:** victorylist.desktop (1 file, 3 actions: GTK4 / Web / TUI)
- **Global command:** `sejrliste` (symlinked)

---

## STATISTICS

| Metric | Value |
|--------|-------|
| Archived victories | 31 |
| Average score | 29.9/30 (99.7%) |
| Grand Admiral rate | 100% |
| Learned patterns | 52 |
| Scripts | 22 (active) |
| Interfaces | 3 (GTK4 + Web + TUI) |
| Access methods | 6 |
| DNA layers | 7 |
| Tests | 77/77 PASSED |
| Health checks | 41/41 PASSED |

---

## ADMIRAL COMPETITION SYSTEM

### Positive Points (Reward)
| Event | Points |
|-------|--------|
| CHECKBOX_DONE | +1 |
| PASS_COMPLETE | +10 |
| VERIFIED_WORKING | +5 |
| ADMIRAL_MOMENT | +10 |
| SEJR_ARCHIVED | +20 |

### Negative Points (Penalty x2!)
| Event | Points |
|-------|--------|
| TOKEN_WASTE | -6 |
| MEMORY_LOSS | -10 |
| LIE_DETECTED | -20 |
| RULE_BREAK | -20 |

### Rankings
| Rank | Score |
|------|-------|
| GRAND ADMIRAL | 150+ |
| ADMIRAL | 100-149 |
| CAPTAIN | 50-99 |
| LIEUTENANT | 20-49 |
| CADET | 0-19 |
| DECKHAND | < 0 |

---

**Status:** OPERATIONAL — Cross-device, self-learning, 100% Grand Admiral rate
**Git:** github.com/opnureyes2-del/sejrliste-system
**Test suite:** 77/77 PASSED | **Health check:** 41/41 PASSED
