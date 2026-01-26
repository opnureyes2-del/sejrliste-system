# 📜 SCRIPT REFERENCE - Alle 11 Scripts Dokumenteret

> **LÆS DETTE** for at forstå hvad hvert script gør og hvornår du bruger det.

---

## OVERSIGT

| Script | Formål | Hvornår Bruges |
|--------|--------|----------------|
| `generate_sejr.py` | Opret ny sejr | Når du starter ny opgave |
| `auto_verify.py` | Verificer progress | Efter HVER ændring |
| `auto_archive.py` | Arkiver færdig sejr | Når 3-pass er done |
| `build_claude_context.py` | Byg CLAUDE.md | Efter checkbox changes |
| `update_claude_focus.py` | Opdater fokus state | Når task skifter |
| `auto_track.py` | Opdater STATE.md | Ved state changes |
| `auto_learn.py` | Lær patterns | Ved sejr completion |
| `auto_predict.py` | Generér predictions | Ved phase completion |
| `admiral_tracker.py` | Track scores | Ved events |
| `auto_live_status.py` | Live status display | For real-time view |
| `auto_optimize.py` | Auto-optimering | Ved PHASE 0 |

---

## 1. generate_sejr.py

### Formål
Opretter en ny sejr-mappe med alle 4 standardfiler.

### Brug
```bash
python3 scripts/generate_sejr.py --name "Min Opgave"
```

### Argumenter
| Argument | Required | Beskrivelse |
|----------|----------|-------------|
| `--name` | Ja | Navn på sejren (bruges i mappenavn) |
| `--goal` | Nej | Beskrivelse af målet |

### Output
```
10_ACTIVE/MIN_OPGAVE_2026-01-26/
├── SEJR_LISTE.md      ← Hovedopgave med checkboxes
├── CLAUDE.md          ← AI fokus lock
├── STATUS.yaml        ← Status data
└── AUTO_LOG.jsonl     ← Automatisk log
```

### Eksempel
```bash
python3 scripts/generate_sejr.py --name "Fix Login Bug" --goal "Rette login timeout issue"
```

---

## 2. auto_verify.py

### Formål
Verificerer 3-pass progress og checker om sejr kan arkiveres.

### Brug
```bash
# Verificer alle aktive sejr
python3 scripts/auto_verify.py --all

# Verificer specifik sejr
python3 scripts/auto_verify.py --sejr "MIN_OPGAVE_2026-01-26"
```

### Argumenter
| Argument | Required | Beskrivelse |
|----------|----------|-------------|
| `--all` | Nej | Verificer alle i 10_ACTIVE/ |
| `--sejr` | Nej | Specifik sejr mappenavn |

### Output
```
=== VERIFICATION REPORT ===
Sejr: MIN_OPGAVE_2026-01-26
Pass 1: 8/10 checkboxes (80%)
Pass 2: 0/12 checkboxes (0%)
Pass 3: 0/15 checkboxes (0%)
Current Pass: 1
Can Archive: NO - Pass 1 not complete
```

### Hvornår Bruges
- Efter HVER checkbox du afkrydser
- Før du fortsætter til næste pass
- Før du forsøger at arkivere

---

## 3. auto_archive.py

### Formål
Arkiverer en færdig sejr fra 10_ACTIVE/ til 90_ARCHIVE/.

### Brug
```bash
# Normal arkivering (blokeret hvis 3-pass ikke done)
python3 scripts/auto_archive.py --sejr "MIN_OPGAVE_2026-01-26"

# Force arkivering (ignorer 3-pass check)
python3 scripts/auto_archive.py --sejr "MIN_OPGAVE_2026-01-26" --force
```

### Argumenter
| Argument | Required | Beskrivelse |
|----------|----------|-------------|
| `--sejr` | Ja | Sejr mappenavn |
| `--force` | Nej | Ignorer 3-pass krav (IKKE anbefalet) |

### Arkivering Krav
- [ ] Pass 1 complete + reviewed
- [ ] Pass 2 complete + reviewed (score > Pass 1)
- [ ] Pass 3 complete + final verification (score > Pass 2)
- [ ] Total score >= 24/30
- [ ] All 5+ final tests passed

### Output
```
90_ARCHIVE/MIN_OPGAVE_2026-01-26_20260126_153000/
├── CONCLUSION.md      ← Semantisk essens (kun det vigtige)
├── SEJR_DIPLOM.md     ← Achievement certificate
├── STATUS.yaml        ← Final status
└── ARCHIVE_METADATA.yaml
```

---

## 4. build_claude_context.py

### Formål
Bygger dynamisk CLAUDE.md baseret på faktisk state i STATUS.yaml.

### Brug
```bash
# Byg for alle aktive sejr
python3 scripts/build_claude_context.py --all

# Byg for specifik sejr
python3 scripts/build_claude_context.py --sejr "MIN_OPGAVE_2026-01-26"
```

