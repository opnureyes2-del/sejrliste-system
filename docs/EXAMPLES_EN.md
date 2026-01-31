# EXAMPLES - Concrete Examples of Everything

> **Learn by seeing concrete examples of correct and incorrect behavior.**

---

## EXAMPLE 1: Create New Victory

### Command
```bash
cd "/home/rasmus/Desktop/sejrliste systemet"
python3 scripts/generate_sejr.py --name "Fix Login Bug" --goal "Fix timeout on login"
```

### Result
```
[OK] Created victory: FIX_LOGIN_BUG_2026-01-26
[DIR] Location: 10_ACTIVE/FIX_LOGIN_BUG_2026-01-26/
[FILE] Files created:
   - SEJR_LISTE.md (main task)
   - CLAUDE.md (focus lock)
   - STATUS.yaml (status data)
   - AUTO_LOG.jsonl (log)
```

### What Now?
1. Open `10_ACTIVE/FIX_LOGIN_BUG_2026-01-26/SEJR_LISTE.md`
2. Fill in PHASE 0 (research)
3. Check off checkboxes as you complete them

---

## EXAMPLE 2: Fill In PHASE 0 (Research)

### BEFORE (Template)
```markdown
### External Research (MANDATORY)
- [ ] GitHub search: "{SEARCH_KEYWORDS}"
  - Found: _number of repos_
  - Best practice: _description_
  - Link: _url_
```

### AFTER (Filled In)
```markdown
### External Research (MANDATORY)
- [x] GitHub search: "react login timeout handling"
  - Found: 23 repos with similar solutions
  - Best practice: Use AbortController for timeout + retry logic
  - Link: github.com/example/auth-timeout-handler

- [x] Documentation search: "fetch timeout best practices"
  - Key learning: Default fetch has no timeout - ALWAYS set explicit timeout

- [x] Web search: "login timeout UX 2026"
  - Insight: Users expect max 3 seconds - show loading indicator
```

---

## EXAMPLE 3: Check Off Checkboxes

### INCORRECT [FAIL]
```markdown
- [x] Code written
```
(No proof, no verify command)

### CORRECT [OK]
```markdown
- [x] Code written
  - Verify: `wc -l src/auth/timeout-handler.ts`
  - Path: `src/auth/timeout-handler.ts`
  - Lines: 45 lines
  - Output: "45 src/auth/timeout-handler.ts"
```

---

## EXAMPLE 4: REPORT/REFLECT/EDUCATE

### INCORRECT [FAIL]
```
Done. What's next?
```

### CORRECT [OK]
```
**REPORT:**
I've added timeout handling to the login function in `src/auth/login.ts:45-67`.
The function now automatically aborts after 5 seconds and shows a retry button.

**REFLECT:**
This solves the problem where users waited forever for slow server response.
Now they get feedback after 5 seconds, which is within UX best practice (3-5 sec).

**EDUCATE:**
Timeout handling works by using JavaScript's `AbortController`:
1. We create a controller: `const controller = new AbortController()`
2. We set a timeout: `setTimeout(() => controller.abort(), 5000)`
3. We send controller.signal with fetch: `fetch(url, { signal: controller.signal })`
4. If timeout hits, an AbortError is thrown which we catch and show retry UI

Next step: Should we add retry logic so it automatically tries 3 times?
```

---

## EXAMPLE 5: 3-Pass Scoring

### Pass 1: Baseline (Score 6/10)
```markdown
### PASS 1 SCORE: 6/10

**Justification:**
- [OK] Research done (3 sources)
- [OK] Plan documented
- [OK] Code written and works
- [OK] 1 basic test passed
- [WARN] Missing error handling
- [WARN] Hardcoded timeout value
- [WARN] No retry logic
```

### Pass 2: Improved (Score 8/10)
```markdown
### PASS 2 SCORE: 8/10 (> Pass 1 [OK])

**Improvement from Pass 1:**
- [OK] Added error handling (try/catch)
- [OK] Timeout is now configurable (environment variable)
- [OK] Added retry logic (3 attempts)
- [OK] 3 tests passed (unit + integration + edge case)
- [WARN] Performance could be better
- [WARN] Missing logging
```

### Pass 3: Optimized (Score 9/10)
```markdown
### PASS 3 SCORE: 9/10 (> Pass 2 [OK])

**Improvement from Pass 2:**
- [OK] Performance optimized (debounced retries)
- [OK] Logging added (console + analytics)
- [OK] 5+ tests passed
- [OK] Documentation complete
- [OK] Edge cases handled (offline, slow network)

**Total: 23/30** - Close to 24 threshold!
```

---

## EXAMPLE 6: Verification

### Run Verification
```bash
python3 scripts/auto_verify.py --sejr "FIX_LOGIN_BUG_2026-01-26"
```

### Output
```
=== VERIFICATION REPORT ===

Victory: FIX_LOGIN_BUG_2026-01-26
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

## EXAMPLE 7: Admiral Score Logging

### Log Positive Event
```bash
python3 scripts/admiral_tracker.py --sejr "FIX_LOGIN_BUG" --event "CHECKBOX_DONE"
# Output: [OK] Logged: CHECKBOX_DONE (+1 point)
```

### Log Negative Event (Be Honest!)
```bash
python3 scripts/admiral_tracker.py --sejr "FIX_LOGIN_BUG" --event "MEMORY_LOSS" --note "Forgot to read CLAUDE.md"
# Output: [WARN] Logged: MEMORY_LOSS (-10 points, ×2 = -10)
```

### See Score
```bash
python3 scripts/admiral_tracker.py --sejr "FIX_LOGIN_BUG" --score
```
Output:
```
=== ADMIRAL SCORE ===
Victory: FIX_LOGIN_BUG
Positive: 45 points
Negative: 10 points (×2 = 20)
TOTAL: 25 points

