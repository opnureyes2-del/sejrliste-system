# SYSTEM MAP — Komplet Forbindelseskort

> **ADMIRAL STANDARD — Alt kan spores**
> **Version:** 3.0.0
> **Dato:** 2026-01-31

---

## OVERBLIK

```
BRUGER INTERAKTION
├─ Desktop App: victorylist.desktop → masterpiece_en.py (GTK4)
├─ Web Interface: Browser → start-web.sh → web_app.py (Streamlit :8501)
├─ Terminal: ./sejr → Python subkommandoer
├─ TUI App: app/sejr_app.py (Textual)
└─ Cron Jobs: Daglige automatiske opgaver (07:55 + 08:00)
```

---

## DATA FLOW

```
┌────────────────────────────────────────────────────────────────┐
│                        BRUGER INPUT                            │
│                                                                │
│  Desktop launcher ──→ masterpiece_en.py ──→ 10_ACTIVE/        │
│  Browser :8501 ──────→ web_app.py ──────────→ 10_ACTIVE/      │
│  Terminal `sejrliste` → sejr (bash) ─────────→ scripts/       │
│  Systemd (login) ────→ start-web.sh ─────────→ web_app.py    │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                     KERNE AUTOMATION                           │
│                                                                │
│  generate_sejr.py ──→ Opret ny sejr i 10_ACTIVE/              │
│       ↑                     │                                  │
│       │                     ▼                                  │
│  PATTERNS.json        auto_verify.py ──→ Opdater STATUS.yaml  │
│       ↑                     │                                  │
│       │                     ▼                                  │
│  auto_learn.py ←──── auto_archive.py ──→ 90_ARCHIVE/          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                     DAGLIG VEDLIGEHOLDELSE                     │
│                                                                │
│  07:55  auto_health_check.py (51 checks + auto-repair)        │
│  08:00  auto_learn.py (pattern extraction → PATTERNS.json)    │
└────────────────────────────────────────────────────────────────┘
```

---

## IMPORT GRAF

```
masterpiece_en.py / masterpiece.py
├─ gi (GTK4/Adw)
├─ cairo
├─ checkbox_utils.py ─→ count_checkboxes (DELT MODUL)
├─ intro_integration.py ─→ Scanner INTRO mapper
└─ subprocess ─→ scripts/

web_app.py / web_app_en.py
├─ streamlit
├─ checkbox_utils.py ─→ count_checkboxes (DELT MODUL)
├─ enforcement_engine.py ─→ 3-pass kvalitets-gate
└─ subprocess ─→ scripts/

sejr (bash CLI)
└─ subprocess ─→ scripts/ + app/sejr_app.py

generate_sejr.py
├─ yaml_utils.py (PyYAML)
└─ _CURRENT/PATTERNS.json (feedback loop input)

auto_verify.py
├─ yaml_utils.py (PyYAML)
└─ checkbox_utils.py ─→ count_checkboxes (DELT MODUL)

auto_archive.py, auto_learn.py,
build_claude_context.py, admiral_tracker.py
└─ yaml_utils.py (PyYAML) ← DELT MODUL, 6 scripts importerer

auto_health_check.py
├─ yaml (PyYAML direkte)
├─ py_compile (syntax check)
└─ subprocess (curl, systemctl)
```

---

## TRIGGER MATRIX

| Trigger | Kilde | Kalder | Læser | Skriver |
|---------|-------|--------|-------|---------|
| Desktop launcher | victorylist.desktop | masterpiece_en.py | 10_ACTIVE/, 90_ARCHIVE/, INTRO/ | Ingen |
| Web (port 8501) | Browser | web_app.py | 10_ACTIVE/, STATUS.yaml | Ingen direkte |
| Terminal: sejrliste | Bruger | sejr → scripts/ | 10_ACTIVE/, 90_ARCHIVE/ | Ingen |
| TUI: sejr app | Bruger | app/sejr_app.py | 10_ACTIVE/, DNA.yaml | Ingen |
| Systemd (login) | Login event | start-web.sh | Ingen | Streamlit stdout |
| Cron 07:55 | Scheduler | auto_health_check.py | Alle YAML filer | Repareret YAML |
| Cron 08:00 | Scheduler | auto_learn.py | 90_ARCHIVE/ | PATTERNS.json |
| Ny sejr | Bruger | generate_sejr.py | PATTERNS.json | 10_ACTIVE/[ny]/ |
| Verificer | Bruger/script | auto_verify.py | SEJR_LISTE.md | STATUS.yaml |
| Arkiver | Bruger | auto_archive.py | STATUS.yaml | 90_ARCHIVE/ |

---

## FEEDBACK LOOPS

### 1. Lærings-Loop (Selvforbedrende)

```
arkiveret sejr ──→ auto_learn.py ──→ PATTERNS.json (52 patterns)
                                          │
                                          ▼
                                    generate_sejr.py ──→ nye sejre med lærte patterns
                                          │
                                          └──→ bruger fuldfører ──→ arkivering ──→ LOOP LUKKET
```

### 2. Kvalitets-Loop (Enforcement)

```
enforcement_engine.py ──→ web_app viser checkpoint status
       │
       ▼
bruger giver bevis ──→ auto_verify.py ──→ STATUS.yaml opdateret
       │
       ▼
build_claude_context.py ──→ CLAUDE.md opdateret ──→ AI har aktuel kontekst
```

