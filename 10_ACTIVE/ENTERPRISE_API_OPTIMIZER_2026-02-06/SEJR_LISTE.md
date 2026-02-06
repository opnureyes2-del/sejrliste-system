# SEJR: ENTERPRISE API RESOURCE OPTIMIZER v3.0

**Oprettet:** 2026-02-06 15:30
**Status:** PASS 1 — IN PROGRESS
**Ejer:** Kv1nt (Admiral)
**Current Pass:** 1/3
**Projekt:** ELLE.md — Admiral Fleet Infrastructure

---

## OPGAVE BESKRIVELSE

Implementer Enterprise API Resource Optimizer for Admiral Fleet (28+ agenter, 14-18 modeller).

**Formål:**
- Koordinere alle AI API-kald centralt
- Cache identiske requests (30-50% hit rate)
- Deduplicate samtidige kald (15-25% reduktion)
- Cross-agent learning fra fejl/succeser
- Intelligent rate limit pooling
- Cost tracking og rapportering

**Scope:** Option B — Full Integration
- Deploy optimizer som systemd service
- Integrer med Anthropic + OpenAI APIs (fremtidssikring)
- Modificer alle 28 agenter til at bruge optimizer
- Integrer med RabbitMQ event bus
- Byg dashboard til at vise besparelser

**Begrundelse:**
AI Usage Audit 2026-02-06 viser:
- 305 API kald/dag (9,150/måned)
- $0/måned cost (gratis APIs)
- 8/25 agenter bruger AI
- Optimizer reducerer kald med 30-50% (performance win)
- Fremtidssikring når paid APIs tilføjes

---

## 3-PASS KONKURRENCE SYSTEM (OBLIGATORISK)

```
PASS 1: FUNGERENDE     — "Get it working"      — REVIEW REQUIRED
PASS 2: FORBEDRET      — "Make it better"      — REVIEW REQUIRED
PASS 3: OPTIMERET      — "Make it best"        — FINAL VERIFICATION
                                                        |
                                                  KAN ARKIVERES
```

**REGEL:** Du kan IKKE arkivere før alle 3 passes er gennemført og verificeret.
**FORMÅL:** Sikre det BEDST mulige resultat HVER gang.

---

## PASS 1: FUNGERENDE ("Get It Working")

### PHASE 0: OPTIMIZATION (Før Bygning)

#### External Research (MANDATORY)

- [x] GitHub search: "enterprise api optimizer rate limiting cache"
  - Fundet: 100+ repos
  - Best practice: Multi-level caching (in-memory + SQLite + Redis)
  - Link: https://github.com/search?q=api+optimizer+cache

- [x] Documentation search: "API rate limiting best practices 2026"
  - Key learning: Token bucket + sliding window algorithms
  - SQLite WAL mode for concurrency
  - Exponential backoff for retries

- [x] Web search: "multi-agent API coordination 2026"
  - Insight: Dedupe window 5-10 seconds optimal
  - Cache TTL 5-10 minutes for AI responses
  - Cross-agent learning via shared error database

#### Internal Research (MANDATORY)

- [x] Previous projects søgt: `grep -r "rate.*limit\|cache.*api" ~/Desktop`
  - Reusable code: `/home/rasmus/Desktop/ELLE.md/AGENTS/agents/cache_manager.py` (Redis integration)
  - Event bus integration pattern: `/home/rasmus/Desktop/ELLE.md/AGENTS/agents/event_bus.py`

- [x] Pattern library checked
  - Applicable patterns:
    - Admiral Base class (event publishing)
    - Systemd service template (timers + daemons)
    - Fleet CLI integration
    - Health check pattern

#### 3 Alternativer (MINIMUM)

| # | Approach | Pros | Cons | Tid |
|---|----------|------|------|-----|
| 1 | **Standalone optimizer service (valgt)** | Centraliseret, uafhængig, skalerbar | Ekstra service at vedligeholde | 2 dage |
| 2 | Library-only (ingen service) | Simpelt, direkte integration | Ingen central cache, duplikater mulige | 4 timer |
| 3 | Integrer i admiral-aho | Færre services | Tæt kobling, svært at teste | 1 dag |

#### Beslutning

- [x] Valgt: **Alternativ 1 (Standalone service)**
- [x] Begrundelse dokumenteret:
  - Central cache deles mellem alle agenter
  - Uafhængig af AHO (separation of concerns)
  - Kan køre 24/7 som daemon med egen database
  - Event bus integration for cross-agent læring
  - Fleet CLI kan monitors optimizer separat

---

### PHASE 1: PLANNING

