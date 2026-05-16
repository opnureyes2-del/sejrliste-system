# SEJRLISTE — SINGLE-SOURCE REGISTER (S175 R1)

**Sti:** `/home/rasmus/sejrliste systemet/REGISTER_SEJRLISTE_LOKATIONER.md`
**Forfatter:** KV1NT-PRO PID 517723 (S175 R1)
**Datum:** 2026-05-16T15:55Z
**Status:** PERMANENT IDENTIFIKATION — Rasmus' kritik "SEJRLISTE-mappen aldrig er identificeret" lukket

---

## 1. KERNE-INDSIGT (gåde-svar)

Sejrliste-systemet er **IKKE fragmenteret**. Det er **3 KOMPLEMENTERE ANSVARSOMRÅDER** + tilhørende støttefiler.
Tidligere kritik "aldrig identificeret" skyldtes manglende REGISTER-fil der peger på ALLE 3 + deres rolle.

Denne fil ER registret. Fra nu af = SINGLE-SOURCE for "hvor er hvad i sejrliste-systemet".

---

## 2. DE 3 ANSVARSOMRÅDER

### A. STREAMLIT-APP + MASTER-KODE (denne mappe)

- **Sti:** `/home/rasmus/sejrliste systemet/` ← du er her
- **Type:** Git-styret Python/Streamlit-applikation
- **Indhold (verificeret 2026-05-16):** 513 filer, 190 .md, struktur:
  - `app/` — Streamlit UI (LIVE port 8501 / 8503)
  - `10_ACTIVE/` — aktive sejre i workflow
  - `90_ARCHIVE/` — afsluttede sejre (43 underfoldere)
  - `_CURRENT/` — runtime state (MORNING_BRIEFING, STATE, NEXT, OPTIMIZED_PROMPT, LEARNED_TIPS)
  - `00_TEMPLATES/` — sejr-skabeloner
  - `app/`, `assets/`, `command-center/`, `docs/`, `DROP_HER/`
  - `DNA.yaml` (14KB) + `enforcement_engine.py` (26KB)
- **Live:** Streamlit-app kører på port 8501 + 8503 (verified `ss -tln`)
- **Rolle:** Visning + workflow-engine + state-mgmt for sejrliste

### B. SESSION-RENT_AFSLUT BOGFØRING (Desktop-arkiv)

- **Sti:** `/home/rasmus/Desktop/New 0 and alle 0s/SEJRLISTE/`
- **Type:** Historisk session-arkiv (ikke git, ikke duplikat af A)
- **Indhold (verificeret 2026-05-16):** 156 .md filer, **0 filnavn-overlap med A**
- **Eksempler:** `RENT_AFSLUT_KA5_S137_PID1634187.md`, `CROSS_PID_SYNTHESE_S165_S166_3PIDs.md`, `KRONOS_SYNTHESE_S166_PID1785747.md`, `MANGLENDE_SEJRE.md`
- **Rolle:** Permanent menneskelæsbar bogføring af cross-PID synteser, KRITISK_AUDIT-rapporter, projekt-gennemgange og rent-afslutter med 7-perspektiver
- **MEMORY-status:** 43 entries i `MEMORY.md` peger her — aktivt brugt

### C. MASTERMIND-ROLLE SPECIFIKATION

- **Sti:** `/home/rasmus/.admiral/mastermind_rum/SEJRLISTE/`
- **Type:** Organ-spec (SEJRLISTE som mastermind-rolle i admiral-fleet)
- **Indhold (verificeret 2026-05-16):** 12 filer / 10 .md
- **Struktur:** `1_INDHOLD`, `2_INFRASTRUKTUR`, `3_OPSAETNING`, `4_FRAMEWORKS`, `5_RAGS`, `6_PROMPTS`, `7_WORKFLOWS`, `8_RESEARCH`, `9_HOEJESTE_COUNCIL`, `_LAERERUM`, `MASTERMIND_INDEX.md`
- **Rolle:** Mastermind-rum hvor SEJRLISTE-admiralen "sidder" — fælles med 46 andre admiral-mastermind-rum

---

## 3. STØTTEFILER OG STATE

