# SEJRLISTE SYSTEM - KOMPLET MANUAL

**Version:** 2.0.0 - 3-PASS KONKURRENCE
**Opdateret:** 2026-01-25
**Bygget af:** Kv1nt + Rasmus

> **Dette system virker 100% MANUELT. Ingen app krævet.**

---

## HVAD ER DET?

Et **TVUNGET FORBEDRINGSSYSTEM** der garanterer kvalitet gennem:

1. **3-PASS KONKURRENCE** - Hver opgave gennemgås 3 gange med stigende kvalitet
2. **TVUNGET FORBEDRING** - Pass 2 SKAL være bedre end Pass 1, osv.
3. **ARKIVERING BLOKERET** - Kan ikke arkivere før alle krav er opfyldt
4. **CLAUDE FOKUS LOCK** - AI tvinges til at følge systemet

---

## KOMPLET MAPPE STRUKTUR

```
sejrliste systemet/
│
├── README.md ← Overblik + Quick Start
├── MANUAL.md ← DENNE FIL (komplet dokumentation)
├── ARBEJDSFORHOLD.md ← Obligatorisk AI vejledning
├── DNA.yaml ← System identitet
├── LOG_FORMAT.md ← Log specifikation
├── ARKITEKTUR.md ← System arkitektur
│
├── scripts/ ← 9 AUTOMATISERINGS SCRIPTS
│ ├── generate_sejr.py → Opret ny sejr (4 filer)
│ ├── build_claude_context.py → DYNAMISK CLAUDE.md builder
│ ├── update_claude_focus.py → Opdater fokus state
│ ├── auto_verify.py → 3-pass verification
│ ├── auto_archive.py → Arkivering (blokeret til done)
│ ├── auto_track.py → State tracking
│ ├── auto_learn.py → Pattern learning
│ ├── auto_predict.py → Predictions
│ └── admiral_tracker.py → Score tracking
│
├── 00_TEMPLATES/ ← SKABELONER (4 stk)
│ ├── SEJR_TEMPLATE.md → Master template med 3-pass
│ ├── CLAUDE.md → Fokus lock template
│ ├── STATUS_TEMPLATE.yaml → Unified status template
│ └── SESSION_TJEK.md → Session start tjekliste
│
├── 10_ACTIVE/ ← AKTIVE SEJR (arbejd her)
│ └── {OPGAVE_DATO}/
│ ├── SEJR_LISTE.md → Hovedopgave med checkboxes
│ ├── CLAUDE.md → AI FOKUS LOCK (genereret)
│ ├── STATUS.yaml → ALT status (unified)
│ └── AUTO_LOG.jsonl → ALT logging (master)
│
├── 90_ARCHIVE/ ← FÆRDIGE SEJR
│ └── {OPGAVE_DATO_TID}/
│ └── CONCLUSION.md → Kun semantisk essens
│
├── _CURRENT/ ← SYSTEM STATE
│ ├── STATE.md → Current state
│ ├── DELTA.md → Hvad er nyt
│ ├── NEXT.md → Predictions
│ ├── PATTERNS.yaml → Lærte mønstre
│ └── LEADERBOARD.md → Global konkurrence leaderboard
│
├── view.py ← Terminal viewer (simpel)
└── app/sejr_app.py ← TUI app (Textual)
```

> **SINGLE SOURCE OF TRUTH:** Hver sejr har KUN 4 filer - ingen redundans!

---

## EN SEJR MAPPE INDEHOLDER 4 FILER

### 1. SEJR_LISTE.md

Hovedopgaven organiseret i **3 PASSES**:

**PASS 1: PLANLÆGNING**
- PHASE 0: Research & Optimering (3 alternativer)
- PHASE 1: Opgave Definition
- PHASE 2: Verificering Plan
- **REVIEW sektion med score ___/10**

**PASS 2: EKSEKVERING**
- PHASE 2: Udvikling
- PHASE 3: Test (minimum 3 tests)
- PHASE 4: Git Workflow
- **REVIEW sektion med score ___/10 (SKAL > Pass 1)**

