# SEJR: OPTIMERINGER O4-O15

**Oprettet:** 2026-01-30
**Status:** PASS 1 — IN PROGRESS
**Ejer:** Kv1nt + Rasmus
**Current Pass:** 1/3
**Kilde:** TODO.md sektion 6 (Optimeringer O4-O15)

---

## 3-PASS KONKURRENCE SYSTEM (OBLIGATORISK)

```
PASS 1: FUNGERENDE     — "Get it working"      — REVIEW REQUIRED
PASS 2: FORBEDRET      — "Make it better"      — REVIEW REQUIRED
PASS 3: OPTIMERET      — "Make it best"        — FINAL VERIFICATION
                                                        |
                                                  KAN ARKIVERES
```

**REGEL:** Du kan IKKE arkivere foer alle 3 passes er gennemfoert og verificeret.

---

## PASS 1: FUNGERENDE ("Get It Working")

### A. O4 — INTRO App Integration (AGENT KOERER)

**Hvad:** INTRO appen (Streamlit) skal have fuld integration med MASTER FOLDERS data
**Hvorfor:** INTRO appen viser systemet visuelt — den SKAL matche virkeligheden
**Status:** AGENT KOERER — Fase 0-6 implementeret i denne session

- [x] **A1.** Fase 0: Data model og I-file parsing
  - Verify: `python3 -c "from intro_app.data_model import parse_i_files; print('OK')"`
  - Result: Implementeret i session 24

- [x] **A2.** Fase 1-3: Sidebar, detail view, folder structure
  - Verify: `cd ~/Desktop/MASTER\ FOLDERS\(INTRO\) && streamlit run intro_app/app.py`
  - Result: Implementeret i session 24

- [x] **A3.** Fase 4-5: SystemFunctions + DNA layers
  - Verify: App viser DNA lag og system funktioner
  - Result: Implementeret i session 24

- [x] **A4.** Fase 6: Quick Actions panel
  - Verify: App har quick actions
  - Result: Implementeret i session 24

### B. O5 — ELLE Agent System Revival (AGENT KOERER)

**Hvad:** ELLE agent systemet skal have fungerende venv, config, og imports
**Hvorfor:** ELLE er Rasmus' AI-oekosystem — det SKAL koere
**Status:** AGENT KOERER — Pass 1-3 gennemfoert i denne session

- [x] **B1.** requirements.txt og venv oprettet
  - Verify: `source ~/Desktop/ELLE.md/.venv/bin/activate && pip list`
  - Result: Implementeret i session 24

- [x] **B2.** config.yaml med alle stier
  - Verify: `cat ~/Desktop/ELLE.md/config.yaml`
  - Result: Implementeret i session 24

- [x] **B3.** Hardcoded paths fikset
  - Verify: `grep -r "/home/rasmus/Desktop" ~/Desktop/ELLE.md/agents/ | grep -v ".venv"`
  - Result: Refaktoreret til config-baseret

- [x] **B4.** Cross-module imports fikset
  - Verify: Python imports virker uden fejl
  - Result: Implementeret i session 24

### C. O9 — Scripts Katalog (FAERDIG)

**Hvad:** Dokumenter ALLE scripts i systemet med fuld dybde
**Hvorfor:** Ingen vidste hvilke scripts der fandtes eller hvad de goer
**Status:** FAERDIG — Dokumenteret i GENVEJE_OG_KOMMANDOER.md

- [x] **C1.** 11 scripts dokumenteret i GENVEJE_OG_KOMMANDOER.md
  - Verify: `grep -c "###" "/home/rasmus/Desktop/MIN ADMIRAL/GENVEJE_OG_KOMMANDOER.md"`
  - Result: 3 admiral scripts + 8 projekt kommandoer, alle med fuld dybde per Rule -51

### D. O12 — Dependency Update Check Cron

**Hvad:** Automatisk daglig check af Python/npm dependencies for sikkerhedsopdateringer
**Hvorfor:** Forældede dependencies = sikkerhedsrisiko
**Status:** DONE — script bygget, cron sat, dokumenteret

