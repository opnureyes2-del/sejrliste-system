# SEJR LISTE SYSTEM

**Version:** 3.0.0 - UNIFIED CROSS-DEVICE APP
**Opdateret:** 2026-01-31
**DNA Lag:** 7 (SELF-AWARE → SELF-OPTIMIZING)
**Bygget af:** Kv1nt + Rasmus

---

## HVAD ER DET?

Et **TVUNGET FORBEDRINGSSYSTEM** med 3 brugerflader (desktop, web, terminal) der sikrer at HVER opgave gennemgaas 3 gange med stigende kvalitet — og at systemet LAERER af HVER afsluttet opgave.

| Pass | Fokus | Krav |
|------|-------|------|
| **Pass 1** | Planlaegning | Baseline score |
| **Pass 2** | Eksekvering | Score > Pass 1 |
| **Pass 3** | 7-DNA Review | Score > Pass 2, Total >= 24/30 |

**ARKIVERING ER BLOKERET** indtil alle 3 passes er faerdige med tilstraekkelig score.

---

## HVAD SKAL DET BRUGES TIL?

### For Rasmus (daglig brug)
- **Planlaeg opgaver systematisk** — aldrig start uden research og plan
- **Tving dig selv til at forbedre** — Pass 2 SKAL vaere bedre end Pass 1
- **Laer af dine fejl permanent** — systemet husker alle patterns
- **Arbejd fra alle enheder** — desktop, telefon, terminal
- **Se din fremgang** — leaderboard, statistik, laering

### For AI-modeller (Claude, Gemini, etc.)
- **Fokus lock** — CLAUDE.md tvinger modellen til EN opgave ad gangen
- **Verificering** — kan ikke lyve om fremgang (auto_verify checker)
- **Score system** — objektiv maaling af AI performance
- **Pattern injection** — laeringer fra tidligere sejre injiceres automatisk

### For systemet selv (automatisk)
- **Daglig laering** — kl 08:00 scanner den alle arkiverede sejre for patterns
- **Feedback loop** — nye sejre faar automatisk top-5 patterns injiceret
- **Self-archiving** — blokerer arkivering indtil kvalitetskrav er opfyldt
- **Self-optimizing** — templates forbedres loebende baseret paa data

---

## ADGANG — 6 MAADER AT BRUGE SYSTEMET

### 1. Desktop App (GTK4 Native)
```bash
# Dobbeltklik "Sejrliste" paa desktop
# Eller:
python3 masterpiece_en.py   # English
python3 masterpiece.py       # Dansk
```
- Fuld GNOME-integration med Libadwaita
- Sidebar navigation, real-time opdatering
- 7 DNA lag visualisering

### 2. Web App (Browser)
```
http://localhost:8501
```
- Starter AUTOMATISK ved login (systemd service)
- 5 sider: Aktive Sejre, Arkiv, Ny Sejr, Statistik, Indstillinger
- Koer scripts direkte fra UI

### 3. Telefon (via Tailscale HTTPS)
```
https://rog.tailc9c1c5.ts.net
```
- Sikker forbindelse via Tailscale mesh VPN
- Samme web app som localhost
- Virker OVERALT (ikke kun lokal WiFi)

### 4. Telefon (lokal WiFi)
```
http://10.168.6.233:8501
```
- Direkte adgang paa samme netvaerk
- QR kode: `bash scripts/show_phone_url.sh`

### 5. Terminal Dashboard
```bash
sejrliste                    # Global kommando — fuld system status
bash scripts/sejr_dashboard.sh  # Detaljeret enforcement dashboard
```

### 6. TUI App (Textual)
```bash
python3 app/sejr_app.py
```
- Steam-style terminal brugerflade
- Keyboard-drevet (j/k navigation, Enter for aabning)
- Real-time fil-overvagning

---

## QUICK START

```bash
cd "/home/rasmus/Desktop/sejrliste systemet"

# 1. Opret ny sejr
python3 scripts/generate_sejr.py --name "Min Opgave" --goal "Hvad bygger vi" --tech "Python"

# 2. Arbejd med sejr i 10_ACTIVE/

# 3. Verificer progress (koer ofte!)
python3 scripts/auto_verify.py --all

# 4. Arkiver naar faerdig (blokeret til 3-pass done)
python3 scripts/auto_archive.py --sejr "MIN_OPGAVE_2026-01-31"

# 5. Se systemstatus
sejrliste
```

---

## EN SEJR MAPPE INDEHOLDER

Naar du opretter en ny sejr, faar du disse **5 filer** (Single Source of Truth):

### 1. PROJECT_BRIEF.md
> LAES DENNE FOERST. 30 sekunder. Komplet forstaaelse.
- Maal, success criteria, scope, teknologi

