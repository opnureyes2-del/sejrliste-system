# SEJR: AUTOFIX_SCRIPTS_KONSOLIDERING

**Oprettet:** 2026-02-05 21:42
**Status:** PASS 1 — IN PROGRESS
**Ejer:** Kv1nt + Rasmus
**Current Pass:** 1/3

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
**FORMAAL:** Sikre det BEDST mulige resultat HVER gang.

---



> **TIP:** Check `_CURRENT/LEARNED_TIPS.md` for advice baseret på tidligere sejr!

## PASS 1: FUNGERENDE ("Get It Working")

### PHASE 0: OPTIMIZATION (Foer Bygning)

#### External Research (MANDATORY)
- [ ] GitHub search: "{SEARCH_KEYWORDS}"
  - Fundet: _antal repos_
  - Best practice: _beskrivelse_
  - Link: _url_

- [ ] Documentation search: "{TECHNOLOGY} best practices"
  - Key learning: _beskrivelse_

- [ ] Web search: "{OPGAVE} optimization 2026"
  - Insight: _beskrivelse_

#### Internal Research (MANDATORY)
- [ ] Previous projects soegt: `grep "{KEYWORDS}"`
  - Reusable code: _path_

- [ ] Pattern library checked
  - Applicable patterns: _liste_

#### 3 Alternativer (MINIMUM)

| # | Approach | Pros | Cons | Tid |
|---|----------|------|------|-----|
| 1 | {NAVN} | {FORDELE} | {ULEMPER} | {TID} |
| 2 | {NAVN} | {FORDELE} | {ULEMPER} | {TID} |
| 3 | {NAVN} | {FORDELE} | {ULEMPER} | {TID} |

#### Beslutning
- [ ] Valgt: **Alternativ {X}**
- [ ] Begrundelse dokumenteret: _hvorfor_

---

### PHASE 1: PLANNING

- [ ] Hvad skal bygges: _beskrivelse_
- [ ] Hvorfor: _formaal_
- [ ] Success criteria: _kriterier_
- [ ] Arkitektur skitseret: _beskrivelse_
- [ ] Dependencies identificeret: _liste_

---

### PHASE 2: DEVELOPMENT

#### Component 1: {NAVN}
- [ ] Kode skrevet
  - Verify: `{COMMAND}`
  - Path: _{PATH}_

#### Component 2: {NAVN}
- [ ] Kode skrevet
  - Verify: `{COMMAND}`
  - Path: _{PATH}_

#### Integration
- [ ] Komponenter forbundet
  - Verify: `{COMMAND}`

---

### PHASE 3: BASIC VERIFICATION

#### RUNNING (System Operationelt)
- [ ] Service/kode koerer
  - Verify: `{COMMAND}`
  - Result: _{OUTPUT}_

#### PROVEN (Testet Med Data)
- [ ] Test med real data
  - Verify: `{COMMAND}`
  - Result: _{OUTPUT}_

#### TESTED (Minimum 1 Test)
- [ ] Basic test passed
  - Command: `{COMMAND}`
  - Result: _{OUTPUT}_

---

### PHASE 4: GIT WORKFLOW

- [ ] git add: `git add {FILES}`
- [ ] git commit: `git commit -m "PASS 1: {MESSAGE}"`
- [ ] git push: `git push origin {BRANCH}`
- [ ] Remote sync verified
- [ ] Working tree clean

---

### PASS 1 COMPLETION CHECKLIST

- [ ] Alle PHASE 0-4 checkboxes afkrydset
- [ ] Koden KOERER (ikke perfekt, men fungerende)
- [ ] Minimum 1 test passed
- [ ] Git committed med "PASS 1:" prefix

#### PASS 1 SCORE: ___/10

**Tid brugt paa Pass 1:** _{TID}_

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

### Forbedringer Fra Review

#### Fix 1: {PROBLEM}
- [ ] Implementeret: _beskrivelse af fix_
  - Before: _hvordan det var_
  - After: _hvordan det er nu_
  - Verify: `{COMMAND}`

