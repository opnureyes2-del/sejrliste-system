# LOG FORMAT SPECIFIKATION

> **ADMIRAL STANDARD - Komplet Sporbarhed**
> **Version:** 1.0.0
> **Dato:** 2026-01-25

---

## FORMÅL

Sikre at HVER handling i systemet kan spores tilbage til:
- **HVEM** (hvilken model/bruger)
- **HVAD** (hvilken handling)
- **HVORNÅR** (præcis tidspunkt)
- **HVOR** (hvilken sejr/fil)
- **HVORFOR** (kontekst)
- **RESULTAT** (terminal output/status)

---

## LOG FILER PER SEJR

Hver sejr mappe har disse log filer:

| Fil | Formål | Format |
|-----|--------|--------|
| `AUTO_LOG.jsonl` | Alle handlinger | JSON Lines |
| `TERMINAL_LOG.md` | Terminal output | Markdown |
| `MODEL_HISTORY.yaml` | Hvilke modeller arbejdede | YAML |

---

## AUTO_LOG.jsonl FORMAT

### Påkrævet Schema

```json
{
  "timestamp": "2026-01-25T14:30:00.123456+01:00",
  "session_id": "sess_abc123",
  "actor": {
    "type": "ai|human|script",
    "name": "Claude Opus 4.5|Rasmus|generate_sejr.py",
    "model_id": "claude-opus-4-5-20251101|null|null"
  },
  "action": "ACTION_TYPE",
  "target": {
    "file": "SEJR_LISTE.md",
    "line": 42,
    "section": "PHASE 2: Development"
  },
  "details": {
    "description": "Hvad blev gjort",
    "before": "Før-tilstand (hvis relevant)",
    "after": "Efter-tilstand (hvis relevant)"
  },
  "terminal": {
    "command": "python3 test.py",
    "exit_code": 0,
    "stdout": "Test passed",
    "stderr": "",
    "duration_ms": 1234
  },
  "pass": 1,
  "checkpoint": "PHASE_2_DEV",
  "score_impact": "+1 CHECKBOX_DONE"
}
```

### Påkrævede Felter (ALTID)

| Felt | Type | Beskrivelse |
|------|------|-------------|
| `timestamp` | ISO 8601 | Fuld tidsstempel med timezone |
| `session_id` | string | Unik session identifier |
| `actor.type` | enum | `ai`, `human`, eller `script` |
| `actor.name` | string | Navn på model/bruger/script |
| `action` | string | Handling type (se liste nedenfor) |
| `pass` | int | Hvilken pass (1, 2, eller 3) |

### Valgfrie Felter (Når Relevant)

| Felt | Type | Hvornår |
|------|------|---------|
| `actor.model_id` | string | Når actor er AI |
| `target.*` | object | Når handling rammer specifik fil/linje |
| `details.*` | object | Ekstra kontekst |
| `terminal.*` | object | Når terminal kommando køres |
| `score_impact` | string | Når handling påvirker score |

---

## ACTION TYPES

### Session Actions
| Action | Beskrivelse |
|--------|-------------|
| `SESSION_START` | Ny session startet |
| `SESSION_END` | Session afsluttet |
| `SESSION_RESUME` | Session genoptaget |
| `CONTEXT_LOADED` | CLAUDE.md læst |

### Arbejds Actions
| Action | Beskrivelse |
|--------|-------------|
| `CHECKBOX_START` | Begyndt på checkbox |
| `CHECKBOX_DONE` | Checkbox afkrydset |
| `PHASE_START` | Startet ny phase |
| `PHASE_COMPLETE` | Phase færdiggjort |
| `PASS_COMPLETE` | Pass færdiggjort |

### Fil Actions
| Action | Beskrivelse |
|--------|-------------|
| `FILE_READ` | Fil læst |
| `FILE_EDIT` | Fil redigeret |
| `FILE_CREATE` | Fil oprettet |
| `FILE_DELETE` | Fil slettet |

### Terminal Actions
| Action | Beskrivelse |
|--------|-------------|
| `COMMAND_RUN` | Terminal kommando kørt |
| `TEST_RUN` | Test kørt |
| `GIT_COMMIT` | Git commit lavet |
| `GIT_PUSH` | Git push lavet |
| `SCRIPT_RUN` | Python script kørt |