### 2. SEJR_LISTE.md
Hovedopgaven med alle checkboxes organiseret i 3 passes:
- **Pass 1:** PHASE 0-1-2 (Research, Planlaegning, Verificering)
- **Pass 2:** PHASE 2-3-4 (Udvikling, Test, Git)
- **Pass 3:** 7-DNA Gennemgang (alle 7 lag checkes)

### 3. CLAUDE.md
**DYNAMISK** fokus lock (genereret + pattern-injiceret):
- Praecis hvilken checkbox der er naeste
- Top 5 laerte patterns fra PATTERNS.json
- Anti-dum checkpoints

### 4. STATUS.yaml (UNIFIED)
**Single Source of Truth** for ALT status:
- **Pass tracking:** Completion %, scores, checkboxes
- **Score tracking:** Positive/negative events, rank
- **Model tracking:** Hvilke modeller arbejdede, sessions

### 5. AUTO_LOG.jsonl (MASTER)
**Single Source of Truth** for ALT logging:
- Alle handlinger med ISO 8601 timestamps
- Actor info (model_id, type)
- Session tracking

> **INGEN REDUNDANS:** Alt data eksisterer KUN et sted!

---

## 3-PASS KONKURRENCE SYSTEM

### Pass 1: PLANLAEGNING
- Research 3 alternativer (PHASE 0)
- Definer opgaven (PHASE 1)
- Plan verificering (PHASE 2)
- **Giv score og udfyld REVIEW**

### Pass 2: EKSEKVERING
- Implementer loesning
- Koer tests (minimum 3)
- Git workflow
- **Score SKAL vaere hoejere end Pass 1**

### Pass 3: 7-DNA GENNEMGANG
- Gennemgaa ALLE 7 DNA lag:
  1. SELF-AWARE — Kender systemet sig selv?
  2. SELF-DOCUMENTING — Er alt logget?
  3. SELF-VERIFYING — Er alt testet?
  4. SELF-IMPROVING — Har vi laert noget?
  5. SELF-ARCHIVING — Kun essens bevaret?
  6. PREDICTIVE — Hvad er naeste skridt?
  7. SELF-OPTIMIZING — Kunne vi have gjort det bedre?
- Koer 5+ tests
- **Score SKAL vaere hoejere end Pass 2**
- **Total score SKAL vaere >= 24/30**

---

## LAERINGS-SYSTEMET (FEEDBACK LOOP)

```
Sejr FAERDIG
    |
    v
auto_archive.py → flytter til 90_ARCHIVE/
    |
    v
auto_learn.py → scanner ALLE arkiverede sejre
    |                → identificerer patterns, bugs, workflows
    |                → gemmer i PATTERNS.json (52 patterns, stigende)
    v
generate_sejr.py → laeser top-5 patterns
    |             → injicerer i ny CLAUDE.md som "LEARNED WISDOM"
    |             → tracker applied_count for fair rotation
    v
NY SEJR starter med VIDEN fra ALLE tidligere sejre
```

**Cron job:** Daglig laering kl 08:00 (uanset om der er nye sejre)

---

## ALLE SCRIPTS (25 stk)

### Kvalitet og Laering (7 scripts)
| Script | Funktion |
|--------|----------|
| `auto_verify.py` | 3-pass verifikation + blocker-check |
| `auto_archive.py` | Arkivering (blokeret til done) + trigger laering |
| `auto_learn.py` | Pattern-ekstraktion fra alle sejre |
| `auto_optimize.py` | Template-forbedring baseret paa patterns |
| `auto_track.py` | Live state tracking til _CURRENT/ |
| `auto_live_status.py` | LIVE_STATUS.md dashboard (--watch mode) |
| `auto_predict.py` | Forudsigelser for naeste skridt |

### AI Integration (6 scripts)
| Script | Funktion |
|--------|----------|
| `ai_assistant.py` | Unified task router (Opus/Sonnet/Haiku/Ollama) |
| `model_router.py` | Intelligent model-valg baseret paa opgavetype |
| `token_tools.py` | Token-taelling + cost-estimering |
| `hybrid_generate.py` | Ollama draft + Claude finish (sparer 70% tokens) |
| `dna_model_enforcer.py` | Verificer at rette model bruges til rette DNA-lag |
| `automation_pipeline.py` | Syntax → Lint → Security → Rapport |

### Generation og Kontekst (4 scripts)
| Script | Funktion |
|--------|----------|
| `generate_sejr.py` | Opret ny sejr (5 filer + pattern injection) |
| `build_claude_context.py` | Dynamisk CLAUDE.md builder |
| `update_claude_focus.py` | Opdater fokus-state |
| `build_knowledge_base.py` | ChromaDB indeksering af al dokumentation |

### Dashboard og Monitoring (3 scripts)
| Script | Funktion |
|--------|----------|
| `sejrliste_status.sh` | System status overblik (symlinked til `sejrliste`) |
| `sejr_dashboard.sh` | Terminal enforcement dashboard |
| `show_phone_url.sh` | QR kode til telefon-adgang |