- [x] **D1.** Byg script: `admiral_dependency_check.sh`
  - Verify: `bash ~/Desktop/MIN\ ADMIRAL/SCRIPTS/admiral_dependency_check.sh`
  - Result: 190 linjer, scanner 7 Python venvs + 6 npm projekter. Global `depcheck` kommando.

- [x] **D2.** Tilfoej cron job (daglig kl 06:00)
  - Verify: `crontab -l | grep dependency`
  - Result: `0 6 * * * ~/Desktop/MIN\ ADMIRAL/SCRIPTS/admiral_dependency_check.sh`

- [x] **D3.** Dokumenter i GENVEJE_OG_KOMMANDOER.md
  - Verify: `grep "depcheck" "/home/rasmus/Desktop/MIN ADMIRAL/GENVEJE_OG_KOMMANDOER.md"`
  - Result: Fuld dybde dokumentation med 3 subkommandoer, 2 sektioner, output-beskrivelse

### E. O13 — VS Code Workspace Profiles

**Hvad:** Opret VS Code workspace profiles for hvert projekt
**Hvorfor:** Hurtigere skift mellem projekter med korrekte settings
**Status:** DONE — 3 workspace filer oprettet

- [x] **E1.** Opret workspace fil for ELLE.md
  - Verify: `ls ~/Desktop/ELLE.md/*.code-workspace`
  - Result: ELLE.code-workspace — Python settings, .venv interpreter, 3 tasks (tests, group chat, type check), blaa titellinje

- [x] **E2.** Opret workspace fil for MIN ADMIRAL
  - Verify: `ls ~/Desktop/MIN\ ADMIRAL/*.code-workspace`
  - Result: ADMIRAL.code-workspace — Markdown+shell settings, 5 tasks (health, audit, depcheck, briefing, verify), lilla titellinje

- [x] **E3.** Opret workspace fil for MASTER FOLDERS(INTRO)
  - Verify: `ls ~/Desktop/MASTER\ FOLDERS\(INTRO\)/*.code-workspace`
  - Result: INTRO.code-workspace — Python+markdown settings, 4 tasks (app start, verify, syntax, sejrstatus), groen titellinje

### F. O14 — Ollama Model Aliases

**Hvad:** Opret shell aliases for hyppigt brugte Ollama modeller
**Hvorfor:** `ollama run qwen2.5-coder:7b` er for langt at skrive
**Status:** DONE — 4 nye aliases tilfojet (total 9)

- [x] **F1.** Identificer top 5 mest brugte modeller
  - Verify: `ollama list`
  - Result: 14 modeller. Top: llama3.2 (general), qwen2.5-coder (kode), mistral (reasoning), deepseek-r1 (dyb), phi4 (stoerst)

- [x] **F2.** Opret aliases i .bashrc/.zshrc
  - Verify: `grep "ollama" ~/.zshrc | wc -l` → 9 aliases
  - Nye: `deep` (deepseek-r1:8b), `phi` (phi4), `qwen` (qwen3:8b), `fast` (gemma3:4b)

- [x] **F3.** Dokumenter i GENVEJE_OG_KOMMANDOER.md
  - Verify: Allerede dokumenteret i SHELL ALIASES sektionen (linje ~50)
  - Result: 9 ollama aliases total: ask, code-ai, think, codellama, models, deep, phi, qwen, fast

### G. O15 — Desktop Environment Guide

**Hvad:** Dokumenter hele desktop-miljoeet (shortcuts, panels, workflow)
**Hvorfor:** Rasmus glemmer keyboard shortcuts og workflow-tricks
**Status:** DONE — DESKTOP_GUIDE.md oprettet (620 linjer)

- [x] **G1.** Dokumenter system keyboard shortcuts
  - Verify: `grep "Super" "/home/rasmus/Desktop/MIN ADMIRAL/DESKTOP_GUIDE.md" | head -5`
  - Result: 5 custom GNOME keybindings + 41 window manager bindings fra gsettings

- [x] **G2.** Dokumenter VS Code shortcuts brugt dagligt
  - Verify: VS Code 1.108.2, 27 extensions, standard keybindings (ingen custom)
  - Result: Python/Markdown/Git workflow shortcuts dokumenteret

