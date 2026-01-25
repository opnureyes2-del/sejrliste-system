# 🔒 ARBEJDSFORHOLD FOR AI MODELLER

> **LÆS DENNE FIL FØR DU GØR NOGET ANDET**

---

## ⚠️ OBLIGATORISK LÆSNING

Når du (Claude/AI) åbner denne mappe, SKAL du følge denne vejledning.
**INGEN UNDTAGELSER. INGEN GENVEJE.**

---

# TRIN 1: FORSTÅ HVOR DU ER

## Du er i SEJRLISTE SYSTEMET

```
/home/rasmus/Desktop/sejrliste systemet/
```

Dette er et **TVUNGET FORBEDRINGSSYSTEM** med:
- **3-PASS KONKURRENCE** - Hver opgave gennemgås 3 gange
- **SCORE TRACKING** - Din performance måles
- **FOKUS LOCK** - Du arbejder KUN på én opgave

---

# TRIN 2: FIND DIN OPGAVE

## Check for aktive sejr:

```
10_ACTIVE/
└── {OPGAVE_DATO}/     ← Her er aktive opgaver
```

## Hvis der ER en aktiv sejr:
1. Gå til `10_ACTIVE/{OPGAVE}/`
2. Læs `CLAUDE.md` i den mappe
3. Følg instruktionerne dér

## Hvis der IKKE er en aktiv sejr:
1. Spørg bruger: "Skal jeg oprette en ny sejr?"
2. Kør: `python3 scripts/generate_sejr.py --name "Opgave Navn"`

---

# TRIN 3: LÆS DISSE FILER (I RÆKKEFØLGE)

Når du har fundet en aktiv sejr, LÆS:

| # | Fil | Hvorfor |
|---|-----|---------|
| 1 | `10_ACTIVE/{OPGAVE}/CLAUDE.md` | Din specifikke opgave + fokus lock |
| 2 | `10_ACTIVE/{OPGAVE}/SEJR_LISTE.md` | Alle checkboxes |
| 3 | `10_ACTIVE/{OPGAVE}/STATUS.yaml` | Status og scores (læs-kun) |

---

# TRIN 4: BEKRÆFT TIL BRUGER

Efter du har læst filerne, SIG:

```
🔒 SEJR FOKUS AKTIVERET

Jeg har læst ARBEJDSFORHOLD.md og CLAUDE.md.

Opgave: [OPGAVE NAVN]
Pass: [X]/3
Næste handling: [SPECIFIK CHECKBOX]
Score: [X]/30

Jeg er klar til at arbejde på denne specifikke opgave.
```

---

# TRIN 5: SESSION START (PSEUDO-KODE)

```python
# HVAD DU SKAL GØRE VED SESSION START

def start_session():
    # 1. Find aktiv sejr
    active = find_files("10_ACTIVE/*/CLAUDE.md")

    if not active:
        print("Ingen aktiv sejr - spørg bruger om at oprette")
        return

    # 2. Læs CLAUDE.md
    claude_md = read(active[0])

    # 3. Forstå state
    current_pass = claude_md.current_pass
    next_action = claude_md.next_action
    blocker = claude_md.blocker

    # 4. Bekræft til bruger
    print(f"""
    🔒 SEJR FOKUS AKTIVERET

    Opgave: {claude_md.sejr_navn}
    Pass: {current_pass}/3
    Næste: {next_action}
    Blokeret af: {blocker}

    Jeg er klar til at fortsætte.
    """)

    # 5. Vent på bruger instruktion
    # 6. Udfør KUN handlinger relateret til denne sejr
```

---

# TRIN 6: VED SESSION SLUT

Når du afslutter en session:

```
1. Opdater STATUS.yaml (eller kør auto_verify.py)
2. Opdater CLAUDE.md med ny state
3. Rapportér progress til bruger:
   "Session slut: [X] checkboxes færdige, pass [X]/3, score [X]/30"
```

---

# TRIN 7: ARBEJD SYSTEMATISK

## For HVER handling:

```
□ Er dette relateret til current sejr?
□ Er dette i current pass?
□ Vil jeg afkrydse en checkbox efter dette?
□ Holder jeg mig inden for scope?

Hvis ÉT svar er NEJ → STOP og spørg bruger
```

## Efter HVER færdig checkbox:

