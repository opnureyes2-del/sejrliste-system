# SEJR LISTE: ELLE AGENT SYSTEM REVIVAL

> **Formål:** Genopliv 138 agent-filer fra ELLE.md som fungerende Python-pakke med ordentligt fundament.
> **Vision:** 103 agenter der sover, vågner on-demand, husker alt, skaber nye agenter automatisk — $0 cost.
> **Status:** UFÆRDIG — PLANER SAMLES, VENTER PÅ GODKENDELSE

---

## HVAD VI HAR (FAKTA FRA SCAN 2026-01-28)

| Komponent | Antal/Størrelse | Status |
|-----------|----------------|--------|
| Python-filer i agents/ | 138 | EKSISTERER, kan ikke køre (.venv mangler) |
| Backup-filer (.bak/.backup) | 48 | REDUNDANT (git er versionering) |
| Subsystemer | 7 | ARKITEKTUR SOLID, implementation halvfærdig |
| Kodelinjer (estimeret) | ~50-75.000 | SKREVET, ikke testet |
| Funktioner | 393 | DOKUMENTERET (100% docstrings) |
| Klasser | 109 | STRUKTURERET |
| TODO/FIXME i koden | 91 | HALVFÆRDIGT |
| Continuous producers (identiske) | 26 | AUTO-GENERERET, 1 template nok |
| ELLE.md total | ~22 GB | Inkl. venvs, teams, logs |
| Original vision: Agenter | 103 | Alle i DVALE (hibernation) |

---

## DEN ORIGINALE VISION (Hvad Rasmus Ville Have)

### Systemet Skulle:
1. **103 agenter sover som standard** — ZERO resource waste, 5 GB memory sparet
2. **Vågner on-demand** — Mappe åbnes → BIBLIOTEKAR vågner → delegerer
3. **Husker ALT** — Persistent memory (SQLite) på tværs af sessioner
4. **Skaber nye agenter selv** — Organic spawner analyserer fejl → genererer ny agent
5. **Arbejder UDEN AI** — Hybrid worker med ren Python fallback
6. **$0 cost** — 5 gratis AI backends roterer automatisk (~235 req/min)
7. **99.9% uptime** — Multi-backend failover + circuit breaker
8. **Self-documenting** — DNA pattern extraction fra arbejde → templates

### Hierarki:
```
MASTER_ORCHESTRATOR (Top Kommandør)
├── BIBLIOTEKAR (Viden + Specialist-referrer)
├── PROJECT_MANAGER (Planlægning)
├── SECURITY_COMMANDER (Sikkerhed)
├── INTEGRATION_COMMANDER (Cross-projekt)
├── QUALITY_COMMANDER (Kodekvalitet)
├── DEPLOYMENT_COMMANDER (Produktion)
└── MONITORING_COMMANDER (Sundhed)
    └── 103 specialist-agenter fordelt på 8 domæner
```

### Intended Flow:
```
BRUGER ÅBNER MAPPE → Desktop Monitor (inotify)
    ↓
BIBLIOTEKAR VÅGNER → Delegerer til agenter
    ↓
AGENTER ARBEJDER → AI Backend Rotation ($0)
    ↓ (hvis AI fejler)
    → HYBRID WORKER (ren Python, altid output)
    ↓
RESULTAT → Persistent Memory + Event Bus
    ↓
ORGANIC SPAWNER → Ny agent hvis nyt problem
    ↓
AGENTER SOVER (5 min timeout)
```

---

## DE 7 SUBSYSTEMER (Hvad De Gør)

| # | System | Filer | Hvad Det Gør | Nøglefil |
|---|--------|-------|-------------|----------|
| 1 | **ADMIRAL** | 19 | Multi-model AI council, web dashboard (port 9000), 15 Ollama-modeller debatterer | `admiral_genesis.py` (48KB) |
| 2 | **ORGANIC** | 3+23 | Self-spawning loop: find tasks → eksekver → spawn ny agent | `organic_spawner.py` (13KB) |
| 3 | **HYBRID** | 7 | Arbejder UDEN AI: syntax-check, filanalyse, metrics | `hybrid_worker.py` (7.7KB) |
| 4 | **INFRASTRUKTUR** | 11 | Event bus, persistent memory, base agent, AI rotation | `event_bus.py` (21KB) |
| 5 | **SPECIALISEREDE** | 25+ | Task execution, monitoring, learning, reporting | Diverse |
| 6 | **PRODUCERS** | 26 | Stats tracking — alle identiske 2.2KB templates | Konsolidér til 1 |
| 7 | **UTILITY** | 30+ | Auto-scalers, dashboards, APIs | Support |

