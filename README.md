# SEJR LISTE SYSTEM

**Version:** 2.1.0 - SINGLE SOURCE OF TRUTH
**Opdateret:** 2026-01-25
**DNA Lag:** 7 (SELF-AWARE → SELF-OPTIMIZING)

---

## HVAD ER DET?

Et **TVUNGET FORBEDRINGSSYSTEM** der sikrer at HVER opgave gennemgås 3 gange med stigende kvalitet:

| Pass | Fokus | Krav |
|------|-------|------|
| **Pass 1** | Planlægning | Baseline score |
| **Pass 2** | Eksekvering | Score > Pass 1 |
| **Pass 3** | 7-DNA Review | Score > Pass 2, Total ≥ 24/30 |

**ARKIVERING ER BLOKERET** indtil alle 3 passes er færdige med tilstrækkelig score.

---

## QUICK START

```bash
cd "/home/rasmus/Desktop/sejrliste systemet"

# 1. Opret ny sejr
python3 scripts/generate_sejr.py --name "Min Opgave"

# 2. Byg DYNAMISK CLAUDE.md
python3 scripts/build_claude_context.py --all

# 3. Arbejd med sejr i 10_ACTIVE/

# 4. Verificer progress (kør ofte!)
python3 scripts/auto_verify.py --all

# 5. Arkiver når færdig (blokeret til 3-pass done)
python3 scripts/auto_archive.py --sejr "MIN_OPGAVE_2026-01-25"
```

---

## KOMPLET MAPPE STRUKTUR

```
sejrliste systemet/
│
├── README.md                 ← Du læser denne (inkl. Quick Start)
├── ADMIRAL.md                ← 🆕 HVAD ER EN ADMIRAL? (5 kvaliteter)
├── MODEL_ONBOARDING.md       ← 🆕 AI ONBOARDING (læs først som ny model!)
├── SCRIPT_REFERENCE.md       ← 🆕 Alle 11 scripts dokumenteret
├── EKSEMPLER.md              ← 🆕 10+ konkrete eksempler
├── ARBEJDSFORHOLD.md         ← KOMPLET VEJLEDNING (AI regler inkluderet)
├── MANUAL.md                 ← Fuld dokumentation (3-pass + score system)
├── LOG_FORMAT.md             ← Log format specifikation
├── DNA.yaml                  ← System identitet
├── ARKITEKTUR.md             ← System arkitektur
├── view.py                   ← Terminal viewer (simpel)
├── app/sejr_app.py           ← TUI app (Textual - avanceret)
│
├── scripts/                  ← Automatisering (9 scripts)
│   ├── generate_sejr.py          → Opret ny sejr + CLAUDE.md
│   ├── build_claude_context.py   → DYNAMISK CLAUDE.md builder
│   ├── update_claude_focus.py    → Opdater fokus state
│   ├── auto_verify.py            → 3-pass verification
│   ├── auto_archive.py           → Arkivering (blokeret til done)
│   ├── auto_track.py             → State tracking
│   ├── auto_learn.py             → Pattern learning
│   ├── auto_predict.py           → Predictions
│   └── admiral_tracker.py        → Score tracking + leaderboard
│
├── 00_TEMPLATES/             ← Skabeloner (4 stk)
│   ├── SEJR_TEMPLATE.md          → Master template med 3-pass
│   ├── CLAUDE.md                 → Fokus lock template
│   ├── STATUS_TEMPLATE.yaml      → Unified status template
│   └── SESSION_TJEK.md           → Session start tjekliste
│
├── 10_ACTIVE/                ← AKTIVE SEJR (arbejd her)
│   └── {OPGAVE_DATO}/
│       ├── SEJR_LISTE.md         → Hovedopgave med checkboxes
│       ├── CLAUDE.md             → AI FOKUS LOCK (genereret)
│       ├── STATUS.yaml           → UNIFIED (pass + score + model)
│       └── AUTO_LOG.jsonl        → MASTER (alt logging)
│
├── 90_ARCHIVE/               ← FÆRDIGE SEJR (kun konklusion)
│   └── {OPGAVE_DATO_TID}/
│       └── CONCLUSION.md         → Semantisk essens
│
└── _CURRENT/                 ← System state (5 filer)
    ├── STATE.md                  → Current state
    ├── DELTA.md                  → Hvad er nyt
    ├── NEXT.md                   → Predictions
    ├── PATTERNS.yaml             → Lærte mønstre
    └── LEADERBOARD.md            → Global konkurrence leaderboard
```

---

## EN SEJR MAPPE INDEHOLDER

Når du opretter en ny sejr, får du disse **4 filer** (Single Source of Truth):

### 1. SEJR_LISTE.md
Hovedopgaven med alle checkboxes organiseret i 3 passes:
- **Pass 1:** PHASE 0-1-2 (Research, Planlægning, Verificering)
- **Pass 2:** PHASE 2-3-4 (Udvikling, Test, Git)
- **Pass 3:** 7-DNA Gennemgang (alle 7 lag checkes)

### 2. CLAUDE.md
**DYNAMISK** fokus lock (genereret fra STATUS.yaml):
- Præcis hvilken checkbox der er næste
- Progress bars for hver pass
- Scores og krav
- Anti-dum checkpoints

