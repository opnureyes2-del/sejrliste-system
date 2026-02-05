# FORBINDELSESKORT — HELE RASMUS' DESKTOP

**Oprettet:** 2026-02-05
**Formaal:** Vis ALLE sammenhænge mellem systemer, mapper, services, repos, data
**Perspektiv:** Bogfører + Admiral — ikke bare hvad der findes, men hvad der HÆNGER SAMMEN

---

## 1. DE 5 LAG

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAG 1: IDENTITET — Hvem er Kv1nt? Hvad er standarden?                │
│   MIN ADMIRAL/ ──────────> 51+ regler, 7 DNA lag, 5 protokoller      │
│   MANUAL HJERNESKADE/ ──> Recovery hvis alt går galt                  │
│   WHO_I_AM.md ──────────> "Jeg er kv1nt. Jeg bygger systemer."       │
├─────────────────────────────────────────────────────────────────────────┤
│ LAG 2: STRUKTUR — Hvordan er det organiseret?                         │
│   MASTER FOLDERS(INTRO)/ ──> I1-I12 regler + folder DNA             │
│   INTRO FOLDER SYSTEM/ ───> Meta-dokumentation (296/300)             │
│   sejrliste systemet/ ────> 3-pass kvalitetssystem                   │
├─────────────────────────────────────────────────────────────────────────┤
│ LAG 3: PRODUKTION — Hvad kører lige nu?                              │
│   projekts/projects/ ─────> 6 kørende services                       │
│   Pictures/Admiral/ ──────> Brain + Watchdog + Gateway               │
├─────────────────────────────────────────────────────────────────────────┤
│ LAG 4: INTELLIGENCE — Hvad lærer og vokser?                          │
│   ELLE.md/ ──────────────> 35.000 filer, agents, organic teams       │
│   cosmic-library/ ───────> Eternal Learner + 9-agent Research Team   │
├─────────────────────────────────────────────────────────────────────────┤
│ LAG 5: PLAN — Hvad skal ske fremover?                                │
│   RASMUS TODO/ ──────────> 120 timers roadmap + API keys             │
│   ORGANIZE/ ─────────────> Arkiveret historie (jan-faser)            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. SYSTEM-TIL-SYSTEM FORBINDELSER

### 2a. Services der taler med hinanden

```
cirkelline-backend (7777) ──┐
cirkelline-frontend (3000) ─┤── DELER database port 5532 (cirkelline-postgres)
                            │
cosmic-library (7778) ──────┤── Egen database port 5534 (cosmic-postgres)
                            │
lib-admin (7779) ───────────┤── Egen database port 5533 (ckc-postgres)
                            │
cirkelline-consulting (3003)┤── Egen database port 5435 (consulting-postgres)
                            │
admiral-hq (5555) ──────────┘
    ├── admiral-brain (15 min cycles) → checker ALLE services
    ├── admiral-watchdog (60s) → overvåger sundhed
    ├── admiral-gateway/caddy (5580) → reverse proxy
    ├── admiral-terminal/ttyd (7681) → web terminal
    ├── admiral-tunnel/cloudflared → ekstern adgang (FEJLER)
    └── admiral-wallpaper-animate → desktop baggrund
```

**VIGTIG KONKLUSION:** Alle 6 projekter har SEPARATE databaser. INTET deles. Admiral HQ overvåger dem alle men kan ikke ændre dem.

### 2b. Dokumentation der refererer til hinanden

```
MIN ADMIRAL/02_REGLER_KOMPLET.md
    ├──→ MASTER FOLDERS/I2_ADMIRAL_OBLIGATORY_ORDERS.md (DUPLIKAT af reglerne)
    ├──→ MANUAL HJERNESKADE/12_OBLIGATORISKE_ORDRER.md (TREDJE kopi)
    ├──→ ELLE.md/ADMIRAL_STANDARD.md (FJERDE kopi)
    └──→ sejrliste/enforcement_engine.py (IMPLEMENTERER reglerne)

MIN ADMIRAL/DNA.yaml
    ├──→ sejrliste systemet/DNA.yaml (KOPI)
    ├──→ MASTER FOLDERS/I12_SEJR_LISTE_SYSTEM.md (BESKRIVER det)
    └──→ INTRO FOLDER SYSTEM/README.md (REFERERER til det)

RASMUS TODO/TODO.md
    ├──→ MASTER FOLDERS/OBLIGATORISK_OPGAVER.md (DELVIST OVERLAP)
    └──→ sejrliste/10_ACTIVE/INTRO_DNA_AABNE_TASKS (SPECIFIK DELMÆNGDE)
```