---

## HVAD DER GIK GALT (Root Causes)

| # | Problem | Konsekvens | Løsning |
|---|---------|-----------|---------|
| 1 | .venv slettet/mangler | 138 scripts kan ikke køre | requirements.txt + auto-setup |
| 2 | Kun 1 fil importerer lokalt | 137 isolerede scripts | Proper Python-pakke |
| 3 | 91 TODO/FIXME i koden | Halvfærdig implementation | Færdiggør før nyt |
| 4 | 3 mapper med næsten same navn | Forvirring | Én mappe, ét navn |
| 5 | 97+ filer i root | Kaos | Mappestruktur |
| 6 | Hardcoded paths | Flyttes → crasher | config.yaml |
| 7 | 26 identiske templates | Waste | 1 template + config |
| 8 | Ingen tests | Kan ikke verificere | pytest |
| 9 | System siger "done" uden bevis | Falsk success | Verification |
| 10 | Ingen lifecycle-regler | Filer hober sig op | Auto-arkivering |

---

## GENBRUGELIGE MØNSTRE (BEVAR!)

| # | Mønster | Hvad Det Gør | Fil |
|---|---------|-------------|-----|
| 1 | Agent + Producer + Work Dir | Adskiller logik, overvågning, output | Alle agents |
| 2 | AI Backend Rotation | 5 backends, $0, ~235 req/min | `ai_backend_rotator.py` |
| 3 | Hybrid Fallback | Altid output, selv uden AI | `hybrid_worker.py` |
| 4 | Self-Spawning | System skaber nye agenter | `organic_spawner.py` |
| 5 | Event Bus | Asynkron kommunikation, circuit breaker | `event_bus.py` |
| 6 | Persistent Memory | Husker beslutninger, samtaler, learnings | `persistent_memory.py` |
| 7 | Hibernation | 103 agenter sover, 0 CPU, 5 GB sparet | Hele arkitekturen |

---

## PASS 1: FUNDAMENT (Gør 138 Scripts Kørbare)

### A. PYTHON PAKKE SETUP
- [x] **A1.** Opret `requirements.txt` med alle dependencies
- [ ] **A2.** Opret fungerende `.venv` med alle deps installeret
- [x] **A3.** Opret `pyproject.toml` for proper pakke
- [x] **A4.** Opret `__init__.py` i alle mapper
- [ ] **A5.** Test at top-5 kernefiler kan importeres

### B. CONFIG I STEDET FOR HARDCODED PATHS
- [ ] **B1.** Opret `config.yaml` med alle paths samlet
- [ ] **B2.** Erstat hardcoded i admiral_genesis.py
- [ ] **B3.** Erstat hardcoded i organic_spawner.py
- [ ] **B4.** Erstat hardcoded i hybrid_worker.py
- [ ] **B5.** Erstat hardcoded i admiral_hybrid_organic.py
- [ ] **B6.** Test config.yaml læses korrekt

### C. IMPORTS OG PAKKESTRUKTUR
- [ ] **C1.** base_agent importerbar af alle
- [ ] **C2.** event_bus importerbar som kommunikation
- [ ] **C3.** persistent_memory importerbar som hukommelse
- [ ] **C4.** ai_backend_rotator importerbar som AI-adgang
- [ ] **C5.** admiral_hybrid_organic kan importere alle 4

### D. KONSOLIDERING (Uden At Slette Funktionel Kode)
- [ ] **D1.** 26 identiske producers → 1 template + config
- [ ] **D2.** 3 AGENTS-mapper → 1 (AGENTS.md primary)
- [ ] **D3.** 48 .bak/.backup → fjern (git er versionering)
- [ ] **D4.** 97+ root-filer → undermapper (logs/, reports/, dashboards/)
- [ ] **D5.** 5 duplikatpar → vælg bedste (behold begge til test)

