# SEJR: SIKKERHED_ENV_KEYS_OPRYDNING

**Oprettet:** 2026-02-05 13:47
**Status:** PASS 1 — IN PROGRESS
**Prioritet:** P0 — KRITISK SIKKERHED
**Current Pass:** 1/3

---

## 3-PASS KONKURRENCE SYSTEM (OBLIGATORISK)

```
PASS 1: FUNGERENDE     — Identificer og fjern trusler
PASS 2: FORBEDRET      — Roter keys, hærde systemet
PASS 3: OPTIMERET      — Automatiser fremtidig beskyttelse
```

---

## PASS 1: SIKKERHEDSHANDLINGER

### A: Purge .env filer fra backups (14 filer med LIVE keys)

**Risiko:** Google API key, OpenAI key, Brave key, DB passwords i plaintext.
**Sti:** `/home/rasmus/Desktop/projekts/backups/`

- [ ] A1: List alle .env filer i backups
  - Verify: `find /home/rasmus/Desktop/projekts/backups/ -name ".env*" -type f`
- [ ] A2: Slet ALLE .env fra cirkelline-system-v1.3.2 backup (12 filer)
  - Command: `find .../cirkelline-system-v1.3.2-20251216-183102/ -name ".env*" -delete`
  - Verify: 0 .env filer i den mappe
- [ ] A3: Slet ALLE .env fra BACKUP-20251211 (2 filer)
  - Command: `find .../BACKUP-20251211_204926/ -name ".env*" -delete`
- [ ] A4: Verify TOTAL: Ingen .env i backups
  - Expected: `find ... -name ".env*" | wc -l` = 0

---

### B: Key rotation evaluering

- [ ] B1: Dokumenter hvilke keys der var eksponeret
  - Google API: AIzaSyC8...
  - OpenAI: sk-proj-txV...
  - Brave: BSAqilr5...
  - DB passwords: ckc_secure_password_2025, etc.
- [ ] B2: Check om keys stadig er aktive (test med curl)
- [ ] B3: Anbefaling til Rasmus: Roter eller accepter risiko
  - Beslutning: _Rasmus afgør_
- [ ] B4: Hvis rotation: Opdater .env i aktive projekter

---

### C: Root-ejet duplikat fjernelse

**Problem:** `Cirkelline-Consulting-main/` ejet af root:root i user space.

- [ ] C1: Verificer det er duplikat af cirkelline-consulting
  - Verify: `diff -rq` mellem de to
- [ ] C2: Slet med sudo
  - Command: `sudo rm -rf "/home/rasmus/Desktop/projekts/projects/Cirkelline-Consulting-main/"`
- [ ] C3: Verify fjernet

---

### D: Credential audit — aktive projekter

- [ ] D1: Verify alle .env er i .gitignore
- [ ] D2: Verify ingen .env er tracked i git
- [ ] D3: githubtoken.md slettet ✅ (allerede gjort)

---

## PASS 1 SCORE: ___/10

---

## PASS 2: FORBEDRET — Key rotation + hardening
_Udfyldes efter Pass 1 review_

## PASS 3: OPTIMERET — Automatiseret credential scanning
_Udfyldes efter Pass 2 review_

---

## ARCHIVE LOCK
```yaml
can_archive: false
total_score: null
```