### Verification Actions
| Action | Beskrivelse |
|--------|-------------|
| `VERIFY_START` | Verificering startet |
| `VERIFY_PASS` | Verificering bestået |
| `VERIFY_FAIL` | Verificering fejlet |

### Score Actions
| Action | Beskrivelse |
|--------|-------------|
| `SCORE_POSITIVE` | Positive points tilføjet |
| `SCORE_NEGATIVE` | Negative points tilføjet |
| `RANK_CHANGED` | Rang ændret |

### Error Actions
| Action | Beskrivelse |
|--------|-------------|
| `ERROR_OCCURRED` | Fejl opstået |
| `ERROR_FIXED` | Fejl rettet |
| `FOCUS_LOST` | Fokus mistet (anti-dum) |
| `FOCUS_RESTORED` | Fokus genoprettet |

---

## TERMINAL_LOG.md FORMAT

Human-readable log af alle terminal kommandoer:

```markdown
# TERMINAL LOG - {SEJR_NAVN}

---

## Session: {SESSION_ID}
**Startet:** {TIMESTAMP}
**Model:** {MODEL_NAME}

### Kommando 1
```bash
$ python3 test.py
```
**Exit code:** 0
**Tid:** 1.234s
**Output:**
```
Test passed
All 5 tests OK
```

### Kommando 2
```bash
$ git status
```
**Exit code:** 0
**Tid:** 0.045s
**Output:**
```
On branch main
nothing to commit, working tree clean
```

---
```

---

## MODEL_HISTORY.yaml FORMAT

Tracker hvilke modeller arbejdede på denne sejr:

```yaml
# MODEL HISTORY - Auto-generated
# DO NOT EDIT MANUALLY

sejr_navn: "Min Opgave"
created: "2026-01-25T14:00:00+01:00"

models_used:
  - model_id: "claude-opus-4-5-20251101"
    model_name: "Claude Opus 4.5"
    first_seen: "2026-01-25T14:00:00+01:00"
    last_seen: "2026-01-25T16:30:00+01:00"
    sessions: 3
    actions_count: 45
    checkboxes_completed: 12

  - model_id: "claude-sonnet-4-20250514"
    model_name: "Claude Sonnet 4"
    first_seen: "2026-01-25T15:00:00+01:00"
    last_seen: "2026-01-25T15:45:00+01:00"
    sessions: 1
    actions_count: 23
    checkboxes_completed: 8

human_activity:
  first_seen: "2026-01-25T14:00:00+01:00"
  last_seen: "2026-01-25T16:30:00+01:00"
  sessions: 2
  approvals: 5
  corrections: 2

sessions:
  - id: "sess_abc123"
    started: "2026-01-25T14:00:00+01:00"
    ended: "2026-01-25T14:30:00+01:00"
    model: "claude-opus-4-5-20251101"
    pass: 1
    checkboxes_done: 5

  - id: "sess_def456"
    started: "2026-01-25T15:00:00+01:00"
    ended: "2026-01-25T15:45:00+01:00"
    model: "claude-sonnet-4-20250514"
    pass: 2
    checkboxes_done: 8

statistics:
  total_sessions: 4
  total_actions: 68
  total_commands: 23
  total_time_minutes: 120
  models_count: 2
```

---

## LOGGING EKSEMPLER

### Eksempel 1: Session Start
```json
{
  "timestamp": "2026-01-25T14:00:00.000000+01:00",
  "session_id": "sess_abc123",
  "actor": {
    "type": "ai",
    "name": "Claude Opus 4.5",
    "model_id": "claude-opus-4-5-20251101"
  },
  "action": "SESSION_START",
  "details": {
    "description": "Startede arbejde på sejr",
    "context_loaded": true,
    "claude_md_read": true
  },
  "pass": 1
}
```

### Eksempel 2: Checkbox Completed
```json
{
  "timestamp": "2026-01-25T14:15:30.123456+01:00",
  "session_id": "sess_abc123",
  "actor": {
    "type": "ai",
    "name": "Claude Opus 4.5",
    "model_id": "claude-opus-4-5-20251101"
  },
  "action": "CHECKBOX_DONE",
  "target": {
    "file": "SEJR_LISTE.md",
    "line": 42,
    "section": "PHASE 2: Development"
  },
  "details": {
    "description": "Implementerede auth handler",
    "checkbox_text": "Kode skrevet for auth handler"
  },
  "pass": 1,
  "score_impact": "+1 CHECKBOX_DONE"
}
```

