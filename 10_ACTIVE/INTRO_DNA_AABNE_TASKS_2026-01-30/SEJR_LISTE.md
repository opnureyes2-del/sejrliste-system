# SEJR: INTRO DNA — 4 Aabne Tasks

**Oprettet:** 2026-01-30
**Status:** PASS 1 — IN PROGRESS
**Ejer:** Kv1nt + Rasmus
**Current Pass:** 1/3
**Kilde:** TODO.md sektion 5 + MASTER_TODO_2026-01-03.md

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

### A. STRIPE MIGRATION (P0-2 — Consulting Project)

**Hvad:** Migrer betalingssystem til Stripe for cirkelline-consulting
**Hvorfor:** Nyt betalings-setup kraeves for consulting-projektet
**Status:** AABEN — ikke paabeyndt

- [ ] **A1.** Undersoeeg nuvaerende betalingssetup i cirkelline-consulting
  - Verify: `ls ~/Desktop/projekts/projects/cirkelline-consulting/`
  - Dokumenter: Hvad bruger vi i dag?

- [ ] **A2.** Opret Stripe-konto (Rasmus' haender) ELLER verificer eksisterende
  - Verify: Stripe dashboard tilgaengelig

- [ ] **A3.** Implementer Stripe integration
  - Verify: `python3 -c "import stripe; print(stripe.VERSION)"`
  - Dependencies: stripe Python pakke

- [ ] **A4.** Test betaling med Stripe test-mode
  - Verify: Test-transaktion gennemfoert
  - Result: _output_

- [ ] **A5.** Dokumenter i MASTER FOLDERS(INTRO)
  - Verify: `ls "/home/rasmus/Desktop/MASTER FOLDERS(INTRO)/cirkelline-consulting/"`

### B. CLE ENGINE STARTUP (P0-3)

**Hvad:** Start CLE Engine korrekt
**Hvorfor:** CLE Engine er en del af ELLE-oekosystemet men koerer ikke
**Status:** AABEN — ikke paabeyndt

- [ ] **B1.** Find CLE Engine lokation og laes kildekode
  - Verify: `find ~/Desktop -name "*cle*engine*" -type f 2>/dev/null`
  - Dokumenter: Hvad er CLE Engine?

- [ ] **B2.** Identificer dependencies og manglende setup
  - Verify: Laes imports og requirements

- [ ] **B3.** Opret venv og installer dependencies
  - Verify: `python3 -c "import cle_engine"` (eller tilsvarende)

- [ ] **B4.** Start CLE Engine og verificer funktionalitet
  - Verify: Service koerer + health check

- [ ] **B5.** Dokumenter i MASTER FOLDERS(INTRO)
  - Verify: INTRO-fil opdateret

### C. GRAPHQL FEDERATION (P1-6 — BLOKERET)

**Hvad:** GraphQL Federation setup
**Hvorfor:** Service-to-service kommunikation via GraphQL
**Status:** BLOKERET — Service inaktiv (ELLE Phase 2 done, service disabled)
**Blocker:** ELLE Phase 3 Agent Consolidation skal vaere faerdig foerst

- [ ] **C1.** Verificer at blocker stadig gaelder
  - Verify: `systemctl --user list-units | grep graphql`
  - Dokumenter: Er service stadig disabled?

- [ ] **C2.** Naar unblocked: Genaktiver GraphQL service
  - Verify: Service koerer

- [ ] **C3.** Implementer Federation gateway
  - Verify: `curl localhost:XXXX/graphql`

- [ ] **C4.** Test med real queries
  - Verify: Query returnerer data

- [ ] **C5.** Dokumenter i MASTER FOLDERS(INTRO)

### D. DELETE/ARCHIVE DUPLICATES (P1-11)

**Hvad:** Find og slet/arkiver duplikerede filer paa tvaers af systemet
**Hvorfor:** Duplikater skaber forvirring og spilder disk
**Status:** AABEN — pending verifikation

- [ ] **D1.** Scan for duplikater i ELLE.md (25 GB)
  - Verify: `fdupes -r ~/Desktop/ELLE.md/ | head -50` (eller tilsvarende)
  - Dokumenter: Antal duplikater + stoerrelse

- [ ] **D2.** Scan for duplikater i Desktop generelt
  - Verify: Rapport med fund

- [ ] **D3.** Kategoriser: SLET vs ARKIVER
  - Verify: Liste med beslutninger

- [ ] **D4.** Eksekverer sletning/arkivering
  - Verify: `df -h /` foer og efter

- [ ] **D5.** Dokumenter hvad der blev ryddet
  - Verify: Rapport i MIN ADMIRAL

---

## PASS 1 COMPLETION CHECKLIST

- [ ] Alle A1-A5 checkboxes afkrydset (Stripe)
- [ ] Alle B1-B5 checkboxes afkrydset (CLE Engine)
- [ ] C1 verificeret (GraphQL blocker status)
- [ ] Alle D1-D5 checkboxes afkrydset (Duplikater)
- [ ] Git committed med "PASS 1:" prefix

#### PASS 1 SCORE: ___/10

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
