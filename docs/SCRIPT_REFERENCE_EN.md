# SCRIPT REFERENCE - All 11 Scripts Documented

> **READ THIS** to understand what each script does and when to use it.

---

## OVERVIEW

| Script | Purpose | When Used |
|--------|---------|-----------|
| `generate_sejr.py` | Create new victory | When starting new task |
| `auto_verify.py` | Verify progress | After EVERY change |
| `auto_archive.py` | Archive finished victory | When 3-pass is done |
| `build_claude_context.py` | Build CLAUDE.md | After checkbox changes |
| `update_claude_focus.py` | Update focus state | When task changes |
| `auto_track.py` | Update STATE.md | On state changes |
| `auto_learn.py` | Learn patterns | On victory completion |
| `auto_predict.py` | Generate predictions | On phase completion |
| `admiral_tracker.py` | Track scores | On events |
| `auto_live_status.py` | Live status display | For real-time view |
| `auto_optimize.py` | Auto-optimization | On PHASE 0 |

---

## 1. generate_sejr.py

### Purpose
Creates a new victory folder with all 4 standard files.

### Usage
```bash
python3 scripts/generate_sejr.py --name "My Task"
```

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `--name` | Yes | Name of the victory (used in folder name) |
| `--goal` | No | Description of the goal |

### Output
```
10_ACTIVE/MY_TASK_2026-01-26/
├── SEJR_LISTE.md      ← Main task with checkboxes
├── CLAUDE.md          ← AI focus lock
├── STATUS.yaml        ← Status data
└── AUTO_LOG.jsonl     ← Automatic log
```

### Example
```bash
python3 scripts/generate_sejr.py --name "Fix Login Bug" --goal "Fix login timeout issue"
```

---

## 2. auto_verify.py

### Purpose
Verifies 3-pass progress and checks if victory can be archived.

### Usage
```bash
# Verify all active victories
python3 scripts/auto_verify.py --all

# Verify specific victory
python3 scripts/auto_verify.py --sejr "MY_TASK_2026-01-26"
```

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `--all` | No | Verify all in 10_ACTIVE/ |
| `--sejr` | No | Specific victory folder name |

### Output
```
=== VERIFICATION REPORT ===
Victory: MY_TASK_2026-01-26
Pass 1: 8/10 checkboxes (80%)
Pass 2: 0/12 checkboxes (0%)
Pass 3: 0/15 checkboxes (0%)
Current Pass: 1
Can Archive: NO - Pass 1 not complete
```

### When Used
- After EVERY checkbox you check off
- Before continuing to next pass
- Before attempting to archive

---

## 3. auto_archive.py

### Purpose
Archives a finished victory from 10_ACTIVE/ to 90_ARCHIVE/.

### Usage
```bash
# Normal archiving (blocked if 3-pass not done)
python3 scripts/auto_archive.py --sejr "MY_TASK_2026-01-26"

# Force archiving (ignore 3-pass check)
python3 scripts/auto_archive.py --sejr "MY_TASK_2026-01-26" --force
```

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `--sejr` | Yes | Victory folder name |
| `--force` | No | Ignore 3-pass requirements (NOT recommended) |

### Archiving Requirements
- [ ] Pass 1 complete + reviewed
- [ ] Pass 2 complete + reviewed (score > Pass 1)
- [ ] Pass 3 complete + final verification (score > Pass 2)
- [ ] Total score >= 24/30
- [ ] All 5+ final tests passed

### Output
```
90_ARCHIVE/MY_TASK_2026-01-26_20260126_153000/
├── CONCLUSION.md      ← Semantic essence (only the important stuff)
├── SEJR_DIPLOM.md     ← Achievement certificate
├── STATUS.yaml        ← Final status
└── ARCHIVE_METADATA.yaml
```

---

## 4. build_claude_context.py

### Purpose
Builds dynamic CLAUDE.md based on actual state in STATUS.yaml.

### Usage
```bash
# Build for all active victories
python3 scripts/build_claude_context.py --all

# Build for specific victory
python3 scripts/build_claude_context.py --sejr "MY_TASK_2026-01-26"
```

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `--all` | No | Rebuild all CLAUDE.md files |
| `--sejr` | No | Specific victory |

### When Used
- After you check off checkboxes
- When pass changes
- When scores are updated

---

## 5. update_claude_focus.py

### Purpose
Updates focus state in CLAUDE.md without rebuilding the entire file.

### Usage
```bash
python3 scripts/update_claude_focus.py --sejr "MY_TASK_2026-01-26" --task "Next task description"
```

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `--sejr` | Yes | Victory folder name |
| `--task` | Yes | New focus task |

---

## 6. auto_track.py

### Purpose
Updates _CURRENT/STATE.md with current system state.

### Usage
```bash
python3 scripts/auto_track.py
python3 scripts/auto_track.py --rebuild-state  # Full rebuild
```

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `--rebuild-state` | No | Force full rebuild of STATE.md |