#### Fix 2: {PROBLEM}
- [ ] Implementeret: _beskrivelse af fix_
  - Before: _hvordan det var_
  - After: _hvordan det er nu_
  - Verify: `{COMMAND}`

#### Fix 3: {PROBLEM}
- [ ] Implementeret: _beskrivelse af fix_
  - Before: _hvordan det var_
  - After: _hvordan det er nu_
  - Verify: `{COMMAND}`

---

### Nye Features Tilfojet

- [ ] Feature 1: _beskrivelse_
  - Verify: `{COMMAND}`

- [ ] Feature 2: _beskrivelse_
  - Verify: `{COMMAND}`

---

### Forbedret Testing

- [ ] Test 1 (Unit): _beskrivelse_
  - Command: `{COMMAND}`
  - Result: _{OUTPUT}_

- [ ] Test 2 (Integration): _beskrivelse_
  - Command: `{COMMAND}`
  - Result: _{OUTPUT}_

- [ ] Test 3 (Edge Case): _beskrivelse_
  - Command: `{COMMAND}`
  - Result: _{OUTPUT}_

---

### Forbedret Dokumentation

- [ ] README opdateret: _ja/nej_
- [ ] Inline comments tilfojet: _ja/nej_
- [ ] Usage examples tilfojet: _ja/nej_

---

### PASS 2 Git Commit

- [ ] git add: `git add .`
- [ ] git commit: `git commit -m "PASS 2: {IMPROVEMENTS}"`
- [ ] git push
- [ ] Working tree clean

---

### PASS 2 COMPLETION CHECKLIST

- [ ] ALLE review issues fixed
- [ ] Minimum 3 tests passed
- [ ] Dokumentation forbedret
- [ ] Kode kvalitet forbedret
- [ ] Git committed med "PASS 2:" prefix

#### PASS 2 SCORE: ___/10 (SKAL vaere > PASS 1 score)

**Tid brugt paa Pass 2:** _{TID}_
**Forbedring fra Pass 1:** _{BESKRIVELSE}_

---

## PASS 2 REVIEW (OBLIGATORISK)

> STOP. Foer du fortsaetter til Pass 3, SKAL du gennemgaa Pass 2 kritisk.

### Performance Optimering Muligheder
1. [ ] _mulighed 1_
2. [ ] _mulighed 2_

### Edge Cases Ikke Haandteret
1. [ ] _edge case 1_
2. [ ] _edge case 2_

### Kode Der Kan Simplificeres
1. [ ] _kompleks kode 1_ — _simplere version_
2. [ ] _kompleks kode 2_ — _simplere version_

### Manglende Error Handling
1. [ ] _scenario 1_
2. [ ] _scenario 2_

### Dokumentation Gaps
1. [ ] _hvad mangler_

---

## PASS 3: OPTIMERET ("Make It Best")

### Performance Optimeringer

- [ ] Optimering 1: _beskrivelse_
  - Before: _X ms/MB/etc_
  - After: _Y ms/MB/etc_
  - Improvement: _Z%_
  - Verify: `{COMMAND}`

- [ ] Optimering 2: _beskrivelse_
  - Before: _metric_
  - After: _metric_
  - Improvement: _%_

---

### Edge Cases Haandteret

- [ ] Edge case 1: _beskrivelse_
  - Test: `{COMMAND}`
  - Result: _{OUTPUT}_

- [ ] Edge case 2: _beskrivelse_
  - Test: `{COMMAND}`
  - Result: _{OUTPUT}_

---

### Kode Simplificering

- [ ] Refactoring 1: _beskrivelse_
  - Lines reduced: _X — Y_
  - Complexity reduced: _ja/nej_

---

### Final Error Handling

- [ ] All errors caught and logged: _ja/nej_
- [ ] Graceful degradation: _ja/nej_
- [ ] User-friendly error messages: _ja/nej_

---

### Final Documentation

- [ ] README komplet
- [ ] All functions documented
- [ ] Examples for all use cases
- [ ] Changelog updated

---

## FINAL VERIFICATION (OBLIGATORISK — 300% FAERDIG)