### 2c. Git repos og deres forbindelser

```
GitHub: opnureyes2-del/
    ├── lib-admin ──────────── projekts/projects/lib-admin/ ✅ CLEAN
    ├── Cosmic-Library ─────── projekts/projects/cosmic-library/ ✅ CLEAN
    ├── Commando-Center ────── projekts/projects/commando-center/ ✅ CLEAN
    ├── cirkelline-consulting ─ projekts/projects/cirkelline-consulting/ ✅ CLEAN
    ├── ELLE.md ────────────── Desktop/ELLE.md/ ⚠️ 5 modified + 29 untracked
    ├── manual-hjerneskade ─── Desktop/MANUAL I TILFÆLDE AF HJERNESKADE/ ⚠️ 26 DIRTY
    └── intro-folder-system ── Desktop/INTRO FOLDER SYSTEM/ ✅ CLEAN

GitHub: eenvywithin/ (Ivo)
    └── cirkelline-system ──── projekts/projects/cirkelline-system-DO-NOT-PUSH/ 🔒 READ ONLY

LOKALT GIT (mangler remote):
    ├── Pictures/Admiral/ ─── git init 2026-02-05 (95c2fc8, 48 filer)
    ├── projekts/projects/cirkelline-kv1ntos/ ── git SLETTET med vilje
    ├── Desktop/ORGANIZE/ ── arkiv, ingen VCS
    ├── Desktop/RASMUS TODO/ ── ingen VCS
    └── Desktop/MIN ADMIRAL/ ── har git lokalt
```

---

## 3. DATA-FLOW: Hvordan information bevæger sig

```
Rasmus skriver kode
    │
    ▼
projekts/projects/ (lokal udvikling)
    │
    ├──[git push]──→ GitHub (opnureyes2-del/)
    │
    ├──[systemd service]──→ Kørende service (port 77xx/3xxx)
    │                           │
    │                           ▼
    │                    Admiral Brain (hvert 15 min)
    │                           │
    │                    ├── Checker health endpoints
    │                    ├── Logger til evolution.jsonl
    │                    ├── Opdaterer ELLE.md/ENFORCEMENT/
    │                    └── Genererer REPORTS/ (COUNCIL, INTEL, QUALITY)
    │                                    │
    │                                    ▼
    │                            ELLE.md/REPORTS/ (29.218 auto-rapporter)
    │
    ├──[sejrliste]──→ sejrliste systemet/10_ACTIVE/
    │                    │
    │                    ├── Pass 1 → Pass 2 → Pass 3
    │                    │
    │                    └──[auto_archive.py]──→ 90_ARCHIVE/ (31 arkiveret)
    │
    └──[dokumentation]──→ MASTER FOLDERS(INTRO)/ + MIN ADMIRAL/
                              │
                              └── INTRO FOLDER SYSTEM/ (meta-index)
```

---

## 4. DUPLIKATER OG REDUNDANS

### Dokumentation der findes FLERE steder (SKAL ryddes op):

| Emne | Placering 1 | Placering 2 | Placering 3 | Handling |
|------|-------------|-------------|-------------|---------|
| Admiral regler | MIN ADMIRAL/02_REGLER.md | MASTER FOLDERS/I2.md | HJERNESKADE/12.md | MIN ADMIRAL er KILDEN |
| Naughty/Not | MIN ADMIRAL/NAUGHTY.md | MASTER FOLDERS/I11.md | HJERNESKADE/14.md | MIN ADMIRAL er KILDEN |
| Port mapping | MASTER FOLDERS/I6.md | projekts/CLAUDE.md | projekts/PORTS.md | INGEN er 100% korrekt |
| System status | MASTER FOLDERS/STATUS/ | HJERNESKADE/00.md | ELLE.md/ENFORCEMENT/ | ELLE.md er LIVE data |
| Obligatoriske ordrer | MIN ADMIRAL/OBLIGATORY.md | MASTER FOLDERS/OBLIGATORISKE.md | HJERNESKADE/12.md | Tre kopier, potentielt ude af sync |
| Sejrliste system | MIN ADMIRAL/TEMPLATES/ | MASTER FOLDERS/I12.md | sejrliste/00_TEMPLATES/ | sejrliste/ er KILDEN |
| Bug fixes | MASTER FOLDERS/I7.md | HJERNESKADE/13.md | — | Skal synces |