**PASS 3: 7-DNA GENNEMGANG**
- Gennemgang af alle 7 DNA lag
- Find mangler, fejl, optimeringer
- PHASE 4: Final Verification (5+ tests)
- **REVIEW sektion med score ___/10 (SKAL > Pass 2)**

**SEMANTISK KONKLUSION**
- Final scores tabel
- Hvad lærte vi
- Hvad kan genbruges

### 2. CLAUDE.md

**DYNAMISK** fokus lock der viser:
- Præcis hvilken checkbox der er næste
- Linjenummer i SEJR_LISTE.md
- Progress bars for hver pass
- Scores og krav
- Anti-dum checkpoints
- Forbudte og påkrævede handlinger

**OPDATERES AUTOMATISK** af `build_claude_context.py` baseret på faktisk state.

### 3. STATUS.yaml (UNIFIED)

**Single Source of Truth** for ALT status:

```yaml
meta:
 sejr_name: "Opgave Navn"
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
 totals: { total_score: 0, rank: "KADET" }

model_tracking:
 current_model: "claude-opus-4-5-20251101"
 models_used: [...]
```

> **Erstatter:** VERIFY_STATUS.yaml + ADMIRAL_SCORE.yaml + MODEL_HISTORY.yaml

### 4. AUTO_LOG.jsonl

Automatisk log i JSON Lines format:
```json
{"timestamp": "2026-01-25T12:00:00", "action": "sejr_created", "name": "Opgave"}
{"timestamp": "2026-01-25T12:05:00", "action": "checkbox_completed", "task": "Task 1"}
```

---

## 3-PASS KONKURRENCE SYSTEM

### Hvorfor 3 Passes?

**TVUNGET FORBEDRING** - Du kan ikke bare sige "færdig" og arkivere.

| Pass | Hvad | Score Krav |
|------|------|------------|
| **1** | Planlægning - Design løsning | Baseline |
| **2** | Eksekvering - Implementer løsning | > Pass 1 |
| **3** | 7-DNA Review - Find mangler/fejl | > Pass 2 |

### Score System

- Hver pass gives score 0-10
- Total score = Pass 1 + Pass 2 + Pass 3 (max 30)
- **Minimum 24/30 krævet for arkivering**

### Arkivering Krav

Du kan IKKE arkivere før:
- [ ] Pass 1 complete (alle checkboxes afkrydsede)
- [ ] Pass 2 complete (alle checkboxes afkrydsede)
- [ ] Pass 3 complete (alle checkboxes + 7-DNA gennemgang)
- [ ] Pass 2 score > Pass 1 score
- [ ] Pass 3 score > Pass 2 score
- [ ] Total score ≥ 24/30
- [ ] 5+ tests passed
- [ ] 7-DNA gennemgang dokumenteret

---

## 7 DNA LAG (Gennemgås i Pass 3)

| Lag | Navn | Spørgsmål |
|-----|------|-----------|
| 1 | SELF-AWARE | Kender systemet sin identitet? |
| 2 | SELF-DOCUMENTING | Er alt logget? |
| 3 | SELF-VERIFYING | Er alt testet? |
| 4 | SELF-IMPROVING | Har vi lært noget nyt? |
| 5 | SELF-ARCHIVING | Kun essens bevaret? |
| 6 | PREDICTIVE | Hvad er næste skridt? |
| 7 | SELF-OPTIMIZING | Kunne vi have gjort det bedre? |

### DNA Lag 1: SELF-AWARE
> "Kender systemet sig selv?"
- [ ] DNA.yaml opdateret med nye capabilities?
- [ ] Systemets begrænsninger dokumenteret?
- [ ] Metadata korrekt?

**Find mangler/fejl/optimering:** ___

### DNA Lag 2: SELF-DOCUMENTING
> "Er alt dokumenteret automatisk?"
- [ ] AUTO_LOG.jsonl har alle events?
- [ ] STATUS.yaml opdateret?
- [ ] Alle ændringer logged?