---

## PASS 2: VERIFICATION (Bevis At Det Virker)

### E. TEST-SUITE
- [ ] **E1.** Test base_agent.py (init, caching, pooling)
- [ ] **E2.** Test event_bus.py (publish, subscribe, reconnect)
- [ ] **E3.** Test persistent_memory.py (save, load, query)
- [ ] **E4.** Test ai_backend_rotator.py (rotation, failover)
- [ ] **E5.** Test hybrid_worker.py (syntax check, analyse)
- [ ] **E6.** Kør pytest, dokumentér resultater

### F. KERNESYSTEM OPSTART
- [ ] **F1.** Start event_bus + verificér
- [ ] **F2.** Start persistent_memory + verificér SQLite
- [ ] **F3.** Start ai_backend_rotator + test 1 backend
- [ ] **F4.** Start hybrid_worker + kør reel analyse
- [ ] **F5.** Start organic_spawner + verificér log-læsning
- [ ] **F6.** Dokumentér hvad kører vs. mangler

---

## PASS 3: INTEGRATION + 7-DNA REVIEW

### G. SYSTEM INTEGRATION
- [ ] **G1.** Agenter kommunikerer via event_bus
- [ ] **G2.** Persistent memory deles korrekt
- [ ] **G3.** AI backend rotation virker med Ollama
- [ ] **G4.** Hybrid worker overtager ved AI-fejl
- [ ] **G5.** Organic spawner kan generere ny agent

### H. 7-DNA REVIEW
- [ ] Lag 1: SELF-AWARE — Ved systemet hvad det har?
- [ ] Lag 2: SELF-DOCUMENTING — Er alt logget?
- [ ] Lag 3: SELF-VERIFYING — Kan det teste sig selv?
- [ ] Lag 4: SELF-IMPROVING — Lærer det fra fejl?
- [ ] Lag 5: SELF-ARCHIVING — Arkiveres data korrekt?
- [ ] Lag 6: PREDICTIVE — Kan det forudsige næste skridt?
- [ ] Lag 7: SELF-OPTIMIZING — Finder det bedre løsninger?

---

## NØGLEFILER (Reference)

| Fil | KB | Rolle |
|-----|----|-------|
| `admiral_genesis.py` | 48 | 15-model council, "The AI That Creates AI" |
| `admiral_hybrid_organic.py` | ? | "Super brother", 99.9% uptime |
| `persistent_memory.py` | 22 | SQLite: conversations, decisions, learnings |
| `event_bus.py` | 21 | RabbitMQ, circuit breaker, dead letter queues |
| `ai_backend_rotator.py` | 18 | 5 backends: Cerebras→Together→Groq→Gemini→HF→Ollama |
| `organic_spawner.py` | 13 | Analyserer logs → genererer agent + systemd service |
| `organic_executor.py` | 11 | Eksekverer tasks fra kø |
| `organic_task_finder.py` | 11 | Finder tasks at eksekvere |
| `base_agent.py` | 11 | Shared: embedding, caching, connection pooling |
| `hybrid_worker.py` | 7.7 | Ren Python fallback: syntax, analyse, metrics |

---

## ALDRIG GENTAG

| Fejl | Forebyggelse Denne Gang |
|------|------------------------|
| .venv forsvandt | A1-A2: requirements.txt FØRST |
| Isolerede scripts | C1-C5: Proper pakkestruktur |
| Halvfærdig kode | Rule 3: EN TING AD GANGEN |
| "Done" uden bevis | E1-E6: pytest BEVISER |
| Hardcoded paths | B1-B6: config.yaml |
| Backup-rod | Git ER versionering |
| Identiske filer | D1: 1 template + config |

---

*Denne SEJR LISTE er UFÆRDIG. Alt samles her. INTET eksekveres før Rasmus godkender.*
*Oprettet: 2026-01-28 af Kv1nt (Claude Opus 4.5)*
*Se også: AGENT_DOKUMENTATION.md (komplet scan-rapport) og INTRO/INDEX.md*