### Output
Updates `_CURRENT/STATE.md` with:
- Number of active victories
- Total checkboxes done
- Current focus
- Last activity

---

## 7. auto_learn.py

### Purpose
Learns patterns from finished victories and updates PATTERNS.yaml.

### Usage
```bash
python3 scripts/auto_learn.py
python3 scripts/auto_learn.py --sejr "MY_TASK_2026-01-26"  # Learn from specific
```

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `--sejr` | No | Learn from specific victory (default: all in archive) |

### Output
Updates `_CURRENT/PATTERNS.yaml` with:
- Reusable patterns
- Learned tips
- Common mistakes to avoid

---

## 8. auto_predict.py

### Purpose
Generates predictions for next steps based on patterns.

### Usage
```bash
python3 scripts/auto_predict.py
```

### Output
Updates `_CURRENT/NEXT.md` with:
- Predicted next tasks
- Suggested improvements
- Risk areas to watch

---

## 9. admiral_tracker.py

### Purpose
Tracks Admiral competition scores and updates leaderboard.

### Usage
```bash
# See leaderboard
python3 scripts/admiral_tracker.py --leaderboard

# Log event
python3 scripts/admiral_tracker.py --sejr "MY_TASK" --event "CHECKBOX_DONE"

# Log event with note
python3 scripts/admiral_tracker.py --sejr "MY_TASK" --event "ERROR_MADE" --note "Forgot verification"

# See score
python3 scripts/admiral_tracker.py --sejr "MY_TASK" --score
```

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `--leaderboard` | No | Show global leaderboard |
| `--sejr` | No | Specific victory |
| `--event` | No | Event type to log |
| `--note` | No | Note for event |
| `--score` | No | Show current score |

### Event Types
**Positive:**
- `CHECKBOX_DONE` (+1)
- `PASS_COMPLETE` (+10)
- `VERIFIED_WORKING` (+5)
- `TEST_PASSED` (+3)
- `ADMIRAL_MOMENT` (+10)
- `SEJR_ARCHIVED` (+20)

**Negative:**
- `TOKEN_WASTE` (-6)
- `MEMORY_LOSS` (-10)
- `LIE_DETECTED` (-20)
- `RULE_BREAK` (-20)
- `FOCUS_LOST` (-6)

---

## 10. auto_live_status.py

### Purpose
Shows real-time status in the terminal.

### Usage
```bash
python3 scripts/auto_live_status.py
```

### Output
Live updating display with:
- Active victories
- Current checkboxes
- Scores
- Recent activity

---

## 11. auto_optimize.py

### Purpose
Helps with PHASE 0 optimization - research and alternatives.

### Usage
```bash
python3 scripts/auto_optimize.py --sejr "MY_TASK_2026-01-26"
```

### Output
Suggestions for:
- External research queries
- Internal pattern matches
- 3 alternative approaches

---

## WORKFLOW: Normal Day

```bash
# 1. Start the day - see status
python3 scripts/auto_track.py
python3 view.py

# 2. Find active victory or create new
python3 scripts/generate_sejr.py --name "Today's Task"

# 3. Work on checkboxes...

# 4. After each change - verify
python3 scripts/auto_verify.py --all

# 5. Update CLAUDE.md
python3 scripts/build_claude_context.py --all

# 6. Log events
python3 scripts/admiral_tracker.py --sejr "TODAYS_TASK" --event "CHECKBOX_DONE"

# 7. When done (3-pass complete) - archive
python3 scripts/auto_archive.py --sejr "TODAYS_TASK_2026-01-26"

# 8. Learn from victory
python3 scripts/auto_learn.py
```

---

---

## COMMON ERRORS & SOLUTIONS

### Error 1: "Victory folder not found"
```
[FAIL] Error: No active victory found in 10_ACTIVE/
```
**Solution:** Create a new victory first: `python3 scripts/generate_sejr.py --name "My Task"`

### Error 2: "Archive blocked"
```
[FAIL] ARCHIVE BLOCKED - Total score 23 < 24 required
```
**Solution:** Improve Pass scores. See review sections in SEJR_LISTE.md for what can be improved.

### Error 3: "CLAUDE.md outdated"
```
[WARN] Warning: CLAUDE.md does not reflect current STATUS.yaml
```
**Solution:** Rebuild: `python3 scripts/build_claude_context.py --all`

### Error 4: "Permission denied"
```
[FAIL] Permission denied: scripts/generate_sejr.py
```
**Solution:** Make script executable: `chmod +x scripts/generate_sejr.py`

### Error 5: "Missing dependency"
```
[FAIL] ModuleNotFoundError: No module named 'yaml'
```
**Solution:** Scripts don't use PyYAML - they have simple YAML parser built-in. Check file paths.

---

**Last updated:** 2026-01-31
**Version:** 3.0.0 (PASS 2 - added Common Errors)
