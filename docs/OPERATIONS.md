# OPERATIONS — Kvalitetssikring og Vedligeholdelse

**Version:** 3.0.0
**Opdateret:** 2026-01-31
**Formaal:** Dokumenterer HVORDAN systemkvalitet sikres permanent.

---

## PRINCIP: HVER SAMTALE EFTERLADER SYSTEMET BEDRE

Optimering er IKKE en opgave. Det er en PARALLEL PROCES der koerer ALTID:

```
FOER ARBEJDE:
  1. Scan alt du roerer ved for staleness
  2. Tjek versioner matcher (DK=EN, docs=root, DNA=README)
  3. Noter hvad der skal fikses

UNDER ARBEJDE:
  4. Fix documentation PARALLELT med hovedopgaven
  5. Opdater versioner naar kode aendres
  6. Hold DK og EN i sync

EFTER ARBEJDE:
  7. Koer tests (77/77 PASSED kraeves)
  8. Koer health check (41/41 PASSED kraeves)
  9. Commit + push ALLE aendringer (inkl. doc fixes)
```

---

## AUTOMATISKE KVALITETSSYSTEMER

### 1. Test Suite (pytest)
- **Hvad:** 77 unit tests across 5 testfiler
- **Koer:** `./venv/bin/python -m pytest app/tests/ -q`
- **Krav:** 77/77 PASSED (0 failures tilladt)
- **Naar:** FOER hvert git commit

### 2. Health Check (auto_health_check.py)
- **Hvad:** 41 system integrity checks
- **Koer:** `./venv/bin/python scripts/auto_health_check.py`
- **Krav:** 41/41 PASSED = ADMIRAL STANDARD
- **Naar:** Daglig cron kl 07:55 + FOER hvert commit
- **Auto-repair:** `--repair` flag fikser kendte problemer

### 3. Pre-commit Hook
- **Hvad:** Python syntax check + Flake8 errors + Bandit security
- **Trigger:** Automatisk ved `git commit`
- **Krav:** ALLE checks PASSED foer commit accepteres

### 4. Cron Jobs
- **07:55:** Health check med repair + desktop notification ved fejl
- **08:00:** Pattern learning fra alle arkiverede sejre

---

## DOKUMENTATIONSKVALITET

### Versionssync
Disse SKAL ALTID have SAMME version:
- `README.md` (root) ↔ `README_EN.md` (root)
- `DNA.yaml` version ↔ README version
- Alle fil-headers i root ↔ faktisk systemversion
- `docs/*.md` ↔ aktuel systemtilstand

### Fil-header Standard (WHAT/WHY/WHO/HOW)
HVER Python-fil og shell-script i root og scripts/ SKAL have:
```
WHAT:  Hvad goer denne fil?
WHY:   Hvorfor er den her? Hvem importerer den?
WHO:   Hvem kalder den? Hvad er dens dependencies?
HOW:   Hvordan bruger man den? (kommando/import)
Version: X.X.X | Opdateret: YYYY-MM-DD
```

### Dokumenter der SKAL holdes opdateret
| Dokument | Indhold | Trigger for opdatering |
|----------|---------|------------------------|
| `README.md` | Komplet overblik | Ny feature, ny script, nyt system |
| `README_EN.md` | Engelsk version | ALTID naar README.md opdateres |
| `DNA.yaml` | System identitet | Version bump, ny feature |
| `docs/SCRIPT_REFERENCE.md` | Alle scripts | Script tilfojet/fjernet/aendret |
| `docs/ARKITEKTUR.md` | System arkitektur | Ny komponent, ny integration |
| `docs/MODEL_ONBOARDING.md` | AI onboarding | Ny feature AI skal kende |

---

## STALENESS DETEKTION

### Tegn paa staleness (ALTID fix oejeblikkeligt):
- Version i fil-header != aktuel version (f.eks. v2.1.0 naar systemet er v3.0.0)
- DK og EN versioner har forskelligt indhold
- Script reference naevner scripts der er i `_unused/`
- Dokumentation beskriver features der ikke eksisterer
- Mappestruktur i docs matcher ikke virkeligheden

### Automatisk check (via auto_health_check.py):
- YAML parser integritet (alle scripts bruger PyYAML)
- Arkiv komplethed (alle filer til stede)
- Service status (systemd aktiv)
- Foraeldre-loese filer (temp dirs, orphans)
- Dokumentation freshness (version matching) — PLANLAGT

---

## FEJLHAANDTERING

### Problem: Test failures
```bash
./venv/bin/python -m pytest app/tests/ -v  # Se hvilke tests fejler
# Fix koden, ALDRIG workaround
# Koer tests igen
```

### Problem: Health check failures
```bash
./venv/bin/python scripts/auto_health_check.py --repair  # Auto-fix kendte issues
# Resterende fejl: fix manuelt
```

### Problem: Service nede
```bash
systemctl --user status sejrliste-web.service    # Se fejl
systemctl --user restart sejrliste-web.service   # Genstart
journalctl --user -u sejrliste-web.service -n 20 # Se logs
```

### Problem: Staleness opdaget
1. Identificer ALLE filer med samme staleness (ikke kun den ene du fandt)
2. Fix ALLE paa en gang (DK+EN, alle referencer)
3. Commit med beskrivende besked
4. Push oejeblikkeligt

---

## KVALITETSMETRIKKER

| Metrik | Krav | Verifikation |
|--------|------|-------------|
| Tests | 77/77 PASSED | `pytest app/tests/ -q` |
| Health | 41/41 PASSED | `auto_health_check.py` |
| Service | active | `systemctl --user is-active sejrliste-web.service` |
| Git | clean + pushed | `git status && git log origin/main..HEAD` |
| Versioner | alle matcher | Manuel check DK=EN=DNA=README |
| Docstrings | WHAT/WHY/WHO/HOW | Manuel check per fil |

---

## AUDIT PROTOKOL

Naar som helst man vil verificere at systemet er ADMIRAL STANDARD:

```bash
cd "/home/rasmus/Desktop/sejrliste systemet"

# 1. Tests
./venv/bin/python -m pytest app/tests/ -q

# 2. Health check
./venv/bin/python scripts/auto_health_check.py

# 3. Service
systemctl --user is-active sejrliste-web.service

# 4. Git status (clean = intet uncommitted)
git status

# 5. Version sync (alle skal sige 3.0.0)
head -3 README.md
head -3 README_EN.md
grep "version:" DNA.yaml | head -1

# 6. Compile check (alle scripts)
for f in scripts/*.py; do ./venv/bin/python -m py_compile "$f" && echo "OK: $(basename $f)"; done
```

**Resultat:** ALLE 6 checks PASSED = ADMIRAL STANDARD

---

*Oprettet: 2026-01-31 (Rule -52 + -53: parallel optimization + auditable quality)*
*Vedligeholdes: PERMANENT — opdateres naar nye kvalitetssystemer tilfojes*
