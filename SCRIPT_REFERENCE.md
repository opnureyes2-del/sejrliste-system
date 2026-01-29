# 📜 SCRIPT REFERENCE - Alle 15 Scripts Dokumenteret

> **LÆS DETTE** for at forstå hvad hvert script gør og hvornår du bruger det.
> **Sidst verificeret:** 2026-01-28 (alle 15 testet og virker)

---

## OVERSIGT

| Script | Formål | Hvornår Bruges | Status |
|--------|--------|----------------|--------|
| `generate_sejr.py` | Opret ny sejr | Når du starter ny opgave | ✅ |
| `auto_verify.py` | Verificer progress | Efter HVER ændring | ✅ |
| `auto_archive.py` | Arkiver færdig sejr | Når 3-pass er done | ✅ |
| `build_claude_context.py` | Byg CLAUDE.md | Efter checkbox changes | ✅ |
| `update_claude_focus.py` | Opdater fokus state | Når task skifter | ✅ |
| `auto_track.py` | Opdater STATE.md | Ved state changes | ✅ |
| `auto_learn.py` | Lær patterns | Ved sejr completion | ✅ |
| `auto_predict.py` | Generér predictions | Ved phase completion | ✅ |
| `admiral_tracker.py` | Track scores + leaderboard | Ved events | ✅ |
| `auto_live_status.py` | Live status display | For real-time view | ✅ |
| `auto_optimize.py` | Auto-optimering | Ved PHASE 0 | ✅ |
| `model_router.py` | Vælg AI model per opgave | Ved model-valg | ✅ |
| `token_tools.py` | Tæl tokens + estimer pris | Før API kald | ✅ |
| `build_knowledge_base.py` | Byg ChromaDB søge-index | Ved ny dokumentation | ✅ |
| `automation_pipeline.py` | Pre-commit kvalitets-check | Ved git commit | ✅ |

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

---

## ⚠️ COMMON ERRORS & SOLUTIONS

### Error 1: "Sejr folder not found"
```
❌ Error: No active sejr found in 10_ACTIVE/
```
**Løsning:** Opret ny sejr først: `python3 scripts/generate_sejr.py --name "Min Opgave"`

### Error 2: "Archive blocked"
```
❌ ARCHIVE BLOCKED - Total score 23 < 24 required
```
**Løsning:** Forbedre Pass scores. Se review sektioner i SEJR_LISTE.md for hvad der kan forbedres.

### Error 3: "CLAUDE.md outdated"
```
⚠️ Warning: CLAUDE.md does not reflect current STATUS.yaml
```
**Løsning:** Rebuild: `python3 scripts/build_claude_context.py --all`

### Error 4: "Permission denied"
```
❌ Permission denied: scripts/generate_sejr.py
```
**Løsning:** Gør script executable: `chmod +x scripts/generate_sejr.py`

### Error 5: "Missing dependency"
```
❌ ModuleNotFoundError: No module named 'yaml'
```
**Løsning:** Scripts bruger ikke PyYAML - de har simple YAML parser indbygget. Check fil paths.

---

---

## 12. model_router.py

### Formål
Vælger den rigtige AI model baseret på opgavetype (Opus/Sonnet/Haiku/Ollama).

### Brug
```bash
# Klassificér en opgave
python3 scripts/model_router.py --classify "Design arkitekturen for login"

# Test routing med alle eksempler
python3 scripts/model_router.py --test

# Kør lokalt med Ollama (GRATIS)
python3 scripts/model_router.py --local "Forklar hvad en variabel er"
```

### Routing Regler
| Model | Opgavetype | Pris |
|-------|-----------|------|
| Opus | Arkitektur, strategi, patterns, komplekse beslutninger | $$$ |
| Sonnet | Kode, refactoring, git, implementation | $$ |
| Haiku | Verification, checks, logging, simple spørgsmål | $ |
| Ollama | Forklaringer, brainstorm, simple formatting | GRATIS |

---

## 13. token_tools.py

### Formål
Tæller tokens, estimerer pris, og cacher Ollama-svar.

### Brug
```bash
# Tæl tokens i tekst ELLER fil (auto-detect)
python3 scripts/token_tools.py count "Din tekst her"
python3 scripts/token_tools.py count masterpiece_en.py

# Tæl tokens i fil (eksplicit)
python3 scripts/token_tools.py count-file masterpiece_en.py

# Estimér pris
python3 scripts/token_tools.py cost "Din tekst" --model opus --max-tokens 2000

# Se cache statistik
python3 scripts/token_tools.py cache-stats
```

### Cost Oversigt
| Model | Input/1M tokens | Output/1M tokens |
|-------|-----------------|------------------|
| Opus | $15.00 | $75.00 |
| Sonnet | $3.00 | $15.00 |
| Haiku | $0.25 | $1.25 |
| Ollama | GRATIS | GRATIS |

---

## 14. build_knowledge_base.py

### Formål
Bygger en ChromaDB-baseret søge-index over al dokumentation.

### Brug
```bash
# Byg/rebuild knowledge base
python3 scripts/build_knowledge_base.py

# Søg i knowledge base
python3 scripts/build_knowledge_base.py --query "Hvad er DNA lag systemet?"

# Se statistik
python3 scripts/build_knowledge_base.py --stats
```

### Output
- 82+ dokumenter indekseret
- Semantisk søgning med relevance-scores
- Token-estimat for context

---

## 15. automation_pipeline.py

### Formål
Pre-commit kvalitets-pipeline. Kører syntax, flake8, og bandit checks.

### Brug
```bash
# Hurtig check (kun syntax + kritiske fejl)
python3 scripts/automation_pipeline.py --quick

# Fuld pipeline med rapportering
python3 scripts/automation_pipeline.py masterpiece_en.py
```

### Output
Rapporterer:
- Syntax errors (BLOKERENDE)
- Flake8 kritiske fejl (BLOKERENDE)
- Style warnings (INFORMATIONELLE)
- Bandit security issues (INFORMATIONELLE)

---

**Sidst opdateret:** 2026-01-28
**Version:** 2.0.0 (Komplet - alle 15 scripts dokumenteret + verificeret)
