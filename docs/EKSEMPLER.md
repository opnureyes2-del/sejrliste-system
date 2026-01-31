# [DOCS] EKSEMPLER - Konkrete Eksempler På Alt

> **Lær ved at se konkrete eksempler på korrekt og forkert adfærd.**

---

## EKSEMPEL 1: Opret Ny Sejr

### Kommando
```bash
cd "/home/rasmus/Desktop/sejrliste systemet"
python3 scripts/generate_sejr.py --name "Fix Login Bug" --goal "Rette timeout ved login"
```

### Resultat
```
[OK] Created sejr: FIX_LOGIN_BUG_2026-01-26
[DIR] Location: 10_ACTIVE/FIX_LOGIN_BUG_2026-01-26/
[FILE] Files created:
   - SEJR_LISTE.md (hovedopgave)
   - CLAUDE.md (fokus lock)
   - STATUS.yaml (status data)
   - AUTO_LOG.jsonl (log)
```

### Hvad Nu?
1. Åbn `10_ACTIVE/FIX_LOGIN_BUG_2026-01-26/SEJR_LISTE.md`
2. Udfyld PHASE 0 (research)
3. Afkryds checkboxes som du færdiggør dem

---

## EKSEMPEL 2: Udfyld PHASE 0 (Research)

### FØR (Template)
```markdown
### External Research (MANDATORY)
- [ ] GitHub search: "{SEARCH_KEYWORDS}"
  - Fundet: _antal repos_
  - Best practice: _beskrivelse_
  - Link: _url_
```

### EFTER (Udfyldt)
```markdown
### External Research (MANDATORY)
- [x] GitHub search: "react login timeout handling"
  - Fundet: 23 repos med lignende løsninger
  - Best practice: Use AbortController for timeout + retry logic
  - Link: github.com/example/auth-timeout-handler

- [x] Documentation search: "fetch timeout best practices"
  - Key learning: Default fetch has no timeout - ALTID sæt explicit timeout

- [x] Web search: "login timeout UX 2026"
  - Insight: Brugere forventer max 3 sekunder - vis loading indicator
```

---

## EKSEMPEL 3: Afkryds Checkboxes

### FORKERT [FAIL]
```markdown
- [x] Kode skrevet
```
(Ingen bevis, ingen verify kommando)

### KORREKT [OK]
```markdown
- [x] Kode skrevet
  - Verify: `wc -l src/auth/timeout-handler.ts`
  - Path: `src/auth/timeout-handler.ts`
  - Lines: 45 linjer
  - Output: "45 src/auth/timeout-handler.ts"
```

---

## EKSEMPEL 4: REPORT/REFLECT/EDUCATE

### FORKERT [FAIL]
```
Færdig. Hvad er næste?
```

### KORREKT [OK]
```
**REPORT:**
Jeg har tilføjet timeout handling til login funktionen i `src/auth/login.ts:45-67`.
Funktionen afbryder nu automatisk efter 5 sekunder og viser en retry knap.

**REFLECT:**
Dette løser det problem hvor brugere ventede i evighed på langsom server response.
Nu får de feedback efter 5 sekunder, hvilket er indenfor UX best practice (3-5 sek).

**EDUCATE:**
Timeout handling virker ved at bruge JavaScript's `AbortController`:
1. Vi opretter en controller: `const controller = new AbortController()`
2. Vi sætter en timeout: `setTimeout(() => controller.abort(), 5000)`
3. Vi sender controller.signal med fetch: `fetch(url, { signal: controller.signal })`
4. Hvis timeout rammer, kastes en AbortError som vi fanger og viser retry UI

Næste skridt: Skal vi tilføje retry logic så den automatisk prøver 3 gange?
```

---

## EKSEMPEL 5: 3-Pass Scoring

### Pass 1: Baseline (Score 6/10)
```markdown
### PASS 1 SCORE: 6/10

**Begrundelse:**
- [OK] Research gjort (3 sources)
- [OK] Plan dokumenteret
- [OK] Kode skrevet og virker
- [OK] 1 basic test passed
- [WARN] Mangler error handling
- [WARN] Hardcoded timeout value
- [WARN] Ingen retry logic
```

