# ENTERPRISE API OPTIMIZER - PASS 2 MASTER PLAN
**Dato:** 2026-02-06 19:05
**Status:** PASS 1 COMPLETE (8/10) → PASS 2 PLANNING
**Mission:** GØR DET FÆRDIGT — IKKE NÆSTEN

---

## EXECUTIVE SUMMARY

**PASS 1 OPNÅET:**
✅ Core engine (450 linjer production code)
✅ Cache system (50x speedup proven)
✅ Rate limiting (300/min global, 30/min per-agent)
✅ Deduplication (5-second window)
✅ RabbitMQ events (6 event types)
✅ Fleet CLI integration
✅ 3 test agents integrated
✅ Service RUNNING (PID 629821)

**PASS 1 MANGLER (8/10 ikke 10/10):**
⚠ Real API integration (simulated calls)
⚠ Pytest test suite

**PASS 2 MISSION:**
Gør optimizeren til et **PERMANENT PRODUKTIONSSYSTEM** der:
1. Håndterer REAL AI API calls (ikke simulation)
2. Roterer intelligent mellem ALLE backends
3. Integrerer med eksisterende infrastruktur (AHO, Gateway, vLLM)
4. Har fuld test coverage (pytest + integration)
5. Tracking & metrics dashboard
6. FÆRDIG = kan køre 24/7 uden supervision

---

## FASE 1: REAL API INTEGRATION

### Komponent 1.1: Backend Connector
**Opgave:** Udskift `_execute_actual_call()` simulation med real API calls

**Fil:** `enterprise_optimizer.py` linje 467-478

**Implementation:**
```python
def _execute_actual_call(self, endpoint: str, params: dict, model: str) -> dict:
    """Real API call via backend rotator"""
    # Import ai_backend_rotator
    from ai_backend_rotator import AIBackendRotator
    rotator = AIBackendRotator()

    # Extract message from params (standardize format)
    messages = params.get("messages", [])
    prompt = messages[-1]["content"] if messages else str(params)

    # Call via rotator (automatic failover)
    response = await rotator.chat(
        message=prompt,
        temperature=params.get("temperature", 0.7),
        max_tokens=params.get("max_tokens", 600)
    )

    # Return OpenAI-compatible format
    return {
        "choices": [{"message": {"content": response}}],
        "model": model,
        "timestamp": time.time()
    }
```

**Test:** 3 agents (quality, autohealer, council) skal kunne lave REAL AI calls via optimizer

---

### Komponent 1.2: Async Support
**Problem:** Backend rotator er async, optimizer er sync

**Løsning:**
- Tilføj `asyncio` support til `EnterpriseOptimizer`
- Opdater `execute_api_call()` til async
- Opdater optimizer_client til async wrapper

**Files:**
- `enterprise_optimizer.py` — add async methods
- `optimizer_client.py` — async wrapper

---

## FASE 2: BACKEND INTELLIGENCE

### Komponent 2.1: Task-Aware Routing
**Opgave:** Intelligent backend valg baseret på task type

**Backend Specialization:**
| Task Type | Primary Backend | Reason |
|-----------|-----------------|--------|
| Reasoning | DeepSeek R1 (lokal) | Reasoning-optimized model |
| Code | Cerebras/Codellama | Code specialization |
| General | Cerebras/Groq | Fast, reliable |
| Long-form | Together/xAI | High token limits |
| Embeddings | Ollama nomic-embed | Specialized |

**Implementation:**
```python
class TaskRouter:
    def select_backend(self, agent_type: str, params: dict) -> str:
        """Select optimal backend for task"""
        # Detect task type from params
        if "code" in str(params).lower():
            return "cerebras"  # Code-optimized
        elif "reason" in str(params).lower():
            return "deepseek-r1"  # Reasoning model
        elif len(str(params)) > 2000:
            return "together"  # Long context
        else:
            return "cerebras"  # Default fast
```

---

### Komponent 2.2: vLLM Integration
**Opgave:** Aktiver vLLM direct inference (unified_model_gateway.py)

**Current State:**
- Gateway routes til Ollama (Phase 1)
- vLLM kode EXISTS men IKKE aktiveret

**Activation:**
1. Installer vLLM: `pip install vllm`
2. Load models in vLLM
3. Replace Ollama routing (linje 126-143) med vLLM inference
4. Test 665+ concurrent requests

**Performance Target:** 10x throughput vs Ollama

---