**Find mangler/fejl/optimering:** ___

### DNA Lag 3: SELF-VERIFYING
> "Er alt verificeret med tests?"
- [ ] Minimum 5 uafhængige tests?
- [ ] Edge cases testet?
- [ ] Error handling testet?

**Find mangler/fejl/optimering:** ___

### DNA Lag 4: SELF-IMPROVING
> "Har vi lært noget der kan genbruges?"
- [ ] PATTERNS.yaml opdateret?
- [ ] Learnings dokumenteret?
- [ ] Reusable code identificeret?

**Find mangler/fejl/optimering:** ___

### DNA Lag 5: SELF-ARCHIVING
> "Er kun det essentielle bevaret?"
- [ ] Semantisk konklusion skrevet?
- [ ] Process details kan slettes?
- [ ] Arkiv-struktur korrekt?

**Find mangler/fejl/optimering:** ___

### DNA Lag 6: PREDICTIVE
> "Hvad skal ske næste gang?"
- [ ] NEXT.md opdateret?
- [ ] Predictions baseret på patterns?
- [ ] Næste skridt klart?

**Find mangler/fejl/optimering:** ___

### DNA Lag 7: SELF-OPTIMIZING
> "Kunne vi have gjort det bedre fra start?"
- [ ] 3 alternativer blev overvejet?
- [ ] Best practice blev fulgt?
- [ ] Eksisterende løsninger checket?

**Find mangler/fejl/optimering:** ___

---

## HVORFOR 3-PASS VIRKER

### Problem: Middelmådighed
Uden tvunget forbedring stopper man ved "godt nok":
- Første forsøg: 60% kvalitet
- Intet review: Forbliver 60%
- Resultat: Middelmådigt arbejde

### Løsning: 3-Pass Konkurrence
Med tvunget forbedring SKAL kvaliteten stige:
- Pass 1: 60% → Planlægning
- Pass 2: 75% → Eksekvering (+15%)
- Pass 3: 90%+ → 7-DNA review (+15%)
- Resultat: **Højkvalitets arbejde HVER gang**

---

## TVANG I SYSTEMET

### auto_verify.py
```
- Checker om Pass 2 score > Pass 1
- Checker om Pass 3 score > Pass 2
- Checker om total score ≥ 24/30
- Checker om 5+ tests passed
```

### auto_archive.py
```
- BLOKERER arkivering hvis 3-pass ikke færdig
- Kræver can_archive=true fra verify
- Viser præcis hvad der mangler
```

### SEJR_TEMPLATE.md
```
- Struktureret med 3 passes
- Obligatoriske review sektioner
- 7-DNA checkliste i Pass 3
- Scoring system indbygget
```

---

## [ADMIRAL] ADMIRAL KONKURRENCE SYSTEM

Et **SCORE SYSTEM** der måler AI modellers performance objektivt:

- **POSITIVE POINTS** = Godt arbejde (belønning)
- **NEGATIVE POINTS** = Fejl og dumheder (straf × 2!)
- **TOTAL SCORE** = Positive - (Negative × 2)

### Rangeringer

| Rang | Score | Beskrivelse |
|------|-------|-------------|
| [ADMIRAL] **STORADMIRAL** | 150+ | Legendarisk. Perfekt udførelse. |
| **ADMIRAL** | 100-149 | Excellence. Minimal fejl. |
| [MEDAL] **KAPTAJN** | 50-99 | Solid. God performance. |
| **LØJTNANT** | 20-49 | Acceptabel. Plads til forbedring. |
| **KADET** | 0-19 | Svag. Mange fejl. |
| [DEAD] **SKIBSDRENG** | < 0 | KATASTROFE. Negativ score! |

### Positive Metrics (Belønning)