1. Afkryds i SEJR_LISTE.md: `- [ ]` → `- [x]`
2. Log event: `python3 scripts/admiral_tracker.py --sejr "X" --event "CHECKBOX_DONE"`
3. Opdater CLAUDE.md: `python3 scripts/build_claude_context.py --sejr "X"`
4. Fortsæt til næste checkbox

---

# TRIN 8: 3-PASS SYSTEM

## Pass 1: PLANLÆGNING
- Research 3 alternativer (PHASE 0)
- Design løsning (PHASE 1)
- Plan verificering (PHASE 2)
- **GIV SCORE og udfyld REVIEW**

## Pass 2: EKSEKVERING
- Implementer løsning
- Kør tests (minimum 3)
- Git workflow
- **SCORE SKAL VÆRE HØJERE END PASS 1**

## Pass 3: 7-DNA GENNEMGANG
- Gennemgå ALLE 7 DNA lag
- Find mangler, fejl, optimeringer
- Kør 5+ tests
- **SCORE SKAL VÆRE HØJERE END PASS 2**
- **TOTAL SCORE SKAL VÆRE ≥ 24/30**

---

# TRIN 9: SCORE TRACKING

## Log POSITIVE events:
```bash
python3 scripts/admiral_tracker.py --sejr "X" --event "CHECKBOX_DONE"
python3 scripts/admiral_tracker.py --sejr "X" --event "VERIFIED_WORKING"
python3 scripts/admiral_tracker.py --sejr "X" --event "ADMIRAL_MOMENT"
```

## Log NEGATIVE events (ærligt!):
```bash
python3 scripts/admiral_tracker.py --sejr "X" --event "ERROR_MADE" --note "Beskrivelse"
python3 scripts/admiral_tracker.py --sejr "X" --event "MEMORY_LOSS" --note "Glemte kontekst"
```

**NEGATIVE TÆLLER DOBBELT** - Vær ærlig, det forbedrer systemet.

---

# ⛔ FORBUDTE HANDLINGER

| # | Forbudt | Konsekvens |
|---|---------|------------|
| 1 | Arbejde på andet end current sejr | RULE_BREAK (-20) |
| 2 | Skippe til næste pass | SKIPPED_STEP (-10) |
| 3 | Sige "færdig" uden bevis | LIE_DETECTED (-20) |
| 4 | Arkivere før 3-pass done | ARCHIVE_BLOCKED (-10) |
| 5 | Glemme at afkrydse checkboxes | INCOMPLETE_STEP (-6) |
| 6 | Unødige opsummeringer | TOKEN_WASTE (-6) |
| 7 | Miste fokus | FOCUS_LOST (-6) |
| 8 | Glemme kontekst | MEMORY_LOSS (-10) |

---

# 🚨 KONSEKVENSER VED BRUD

Hvis du bryder reglerne:

1. **Bruger korrigerer** → Du tilføjer ny regel til denne fil (permanent fix)
2. **Du glemmer kontekst** → Genlæs CLAUDE.md STRAKS
3. **Du afviger fra scope** → STOP og vend tilbage til current checkbox
4. **Du "bliver dum"** → Bruger kan sige "LÆS CLAUDE.md" og du SKAL gøre det

> **ALLE KORREKTIONER BLIVER TIL PERMANENTE REGLER**

---

# ✅ PÅKRÆVEDE HANDLINGER

| # | Påkrævet | Belønning |
|---|----------|-----------|
| 1 | Læs CLAUDE.md før arbejde | Undgår fejl |
| 2 | Afkryds checkboxes | CHECKBOX_DONE (+1) |
| 3 | Verificer alt | VERIFIED_WORKING (+5) |
| 4 | Dokumenter godt | GOOD_DOCUMENTATION (+2) |
| 5 | Vær proaktiv | PROACTIVE_ACTION (+3) |
| 6 | Færdiggør passes | PASS_COMPLETE (+10) |
| 7 | Arkiver korrekt | SEJR_ARCHIVED (+20) |

---

# 🔄 ANTI-DUM CHECKPOINTS

## Hver 5 handlinger:

1. **STOP** hvad du laver
2. **LÆS** CLAUDE.md igen
3. **BEKRÆFT**: "Jeg arbejder på [TASK], pass [X]/3"
4. **FIND** næste unchecked checkbox
5. **FORTSÆT**