### 3. Health Check Loop (Daglig Vagt)

```
auto_health_check.py ──→ scanner alle YAML, scripts, docs, services
       │
       ├─ OK: 51/51 PASSED → desktop notification: alt godt
       └─ FAIL: auto-repair + desktop notification: fejl fundet
```

---

## FIL PER MAPPE

### Root (14 filer)

| Fil | Type | Importeret af | Importerer |
|-----|------|--------------|------------|
| web_app.py | Streamlit | start-web.sh | enforcement_engine |
| web_app_en.py | Streamlit | Ingen (manuelt) | enforcement_engine |
| masterpiece.py | GTK4 | Ingen (DK fallback) | Ingen |
| masterpiece_en.py | GTK4 | victorylist.desktop | intro_integration |
| enforcement_engine.py | Python modul | web_app.py, web_app_en.py | stdlib |
| intro_integration.py | Python modul | masterpiece_en.py | stdlib |
| sejr | Bash CLI | Bruger | subprocess → scripts/ |
| start-web.sh | Bash | systemd service | venv/streamlit |
| DNA.yaml | Config | masterpiece*, sejr_app.py | — |
| README.md | Dok | — | — |
| README_EN.md | Dok | — | — |
| requirements.txt | Config | pip install | — |
| checkbox_utils.py | Python modul | web_app, masterpiece, auto_verify, pages/ | re |
| .gitignore | Config | git | — |

### scripts/ (18 Python + 8 Shell)

| Script | Importerer yaml_utils | Trigget af | Skriver til |
|--------|----------------------|------------|-------------|
| generate_sejr.py | Ja | sejr, web_app | 10_ACTIVE/[ny]/ |
| auto_verify.py | Ja | sejr, pre-commit | STATUS.yaml |
| auto_archive.py | Ja | bruger | 90_ARCHIVE/ |
| auto_learn.py | Ja | cron 08:00 | PATTERNS.json |
| auto_health_check.py | Nej (direkte yaml) | cron 07:55 | Repareret filer |
| build_claude_context.py | Ja | web_app | CLAUDE.md |
| admiral_tracker.py | Ja | manuelt | ADMIRAL_SCORE.yaml |
| yaml_utils.py | — (ER modulet) | 6 scripts | — |
| view.py | Ja | manuelt | stdout |
| auto_track.py | Ja | manuelt | STATE.md |
| auto_predict.py | Nej | manuelt | NEXT.md |
| auto_optimize.py | Nej | manuelt | stdout |
| model_router.py | Nej | manuelt | stdout |
| token_tools.py | Nej | manuelt | stdout |
| build_knowledge_base.py | Nej | manuelt | ChromaDB |
| automation_pipeline.py | Nej | pre-commit | stdout |
| auto_live_status.py | Nej | manuelt | stdout |
| generate_icon_sizes.py | Nej | manuelt | assets/ |

### app/ (TUI System)

| Fil | Rolle |
|-----|-------|
| sejr_app.py | Hoved-TUI app (Textual) |
| executor.py | Task execution engine |
| watcher.py | Fil-overvågning (STATUS.yaml, SEJR_LISTE.md) |
| model_router.py | AI model-valg logik |
| models/*.py | Opus/Sonnet/Haiku handlers |
| widgets/*.py | UI komponenter (progress, liste, log, DNA) |
| integrations/*.py | Hooks (kun brugt af tests) |
| sessions/__init__.py | Ubrugt (dead code) |

---

## INFRASTRUKTUR

### systemd

```
sejrliste-web.service
  Type=simple
  ExecStart=start-web.sh
  Restart=always, RestartSec=5
  WantedBy=default.target (auto-start ved login)
```

### Tailscale Mesh VPN

```
ROG desktop (100.86.106.42) ←→ Pixel 9 Pro
HTTPS: https://rog.tailc9c1c5.ts.net → :8501
```

### Cron

```
55 7 * * * scripts/cron_health_check.sh  → auto_health_check.py --repair
 0 8 * * * scripts/cron_auto_learn.sh     → auto_learn.py
```

### Desktop Launcher

```
victorylist.desktop (3 actions)
├─ Åbn (default): python3 masterpiece_en.py
├─ Åbn i Browser: systemctl start + xdg-open :8501
└─ Åbn Terminal: python3 app/sejr_app.py
```

---

## KENDTE SVAGHEDER

| Problem | Placering | Risiko | Status |
|---------|-----------|--------|--------|
| ~~8× duplicate count_checkboxes()~~ | ~~masterpiece, web_app, pages, scripts~~ | ~~Vedligeholdelse~~ | **FIKSET:** checkbox_utils.py (1 modul, 6 importerer) |
| Hardcoded absolute paths i shell scripts | Alle .sh filer | Portabilitet (lav risiko — kun 1 maskine) | Accepteret |
| ~~app/sessions/ aldrig brugt~~ | ~~app/sessions/__init__.py~~ | ~~Dead code~~ | **FIKSET:** Flyttet til _unused/ |
| app/integrations/ kun brugt af tests | app/integrations/*.py | Dead code (lav risiko) | Accepteret |
| masterpiece.py har 117 funktioner vs masterpiece_en.py har 313 | GTK4 apps | DK version mangler features | Accepteret |

---

**Verificeret af:** auto_health_check.py (51 checks, 12 CHECK-kategorier)
**Sidst opdateret:** 2026-01-31