### Argumenter
| Argument | Required | Beskrivelse |
|----------|----------|-------------|
| `--all` | Nej | Rebuild alle CLAUDE.md filer |
| `--sejr` | Nej | Specifik sejr |

### Hvornår Bruges
- Efter du afkrydser checkboxes
- Når pass ændrer sig
- Når scores opdateres

---

## 5. update_claude_focus.py

### Formål
Opdaterer fokus state i CLAUDE.md uden at rebuilde hele filen.

### Brug
```bash
python3 scripts/update_claude_focus.py --sejr "MIN_OPGAVE_2026-01-26" --task "Næste task beskrivelse"
```

### Argumenter
| Argument | Required | Beskrivelse |
|----------|----------|-------------|
| `--sejr` | Ja | Sejr mappenavn |
| `--task` | Ja | Ny fokus task |

---

## 6. auto_track.py

### Formål
Opdaterer _CURRENT/STATE.md med aktuel system state.

### Brug
```bash
python3 scripts/auto_track.py
python3 scripts/auto_track.py --rebuild-state  # Full rebuild
```

### Argumenter
| Argument | Required | Beskrivelse |
|----------|----------|-------------|
| `--rebuild-state` | Nej | Force fuld rebuild af STATE.md |

### Output
Opdaterer `_CURRENT/STATE.md` med:
- Antal aktive sejr
- Total checkboxes done
- Current focus
- Last activity

---

## 7. auto_learn.py

### Formål
Lærer patterns fra færdige sejr og opdaterer PATTERNS.yaml.

### Brug
```bash
python3 scripts/auto_learn.py
python3 scripts/auto_learn.py --sejr "MIN_OPGAVE_2026-01-26"  # Learn fra specifik
```

### Argumenter
| Argument | Required | Beskrivelse |
|----------|----------|-------------|
| `--sejr` | Nej | Lær fra specifik sejr (default: alle i archive) |

### Output
Opdaterer `_CURRENT/PATTERNS.yaml` med:
- Genbrugelige patterns
- Lærte tips
- Common mistakes to avoid

---

## 8. auto_predict.py

### Formål
Genererer predictions for næste skridt baseret på patterns.

### Brug
```bash
python3 scripts/auto_predict.py
```

### Output
Opdaterer `_CURRENT/NEXT.md` med:
- Predicted next tasks
- Suggested improvements
- Risk areas to watch

---

## 9. admiral_tracker.py

### Formål
Tracker Admiral konkurrence scores og opdaterer leaderboard.

### Brug
```bash
# Se leaderboard
python3 scripts/admiral_tracker.py --leaderboard

# Log event
python3 scripts/admiral_tracker.py --sejr "MIN_OPGAVE" --event "CHECKBOX_DONE"

# Log event med note
python3 scripts/admiral_tracker.py --sejr "MIN_OPGAVE" --event "ERROR_MADE" --note "Glemte verification"

# Se score
python3 scripts/admiral_tracker.py --sejr "MIN_OPGAVE" --score
```

### Argumenter
| Argument | Required | Beskrivelse |
|----------|----------|-------------|
| `--leaderboard` | Nej | Vis global leaderboard |
| `--sejr` | Nej | Specifik sejr |
| `--event` | Nej | Event type at logge |
| `--note` | Nej | Note til event |
| `--score` | Nej | Vis current score |

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

### Formål
Viser real-time status i terminalen.

### Brug
```bash
python3 scripts/auto_live_status.py
```

### Output
Live opdaterende display med:
- Aktive sejr
- Current checkboxes
- Scores
- Recent activity

---

## 11. auto_optimize.py

### Formål
Hjælper med PHASE 0 optimering - research og alternativer.

### Brug
```bash
python3 scripts/auto_optimize.py --sejr "MIN_OPGAVE_2026-01-26"
```

### Output
Suggestions for:
- External research queries
- Internal pattern matches
- 3 alternative approaches

---

## WORKFLOW: Normal Dag

```bash
# 1. Start dagen - se status
python3 scripts/auto_track.py
python3 view.py

# 2. Find aktiv sejr eller opret ny
python3 scripts/generate_sejr.py --name "Dagens Opgave"

# 3. Arbejd på checkboxes...

# 4. Efter hver ændring - verificer
python3 scripts/auto_verify.py --all

# 5. Opdater CLAUDE.md
python3 scripts/build_claude_context.py --all

# 6. Log events
python3 scripts/admiral_tracker.py --sejr "DAGENS_OPGAVE" --event "CHECKBOX_DONE"

# 7. Når færdig (3-pass done) - arkiver
python3 scripts/auto_archive.py --sejr "DAGENS_OPGAVE_2026-01-26"

# 8. Lær fra sejr
python3 scripts/auto_learn.py
```

---

**Sidst opdateret:** 2026-01-26
**Version:** 1.0.0