### 3. STATUS.yaml (UNIFIED)
**Single Source of Truth** for ALT status:
- **Pass tracking:** Completion %, scores, checkboxes
- **Score tracking:** Positive/negative events, rank
- **Model tracking:** Hvilke modeller arbejdede, sessions
- **Statistics:** Total tid, actions, models

### 4. AUTO_LOG.jsonl (MASTER)
**Single Source of Truth** for ALT logging:
- Alle handlinger med ISO 8601 timestamps
- Actor info (model_id, model_name, type)
- Terminal output (command, exit_code, stdout/stderr)
- Session tracking

**Se `LOG_FORMAT.md` for komplet specifikation.**

> **INGEN REDUNDANS:** Alt data eksisterer KUN ét sted!

---

## 3-PASS KONKURRENCE SYSTEM

### Pass 1: PLANLÆGNING
- Research 3 alternativer (PHASE 0)
- Definer opgaven (PHASE 1)
- Plan verificering (PHASE 2)
- **Giv score og udfyld REVIEW**

### Pass 2: EKSEKVERING
- Implementer løsning
- Kør tests (minimum 3)
- Git workflow
- **Score SKAL være højere end Pass 1**

### Pass 3: 7-DNA GENNEMGANG
- Gennemgå ALLE 7 DNA lag:
  1. SELF-AWARE - Kender systemet sig selv?
  2. SELF-DOCUMENTING - Er alt logget?
  3. SELF-VERIFYING - Er alt testet?
  4. SELF-IMPROVING - Har vi lært noget?
  5. SELF-ARCHIVING - Kun essens bevaret?
  6. PREDICTIVE - Hvad er næste skridt?
  7. SELF-OPTIMIZING - Kunne vi have gjort det bedre?
- Kør 5+ tests
- **Score SKAL være højere end Pass 2**
- **Total score SKAL være ≥ 24/30**

---

## ARKIVERING KRAV

Du kan IKKE arkivere før:
- [ ] Alle 3 passes complete
- [ ] Pass 2 score > Pass 1 score
- [ ] Pass 3 score > Pass 2 score
- [ ] Total score ≥ 24/30
- [ ] 5+ tests passed
- [ ] 7-DNA gennemgang udført

---

## CLAUDE FOKUS SYSTEM

### For AI Modeller
Når Claude åbner en sejr mappe:
1. **LÆS** `ARBEJDSFORHOLD.md` (obligatorisk)
2. **LÆS** `CLAUDE.md` i sejr mappen
3. **BEKRÆFT** forståelse til bruger
4. **ARBEJD** KUN på current task
5. **AFKRYDS** checkbox når færdig
6. **OPDATER** CLAUDE.md og fortsæt

### Anti-Dum Checkpoints
Hver 5 handlinger:
- Genlæs CLAUDE.md
- Bekræft task og pass
- Find næste unchecked checkbox
- Fortsæt

---

## SCRIPTS REFERENCE

| Script | Kommando | Funktion |
|--------|----------|----------|
| Opret sejr | `python3 scripts/generate_sejr.py --name "X"` | Ny sejr + alle filer |
| Byg context | `python3 scripts/build_claude_context.py --all` | Dynamisk CLAUDE.md |
| Verificer | `python3 scripts/auto_verify.py --all` | Check 3-pass status |
| Arkiver | `python3 scripts/auto_archive.py --sejr "X"` | Arkiver (hvis allowed) |
| Track | `python3 scripts/auto_track.py` | Opdater STATE.md |
| Learn | `python3 scripts/auto_learn.py` | Opdater PATTERNS.yaml |
| Predict | `python3 scripts/auto_predict.py` | Generer NEXT.md |
| Score | `python3 scripts/admiral_tracker.py --sejr "X"` | Score tracking |

---

## VIEWS (Terminal)

```bash
# Simpel terminal viewer
python3 view.py

# Avanceret TUI app (Textual)
python3 app/sejr_app.py
```

---

## 🎖️ ADMIRAL KONKURRENCE SYSTEM

Et **SCORE SYSTEM** der måler AI modellers performance objektivt!

### Positive Points (Belønning)
| Event | Points |
|-------|--------|
| CHECKBOX_DONE | +1 |
| PASS_COMPLETE | +10 |
| VERIFIED_WORKING | +5 |
| ADMIRAL_MOMENT | +10 |
| SEJR_ARCHIVED | +20 |

### Negative Points (Straf × 2!)
| Event | Points |
|-------|--------|
| TOKEN_WASTE | -6 |
| MEMORY_LOSS | -10 |
| LIE_DETECTED | -20 |
| RULE_BREAK | -20 |

### Rankings
| Rang | Score |
|------|-------|
| 🎖️ STORADMIRAL | 150+ |
| ⭐ ADMIRAL | 100-149 |
| 🏅 KAPTAJN | 50-99 |
| 🎗️ LØJTNANT | 20-49 |
| 📛 KADET | 0-19 |
| 💀 SKIBSDRENG | < 0 |

### Kommandoer
```bash
# Se leaderboard
python3 scripts/admiral_tracker.py --leaderboard

# Log event
python3 scripts/admiral_tracker.py --sejr "X" --event "CHECKBOX_DONE"

# Se score
python3 scripts/admiral_tracker.py --sejr "X" --score
```

Se MANUAL.md for fuld dokumentation af score systemet.

---

**Bygget af:** Kv1nt + Rasmus
**Dato:** 2026-01-25
**Status:** ✅ OPERATIONEL