### RUNNING (100% — System Operationelt)
- [ ] Verification 1: _beskrivelse_
  - Command: `{COMMAND}`
  - Expected: _{OUTPUT}_
  - Actual: _{OUTPUT}_
  - Status: PASS/FAIL

- [ ] Verification 2: _beskrivelse_
  - Command: `{COMMAND}`
  - Expected: _{OUTPUT}_
  - Actual: _{OUTPUT}_
  - Status: PASS/FAIL

### PROVEN (100% — Testet Med Real Data)
- [ ] Real data test 1: _beskrivelse_
  - Command: `{COMMAND}`
  - Result: _{OUTPUT}_
  - Status: PASS/FAIL

- [ ] Real data test 2: _beskrivelse_
  - Command: `{COMMAND}`
  - Result: _{OUTPUT}_
  - Status: PASS/FAIL

### TESTED (100% — 5+ Uafhaengige Tests)
- [ ] Test 1: _{NAVN}_ — PASS/FAIL
- [ ] Test 2: _{NAVN}_ — PASS/FAIL
- [ ] Test 3: _{NAVN}_ — PASS/FAIL
- [ ] Test 4: _{NAVN}_ — PASS/FAIL
- [ ] Test 5: _{NAVN}_ — PASS/FAIL

---

### PASS 3 Git Commit

- [ ] git add: `git add .`
- [ ] git commit: `git commit -m "PASS 3 FINAL: {MESSAGE}"`
- [ ] git push
- [ ] Remote sync verified: `git ls-remote origin {BRANCH}`
- [ ] Working tree clean: `git status`

---

### PASS 3 COMPLETION CHECKLIST

- [ ] ALL performance optimizations done
- [ ] ALL edge cases handled
- [ ] ALL error handling complete
- [ ] 5+ tests passed
- [ ] Documentation 100% complete
- [ ] Git committed med "PASS 3 FINAL:" prefix

#### PASS 3 SCORE: ___/10 (SKAL vaere > PASS 2 score)

**Tid brugt paa Pass 3:** _{TID}_

---

## 3-PASS RESULTAT

| Pass | Score | Tid | Forbedring |
|------|-------|-----|------------|
| Pass 1 | _/10 | _min | Baseline |
| Pass 2 | _/10 | _min | +_% fra Pass 1 |
| Pass 3 | _/10 | _min | +_% fra Pass 2 |
| **TOTAL** | **_/30** | **_min** | **_% total forbedring** |

### Bevis For Forbedring (OBLIGATORISK)

#### Pass 1 — Pass 2 Forbedring
_Beskriv konkret hvad der blev forbedret og hvordan det maalbart er bedre_

#### Pass 2 — Pass 3 Forbedring
_Beskriv konkret hvad der blev optimeret og hvordan det maalbart er bedre_

---

## SEMANTISK KONKLUSION (Kun Naar PASS 3 Komplet)

### Hvad Laerte Vi (3-5 Saetninger)
_learnings_

### Hvad Kan Genbruges
- Template: _{PATH}_
- Script: _{PATH}_
- Pattern: _{BESKRIVELSE}_

### Metrics
- Total tid: _{TID}_
- Pass 1 tid: _{TID}_
- Pass 2 tid: _{TID}_
- Pass 3 tid: _{TID}_
- Tests passed: _{ANTAL}/_{TOTAL}_
- Final score: _{SCORE}/30_

---

## ARCHIVE LOCK

```yaml
# DO NOT EDIT — Auto-generated
pass_1_complete: false
pass_1_score: null
pass_1_time: null
pass_1_review_done: false

pass_2_complete: false
pass_2_score: null
pass_2_time: null
pass_2_review_done: false

pass_3_complete: false
pass_3_score: null
pass_3_time: null
final_verification_done: false

can_archive: false  # Bliver ALDRIG true foer alle 3 passes er done
total_score: null
total_time: null
```

---

**ARCHIVE BLOCKED UNTIL:**
- [ ] Pass 1 complete + reviewed
- [ ] Pass 2 complete + reviewed (score > Pass 1)
- [ ] Pass 3 complete + final verification (score > Pass 2)
- [ ] Total score >= 24/30
- [ ] All 5+ final tests passed

---
