# SEJR: Test SEJR System Proof-of-Concept

**Oprettet:** 2026-01-23 22:55
**Status:** 🔵 IN PROGRESS
**Ejer:** Kv1nt + Rasmus

---

## PHASE 0: OPTIMIZATION (OBLIGATORISK - Før Bygning)

### External Search (MANDATORY)
- [ ] GitHub search: "{SEARCH_KEYWORDS}"
  - Resultat: {ANTAL} repos fundet
  - Best practice: {BESKRIVELSE}
  - Link: {URL}

- [ ] Documentation search: "{TECHNOLOGY} best practices"
  - Resultat: {ANTAL} artikler fundet
  - Key learning: {BESKRIVELSE}
  - Link: {URL}

- [ ] Web search: "{OPGAVE} optimization 2026"
  - Resultat: {ANTAL} ressourcer fundet
  - Insight: {BESKRIVELSE}

### Internal Search (MANDATORY)
- [ ] Previous projects: grep "{KEYWORDS}"
  - Resultat: {ANTAL} matches fundet
  - Reusable: {BESKRIVELSE}
  - Location: {PATH}

- [ ] Pattern library: Check for similar patterns
  - Resultat: {PATTERN_NAME} found/not found
  - Applicability: {BESKRIVELSE}

- [ ] Learned solutions: Query lessons learned
  - Resultat: {ANTAL} relevant lessons
  - Apply: {BESKRIVELSE}

### 3 Alternatives (MINIMUM - Tvungen Kreativ Udforskning)

**Alternative 1: {NAVN}**
- Approach: {BESKRIVELSE}
- Pros: {FORDELE}
- Cons: {ULEMPER}
- Time estimate: {TID}

**Alternative 2: {NAVN}**
- Approach: {BESKRIVELSE}
- Pros: {FORDELE}
- Cons: {ULEMPER}
- Time estimate: {TID}

**Alternative 3: {NAVN}**
- Approach: {BESKRIVELSE}
- Pros: {FORDELE}
- Cons: {ULEMPER}
- Time estimate: {TID}

### Decision (DOKUMENTERET)
- [ ] Chosen: **Alternative {NUMMER}** ({NAVN})
- [ ] Reasoning documented:
  ```
  Why this approach is optimal:
  {REASONING - Hvorfor denne løsning er bedst}

  Trade-offs accepted:
  {TRADE_OFFS - Hvilke kompromiser er acceptable}

  Time saved vs building from scratch:
  {TIME_SAVED}

  Quality gain:
  {QUALITY - Hvordan sikres kvalitet}
  ```

---

## PHASE 1: PLANNING (Baseret På Optimal Approach)

### Forstå Opgave
- [ ] Hvad skal bygges: {BESKRIVELSE}
  - Verify: {VERIFICERINGSKOMMANDO}

- [ ] Hvorfor skal det bygges: {FORMÅL}
  - Success criteria: {KRITERIER}

- [ ] Hvem er målgruppe: {MÅLGRUPPE}
  - User needs: {BEHOV}

### Design Løsning
- [ ] Arkitektur skitseret: {BESKRIVELSE}
  - Verify: {VERIFICERINGSKOMMANDO}

- [ ] Dependencies identificeret: {LISTE}
  - Verify: {VERIFICERINGSKOMMANDO}

- [ ] Integration punkter: {LISTE}
  - Verify: {VERIFICERINGSKOMMANDO}

---

## PHASE 2: UDVIKLING (Live Updates)

### Build Component 1: {NAVN}
- [ ] Kode skrevet: {BESKRIVELSE}
  - Verify: `{VERIFY_COMMAND_1}`
  - Location: {PATH}

- [ ] Tests oprettet: {BESKRIVELSE}
  - Verify: `{TEST_COMMAND_1}`

### Build Component 2: {NAVN}
- [ ] Kode skrevet: {BESKRIVELSE}
  - Verify: `{VERIFY_COMMAND_2}`
  - Location: {PATH}

- [ ] Tests oprettet: {BESKRIVELSE}
  - Verify: `{TEST_COMMAND_2}`

### Integration
- [ ] Komponenter forbundet: {BESKRIVELSE}
  - Verify: `{INTEGRATION_VERIFY}`

- [ ] End-to-end test: {BESKRIVELSE}
  - Verify: `{E2E_TEST}`

---

## PHASE 3: VERIFICATION (OBLIGATORISK - 300% FÆRDIGT)

### RUNNING (100% - System Operationelt)
- [ ] Service kører: {SERVICE_NAVN}
  - Verify: `systemctl status {SERVICE}` eller `curl {URL}`
  - Expected: {EXPECTED_OUTPUT}

- [ ] Port lytter: {PORT}
  - Verify: `ss -tlnp | grep {PORT}`
  - Expected: LISTEN state

### PROVEN (100% - Testet Med Real Data)
- [ ] Test med real data: {TEST_CASE}
  - Verify: `{TEST_COMMAND}`
  - Expected result: {EXPECTED}

- [ ] Output verificeret: {OUTPUT_TYPE}
  - Verify: `{VERIFY_OUTPUT}`
  - Location: {OUTPUT_PATH}

### TESTED (100% - Multiple Independent Verifications)
- [ ] Test 1: {TEST_NAVN}
  - Command: `{TEST_CMD_1}`
  - Result: {RESULT}

- [ ] Test 2: {TEST_NAVN}
  - Command: `{TEST_CMD_2}`
  - Result: {RESULT}

- [ ] Test 3: {TEST_NAVN}
  - Command: `{TEST_CMD_3}`
  - Result: {RESULT}

---

## PHASE 4: GIT WORKFLOW (OBLIGATORISK - Ikke "NÆSTEN")

### 5-Step Git Completion
- [ ] Step 1: git add
  - Command: `git add {FILES}`
  - Verify: `git status` shows staged files

- [ ] Step 2: git commit
  - Command: `git commit -m "{MESSAGE}"`
  - Verify: `git log -1` shows commit

- [ ] Step 3: git push
  - Command: `git push origin main`
  - Verify: Push successful

- [ ] Step 4: Remote sync verify
  - Command: `git ls-remote origin main`
  - Verify: Local SHA = Remote SHA

- [ ] Step 5: Working tree clean
  - Command: `git status`
  - Verify: "nothing to commit, working tree clean"

---

## SEMANTISK KONKLUSION (Skrives Når 100% Færdig)

### Hvad Lærte Vi (1-3 Sætninger)
{LEARNINGS}

### Hvad Kan Genbruges
- Template: {PATH_TIL_TEMPLATE}
- Script: {PATH_TIL_SCRIPT}
- Pattern: {PATTERN_BESKRIVELSE}

### Metrics
- Tid brugt: {TOTAL_TID}
- Tid estimeret: {ESTIMATED_TID}
- Difference: {DIFFERENCE}
- Blockers encountered: {ANTAL}
- Tests passed: {ANTAL}/{TOTAL}

---

## AUTO-TRACKING DATA (Do Not Edit Manually)

```yaml
auto_log_file: "AUTO_LOG.jsonl"
verify_status: "VERIFY_STATUS.yaml"
start_time: "{ISO_TIMESTAMP}"
end_time: null
total_time: null
pattern_learned: false
archived: false
```

---

**Verify this sejr is 300% FÆRDIGT:**
```bash
# RUNNING check
{RUNNING_VERIFY_CMD}

# PROVEN check
{PROVEN_VERIFY_CMD}

# TESTED check
{TESTED_VERIFY_CMD}

# Git check
git status && git log origin/main -1
```
