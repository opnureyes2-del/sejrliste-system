# HVAD SKAL JEG TÆNKE PÅ FOR AT FÅ FASE 2-5 OPFULDT?

**Dato:** 2026-02-06 19:30
**Status:** FASE 1 ✅ DONE, klar til FASE 2-5

---

## CURRENT STATE (Verificeret lige nu)

✅ **FASE 1 COMPLETE:**
- Real API integration via AIBackendRotator
- End-to-end test: 1.03s + 1.08s (proven)
- Backend failover: Cerebras→Gemini→Groq (automatic)
- Service: PID 708130, active, 26MB RAM
- 3 agenter integreret: quality, autohealer, council

⚠️ **Database Status:**
- Cache DB: Eksisterer ikke endnu (oprettes ved første real usage)
- Logs DB: Eksisterer ikke endnu (oprettes ved første real usage)
- Dette er NORMALT - de oprettes automatisk når agenter kalder optimizer

---

## FASE 2: BACKEND INTELLIGENCE

### Hvad skal der til?

**2.1 Task-Aware Routing (1 time)**

SKAL TÆNKE PÅ:
- Hvordan detekterer jeg task type? (keyword-baseret vs ML)
- Hvilke backends er bedst til hvad?
- Fallback hvis specialiseret backend fejler?

IMPLEMENTERING:
```python
class TaskRouter:
    def select_backend(self, agent_type: str, params: dict) -> List[str]:
        """Return prioriteret liste af backends"""
        # Code tasks
        if "code" in str(params).lower() or "function" in str(params):
            return ["cerebras", "groq", "together"]  # Code-optimized
        
        # Reasoning tasks
        elif "analyze" in str(params) or "reason" in str(params):
            return ["deepseek-r1", "mistral", "cerebras"]  # Reasoning-optimized
        
        # Long content
        elif len(str(params)) > 2000:
            return ["together", "xai", "groq"]  # High token limit
        
        # Default: fastest
        else:
            return ["cerebras", "groq", "mistral"]
```

CRITICAL SPØRGSMÅL:
- Skal jeg bruge eksisterende ai_backend_rotator logic ELLER erstatte den?
- SVAR: Extend - rotator kan modtage prioriteret backend liste

---

**2.2 vLLM Activation (2-3 timer)**

SKAL TÆNKE PÅ:
- vLLM kræver GPU (RTX 2080 SUPER er loaded ✅)
- vLLM installer via pip (`pip install vllm`)
- Hvilke modeller skal loades? (deepseek-r1:8b, llama, etc.)
- Memory: 8GB VRAM = kan kun loade 1-2 modeller samtidig
- Performance target: 10x throughput (100 req/min → 1000 req/min)

BLOCKERS:
- Skal `unified_model_gateway.py` ændres? JA (linje 126-143)
- Test: Kan vLLM køre på RTX 2080 SUPER? (skal verificeres)
- Conflicts med Ollama? (begge bruger GPU)

CRITICAL DECISION:
- Start med ÉN model (deepseek-r1:8b) for at bevise det virker
- DEREFTER: Expand til flere modeller

---

## FASE 3: NYE BACKENDS

### Hvad skal der til?

**3.1 DeepSeek R1 Cloud (1-2 timer)**

SKAL TÆNKE PÅ:
- API docs: https://platform.deepseek.com/api-docs
- Er der gratis tier? (SKAL verificeres før signup)
- Rate limits? (skal matche til backend rotator)
- API key storage: ~/.admiral_api_keys_systemd.env

ACTION:
1. Research DeepSeek API (web search)
2. Hvis GRATIS → signup + add til rotator
3. Hvis IKKE gratis → SKIP (vi har allerede 10 gratis)

---

**3.2 OpenClaw, Goose, Kimik2 (Research-dependent)**

SKAL TÆNKE PÅ:
- INGEN dokumentation fundet endnu
- Måske projekter der ikke eksisterer længere?
- Eller måske ikke-offentlige APIs?

CRITICAL DECISION:
- Prioritet: **LAV** (vi har 10 backends, 465 RPM capacity)
- Time box: Max 30 min research per model
- Hvis IKKE accessible → SKIP og fortsæt