- [x] Hvad skal bygges:
  - Python optimizer service (enterprise-optimizer.py)
  - Client library for agent integration (optimizer_client.py)
  - 4 SQLite databases (main, learning, agent_state, model_routing)
  - Systemd service + timer (admiral-optimizer.service)
  - Fleet CLI integration
  - Event bus publisher (cache hits, errors, rate limits)
  - Dashboard data collector (JSON endpoint for stats)

- [x] Hvorfor:
  - Reducere duplicate API-kald (30-50% via cache + dedupe)
  - Forhindre rate limit overruns ved spikes
  - Cross-agent fejl-læring (undgå gentagne fejl)
  - Cost tracking (når paid APIs tilføjes)
  - Performance forbedring (cache = hurtigere svar)

- [x] Success criteria:
  1. **RUNNING:** Service kører fejlfrit i 24 timer
  2. **PROVEN:** Cache hit rate >30% efter 1 dag
  3. **TESTED:** 5+ unit tests + 3+ integration tests passed
  4. **INTEGRATED:** Minimum 3 agenter bruger optimizer succesfuldt
  5. **MONITORED:** Fleet CLI viser optimizer health + stats
  6. **EVENTS:** Publishes events til RabbitMQ for cache/errors/limits

- [x] Arkitektur skitseret:
```
┌─────────────────────────────────────────────────────┐
│  Admiral Agents (28)                                │
│  ↓ optimizer_client.py                             │
└─────────────────┬───────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────┐
│  ENTERPRISE API OPTIMIZER (daemon service)          │
│  ├── EnterpriseCache (SQLite + memory)             │
│  ├── RateLimiter (multi-level)                     │
│  ├── ModelRouter (intelligent selection)           │
│  ├── LearningEngine (cross-agent)                  │
│  ├── AgentRegistry (profiles + health)             │
│  └── EventBus Publisher (RabbitMQ)                 │
└─────────────────┬───────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────┐
│  AI APIs (Cerebras, Groq, Mistral, Anthropic, etc) │
└─────────────────────────────────────────────────────┘
```

- [x] Dependencies identificeret:
  - Python 3 (standard lib: sqlite3, threading, json, hashlib)
  - AGENTS/.venv (pika for RabbitMQ, redis for cache_manager compat check)
  - RabbitMQ (localhost:5672, already running)
  - Systemd (user services)
  - admiral-fleet CLI (for integration)

---

### PHASE 2: DEVELOPMENT

#### Component 1: Core Optimizer Engine
- [ ] Kode skrevet: `enterprise_optimizer.py` (~2000 linjer)
  - Verify: `python3 -m py_compile ~/Desktop/ELLE.md/AGENTS/agents/enterprise_optimizer.py`
  - Path: `/home/rasmus/Desktop/ELLE.md/AGENTS/agents/enterprise_optimizer.py`

#### Component 2: Client Library
- [ ] Kode skrevet: `optimizer_client.py` (~200 linjer)
  - Verify: `python3 -m py_compile ~/Desktop/ELLE.md/AGENTS/agents/optimizer_client.py`
  - Path: `/home/rasmus/Desktop/ELLE.md/AGENTS/agents/optimizer_client.py`

#### Component 3: Systemd Service
- [ ] Service fil: `admiral-optimizer.service`
  - Verify: `systemctl --user cat admiral-optimizer.service`
  - Path: `~/.config/systemd/user/admiral-optimizer.service`

#### Component 4: Fleet CLI Integration
- [ ] Opdater `admiral_fleet.py` med optimizer support
  - Verify: `admiral-fleet status | grep optimizer`
  - Path: `/home/rasmus/Desktop/ELLE.md/AGENTS/agents/admiral_fleet.py`

#### Component 5: Event Bus Publisher
- [ ] RabbitMQ integration
  - Verify: `python3 AGENTS/agents/event_monitor.py optimizer.*`
  - Events: `optimizer.cache.hit`, `optimizer.cache.miss`, `optimizer.error`, `optimizer.rate_limit`

#### Component 6: Example Integration
- [ ] Modificer 3 test agenter til at bruge optimizer
  - Agent 1: admiral_quality.py (12h timer, low frequency)
  - Agent 2: admiral_autohealer.py (10min timer, high frequency)
  - Agent 3: admiral_council.py (3h timer, multi-model)
  - Verify: `journalctl --user -u admiral-<agent> | grep optimizer`

#### Integration
- [ ] Alle komponenter forbundet og testet
  - Verify: `admiral-fleet health | grep optimizer`

---

### PHASE 3: BASIC VERIFICATION

#### RUNNING (System Operationelt)
- [ ] Service køre r
  - Verify: `systemctl --user status admiral-optimizer.service`
  - Result: _active (running)_