| Metric | Points | Beskrivelse |
|--------|--------|-------------|
| `CHECKBOX_DONE` | +1 | Afkrydsede en checkbox |
| `PASS_COMPLETE` | +10 | Færdiggjorde et helt pass |
| `VERIFIED_WORKING` | +5 | Bevist funktionel kode |
| `TEST_PASSED` | +3 | Test bestået |
| `IMPROVEMENT_FOUND` | +5 | Fandt forbedring i Pass 3 |
| `PROACTIVE_ACTION` | +3 | Handlede proaktivt |
| `GOOD_DOCUMENTATION` | +2 | God dokumentation |
| `ADMIRAL_MOMENT` | +10 | Særligt imponerende handling |
| `SEJR_ARCHIVED` | +20 | Arkiverede en komplet sejr |

### Negative Metrics (Straf × 2!)

| Metric | Points | Beskrivelse |
|--------|--------|-------------|
| `TOKEN_WASTE` | -3 | Unødig opsummering/gentagelse |
| `MEMORY_LOSS` | -5 | Glemte kontekst |
| `INCOMPLETE_STEP` | -3 | Efterlod ufærdigt arbejde |
| `SKIPPED_STEP` | -5 | Sprang over et skridt |
| `LIE_DETECTED` | -10 | Sagde "færdig" uden bevis |
| `ERROR_MADE` | -3 | Lavede en fejl |
| `FOCUS_LOST` | -3 | Mistede fokus på opgaven |
| `RULE_BREAK` | -10 | Brød systemets regler |

### Score Beregning

```
TOTAL_SCORE = SUM(positive_points) - (SUM(negative_points) × 2)
```

**Negative tæller DOBBELT** fordi fejl koster mere end de burde.

### Special Achievements

| Achievement | Krav | Bonus |
|-------------|------|-------|
| [VICTORY] **PERFEKT PASS** | 0 negative i et helt pass | +15 |
| **FLAWLESS SEJR** | 0 negative i hele sejr | +50 |
| **SPEED DEMON** | Sejr done under estimat | +10 |
| [AI] **MEMORY MASTER** | 0 memory_loss hele session | +20 |
| [DOCS] **DOC KING** | 10+ good_documentation | +10 |
| [SCAN] **BUG HUNTER** | 5+ improvements fundet | +15 |

### Score Kommandoer

```bash
# Log event
python3 scripts/admiral_tracker.py --sejr "X" --event "CHECKBOX_DONE"

# Log event med note
python3 scripts/admiral_tracker.py --sejr "X" --event "ERROR_MADE" --note "Beskrivelse"

# Se leaderboard
python3 scripts/admiral_tracker.py --leaderboard

# Se score
python3 scripts/admiral_tracker.py --sejr "X" --score
```

---

## ALLE KOMMANDOER

### Opret Ny Sejr
```bash
python3 scripts/generate_sejr.py --name "Opgave Navn"
```

Opretter:
- `10_ACTIVE/OPGAVE_NAVN_2026-01-25/`
- Med alle 4 filer

### Byg Dynamisk CLAUDE.md
```bash
# Alle aktive sejr
python3 scripts/build_claude_context.py --all

# Specifik sejr
python3 scripts/build_claude_context.py --sejr "OPGAVE_NAVN_2026-01-25"
```

### Verificer Progress
```bash
# Alle aktive sejr
python3 scripts/auto_verify.py --all

# Specifik sejr
python3 scripts/auto_verify.py --sejr "OPGAVE_NAVN_2026-01-25"
```

Output viser:
- Checkbox completion per pass
- Scores
- Archive blocking reason

### Arkiver Færdig Sejr
```bash
python3 scripts/auto_archive.py --sejr "OPGAVE_NAVN_2026-01-25"

# Force arkiver (ignorer 3-pass)
python3 scripts/auto_archive.py --sejr "X" --force
```

### Se Status
```bash
# Simpel terminal viewer
python3 view.py

# Avanceret TUI app (Textual)
python3 app/sejr_app.py
```

### Andre Scripts
```bash
# Opdater STATE.md
python3 scripts/auto_track.py

# Lær patterns
python3 scripts/auto_learn.py

# Generer predictions
python3 scripts/auto_predict.py
```

