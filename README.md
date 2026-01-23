# SEJR LISTE SYSTEM

**Version:** 1.0.0
**Created:** 2026-01-23
**DNA Layers:** 7 (SELF-AWARE → SELF-OPTIMIZING)

---

## QUICK START

```bash
# 1. Generate ny sejr liste
python scripts/generate_sejr.py --name "Your Project Name"

# 2. Tjek status
cat _CURRENT/STATE.md

# 3. Arbejd med sejr listen i 10_ACTIVE/

# 4. Verificer completion
python scripts/auto_verify.py

# 5. Archive når færdig
python scripts/auto_archive.py --sejr "your-project"
```

---

## HVAD ER DET?

Automated victory tracking system med **7 obligatoriske DNA lag**:

1. **SELF-AWARE** - Kender sig selv (DNA.yaml)
2. **SELF-DOCUMENTING** - Logger automatisk (AUTO_LOG.jsonl)
3. **SELF-VERIFYING** - Tjekker automatisk completion
4. **SELF-IMPROVING** - Lærer patterns (PATTERNS.yaml)
5. **SELF-ARCHIVING** - Rydder automatisk op
6. **PREDICTIVE** - Foreslår next steps (AI-drevet)
7. **SELF-OPTIMIZING** - MANDATORY creative search før bygning

---

## STRUKTUR

```
/sejrliste systemet/
├── README.md (you are here)
├── DNA.yaml (system metadata)
├── _CURRENT/ (focus here!)
│   ├── STATE.md (hvor er vi?)
│   ├── DELTA.md (hvad er nyt?)
│   ├── NEXT.md (næste skridt?)
│   └── PATTERNS.yaml (lærte mønstre)
├── 00_TEMPLATES/
│   └── SEJR_TEMPLATE.md
├── 10_ACTIVE/ (work in progress)
├── 90_ARCHIVE/ (completed - conclusions only)
└── scripts/ (automation)
```

---

## HVORDAN BRUGES DET?

### Generate Ny Sejr Liste

```bash
python scripts/generate_sejr.py --name "Deploy HYBRID Agents"
```

**Opretter:**
- `10_ACTIVE/DEPLOY_HYBRID_AGENTS_2026-01-23/SEJR_LISTE.md`
- AUTO_LOG.jsonl for tracking
- VERIFY_STATUS.yaml for auto-checks

### Tjek Status

```bash
# Quick overview
cat _CURRENT/STATE.md

# Hvad er nyt?
cat _CURRENT/DELTA.md

# Næste skridt?
cat _CURRENT/NEXT.md
```

### Verificer Completion

```bash
python scripts/auto_verify.py

# Auto-runs all verify commands
# Updates VERIFY_STATUS.yaml
# Marks completed items
```

### Archive Færdig Sejr

```bash
python scripts/auto_archive.py --sejr "DEPLOY_HYBRID_AGENTS"

# Moves to 90_ARCHIVE/
# Saves semantic conclusion only
# Updates PATTERNS.yaml with learnings
```

---

## 7 DNA LAG FORKLARING

### Layer 1: SELF-AWARE
System ved hvad det er:
- DNA.yaml with metadata
- Purpose, status, context

### Layer 2: SELF-DOCUMENTING
Auto-logs while you work:
- AUTO_LOG.jsonl per sejr
- No manual documentation needed

### Layer 3: SELF-VERIFYING
Auto-checks completion:
- Runs verify commands
- Updates status automatically

### Layer 4: SELF-IMPROVING
Learns from history:
- PATTERNS.yaml
- Optimizations suggested

### Layer 5: SELF-ARCHIVING
Cleans up automatically:
- Semantic conclusions only
- Process details discarded

### Layer 6: PREDICTIVE
AI-suggests next:
- Based on patterns
- NEXT.md auto-generated

### Layer 7: SELF-OPTIMIZING
MANDATORY before building:
- External search (GitHub, docs)
- Internal search (projects, patterns)
- 3+ alternatives generated
- Decision documented

---

## INTEGRATION

### TodoWrite Sync
SEJR_LISTE items ↔ TodoWrite (bi-directional)

### Git Automation
Auto-commit + push when sejr complete

### Context System
Auto-updates journal.md + session.md

---

## ADMIRAL STANDARDS

✅ Rule -16: VERIFICATION + DOCUMENTATION always
✅ Rule -28: Git complete = all 5 steps (not just commit)
✅ Rule 0c: 300% FÆRDIGT (RUNNING + PROVEN + TESTED)
✅ FØR/UNDER/EFTER pattern enforced

---

## TROUBLESHOOTING

**STATE.md outdated?**
```bash
python scripts/auto_track.py --rebuild-state
```

**Scripts not executable?**
```bash
chmod +x scripts/*.py
```

**Git out of sync?**
```bash
git pull origin main  # or push
```

---

## SE OGSÅ

- `/home/rasmus/Desktop/MASTER FOLDERS(INTRO)/I12_SEJR_LISTE_SYSTEM.md`
- `/home/rasmus/Desktop/MANUAL I TILFÆLDE AF HJERNESKADE/26_SEJR_LISTE_SYSTEM.md`

---

**Created by:** Kv1nt (Claude Sonnet 4.5)
**For:** Rasmus + Ivo
**Date:** 2026-01-23
**Status:** ✅ OPERATIONAL