### Backups der potentielt overlapper:

| Backup | Størrelse | Overlapper med |
|--------|-----------|----------------|
| ~/backups/backup_20260102_121727/ | 71 GB | Hele Desktop fra 2. jan |
| ~/backups/backup_20260102_114643/ | 39 GB | ELLE.md med 29.819 filer |
| ~/backups/backup_20260102_122746/ | 5 GB | Ukendt subset |
| projekts/backups/ | 12 GB | cirkelline-system backups |
| projekts/.git.backup-consulting-root/ | 686 MB | consulting git |
| ELLE.md/BACKUPS/ | 3.9 MB | 49 agent Python scripts |
| ORGANIZE/ | 400 KB | Scripts fra jan 11-19 |

**TOTAL REDUNDANT STORAGE:** ~128 GB+ (115 GB ~/backups + 12 GB projekts/backups + diverse)

---

## 5. KRITISKE KNUDEPUNKTER

### Ting der AFHÆNGER af hinanden:

```
1. Admiral Brain → afhænger af ALLE 6 services (checker health)
   └── HVIS Brain fejler → ingen overvågning → problemer opdages ikke

2. cosmic-library eternal_learner → afhænger af observation_collector
   └── RETTET: None-rating bug slukkede branden

3. ELLE.md/ENFORCEMENT/ → afhænger af Admiral Brain auto-commits
   └── capabilities.json, learnings.json, quality_history.json = LIVE data

4. ELLE.md/ORGANIC_TEAMS/ → afhænger af organic-teams.timer (1h cyklus)
   └── runtime.log, work_log.json = LIVE data

5. sejrliste systemet → afhænger af generate_sejr.py + auto_archive.py
   └── HELE kvalitetssystemet kører gennem disse scripts

6. MANUAL HJERNESKADE → afhænger af verify_manual_hjerneskade.py
   └── Forventer 14 services, 7 timers, 22 Docker, 4 databases, 5 repos
```

### Ting der er ISOLEREDE (potentielt glemte):

```
1. ORGANIZE/ → Ingen forbindelse til noget. Rene arkiver fra jan 11-19.
2. RASMUS TODO/ → Ikke forbundet til sejrliste systemet (BURDE VÆRE)
3. INTRO FOLDER SYSTEM/ → Minimal, kun 5 filer, mest meta-index
4. projekts/openclaw/ → 2 GB monorepo, ingen dokumentation i INTRO
5. projekts/status opdaterings rapport/ → 80 MB, 100+ filer, ikke forbundet
6. projekts/agents/ → 44 KB, ikke brugt af noget
7. kommandor-og-agenter → 1.1 GB, dirty, ikke dokumenteret i INTRO
8. commander-and-agent → 4 MB, dirty, ikke dokumenteret
9. Cirkelline-Consulting-main → 12 KB, gammel kopi, bør slettes
```

---

## 6. KILDESANDHED — HVAD ER "SANDHEDEN" FOR HVERT EMNE?

| Emne | KILDE (sandhed) | Kopier (kan være forældet) |
|------|-----------------|---------------------------|
| Identitet/Regler | MIN ADMIRAL/ | MASTER FOLDERS, HJERNESKADE |
| Projekt-kode | projekts/projects/ | GitHub repos |
| Service-status | `systemctl --user` (LIVE) | HJERNESKADE/00, MASTER FOLDERS/STATUS |
| Port-mapping | `ss -tlnp` (LIVE) | CLAUDE.md, PORTS.md, I6.md |
| Git-status | `git status` (LIVE) | Ingen kopi |
| Sejrliste-status | sejrliste/10_ACTIVE/ | INTRO FOLDER SYSTEM |
| AI/Agents | ELLE.md/ENFORCEMENT/ (LIVE) | ELLE.md/DOCS/, MASTER FOLDERS |
| Recovery | MANUAL HJERNESKADE/ | — (ingen kopi — RISIKO) |
| Fremtidsplaner | RASMUS TODO/ | MASTER FOLDERS/OBLIGATORISK |
| Arkitektur | MASTER FOLDERS/PROJEKTS ARKITEKTUR/ | projekts/docs/ |

