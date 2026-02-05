# SEJR: ELLE_AGENT_KONSOLIDERING

**Oprettet:** 2026-02-05 13:47
**Status:** PASS 1 — IN PROGRESS
**Prioritet:** P2 — MEDIUM
**Current Pass:** 1/3
**Kontekst:** ELLE Phase 3 + ADMIRAL-HANDLINGER + API keys + INTRO DNA restopgaver

---

## 3-PASS KONKURRENCE SYSTEM (OBLIGATORISK)

```
PASS 1: FUNGERENDE     — Audit og plan
PASS 2: FORBEDRET      — Konsolidering og aktivering
PASS 3: OPTIMERET      — Automatiseret vedligehold
```

---

## PASS 1: AUDIT OG PLANLÆGNING

### A: ELLE Phase 3 — Agent Konsolidering (64 agents)

**Problem:** 64 agents, mange duplikater. 0/40 timer startet.

- [ ] A1: Komplet agent-audit — list ALLE agents
  - Command: `find /home/rasmus/Desktop/ELLE.md/AGENTS/ -maxdepth 2 -name "*.py" -o -name "*.md" | head -50`
  - Mål: Komplet inventar
- [ ] A2: Identificer duplikater og overlap
  - Dokument: Hvilke agents gør det samme?
- [ ] A3: Kategoriser: BEHOLD / MERGE / SLET
  - Beslutning per agent
- [ ] A4: Prioriterings-plan for konsolidering
  - Fase 1: Slet åbenlyse duplikater
  - Fase 2: Merge overlappende agents
  - Fase 3: Dokumenter endelig agent-arkitektur

---

### B: API-nøgle Aktivering (3 manglende)

- [ ] B1: Together.ai — Opret konto og hent API key
  - URL: https://together.ai
  - Indsæt i: relevant .env fil
- [ ] B2: HuggingFace — Opret/aktiver API token
  - URL: https://huggingface.co/settings/tokens
  - Indsæt i: relevant .env fil
- [ ] B3: Cerebras — Opret konto og hent API key
  - URL: https://cerebras.ai
  - Indsæt i: relevant .env fil
- [ ] B4: Verify alle 3 keys virker
  - Test: curl eller python script for hvert API

---

### C: ADMIRAL-HANDLINGER (7 items fra RASMUS TODO)

**Sti:** `/home/rasmus/Desktop/RASMUS TODO/ADMIRAL-HANDLINGER/`

- [ ] C1: Læs 01_ANTHROPIC_NOGLE.md — Anthropic key setup
  - Handling: _beskriv hvad der skal gøres_
- [ ] C2: Læs 02_RESEND_NOGLE.md — Resend key setup
  - Handling: _beskriv_
- [ ] C3: Læs 03_ROTER_NOGLER.md — Key rotation procedures
  - Handling: _beskriv_
- [ ] C4: Læs 04_USET_POTENTIALE.md — Unused potential
  - Handling: _beskriv_
- [ ] C5: Læs 05_HVAD_SYSTEMERNE_KAN_SAMMEN.md — System synergies
  - Handling: _beskriv_
- [ ] C6: Læs 06_ULTIMATIV_REDUNDANS.md — Redundancy plan
  - Handling: _beskriv_
- [ ] C7: Alle items enten udført eller planlagt

---

### D: INTRO DNA Restopgaver (4 items)

- [ ] D1: Stripe migration — Status og næste skridt
  - Blokeret af: Rasmus Stripe konto
- [ ] D2: CLE Engine startup optimering
- [ ] D3: GraphQL Federation — Status (blokeret af ELLE Phase 3)
- [ ] D4: Delete/archive duplicates — identifikation

---

### E: Stale filer cleanup i ELLE.md

- [ ] E1: Ryd LOCAL_TODOS.json (stale)
- [ ] E2: Ryd HVAD_SKAL_BYGGES_NU.md (stale)
- [ ] E3: Ryd ORGANIC_AI_REPLACEMENT_PLAN.md (stale)
- [ ] E4: Ryd MASTER_TODO (stale)
- [ ] E5: Verify ingen vigtig data mistes

---

## PASS 1 SCORE: ___/10

---

## PASS 2: FORBEDRET — Eksekvering
_Udfyldes efter Pass 1 review_

## PASS 3: OPTIMERET — 7-DNA Review
_Udfyldes efter Pass 2 review_

---

## ARCHIVE LOCK
```yaml
can_archive: false
total_score: null
```
