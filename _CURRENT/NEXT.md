# NEXT - Hvad Skal Ske Nu?

**Opdateret:** 2026-01-30
**Baseret paa:** `sejr verify` koerelse — 2 aktive, 10+ arkiverede

---

## STATUS

**2 AKTIVE SEJRLISTER i `10_ACTIVE/`**

| Sejrliste | Score | Naeste Handling |
|-----------|-------|-----------------|
| INTRO_DNA_AABNE_TASKS | 0/30 | Start Pass 1 — foerste uafkrydsede: A1 (Stripe undersoeegelse) |
| OPTIMERINGER_O4_O15 | 4/30 | Fortsaet Pass 1 — naeste uafkrydsede: D1 (Dependency check script) |

---

## INTRO_DNA — 4 Aabne Opgaver

| Task | Prioritet | Status | Blocker? |
|------|-----------|--------|----------|
| A. Stripe Migration | P0-2 | AABEN | Kræver Rasmus' haender (Stripe konto) |
| B. CLE Engine Startup | P0-3 | AABEN | Ingen |
| C. GraphQL Federation | P1-6 | BLOKERET | ELLE Phase 3 Agent Consolidation |
| D. Delete/Archive Duplikater | P1-11 | AABEN | Ingen |

**Anbefaling:** Start med B (CLE Engine) eller D (Duplikater) — de har ingen blokere.
A kraever Rasmus' input (Stripe konto). C er blokeret af ELLE Phase 3.

---

## OPTIMERINGER — 7 Opgaver (3 done, 4 aabne)

| Task | Status | Handling |
|------|--------|----------|
| A. O4 INTRO App | DONE | Implementeret session 24 |
| B. O5 ELLE Agent | DONE | Implementeret session 24 |
| C. O9 Scripts Katalog | DONE | Dokumenteret i GENVEJE |
| D. O12 Dependency Cron | AABEN | Byg admiral_dependency_check.sh |
| E. O13 VS Code Workspaces | AABEN | Opret .code-workspace filer |
| F. O14 Ollama Aliases | AABEN | Shell aliases for modeller |
| G. O15 Desktop Guide | AABEN | Keyboard shortcuts + workflow |

**Anbefaling:** Start med D (Dependency Check) — mest kritisk for systemsundhed.

---

## BAGGRUNDSMUSIK

Rasmus' direktiv: "DEN SKAL KOERE STILLE OG ROLIGT I BAGGRUNDEN SOM MUSIK"

Disse sejrlister er IKKE blokerende for andet arbejde. De er baggrundstasks
der loeses naar der er tid. Ingen stress, ingen rush.

---

## PREDICTIVE INSIGHTS

**Pattern:** 10/10 originale sejrlister gennemfoert med 29.9/30 gennemsnit
**Observation:** 2 nye sejrlister oprettet med REEL data (ikke skabelon-placeholders)
**Risiko:** INTRO_DNA task A (Stripe) kraever Rasmus' manuelle input
**Risiko:** INTRO_DNA task C (GraphQL) er blokeret af ekstern dependency

---

**Verificeret:** `sejr verify` 2026-01-30