ACTION:
- Web search: "OpenClaw API", "Goose AI API", "Kimik2 API"
- Hvis INGEN resultater → SKIP

---

## FASE 4: PYTEST SUITE

### Hvad skal der til?

**4.1 Test Suite (2-3 timer)**

SKAL TÆNKE PÅ:
- Konverter test_optimizer.py til pytest format
- Minimum 15 tests (PASS 2 krav)
- Coverage: cache, dedupe, rate limit, failover, concurrent

TEST STRUKTUR:
```
AGENTS/agents/tests/
├── test_enterprise_optimizer.py (10+ tests)
├── test_optimizer_client.py (3+ tests)
├── conftest.py (fixtures: mock optimizer, mock backends)
└── test_integration.py (end-to-end)
```

CRITICAL TESTS:
1. test_cache_hit() - cache skal returne indenfor 10ms
2. test_cache_miss() - første call skal tage >100ms (real API)
3. test_dedupe() - 2 identiske calls indenfor 5s → 1 API call
4. test_rate_limit_enforcement() - 31. call indenfor 1 min → blocked
5. test_backend_failover() - mock Cerebras fail → Groq success
6. test_concurrent_10() - 10 parallel calls → 0 errors
7. test_real_api_call() - actual AI response (ikke mock)
8. test_agent_integration() - quality agent via optimizer
9. test_cache_database_persistence() - restart → cache intact
10. test_metrics_tracking() - logs DB entries after call

DEPENDENCIES:
- pytest installeret? (check venv)
- pytest-asyncio? (for async tests)
- Mock frameworks? (unittest.mock)

---

**4.2 Load Testing (1 time)**

SKAL TÆNKE PÅ:
- Tool: `locust` eller `pytest-benchmark`
- Scenario: 100 agents × 5 calls = 500 concurrent
- Success: 0% errors, cache hit >30%

MÅLING:
- Response time distribution (p50, p95, p99)
- Error rate under load
- Cache hit rate progression
- Backend distribution

---

## FASE 5: METRICS & DASHBOARD

### Hvad skal der til?

**5.1 Metrics Tracking (1-2 timer)**

SKAL TÆNKE PÅ:
- Metrics allerede tracked i optimizer_logs.db (SQLite)
- Hvad mangler? Dashboard-ready queries

METRICS:
```python
class MetricsCollector:
    def get_cache_hit_rate(self, last_hours=24) -> float:
        """Cache hits / total calls"""
        
    def get_dedupe_savings(self) -> int:
        """Antal calls forhindret af dedupe"""
        
    def get_backend_distribution(self) -> Dict[str, int]:
        """Calls per backend"""
        
    def get_average_latency(self) -> Dict[str, float]:
        """Cache vs API latency"""
```

---

**5.2 Dashboard (2-3 timer)**

SKAL TÆNKE PÅ:
- Streamlit = hurtigst (1-2 timer)
- Port 8502 (sejrliste bruger 8501)
- Real-time updates? (polling vs websockets)

DASHBOARD SECTIONS:
1. Overview: Total calls, cache hits, savings
2. By Agent: quality/autohealer/council usage
3. By Backend: Cerebras/Groq/Mistral distribution
4. Timeline: Calls per hour, hit rate trend
5. Health: Rate limits, errors, uptime

SYSTEMD SERVICE:
- admiral-optimizer-dashboard.service
- ExecStart: streamlit run dashboard.py --server.port 8502
- After: admiral-optimizer.service (dependency)

---

## FASE 6: AHO INTEGRATION (OPTIONAL)

### Hvad skal der til? (1 time)

SKAL TÆNKE PÅ:
- AHO kalder ai_backend_rotator direkte
- Skal ændres til optimizer_client
- Benefit: Shared cache på tværs af 28 agenter + AHO

RISK:
- AHO er kritisk infrastruktur (11 backends)
- Skal teste grundigt før deployment
- Fallback: Hvis optimizer down → direct calls

DECISION:
- Prioritet: **MEDIUM** (nice-to-have, ikke critical)
- Vent til optimizer er 100% stabil (7 dage uptime)

---

## FASE 7: PRODUCTION HARDENING

### Hvad skal der til? (1-2 timer)

**7.1 Error Handling**