### Utility (3 scripts)
| Script | Funktion |
|--------|----------|
| `admiral_tracker.py` | AI model score leaderboard |
| `timestamp_utils.py` | Timestamp-formattering |
| `generate_icon_sizes.py` | Desktop app ikon-generering |

---

## ADMIRAL KONKURRENCE SYSTEM

### Positive Points (Beloennning)
| Event | Points |
|-------|--------|
| CHECKBOX_DONE | +1 |
| PASS_COMPLETE | +10 |
| VERIFIED_WORKING | +5 |
| ADMIRAL_MOMENT | +10 |
| SEJR_ARCHIVED | +20 |

### Negative Points (Straf x2!)
| Event | Points |
|-------|--------|
| TOKEN_WASTE | -6 |
| MEMORY_LOSS | -10 |
| LIE_DETECTED | -20 |
| RULE_BREAK | -20 |

### Rankings
| Rang | Score |
|------|-------|
| STORADMIRAL | 150+ |
| ADMIRAL | 100-149 |
| KAPTAJN | 50-99 |
| LOEJTNANT | 20-49 |
| KADET | 0-19 |
| SKIBSDRENG | < 0 |

---

## INFRASTRUKTUR

### Automatisk
- **systemd service:** `sejrliste-web.service` — auto-start Streamlit ved login
- **Cron kl 08:00:** Daglig pattern-laering
- **Cron soendag 03:00:** Git maintenance

### Tailscale
- **Desktop ROG:** 100.86.106.42
- **Telefon Pixel 9 Pro:** 100.84.174.88
- **HTTPS:** https://rog.tailc9c1c5.ts.net (via Tailscale Serve)
- **Konto:** opnureyes2@gmail.com

### Desktop
- **Launcher:** victorylist.desktop (1 fil, 3 actions: GTK4 / Web / TUI)
- **Global kommando:** `sejrliste` (symlinked)

---

## MAPPE STRUKTUR

```
sejrliste systemet/
|
|-- masterpiece.py              # GTK4 desktop app (Dansk)
|-- masterpiece_en.py           # GTK4 desktop app (English)
|-- web_app.py                  # Streamlit web app (Dansk)
|-- web_app_en.py               # Streamlit web app (English)
|-- start-web.sh                # Wrapper for systemd service
|-- enforcement_engine.py       # Kvalitets-enforcement
|-- intro_integration.py        # INTRO folder integration
|
|-- app/                        # TUI terminal app
|   |-- sejr_app.py             # Hoved TUI (Textual, Steam-style)
|   |-- widgets/                # UI komponenter
|   |-- integrations/           # Git, INTRO, context sync
|   |-- utils/                  # Utilities
|   +-- watcher.py              # Filesystem overvagning
|
|-- scripts/                    # 25 automation scripts
|
|-- pages/                      # Streamlit web pages
|   |-- 1_Aktiv_Sejr.py
|   |-- 2_Arkiv.py
|   |-- 3_Ny_Sejr.py
|   |-- 4_Statistik.py
|   +-- 5_Indstillinger.py
|
|-- 00_TEMPLATES/               # Skabeloner (5 stk)
|-- 10_ACTIVE/                  # Aktive sejre (arbejd her)
|-- 90_ARCHIVE/                 # Arkiverede sejre (31 stk, 100% Grand Admiral)
|-- _CURRENT/                   # System state (live status, patterns, leaderboard)
+-- assets/                     # Ikoner og grafik
```

---

## STATISTIK

| Metric | Vaerdi |
|--------|--------|
| Arkiverede sejre | 31 |
| Gennemsnitlig score | 29.9/30 (99.7%) |
| Grand Admiral rate | 100% |
| Laerte patterns | 52 |
| Scripts | 25 |
| Brugerflader | 3 (GTK4 + Web + TUI) |
| Adgangsmetoder | 6 |
| DNA lag | 7 |
| Aktive sejre | 1 |

---

## DOKUMENTATION

| Fil | Indhold |
|-----|---------|
| `README.md` | Denne fil — komplet overblik |
| `MANUAL.md` | Fuld dokumentation (3-pass + score) |
| `ADMIRAL.md` | Hvad er en Admiral? (5 kvaliteter) |
| `MODEL_ONBOARDING.md` | AI onboarding (laes foerst som ny model) |
| `SCRIPT_REFERENCE.md` | Alle scripts dokumenteret |
| `EKSEMPLER.md` | 10+ konkrete eksempler |
| `ARBEJDSFORHOLD.md` | Komplet vejledning (AI regler) |
| `ARKITEKTUR.md` | System arkitektur |
| `LOG_FORMAT.md` | Log format specifikation |
| `PREVENTION_RULES.md` | Forebyggelsesregler |

Alle dokumenter findes paa baade dansk og engelsk (*_EN.md).

---

**Status:** OPERATIONEL — Cross-device, self-learning, 100% Grand Admiral rate
**Git:** github.com/opnureyes2-del/sejrliste-system