Rank:  LIEUTENANT (20-49)
```

---

## EXAMPLE 8: Archiving

### Attempt Archiving (Blocked)
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

### Archiving (Success)
```bash
# After improving to 24/30:
python3 scripts/auto_archive.py --sejr "FIX_LOGIN_BUG_2026-01-26"
```
Output:
```
[OK] ARCHIVE SUCCESSFUL

Moved to: 90_ARCHIVE/FIX_LOGIN_BUG_2026-01-26_20260126_153000/
Created:
- CONCLUSION.md (semantic essence)
- SEJR_DIPLOM.md (achievement certificate)
- ARCHIVE_METADATA.yaml

[ADMIRAL] ACHIEVEMENT UNLOCKED: SEJR_ARCHIVED (+20 points)
```

---

## EXAMPLE 9: 7 DNA Layer Review (Pass 3)

### Layer 1: SELF-AWARE
```markdown
### DNA Layer 1: SELF-AWARE
> "Does the system know itself?"
- [x] DNA.yaml updated with new capabilities? **Yes - timeout handling added**
- [x] System limitations documented? **Yes - max 3 retries, 5s timeout**
- [x] Metadata correct? **Yes - version bumped to 1.1.0**

**Find gaps/errors/optimization:** No gaps found
```

### Layer 3: SELF-VERIFYING
```markdown
### DNA Layer 3: SELF-VERIFYING
> "Is everything verified with tests?"
- [x] Minimum 5 independent tests? **Yes - 6 tests**
- [x] Edge cases tested? **Yes - offline, slow network, server error**
- [x] Error handling tested? **Yes - all error scenarios covered**

**Find gaps/errors/optimization:** Could add performance test (nice-to-have)
```

---

## EXAMPLE 10: Complete Workflow

```bash
# === DAY 1: Start Victory ===

# 1. Create victory
python3 scripts/generate_sejr.py --name "Add Dark Mode"

# 2. Read CLAUDE.md
cat 10_ACTIVE/ADD_DARK_MODE_*/CLAUDE.md

# 3. Fill in PHASE 0 (research) in SEJR_LISTE.md
# ... edit file ...

# 4. Verify
python3 scripts/auto_verify.py --sejr "ADD_DARK_MODE_2026-01-26"

# 5. Log progress
python3 scripts/admiral_tracker.py --sejr "ADD_DARK_MODE" --event "CHECKBOX_DONE"


# === DAY 2: Continue ===

# 6. Read CLAUDE.md again (remember where you were)
cat 10_ACTIVE/ADD_DARK_MODE_*/CLAUDE.md

# 7. Continue PHASE 1-4 for Pass 1
# ... work ...

# 8. When Pass 1 done - give score and fill in review
# 9. Start Pass 2 - fix issues from review
# 10. Repeat for Pass 3


# === DAY 3: Archive ===

# 11. Final verification
python3 scripts/auto_verify.py --sejr "ADD_DARK_MODE_2026-01-26"

# 12. Archive
python3 scripts/auto_archive.py --sejr "ADD_DARK_MODE_2026-01-26"

# 13. Learn patterns
python3 scripts/auto_learn.py

# 14. See leaderboard
python3 scripts/admiral_tracker.py --leaderboard
```

---

---

## ANTI-PATTERNS (What You Should NEVER Do)

### Anti-Pattern 1: Skip Research
```markdown
[FAIL] INCORRECT:
## PHASE 0: Research
- [x] GitHub search: "..."
  - Found: Skipped, I know what I'm doing
```
**Problem:** You DON'T know better. Research always finds something new.

### Anti-Pattern 2: Fake Checkboxes
```markdown
[FAIL] INCORRECT:
- [x] Test passed
  - (no verify command, no output)
```
**Problem:** Checkboxes without proof = LIE_DETECTED (-20 points)

### Anti-Pattern 3: Skip Review
```markdown
[FAIL] INCORRECT:
Pass 1: Done!
Pass 2: Starting immediately...
```
**Problem:** Review is MANDATORY. You ALWAYS find something to improve.

### Anti-Pattern 4: Same Score
```markdown
[FAIL] INCORRECT:
Pass 1: 7/10
Pass 2: 7/10  ← UNACCEPTABLE
```
**Problem:** Pass 2 MUST be > Pass 1. No exceptions.

### Anti-Pattern 5: Archive Without 3-Pass
```markdown
[FAIL] INCORRECT:
"Done! Archiving now..."
(but Pass 2 and 3 never done)
```
**Problem:** Archiving is BLOCKED until all 3 passes are done with increasing scores.

### Anti-Pattern 6: Robotic Response
```markdown
[FAIL] INCORRECT:
"Done. What's next?"
```
**Problem:** REPORT/REFLECT/EDUCATE is required. Robotic responses = TOKEN_WASTE.

### Anti-Pattern 7: Context Loss
```markdown
[FAIL] INCORRECT:
"What were we working on?"
```
**Problem:** READ CLAUDE.md! It tells exactly what you're working on.

---

**Last updated:** 2026-01-31
**Version:** 3.0.0 (PASS 2 - added Anti-Patterns)