### Eksempel 3: Terminal Kommando
```json
{
  "timestamp": "2026-01-25T14:20:00.000000+01:00",
  "session_id": "sess_abc123",
  "actor": {
    "type": "ai",
    "name": "Claude Opus 4.5",
    "model_id": "claude-opus-4-5-20251101"
  },
  "action": "COMMAND_RUN",
  "terminal": {
    "command": "python3 -m pytest tests/",
    "exit_code": 0,
    "stdout": "5 passed in 1.23s",
    "stderr": "",
    "duration_ms": 1234
  },
  "details": {
    "description": "Kørte test suite",
    "purpose": "Verificer implementation"
  },
  "pass": 1,
  "score_impact": "+3 TEST_PASSED"
}
```

### Eksempel 4: Human Approval
```json
{
  "timestamp": "2026-01-25T14:25:00.000000+01:00",
  "session_id": "sess_abc123",
  "actor": {
    "type": "human",
    "name": "Rasmus"
  },
  "action": "APPROVAL_GIVEN",
  "details": {
    "description": "Godkendte Pass 1 review",
    "approved_item": "Pass 1 completion"
  },
  "pass": 1
}
```

### Eksempel 5: Error Logged
```json
{
  "timestamp": "2026-01-25T14:30:00.000000+01:00",
  "session_id": "sess_abc123",
  "actor": {
    "type": "ai",
    "name": "Claude Opus 4.5",
    "model_id": "claude-opus-4-5-20251101"
  },
  "action": "ERROR_OCCURRED",
  "terminal": {
    "command": "python3 broken_script.py",
    "exit_code": 1,
    "stdout": "",
    "stderr": "ImportError: No module named 'missing'",
    "duration_ms": 50
  },
  "details": {
    "description": "Script fejlede pga manglende modul",
    "error_type": "ImportError",
    "resolution": "Skal installere missing modul"
  },
  "pass": 1,
  "score_impact": "-3 ERROR_MADE"
}
```

---

## AUTO-LOGGING REGLER

### AI Modeller SKAL Logge

| Hvornår | Action | Påkrævet |
|---------|--------|----------|
| Ved session start | `SESSION_START` | [OK] JA |
| Ved læsning af CLAUDE.md | `CONTEXT_LOADED` | [OK] JA |
| Ved start på checkbox | `CHECKBOX_START` | [OK] JA |
| Ved færdig checkbox | `CHECKBOX_DONE` | [OK] JA |
| Ved terminal kommando | `COMMAND_RUN` | [OK] JA |
| Ved fejl | `ERROR_OCCURRED` | [OK] JA |
| Ved pass complete | `PASS_COMPLETE` | [OK] JA |
| Ved session slut | `SESSION_END` | [OK] JA |

### Scripts SKAL Logge

| Script | Auto-logger |
|--------|-------------|
| generate_sejr.py | `sejr_created`, `files_created` |
| build_claude_context.py | `claude_md_generated` |
| auto_verify.py | `verify_start`, `verify_pass/fail` |
| auto_archive.py | `archive_start`, `archive_complete` |
| admiral_tracker.py | `score_positive`, `score_negative` |

---

## VERIFICATION

### Test Log Format
```bash
# Verificer JSON er valid
python3 -c "import json; [json.loads(l) for l in open('AUTO_LOG.jsonl')]"
```

### Påkrævet Felter Check
```bash
# Check alle entries har timestamp og actor
python3 -c "
import json
for line in open('AUTO_LOG.jsonl'):
    e = json.loads(line)
    assert 'timestamp' in e, 'Missing timestamp'
    assert 'actor' in e, 'Missing actor'
    assert 'action' in e, 'Missing action'
print('All entries valid!')
"
```

---

## ADMIRAL STANDARD COMPLIANCE

For at være ADMIRAL compliant SKAL logs:

- [ ] Bruge ISO 8601 timestamps med timezone
- [ ] Inkludere fuld model_id for AI actors
- [ ] Logge ALLE terminal kommandoer med output
- [ ] Logge ALLE checkbox completions
- [ ] Logge ALLE fejl med detaljer
- [ ] Være valid JSON på hver linje

---

**Denne specifikation er OBLIGATORISK for alle sejr i systemet.**