- [x] **G3.** Dokumenter terminal workflow (tmux, aliases, scripts)
  - Verify: zsh 5.9 + oh-my-zsh + Starship, 94 aliases, 80+ ~/.local/bin commands, 19 cron jobs
  - Result: Komplet terminal workflow med alle aliases, funktioner, cron jobs

- [x] **G4.** Saml alt i MIN ADMIRAL som DESKTOP_GUIDE.md
  - Verify: `ls "/home/rasmus/Desktop/MIN ADMIRAL/DESKTOP_GUIDE.md"` → 620 linjer
  - Result: 4 sektioner + daily workflow + troubleshooting. Rule -42 compliant.

---

## PASS 1 COMPLETION CHECKLIST

- [x] A1-A4 checkboxes afkrydset (INTRO App — AGENT DONE)
- [x] B1-B4 checkboxes afkrydset (ELLE Agent — AGENT DONE)
- [x] C1 checkbox afkrydset (Scripts Katalog — DONE)
- [x] D1-D3 checkboxes afkrydset (Dependency Check — DONE)
- [x] E1-E3 checkboxes afkrydset (VS Code Workspaces — DONE)
- [x] F1-F3 checkboxes afkrydset (Ollama Aliases — DONE)
- [x] G1-G4 checkboxes afkrydset (Desktop Guide — DONE)
- [ ] Git committed med "PASS 1:" prefix

#### PASS 1 SCORE: ___/10

---

## PASS 1 REVIEW (OBLIGATORISK)

> STOP. Foer du fortsaetter til Pass 2, SKAL du gennemgaa Pass 1 kritisk.

### Hvad Virker? (Bevar)
1. _beskriv hvad der fungerer godt_
2. _beskriv hvad der fungerer godt_
3. _beskriv hvad der fungerer godt_

### Hvad Kan Forbedres? (SKAL Fixes i Pass 2)
1. [ ] _problem 1_ — _loesning_
2. [ ] _problem 2_ — _loesning_
3. [ ] _problem 3_ — _loesning_

### Hvad Mangler? (SKAL Tilfoejes i Pass 2)
1. [ ] _manglende feature 1_
2. [ ] _manglende feature 2_
3. [ ] _manglende test/docs_

### Performance Issues?
- [ ] Identificeret: _ja/nej_
- [ ] Beskrivelse: _hvad er langsomt_

### Kode Kvalitet Issues?
- [ ] Dupliceret kode: _ja/nej, hvor_
- [ ] Manglende error handling: _ja/nej, hvor_
- [ ] Hardcoded values: _ja/nej, hvor_

---

## PASS 2: FORBEDRET ("Make It Better")

- [ ] Alle Pass 1 fund reviewed
- [ ] Forbedringer fra review implementeret
- [ ] Ekstra tests tilfojet
- [ ] Dokumentation opdateret
- [ ] Git committed med "PASS 2:" prefix

#### PASS 2 SCORE: ___/10

---

## PASS 3: OPTIMERET ("Make It Best")

- [ ] Lag 1: SELF-AWARE — Ved vi hvad vi har?
- [ ] Lag 2: SELF-DOCUMENTING — Er alt logget?
- [ ] Lag 3: SELF-VERIFYING — Er alt testet?
- [ ] Lag 4: SELF-IMPROVING — Har vi laert noget?
- [ ] Lag 5: SELF-ARCHIVING — Kun essens bevaret?
- [ ] Lag 6: PREDICTIVE — Hvad er naeste skridt?
- [ ] Lag 7: SELF-OPTIMIZING — Kunne vi goere det bedre?

#### PASS 3 SCORE: ___/10

---

## 3-PASS RESULTAT

| Pass | Score | Forbedring |
|------|-------|------------|
| Pass 1 | _/10 | Baseline |
| Pass 2 | _/10 | +_% |
| Pass 3 | _/10 | +_% |
| **TOTAL** | **_/30** | |

---

**ARCHIVE BLOCKED UNTIL:**
- [ ] Pass 1 complete + reviewed
- [ ] Pass 2 complete + reviewed (score > Pass 1)
- [ ] Pass 3 complete + final verification (score > Pass 2)
- [ ] Total score >= 24/30
- [ ] All 5+ final tests passed