### State JSON-data

- `/home/rasmus/ELLE.md/AGENTS/state/sejrliste/` — **255 `victory_*.json`** (Streamlit-app læser dette)
- `/home/rasmus/ELLE.md/AGENTS/state/sejrliste/AFFILIATE_READY.md`, `BASELINE_*.md` etc. — daglige snapshots + chains

### Auto-bogføring + enforce-scripts

- `~/.admiral/admiral_sejrliste_enforce.py` — META #9 batch-audit (probe-mode default, --enforce-mode kræver Rasmus)
- `~/.admiral/hooks/sejrliste_auto_register.py` — Auto-registrér sejre i UI fra todo-release eller stdin

### Logs

- `~/ELLE.md/LOGS/sejrliste_web.log` + `sejrliste_web.error.log` — Streamlit-app logs
- `~/ELLE.md/LOGS/admiral-sejrliste-dvale.log` — dvale-tilstand logs
- `~/ELLE.md/REPORTS/autogen-sejrliste-recovery.log` — recovery-trace

### Auto-register hooks

- `~/.admiral/hooks/sejrliste_auto_register.py` (197 linjer, 2026-04-19) — bruges af todo-release og fokus-close

---

## 4. SYMLINKS (allerede konsolideret før denne audit)

- `/home/rasmus/Desktop/sejrliste systemet/` → SYMLINK → `/home/rasmus/sejrliste systemet/` (KLAR — peger på A)

---

## 5. TOMME / STRUKTUR-STUBS

### Helt tom mappe (kan slettes — 0 filer)

- `/home/rasmus/.local/share/sejrliste systemet/` — 0 filer, ingen tilsigtet rolle fundet → MARKERET FOR SLETNING

### Struktur-stubs (4 tomme underfoldere)

- `/home/rasmus/admiral-bogforing/komponenter/sejrliste-arkiv/` med `skelet/`, `system/`, `nul-typer/`, `dna/` — 0 filer total, men forberedt mappe-struktur
- BESLUTNING: Bevar med tilføjet `_STATUS_2026-05-16.md` der dokumenterer "TOM STUB — planlagt 7-nul-typer arkiv, ikke implementeret. Ejer: admiral-bogforing-komponenter."

---

## 6. HVOR REGISTRERER MAN EN NY SEJR?

**Anbefalet flow:**

```bash
# Via auto-register (foretrukken):
python3 ~/.admiral/hooks/sejrliste_auto_register.py \
  --todo-id "S175_R1" \
  --proof "REGISTER_SEJRLISTE_LOKATIONER.md skrevet + tomme oprydet" \
  --helhed-proof "sejrliste_entry:/home/rasmus/sejrliste systemet/REGISTER_SEJRLISTE_LOKATIONER.md" \
  --pid $$ \
  --session S175
```

Auto-register skriver `victory_*.json` til `/home/rasmus/ELLE.md/AGENTS/state/sejrliste/` (område C/Støtte) som Streamlit-app (område A) viser.

**For større session-rapporter** (synteser, kritisk-audit, projekt-gennemgang):
Skriv .md-fil i område B (`~/Desktop/New 0 and alle 0s/SEJRLISTE/`) med navngivning `<TYPE>_S<NUM>_PID<PID>.md`.

---

## 7. CROSS-REFERENCE (MEMORY.md → her)

`/home/rasmus/.claude-pro/projects/-home-rasmus/memory/MEMORY.md` har **43 entries** med sejrliste-referencer. Næste-PID skal læse MEMORY.md for kronologisk overblik + denne fil for strukturelt overblik.

---

## 8. ANSVAR

| Område | Ejer | Frekvens |
|---|---|---|
| A (Streamlit-app) | Rasmus + admiral-sejrliste-web.service | Live (port 8501/8503) |
| B (Desktop-arkiv) | Hver PID skriver eget RENT_AFSLUT | Per session |
| C (Mastermind-rum) | SEJRLISTE-admiral | Per organ-opdatering |
| Auto-register | Hooks fra todo-release | Per sejr |
| State JSON | Streamlit-app læser | Real-time |
| Logs | systemd-services | Per startup |