### Pass 2: Forbedret (Score 8/10)
```markdown
### PASS 2 SCORE: 8/10 (> Pass 1 [OK])

**Forbedring fra Pass 1:**
- [OK] Added error handling (try/catch)
- [OK] Timeout er nu configurable (miljøvariabel)
- [OK] Tilføjet retry logic (3 attempts)
- [OK] 3 tests passed (unit + integration + edge case)
- [WARN] Performance kunne være bedre
- [WARN] Mangler logging
```

### Pass 3: Optimeret (Score 9/10)
```markdown
### PASS 3 SCORE: 9/10 (> Pass 2 [OK])

**Forbedring fra Pass 2:**
- [OK] Performance optimeret (debounced retries)
- [OK] Logging tilføjet (console + analytics)
- [OK] 5+ tests passed
- [OK] Documentation komplet
- [OK] Edge cases håndteret (offline, slow network)

**Total: 23/30** - Tæt på 24 threshold!
```

---

## EKSEMPEL 6: Verificering

### Kør Verification
```bash
python3 scripts/auto_verify.py --sejr "FIX_LOGIN_BUG_2026-01-26"
```

### Output
```
=== VERIFICATION REPORT ===

Sejr: FIX_LOGIN_BUG_2026-01-26
Created: 2026-01-26 09:15

[DATA] Pass Progress:
   Pass 1: 10/10 checkboxes (100%) [OK]
   Pass 2: 12/12 checkboxes (100%) [OK]
   Pass 3: 15/15 checkboxes (100%) [OK]

 Scores:
   Pass 1: 6/10
   Pass 2: 8/10 (> Pass 1 [OK])
   Pass 3: 9/10 (> Pass 2 [OK])
   TOTAL:  23/30

[LOCK] Archive Status:
   Can Archive: NO
   Blocker: Total score 23 < 24 required

[IDEA] Suggestion:
   Review Pass 3 for improvement opportunities
   to reach 24/30 threshold
```

---

## EKSEMPEL 7: Admiral Score Logging

### Log Positive Event
```bash
python3 scripts/admiral_tracker.py --sejr "FIX_LOGIN_BUG" --event "CHECKBOX_DONE"
# Output: [OK] Logged: CHECKBOX_DONE (+1 point)
```

### Log Negative Event (Vær Ærlig!)
```bash
python3 scripts/admiral_tracker.py --sejr "FIX_LOGIN_BUG" --event "MEMORY_LOSS" --note "Glemte at læse CLAUDE.md"
# Output: [WARN] Logged: MEMORY_LOSS (-10 points, ×2 = -10)
```

### Se Score
```bash
python3 scripts/admiral_tracker.py --sejr "FIX_LOGIN_BUG" --score
```
Output:
```
=== ADMIRAL SCORE ===
Sejr: FIX_LOGIN_BUG
Positive: 45 points
Negative: 10 points (×2 = 20)
TOTAL: 25 points

Rang:  LØJTNANT (20-49)
```

---

## EKSEMPEL 8: Arkivering

### Forsøg Arkivering (Blokeret)
```bash
python3 scripts/auto_archive.py --sejr "FIX_LOGIN_BUG_2026-01-26"
```
Output:
```
[FAIL] ARCHIVE BLOCKED

Reason: Total score 23 < 24 required

Missing:
- [ ] Total score >= 24/30

Suggestion: Improve Pass 3 to increase score
```

### Arkivering (Success)
```bash
# Efter at have forbedret til 24/30:
python3 scripts/auto_archive.py --sejr "FIX_LOGIN_BUG_2026-01-26"
```
Output:
```
[OK] ARCHIVE SUCCESSFUL

Moved to: 90_ARCHIVE/FIX_LOGIN_BUG_2026-01-26_20260126_153000/
Created:
- CONCLUSION.md (semantisk essens)
- SEJR_DIPLOM.md (achievement certificate)
- ARCHIVE_METADATA.yaml

[ADMIRAL] ACHIEVEMENT UNLOCKED: SEJR_ARCHIVED (+20 points)
```

---

## EKSEMPEL 9: 7 DNA Lag Gennemgang (Pass 3)

### Lag 1: SELF-AWARE
```markdown
### DNA Lag 1: SELF-AWARE
> "Kender systemet sig selv?"
- [x] DNA.yaml opdateret med nye capabilities? **Ja - timeout handling tilføjet**
- [x] Systemets begrænsninger dokumenteret? **Ja - max 3 retries, 5s timeout**
- [x] Metadata korrekt? **Ja - version bumped to 1.1.0**

**Find mangler/fejl/optimering:** Ingen mangler fundet
```

