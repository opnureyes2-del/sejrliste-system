# LOG FORMAT SPECIFICATION

> **ADMIRAL STANDARD - Complete Traceability**
> **Version:** 3.0.0
> **Date:** 2026-01-31

---

## PURPOSE

Ensure that EVERY action in the system can be traced back to:
- **WHO** (which model/user)
- **WHAT** (which action)
- **WHEN** (exact time)
- **WHERE** (which victory/file)
- **WHY** (context)
- **RESULT** (terminal output/status)

---

## LOG FILES PER VICTORY

Each victory folder has these log files:

| File | Purpose | Format |
|------|---------|--------|
| `AUTO_LOG.jsonl` | All actions | JSON Lines |
| `STATUS.yaml` | Status + model history | YAML |

---

## AUTO_LOG.jsonl FORMAT

### Required Schema

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
    "description": "What was done",
    "before": "Before state (if relevant)",
    "after": "After state (if relevant)"
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

### Required Fields (ALWAYS)

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 | Full timestamp with timezone |
| `session_id` | string | Unique session identifier |
| `actor.type` | enum | `ai`, `human`, or `script` |
| `actor.name` | string | Name of model/user/script |
| `action` | string | Action type (see list below) |
| `pass` | int | Which pass (1, 2, or 3) |

### Optional Fields (When Relevant)

| Field | Type | When |
|-------|------|------|
| `actor.model_id` | string | When actor is AI |
| `target.*` | object | When action affects specific file/line |
| `details.*` | object | Extra context |
| `terminal.*` | object | When terminal command is run |
| `score_impact` | string | When action affects score |

---

## ACTION TYPES

### Session Actions
| Action | Description |
|--------|-------------|
| `SESSION_START` | New session started |
| `SESSION_END` | Session ended |
| `SESSION_RESUME` | Session resumed |
| `CONTEXT_LOADED` | CLAUDE.md read |

### Work Actions
| Action | Description |
|--------|-------------|
| `CHECKBOX_START` | Started on checkbox |
| `CHECKBOX_DONE` | Checkbox checked off |
| `PHASE_START` | Started new phase |
| `PHASE_COMPLETE` | Phase completed |
| `PASS_COMPLETE` | Pass completed |

### File Actions
| Action | Description |
|--------|-------------|
| `FILE_READ` | File read |
| `FILE_EDIT` | File edited |
| `FILE_CREATE` | File created |
| `FILE_DELETE` | File deleted |

### Terminal Actions
| Action | Description |
|--------|-------------|
| `COMMAND_RUN` | Terminal command run |
| `TEST_RUN` | Test run |
| `GIT_COMMIT` | Git commit made |
| `GIT_PUSH` | Git push made |
| `SCRIPT_RUN` | Python script run |

### Verification Actions
| Action | Description |
|--------|-------------|
| `VERIFY_START` | Verification started |
| `VERIFY_PASS` | Verification passed |
| `VERIFY_FAIL` | Verification failed |

### Score Actions
| Action | Description |
|--------|-------------|
| `SCORE_POSITIVE` | Positive points added |
| `SCORE_NEGATIVE` | Negative points added |
| `RANK_CHANGED` | Rank changed |

### Error Actions
| Action | Description |
|--------|-------------|
| `ERROR_OCCURRED` | Error occurred |
| `ERROR_FIXED` | Error fixed |
| `FOCUS_LOST` | Focus lost (anti-drift) |
| `FOCUS_RESTORED` | Focus restored |

---

## LOGGING EXAMPLES

### Example 1: Session Start
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
    "description": "Started work on victory",
    "context_loaded": true,
    "claude_md_read": true
  },
  "pass": 1
}
```

### Example 2: Checkbox Completed
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
    "description": "Implemented auth handler",
    "checkbox_text": "Code written for auth handler"
  },
  "pass": 1,
  "score_impact": "+1 CHECKBOX_DONE"
}
```

### Example 3: Terminal Command
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
    "description": "Ran test suite",
    "purpose": "Verify implementation"
  },
  "pass": 1,
  "score_impact": "+3 TEST_PASSED"
}
```

### Example 4: Human Approval
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
    "description": "Approved Pass 1 review",
    "approved_item": "Pass 1 completion"
  },
  "pass": 1
}
```

### Example 5: Error Logged
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
    "description": "Script failed due to missing module",
    "error_type": "ImportError",
    "resolution": "Need to install missing module"
  },
  "pass": 1,
  "score_impact": "-3 ERROR_MADE"
}
```

---

## AUTO-LOGGING RULES

### AI Models MUST Log

| When | Action | Required |
|------|--------|----------|
| At session start | `SESSION_START` | [OK] YES |
| When reading CLAUDE.md | `CONTEXT_LOADED` | [OK] YES |
| When starting checkbox | `CHECKBOX_START` | [OK] YES |
| When completing checkbox | `CHECKBOX_DONE` | [OK] YES |
| When running terminal command | `COMMAND_RUN` | [OK] YES |
| On error | `ERROR_OCCURRED` | [OK] YES |
| On pass complete | `PASS_COMPLETE` | [OK] YES |
| At session end | `SESSION_END` | [OK] YES |

### Scripts MUST Log

| Script | Auto-logs |
|--------|-----------|
| generate_sejr.py | `sejr_created`, `files_created` |
| build_claude_context.py | `claude_md_generated` |
| auto_verify.py | `verify_start`, `verify_pass/fail` |
| auto_archive.py | `archive_start`, `archive_complete` |
| admiral_tracker.py | `score_positive`, `score_negative` |

---

## VERIFICATION

### Test Log Format
```bash
# Verify JSON is valid
python3 -c "import json; [json.loads(l) for l in open('AUTO_LOG.jsonl')]"
```

### Required Fields Check
```bash
# Check all entries have timestamp and actor
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

To be ADMIRAL compliant, logs MUST:

- [ ] Use ISO 8601 timestamps with timezone
- [ ] Include full model_id for AI actors
- [ ] Log ALL terminal commands with output
- [ ] Log ALL checkbox completions
- [ ] Log ALL errors with details
- [ ] Be valid JSON on each line

---

**This specification is MANDATORY for all victories in the system.**