## FASE 3: NYE BACKENDS

### Komponent 3.1: DeepSeek R1 Cloud
**Problem:** deepseek-r1:8b er lokal, men INGEN cloud variant

**Research:**
- DeepSeek API: https://platform.deepseek.com/api-docs
- Cost: GRATIS tier (? verificer)
- Rate limit: ? RPM

**Implementation:**
1. Signup for API key
2. Add til `ai_backend_rotator.py`
3. Test reasoning tasks
4. Benchmark vs lokal model

---

### Komponent 3.2: OpenClaw, Goose, Kimik2
**Problem:** INGEN referencer fundet

**Action:**
1. Research hver model:
   - **OpenClaw**: ? (find API/docs)
   - **Goose**: ? (find API/docs)
   - **Kimik2**: ? (find API/docs)
2. Hvis GRATIS + ACCESSIBLE → add til rotator
3. Hvis IKKE tilgængelig → SKIP

**Decision Point:** Er disse critical? Eller nice-to-have?

---

## FASE 4: TEST SUITE

### Komponent 4.1: Pytest Suite
**Opgave:** Konverter `test_optimizer.py` til pytest-compatible

**Current:** Integration script (75 lines)

**Pytest Structure:**
```
AGENTS/agents/tests/
├── test_enterprise_optimizer.py
│   ├── test_cache_hit()
│   ├── test_cache_miss()
│   ├── test_dedupe()
│   ├── test_rate_limit()
│   ├── test_backend_failover()
│   ├── test_concurrent_requests()
│   └── test_integration_end_to_end()
├── test_optimizer_client.py
│   ├── test_client_init()
│   ├── test_api_call()
│   └── test_health_check()
└── conftest.py (fixtures)
```

**Minimum:** 10 tests covering all core functionality

---

### Komponent 4.2: Load Testing
**Opgave:** Test under real load (100+ concurrent requests)

**Tool:** `locust` or `pytest-benchmark`

**Scenarios:**
1. 100 agents × 5 calls each = 500 concurrent
2. Cache hit rate measurement
3. Dedupe detection under load
4. Rate limit enforcement
5. Backend failover under stress

**Success Criteria:**
- 0% errors under 500 concurrent
- Cache hit rate > 30%
- Dedupe catches > 90% duplicates

---

## FASE 5: METRICS & DASHBOARD

### Komponent 5.1: Performance Metrics
**Opgave:** Track ALL optimizer metrics

**Metrics:**
- Cache hit rate (per agent, per model)
- Average latency (cache vs API)
- Dedupe savings (calls prevented)
- Rate limit events
- Backend usage distribution
- Cost savings (even if $0, track API calls saved)

**Storage:** SQLite tables + JSONL logs

---

### Komponent 5.2: Dashboard
**Opgave:** Visualiser optimizer performance

**Options:**
1. **Streamlit dashboard** (quick, port 8502)
2. **Flask + Charts.js** (custom, integrates med HQ)
3. **Terminal TUI** (Textual, like sejrliste TUI)

**Dashboard Sections:**
1. **Overview**: Total calls, cache hits, savings
2. **By Agent**: Usage per agent (quality, autohealer, etc.)
3. **By Backend**: Distribution across backends
4. **Timeline**: Calls/hour, hit rate trends
5. **Health**: Current rate limits, active agents

**Decision:** Streamlit = fastest path to FÆRDIG

---

## FASE 6: AHO INTEGRATION

### Komponent 6.1: Optimizer as AHO Backend
**Opgave:** AHO bruger optimizer for ALL AI calls

**Current:** AHO calls `ai_backend_rotator` directly

**New:** AHO → Optimizer → Backend Rotator

**Benefits:**
- Cache shared across ALL agents (including AHO)
- Dedupe works for AHO + 28 agents combined
- Single point of control

**Implementation:**
```python
# In admiral_hybrid_organic.py
from optimizer_client import optimized_api_call

async def chat(self, message: str, context: dict = None) -> str:
    result = optimized_api_call(
        agent_id="aho",
        endpoint="/chat",
        params={"message": message},
        model="cerebras",
        agent_type="aho"
    )
    return result["result"]["choices"][0]["message"]["content"]
```

---

## FASE 7: PRODUCTION HARDENING

### Komponent 7.1: Error Handling
- Retry logic (3 attempts with exponential backoff)
- Graceful degradation (if optimizer down, fall back to direct calls)
- Dead letter queue for failed requests
- Circuit breaker per backend