SKAL TÆNKE PÅ:
- Retry logic (3 forsøg, exponential backoff)
- Circuit breaker per backend (hvis 5 fejl → skip i 5 min)
- Graceful degradation (optimizer down → direct call)

```python
@retry(tries=3, delay=1, backoff=2)
def _execute_with_retry(self, ...):
    """Retry med exponential backoff"""
    
def _circuit_breaker_check(self, backend: str) -> bool:
    """Skip backend hvis for mange fejl"""
    failures = self._get_recent_failures(backend, window=300)
    return failures < 5
```

---

**7.2 Monitoring**

SKAL TÆNKE PÅ:
- Health endpoint: `curl http://localhost:PORT/health`
- Alerts: Email/desktop notification ved kritiske fejl
- Integration med admiral_event_reactor (allerede connected)

EVENTS:
- optimizer.degraded (cache hit rate < 20%)
- optimizer.rate_limit (nået grænse)
- optimizer.backend_down (alle backends fejler)

---

## EXECUTION ORDER (Prioriteret)

**MUST-DO (Core Funktionalitet):**
1. ✅ FASE 1: Real API (DONE)
2. **FASE 4.1: Pytest suite** (2-3 timer) ← START HER
3. FASE 7.1: Error handling (1 time)
4. FASE 5.1: Metrics tracking (1 time)

**SHOULD-DO (Production Quality):**
5. FASE 2.1: Task routing (1 time)
6. FASE 5.2: Dashboard (2 timer)
7. FASE 4.2: Load testing (1 time)

**NICE-TO-DO (Optimering):**
8. FASE 2.2: vLLM activation (2-3 timer)
9. FASE 3.1: DeepSeek R1 cloud (research-dependent)
10. FASE 6: AHO integration (når stabil)

**SKIP FOR NOW:**
- FASE 3.2: OpenClaw/Goose/Kimik2 (ingen dokumentation)

---

## CRITICAL SUCCESS FACTORS

**For at opnå 10/10 i PASS 2:**

1. **NO SIMULATION** ✅ (DONE - real API working)
2. **15+ PYTEST TESTS** ⚠️ (mangler - critical blocker)
3. **3+ BACKENDS ACTIVE** ✅ (10 backends operationelle)
4. **CACHE HIT >30%** ⏳ (skal måles under real usage)
5. **0% ERRORS UNDER 100 CONCURRENT** ⏳ (skal load testes)
6. **24H+ UPTIME** ⏳ (service lige genstartet)
7. **DASHBOARD DEPLOYED** ⏳ (mangler)

---

## BLOCKER ANALYSE

**INGEN HARD BLOCKERS:**
- ✅ GPU loaded (RTX 2080 SUPER, driver 590.48.01)
- ✅ Service running (PID 708130)
- ✅ 3 agents integrated
- ✅ RabbitMQ connected
- ✅ Real API proven

**SOFT BLOCKERS (løsbare):**
- ⚠️ vLLM installation (pip install, GPU test)
- ⚠️ DeepSeek R1 cloud research (API docs)
- ⚠️ Dashboard port (8502 skal være fri)

---

## ANBEFALET NÆSTE SKRIDT

**OPTION A: Færdiggør PASS 1 først (konservativ)**
- Lav pytest suite (15+ tests)
- Opnå 10/10 i PASS 1
- DEREFTER: Start PASS 2

**OPTION B: Start PASS 2 parallelt (aggressiv)**
- Lav pytest suite SAMTIDIG med task routing
- Deploy dashboard mens tests kører
- Parallel execution = hurtigere færdig

**MIN ANBEFALING: OPTION A**
- Pytest suite er CRITICAL (warning i PASS 1)
- Gør PASS 1 → 10/10 først
- DEREFTER: Full speed på PASS 2

**ESTIMERET TID:**
- Pytest suite: 2-3 timer
- Task routing: 1 time
- Dashboard: 2 timer
- Error handling: 1 time
- **TOTAL: 6-7 timer til solid PASS 2**

---

**SPØRGSMÅL TIL RASMUS:**

1. Skal jeg starte med pytest suite (færdiggøre PASS 1 først)?
2. Eller skal jeg gå direkte til task routing (FASE 2)?
3. Skal jeg research DeepSeek R1 cloud nu eller senere?
4. Er vLLM activation critical eller nice-to-have?