### Lag 3: SELF-VERIFYING
```markdown
### DNA Lag 3: SELF-VERIFYING
> "Er alt verificeret med tests?"
- [x] Minimum 5 uafhængige tests? **Ja - 6 tests**
- [x] Edge cases testet? **Ja - offline, slow network, server error**
- [x] Error handling testet? **Ja - alle fejlscenarier covered**

**Find mangler/fejl/optimering:** Kunne tilføje performance test (nice-to-have)
```

---

## EKSEMPEL 10: Komplet Workflow

```bash
# === DAG 1: Start Sejr ===

# 1. Opret sejr
python3 scripts/generate_sejr.py --name "Add Dark Mode"

# 2. Læs CLAUDE.md
cat 10_ACTIVE/ADD_DARK_MODE_*/CLAUDE.md

# 3. Udfyld PHASE 0 (research) i SEJR_LISTE.md
# ... edit file ...

# 4. Verificer
python3 scripts/auto_verify.py --sejr "ADD_DARK_MODE_2026-01-26"

# 5. Log progress
python3 scripts/admiral_tracker.py --sejr "ADD_DARK_MODE" --event "CHECKBOX_DONE"


# === DAG 2: Fortsæt ===

# 6. Læs CLAUDE.md igen (husk hvor du var)
cat 10_ACTIVE/ADD_DARK_MODE_*/CLAUDE.md

# 7. Fortsæt PHASE 1-4 for Pass 1
# ... work ...

# 8. Når Pass 1 færdig - giv score og udfyld review
# 9. Start Pass 2 - fix issues fra review
# 10. Gentag for Pass 3


# === DAG 3: Arkiver ===

# 11. Final verification
python3 scripts/auto_verify.py --sejr "ADD_DARK_MODE_2026-01-26"

# 12. Arkiver
python3 scripts/auto_archive.py --sejr "ADD_DARK_MODE_2026-01-26"

# 13. Lær patterns
python3 scripts/auto_learn.py

# 14. Se leaderboard
python3 scripts/admiral_tracker.py --leaderboard
```

---

---

## [STOP] ANTI-PATTERNS (Hvad Du ALDRIG Skal Gøre)

### Anti-Pattern 1: Skip Research
```markdown
[FAIL] FORKERT:
## PHASE 0: Research
- [x] GitHub search: "..."
  - Fundet: Skippet, jeg ved hvad jeg laver
```
**Problem:** Du VED ikke bedre. Research finder altid noget nyt.

### Anti-Pattern 2: Fake Checkboxes
```markdown
[FAIL] FORKERT:
- [x] Test passed
  - (ingen verify command, ingen output)
```
**Problem:** Checkboxes uden bevis = LIE_DETECTED (-20 points)

### Anti-Pattern 3: Skip Review
```markdown
[FAIL] FORKERT:
Pass 1: Done!
Pass 2: Starting immediately...
```
**Problem:** Review er OBLIGATORISK. Du finder ALTID noget at forbedre.

### Anti-Pattern 4: Same Score
```markdown
[FAIL] FORKERT:
Pass 1: 7/10
Pass 2: 7/10  ← UACCEPTABELT
```
**Problem:** Pass 2 SKAL være > Pass 1. Ingen undtagelser.

### Anti-Pattern 5: Archive Without 3-Pass
```markdown
[FAIL] FORKERT:
"Færdig! Arkiverer nu..."
(men Pass 2 og 3 aldrig gjort)
```
**Problem:** Arkivering er BLOKERET indtil alle 3 passes er done med stigende scores.

### Anti-Pattern 6: Robotic Response
```markdown
[FAIL] FORKERT:
"Done. What's next?"
```
**Problem:** REPORT/REFLECT/EDUCATE er påkrævet. Robotic responses = TOKEN_WASTE.

### Anti-Pattern 7: Context Loss
```markdown
[FAIL] FORKERT:
"Hvad arbejdede vi på?"
```
**Problem:** LÆS CLAUDE.md! Den fortæller præcis hvad du arbejder på.

---

**Sidst opdateret:** 2026-01-26
**Version:** 1.1.0 (PASS 2 - tilføjet Anti-Patterns)