**REGEL:** Hvis to dokumenter modsiger hinanden, er KILDEN sand. Alt andet er potentielt forældet.

---

## 7. FORBINDELSER DER MANGLER (HULLER I SYSTEMET)

| Fra | Til | Mangler | Konsekvens |
|-----|-----|---------|-----------|
| cosmic-library | cirkelline-system | Deploy endpoint | Agents kan ikke graduere |
| RASMUS TODO | sejrliste systemet | Sejr-opgaver | TODO aldrig konverteret til sejrs |
| Admiral HQ | Git | Versionsstyring | 138 KB kode uden backup |
| MIN ADMIRAL | ELLE.md | Regel-sync | Regler kan afvige over tid |
| HJERNESKADE | Git | Commit | 26 filer med uforsikret arbejde |
| ELLE.md | ORGANIZE | Arkivering | Gamle ELLE filer aldrig arkiveret |
| projekts/openclaw | INTRO | Dokumentation | 2 GB projekt uden INTRO coverage |
| projekts/agents | NOGET SOM HELST | Brug | 44 KB agent framework bruges ikke |

---

## 8. SUNDHEDSSTATUS — TRAFIKLYSKORT

```
🟢 GRØN (Fungerer, dokumenteret, clean):
    ├── MIN ADMIRAL/ — git clean, komplet dokumentation
    ├── INTRO FOLDER SYSTEM/ — git clean, 296/300
    ├── sejrliste systemet/ — fungerer, 31 arkiveret
    ├── lib-admin — kører, git clean, port 7779
    ├── cirkelline-consulting — kører, git clean, port 3003
    └── cosmic-library — kører (EFTER fix), git clean, port 7778

🟡 GUL (Fungerer men har issues):
    ├── MASTER FOLDERS(INTRO)/ — forældede oplysninger (A2, A3)
    ├── ELLE.md/ — 29 untracked, 29.218 auto-rapporter vokser
    ├── Admiral HQ — kører men ingen git, tomme core/mapper
    ├── cirkelline-kv1ntos — kører men ingen git overhovedet
    ├── projekts/CLAUDE.md — forkert port (A4)
    └── cloudflared tunnel — gentagne failures

🔴 RØD (Kræver handling):
    ├── NVIDIA GPU — driver offline (kræver MOK enrollment)
    ├── 12 inaktive autogen services — timer-baserede (normalt)
    └── cloudflared tunnel — gentagne connection failures (auto-retries)

✅ LØST (2026-02-05):
    ├── MANUAL HJERNESKADE — committed + pushed ✅
    ├── 115 GB backups — SLETTET ✅
    ├── integration-bridge — pushed ✅
    ├── commander-and-agent — committed + pushed ✅
    └── kommandor-og-agenter — committed + pushed ✅
```

---

## 9. ANBEFALING TIL PASS 2 (PRIORITERET RÆKKEFØLGE)

```
UDFØRT (2026-02-05):
✅ 1. MANUAL HJERNESKADE committed + pushed (5e38bec)
✅ 2. integration-bridge pushed (741f9bf)
✅ 3. cirkelline-system synkroniseret (b1d08cc)
✅ 4. projekts/CLAUDE.md port rettet (3030→5555)
✅ 5. I5 status rettet (selvmodsigende udsagn fjernet)
✅ 6. ELLE.md committed + pushed (bc257ba + 7411ef0)
✅ 7. Pictures/Admiral/ git init (95c2fc8, 48 filer)
✅ 8. 115 GB backups slettet (disk 57%→44%)

AFVENTER:
9. Konverter RASMUS TODO til sejrliste-opgaver
10. Ryd ELLE.md/REPORTS/ (29.218 filer, 127 MB auto-genereret)
```

---

**Genereret:** 2026-02-05 af Kv1nt (Admiral Inspektion)
**Verificeret mod:** 16 parallelle scans af hele Desktop
**Formaal:** Vise at en Admiral ikke bare tæller bøger — men forstår biblioteket
