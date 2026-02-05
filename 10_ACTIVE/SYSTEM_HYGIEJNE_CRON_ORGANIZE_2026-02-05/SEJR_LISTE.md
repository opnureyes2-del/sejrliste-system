# SEJR: SYSTEM_HYGIEJNE_CRON_ORGANIZE

**Oprettet:** 2026-02-05 13:47
**Status:** PASS 1 — IN PROGRESS
**Prioritet:** P3 — LAV (vedligehold)
**Current Pass:** 1/3
**Kontekst:** System-hygiejne, cron audit, oprydning, optimeringsbacklog

---

## 3-PASS KONKURRENCE SYSTEM (OBLIGATORISK)

```
PASS 1: FUNGERENDE     — Audit og identifikation
PASS 2: FORBEDRET      — Oprydning og fixes
PASS 3: OPTIMERET      — Automatiseret vedligehold
```

---

## PASS 1: AUDIT OG IDENTIFIKATION

### A: Cron Job Audit (28+ aktive jobs)

**Problem:** Kommentar siger "14 aktive" men der er 28+. Ingen audit eller vedligehold.

- [ ] A1: List alle cron jobs
  - Command: `crontab -l`
- [ ] A2: Kategoriser: NØDVENDIG / REDUNDANT / UNKNOWN
  - Dokumenter per job
- [ ] A3: Check for /tmp/ log filer der vokser ubegrænset
  - Command: `ls -la /tmp/admiral-*.log /tmp/disk-*.log /tmp/auto-*.log 2>/dev/null`
- [ ] A4: Identificer overlap mellem cron og systemd timers
  - Problem: Nogle ting kører BEGGE steder
- [ ] A5: Check admiral-wisdom.py og admiral-orchestrator.py
  - Kører fra Pictures/Admiral — er det korrekt?
- [ ] A6: Dokumenter anbefalet oprydning

---

### B: ORGANIZE/ Mappe Disposition (396 KB)

**Sti:** `/home/rasmus/Desktop/ORGANIZE/`
**Indhold:** 3 arkiverede mapper fra januar

- [ ] B1: Gennemgå _ARCHIVED_JAN11-17 (308 KB, 20+ filer)
  - Beslutning: SLET / FLYT TIL 90_ARCHIVE / BEHOLD
- [ ] B2: Gennemgå _ARCHIVED_LIB-ADMIN_JAN17 (24 KB)
  - Beslutning: _
- [ ] B3: Gennemgå _ARCHIVED_TOOLS_JAN19 (64 KB)
  - Beslutning: _
- [ ] B4: Eksekvér beslutning (slet eller flyt)
- [ ] B5: Fjern ORGANIZE/ fra Desktop hvis tom

---

### C: Status Opdaterings Rapport (80 MB, 90 filer)

**Sti:** `/home/rasmus/Desktop/projekts/status opdaterings rapport/`

- [ ] C1: Audit indhold — hvad er vigtigt?
  - Command: `ls -la /home/rasmus/Desktop/projekts/status\ opdaterings\ rapport/`
- [ ] C2: Vurder om data kan komprimeres eller arkiveres
- [ ] C3: Beslutning: BEHOLD / ARKIVER / SLET dele
- [ ] C4: Eksekvér

---

### D: Optimeringsbacklog (5 items fra TODO.md)

- [ ] D1: O9 — Scripts dokumentation
  - Hvad: Dokumenter alle scripts i sejrliste systemet/scripts/
- [ ] D2: O12 — Dependency checks
  - Hvad: Verify alle Python/Node dependencies er aktuelle
- [ ] D3: O13 — VS Code profiler
  - Hvad: Opsæt workspace profiles per projekt
- [ ] D4: O14 — Ollama aliases
  - Hvad: Opsæt shell aliases for hyppige Ollama kommandoer
- [ ] D5: O15 — Desktop guide
  - Hvad: Opdater desktop organisation guide

---

### E: Ressource Audit

- [ ] E1: Check om 2 Next.js servere (v14 + v15) begge er nødvendige
  - v14.2.35 = cirkelline-consulting (port 3003)
  - v15.2.3 = cirkelline-frontend (port 3000)
  - Beslutning: Begge nødvendige? Ja/nej
- [ ] E2: cosmic-library bruger 1.2 GB RAM — er det forventet?
- [ ] E3: Docker `docker system prune` mulighed (~3.5 GB reclaimable)
  - Beslutning: Kør prune? Ja/nej

---

### F: .desktop-launchers-backup/ (skjult mappe)

- [ ] F1: Undersøg indhold
  - Command: `ls -la /home/rasmus/Desktop/.desktop-launchers-backup/`
- [ ] F2: Beslutning: SLET / BEHOLD
- [ ] F3: Eksekvér

---

## PASS 1 SCORE: ___/10

---

## PASS 2: FORBEDRET — Oprydning og eksekvering
_Udfyldes efter Pass 1 review_

## PASS 3: OPTIMERET — Automatiseret vedligehold
_Udfyldes efter Pass 2 review_

---

## ARCHIVE LOCK
```yaml
can_archive: false
total_score: null
```