### Komponent 7.2: Monitoring
- Health endpoint: `/health` (response time < 100ms)
- Prometheus metrics export (optional)
- Alert on: high error rate, full rate limit, cache degradation

### Komponent 7.3: Documentation
- API docs (endpoint specs, response formats)
- Integration guide (how to add new agent)
- Troubleshooting guide (common issues)
- CLAUDE.md update (optimizer in ELLE.md architecture)

---

## PASS 2 COMPLETION CHECKLIST

### RUNNING (Production-Ready)
- [ ] Real API calls (no simulation)
- [ ] Async support (no blocking)
- [ ] vLLM activated (10x throughput)
- [ ] All backends tested (10+ working)
- [ ] Error handling robust (retry + fallback)
- [ ] Health endpoint responding
- [ ] 24/7 systemd service stable

### PROVEN (Data-Driven)
- [ ] 10+ pytest tests passing
- [ ] Load test: 500 concurrent (0% errors)
- [ ] Cache hit rate > 30% (measured)
- [ ] Dedupe rate > 90% (measured)
- [ ] Backend failover < 1s (measured)
- [ ] 7 days uptime (no crashes)

### TESTED (Coverage)
- [ ] Unit tests: 15+ tests
- [ ] Integration tests: 5+ scenarios
- [ ] Load tests: 3+ scenarios
- [ ] Real agent integration: 5+ agents using optimizer
- [ ] Dashboard deployed (Streamlit on :8502)

---

## TIDSLINJE & PRIORITETER

**MUST-HAVE (Core Functionality):**
1. Real API integration (Fase 1) — 2-3 hours
2. Async support (Fase 1.2) — 1-2 hours
3. Pytest suite (Fase 4.1) — 2-3 hours
4. Error handling (Fase 7.1) — 1 hour

**SHOULD-HAVE (Production Quality):**
5. Task routing (Fase 2.1) — 1 hour
6. vLLM activation (Fase 2.2) — 2-3 hours
7. Metrics tracking (Fase 5.1) — 1-2 hours
8. Load testing (Fase 4.2) — 1 hour

**NICE-TO-HAVE (Polish):**
9. Dashboard (Fase 5.2) — 2-3 hours
10. AHO integration (Fase 6.1) — 1 hour
11. DeepSeek R1 cloud (Fase 3.1) — 1-2 hours
12. OpenClaw/Goose/Kimik2 (Fase 3.2) — research dependent

**Total Estimeret:** 15-25 hours (over 3-5 work sessions)

---

## SUCCESS CRITERIA (PASS 2 SCORE: 10/10)

**Minimum Requirements:**
- ✅ NO simulation (all real APIs)
- ✅ 15+ pytest tests passing
- ✅ 3+ backends active
- ✅ Cache hit rate > 30%
- ✅ 0% errors under 100 concurrent
- ✅ 24h+ uptime proven
- ✅ Dashboard deployed

**Excellence Indicators:**
- 🏆 10+ backends active
- 🏆 vLLM activated (10x throughput)
- 🏆 50%+ cache hit rate
- 🏆 AHO integrated
- 🏆 7 days uptime
- 🏆 Load tested 500+ concurrent

---

## DECISION POINTS

**Q1: vLLM Now or Later?**
- **Now**: Massive performance gain (10x)
- **Later**: Real API more critical first
- **Recommendation:** PHASE 1 first (real API), PHASE 2 (vLLM) second

**Q2: OpenClaw/Goose/Kimik2 Worth It?**
- **Research Required:** Find APIs, check if gratis
- **If NOT gratis or NOT accessible:** SKIP
- **Current 10 backends:** Already 365 RPM capacity (enough)

**Q3: Dashboard Tool?**
- **Streamlit:** Fastest (1-2 hours)
- **Flask:** Most flexible (3-4 hours)
- **TUI:** Coolest (2-3 hours)
- **Recommendation:** Streamlit (port 8502) = fastest path to FÆRDIG

---

**NÆSTE HANDLING:**
Få Rasmus' godkendelse på prioriteter, start FASE 1 (Real API Integration).

---

**RELATERET:**
- SEJR_LISTE.md (main victory file)
- PASS 1 COMPLETE (commit 2d70fe9)
- AI Usage Audit (305 calls/dag, $0 cost)
- Backend Rotator (ai_backend_rotator.py)
- Gateway (unified_model_gateway.py)