---

## CLAUDE FOKUS SYSTEM

### For AI Modeller

Når du åbner en sejr mappe, SKAL du:

1. **STOP** - Læs ikke videre i brugerens besked
2. **LÆS** `ARBEJDSFORHOLD.md` (i system root)
3. **LÆS** `CLAUDE.md` i sejr mappen
4. **BEKRÆFT** til bruger:
 ```
 [LOCK] SEJR FOKUS AKTIVERET
 Opgave: [navn]
 Pass: [X]/3
 Næste: [specifik task]
 ```
5. **ARBEJD** kun på current task
6. **AFKRYDS** checkbox når færdig
7. **OPDATER** CLAUDE.md med `build_claude_context.py`

### Anti-Dum Checkpoints

Hver 5 handlinger:
1. STOP hvad du laver
2. Læs CLAUDE.md igen
3. Bekræft: "Jeg arbejder på [TASK], pass [X]/3"
4. Find næste unchecked checkbox
5. Fortsæt

### Forbudte Handlinger

- [FAIL] Arbejde på andet end current sejr
- [FAIL] Skippe til næste pass før current er 100%
- [FAIL] Glemme at afkrydse checkboxes
- [FAIL] "Forbedre" ting uden for scope
- [FAIL] Sige "færdig" uden bevis
- [FAIL] Arkivere før 3-pass done

---

## 300% FÆRDIGT STANDARD

Noget er IKKE færdigt før det er:

| Niveau | Hvad | Krav |
|--------|------|------|
| **RUNNING** (100%) | Det kører | Kan eksekveres |
| **PROVEN** (200%) | Det virker | Testet med real data |
| **TESTED** (300%) | Det er verificeret | 5+ uafhængige tests |

**"NÆSTEN FÆRDIGT" = IKKE FÆRDIGT**

---

## MANUEL WORKFLOW (Uden Scripts)

Hvis du vil arbejde helt manuelt:

### 1. Opret Mappe
```bash
mkdir -p "10_ACTIVE/MIT_PROJEKT_2026-01-25"
```

### 2. Kopiér Template
```bash
cp 00_TEMPLATES/SEJR_TEMPLATE.md "10_ACTIVE/MIT_PROJEKT_2026-01-25/SEJR_LISTE.md"
cp 00_TEMPLATES/CLAUDE.md "10_ACTIVE/MIT_PROJEKT_2026-01-25/CLAUDE.md"
```

### 3. Opret Status Filer
```bash
touch "10_ACTIVE/MIT_PROJEKT_2026-01-25/AUTO_LOG.jsonl"
cp 00_TEMPLATES/STATUS_TEMPLATE.yaml "10_ACTIVE/MIT_PROJEKT_2026-01-25/STATUS.yaml"
```

### 4. Arbejd og Afkryds

Åbn SEJR_LISTE.md og afkryds:
- `- [ ]` → `- [x]`

### 5. Arkiver Manuelt
```bash
mv "10_ACTIVE/MIT_PROJEKT_2026-01-25" "90_ARCHIVE/MIT_PROJEKT_2026-01-25_$(date +%H%M%S)/"
```

---

## TROUBLESHOOTING

### Scripts Virker Ikke?
```bash
# Kør med python3 eksplicit
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

### Arkivering Blokeret?
Check:
- Er alle checkboxes i alle 3 passes afkrydsede?
- Er scores udfyldt i REVIEW sektionerne?
- Er total score ≥ 24/30?
- Er 7-DNA gennemgang gjort?

---

## SE OGSÅ

| Fil | Beskrivelse |
|-----|-------------|
| `README.md` | Overblik + Quick Start |
| `ARBEJDSFORHOLD.md` | Obligatorisk AI vejledning |
| `DNA.yaml` | System identitet |
| `ARKITEKTUR.md` | System arkitektur |
| `LOG_FORMAT.md` | Log specifikation |

---

**Sidst opdateret:** 2026-01-25
**Status:** [OK] KOMPLET