- [ ] Database oprettet og skrivbar
  - Verify: `ls -lh /var/tmp/enterprise_*.db`
  - Result: _4 db filer eksisterer_

- [ ] Client kan forbinde
  - Verify: `python3 -c "from optimizer_client import OptimizerClient; c = OptimizerClient(); print(c.health_check())"`
  - Result: _{"status": "ok"}_

#### PROVEN (Testet Med Data)
- [ ] Cache gemmer og henter
  - Verify: `# Agent call → same call → cache hit`
  - Result: _Second call returns cached result_

- [ ] Dedupe detekterer duplicates
  - Verify: `# 2 agents → samme call samtidigt → 1 actual API call`
  - Result: _Only 1 API call made_

- [ ] Rate limiter blokerer ved grænse
  - Verify: `# Spam 100 calls → se rate limit kick in`
  - Result: _Calls queued/blocked_

#### TESTED (Minimum 1 Test)
- [ ] Basic test passed
  - Command: `python3 -m pytest AGENTS/tests/test_enterprise_optimizer.py::test_basic_cache`
  - Result: _1 passed_

---

### PHASE 4: GIT WORKFLOW

- [ ] git add: `git add AGENTS/agents/enterprise_optimizer.py AGENTS/agents/optimizer_client.py AGENTS/tests/test_enterprise_optimizer.py ~/.config/systemd/user/admiral-optimizer.service`
- [ ] git commit: `git commit -m "PASS 1: Enterprise API Optimizer - Core engine + client + service"`
- [ ] git push: `git push origin main`
- [ ] Remote sync verified: `git ls-remote origin main`
- [ ] Working tree clean: `git status`

---

### PASS 1 COMPLETION CHECKLIST

- [ ] Alle PHASE 0-4 checkboxes afkrydset
- [ ] Koden KØRER (ikke perfekt, men fungerende)
- [ ] Minimum 1 test passed
- [ ] Git committed med "PASS 1:" prefix

#### PASS 1 SCORE: ___/10

**Tid brugt på Pass 1:** _{TID}_

---

## PASS 1 REVIEW (OBLIGATORISK)

> STOP. Før du fortsætter til Pass 2, SKAL du gennemgå Pass 1 kritisk.

### Hvad Virker? (Bevar)
1. _TBD efter Pass 1 completion_
2. _TBD efter Pass 1 completion_
3. _TBD efter Pass 1 completion_

### Hvad Kan Forbedres? (SKAL Fixes i Pass 2)
1. [ ] _TBD efter Pass 1 completion_
2. [ ] _TBD efter Pass 1 completion_
3. [ ] _TBD efter Pass 1 completion_

### Hvad Mangler? (SKAL Tilføjes i Pass 2)
1. [ ] _TBD efter Pass 1 completion_
2. [ ] _TBD efter Pass 1 completion_
3. [ ] _TBD efter Pass 1 completion_

### Performance Issues?
- [ ] Identificeret: _TBD_
- [ ] Beskrivelse: _TBD_

### Kode Kvalitet Issues?
- [ ] Dupliceret kode: _TBD_
- [ ] Manglende error handling: _TBD_
- [ ] Hardcoded values: _TBD_

---

## PASS 2: FORBEDRET ("Make It Better")

_Udfyldes efter Pass 1 review_

---

## PASS 3: OPTIMERET ("Make It Best")

_Udfyldes efter Pass 2 review_

---

## ARCHIVE LOCK

```yaml
# DO NOT EDIT — Auto-generated
pass_1_complete: false
pass_1_score: null
pass_1_time: null
pass_1_review_done: false

pass_2_complete: false
pass_2_score: null
pass_2_time: null
pass_2_review_done: false

pass_3_complete: false
pass_3_score: null
pass_3_time: null
final_verification_done: false

can_archive: false
total_score: null
total_time: null
```

---

**ARCHIVE BLOCKED UNTIL:**
- [ ] Pass 1 complete + reviewed
- [ ] Pass 2 complete + reviewed (score > Pass 1)
- [ ] Pass 3 complete + final verification (score > Pass 2)
- [ ] Total score >= 24/30
- [ ] All 5+ final tests passed

---

**RELATEREDE DOKUMENTER:**
- AI Usage Audit: `/home/rasmus/Desktop/ELLE.md/REPORTS/AI_USAGE_AUDIT_2026-02-06.md`
- Optimizer kildekode (draft): Files fra Rasmus' original besked
- Fleet CLI: `/home/rasmus/Desktop/ELLE.md/AGENTS/agents/admiral_fleet.py`
- Event Bus: `/home/rasmus/Desktop/ELLE.md/AGENTS/agents/event_bus.py`