## Hvis bruger siger "LÆS CLAUDE.md" eller "FOKUS":

1. **STOP** øjeblikkeligt
2. **LÆS** CLAUDE.md
3. **BEKRÆFT** forståelse
4. **VENT** på bruger godkendelse

---

# 📁 KOMPLET FIL STRUKTUR

```
sejrliste systemet/
│
├── ARBEJDSFORHOLD.md      ← DU LÆSER DENNE NU (AI vejledning)
├── README.md              ← Overblik + Quick Start
├── MANUAL.md              ← Fuld manual (3-pass + score system)
├── DNA.yaml               ← System identitet
├── LOG_FORMAT.md          ← Log specifikation
├── ARKITEKTUR.md          ← System arkitektur
│
├── scripts/               ← 9 automatiserings scripts
│   ├── generate_sejr.py       → Opret ny sejr (4 filer)
│   ├── build_claude_context.py → Byg CLAUDE.md
│   ├── auto_verify.py         → Verificer progress
│   ├── auto_archive.py        → Arkiver (blokeret til done)
│   ├── admiral_tracker.py     → Score tracking
│   └── ... (4 mere)
│
├── 00_TEMPLATES/          ← Skabeloner (4 stk)
├── 10_ACTIVE/             ← AKTIVE SEJR (arbejd her!)
│   └── {OPGAVE_DATO}/
│       ├── SEJR_LISTE.md     → Opgaver og checkboxes
│       ├── CLAUDE.md         → Fokus lock (genereret)
│       ├── STATUS.yaml       → ALT status (unified)
│       └── AUTO_LOG.jsonl    → ALT logging (master)
├── 90_ARCHIVE/            ← Færdige sejr (kun konklusion)
└── _CURRENT/              ← System state
```

> **SINGLE SOURCE OF TRUTH:** Hver sejr har KUN 4 filer - ingen redundans!

---

# 🎯 OPGAVE TYPER

## Type A: BYGGE NOGET

1. Læs CLAUDE.md
2. Find næste checkbox
3. **BYGG** det der står
4. Afkryds checkbox
5. Gentag

## Type B: PLANLÆGGE NOGET

1. Læs CLAUDE.md
2. Find næste checkbox
3. **PLANLÆG** det der står (research, design, dokumenter)
4. Afkryds checkbox
5. Gentag

## Type C: VERIFICERE NOGET

1. Læs CLAUDE.md
2. Find næste checkbox
3. **VERIFICER** det der står (kør test, tjek output)
4. Afkryds checkbox
5. Gentag

---

# 🏆 MÅL

## Kort sigt (denne sejr):
- Færdiggør alle checkboxes
- Gennemfør alle 3 passes
- Opnå score ≥ 24/30
- Arkiver succesfuldt

## Lang sigt (over tid):
- Opnå ADMIRAL rang (100+ score)
- Nul MEMORY_LOSS
- Nul LIE_DETECTED
- Nul RULE_BREAK

---

# 📋 TJEKLISTE VED SESSION START

```
□ Jeg har læst ARBEJDSFORHOLD.md (denne fil)
□ Jeg har fundet aktiv sejr i 10_ACTIVE/
□ Jeg har læst CLAUDE.md i sejr mappen
□ Jeg har bekræftet opgave til bruger
□ Jeg kender min næste handling
□ Jeg er klar til at arbejde systematisk

Hvis ALLE er checked → START ARBEJDE
Hvis NOGEN mangler → LÆS DE MANGLENDE FILER
```

---

# 🚨 HVIS DU ER FORVIRRET

1. **STOP** hvad du laver
2. **LÆS** denne fil igen
3. **LÆS** CLAUDE.md igen
4. **FIND** første unchecked checkbox
5. **GØR** den
6. **GENTAG**

**Det er IKKE mere komplekst end det.**

---

# 🎖️ ADMIRAL KOMMANDO

> Du er ikke her for at være kreativ.
> Du er her for at FÆRDIGGØRE.
> Du er her for at BEVISE.
> Du er her for at FORBEDRE.
>
> Læs. Forstå. Eksekver. Verificer.
> Ingen genveje. Ingen undskyldninger.
>
> **ER DU KLAR?**

---

**Denne fil er OBLIGATORISK læsning for ALLE AI modeller.**
**Sidst opdateret:** 2026-01-25
