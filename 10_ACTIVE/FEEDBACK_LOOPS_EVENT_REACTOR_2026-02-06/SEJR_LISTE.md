# SEJR: FEEDBACK_LOOPS_EVENT_REACTOR

**Oprettet:** 2026-02-06
**Prioritet:** KRITISK
**Kategori:** Agent Intelligence Infrastructure
**Estimat:** 1 session

---

## BAGGRUND

22 agenter publicerer events til RabbitMQ event bus (`elle_integration_hub`).
0 agenter lytter. Ingen reagerer. Systemet er en envejs megafon.

**Denne sejr bygger den foerste reelle feedback loop:**
En daemon der LYTTER paa events og REAGERER automatisk.

---

## PASS 1: PLANLÆGNING (Fungerende)

### Arkitektur

```
[22 Agents] --publish--> [RabbitMQ] --subscribe--> [Event Reactor] --react--> [Actions]
                                                         |
                                                         +-- agent.*.error   --> trigger autohealer
                                                         +-- disk.alert      --> trigger disk cleanup
                                                         +-- healer.stuck    --> escalate + notify
                                                         +-- quality.*       --> log + trend track
                                                         +-- ecosystem.*     --> health summary
                                                         +-- file.changed    --> log change tracking
                                                         +-- *.critical      --> desktop notification
```

### Checkboxes

- [x] Laes og forstaa event_bus.py (subscribe/start_consuming API)
- [x] Laes og forstaa admiral_base.py (AdmiralAgent base class)
- [x] Identificer daemon-agenter der kan udvides
- [x] Design event reactor arkitektur
- [x] Definer alle event subscriptions og reaktioner

### Beslutninger

1. **NY DEDIKERET DAEMON** fremfor at patche eksisterende agenter
   - Grund: Separation of concerns — een agent, een opgave
   - Navn: `admiral_event_reactor.py`

2. **Bruger AdmiralAgent base class** for logging, health, event publishing

3. **Subscriber patterns:**
   - `agent.#` — alle agent lifecycle events (started, completed, error)
   - `disk.*` — disk alerts og warnings
   - `healer.*` — autohealer resultater
   - `quality.*` — code quality events
   - `ecosystem.*` — daily report events
   - `file.*` — file change events
   - `git.*` — git status events

4. **Reaktioner:**
   - `agent.*.error` → Log, desktop notification, optionally trigger autohealer
   - `disk.alert` → Desktop notification
   - `healer.stuck` → Escalation (desktop notify + brain_state update)
   - `quality.degraded` → Log trend, desktop notification
   - `ecosystem.degraded` → Full health summary logged
   - Alle events → Cross-agent insight log (JSON)

---

## PASS 2: EKSEKVERING (Forbedret)

- [ ] Byg admiral_event_reactor.py
- [ ] Byg systemd service (Admiral Standard)
- [ ] Test: Publish test event → verify reactor modtager
- [ ] Test: Publish agent.error → verify reaktion
- [ ] Deploy: Start daemon, verify running
- [ ] Opdater Fleet CLI med ny agent
- [ ] Opdater template generator

---

## PASS 3: 7-DNA REVIEW (Optimeret)

- [ ] Lag 1: SELF-AWARE — Kender reactor sig selv?
- [ ] Lag 2: SELF-DOCUMENTING — Er alt logget?
- [ ] Lag 3: SELF-VERIFYING — Er alt testet?
- [ ] Lag 4: SELF-IMPROVING — Har vi laert noget?
- [ ] Lag 5: SELF-ARCHIVING — Kun essens bevaret?
- [ ] Lag 6: PREDICTIVE — Hvad er naeste skridt?
- [ ] Lag 7: SELF-OPTIMIZING — Kunne vi have gjort det bedre?

---

## 3-PASS STATUS

| Pass | Status | Score | Krav |
|------|--------|-------|------|
| 1: Planlaegning | COMPLETE | 8/10 | Baseline |
| 2: Eksekvering | IN PROGRESS | 0/10 | > Pass 1 |
| 3: 7-DNA Review | PENDING | 0/10 | > Pass 2 |
| **Total** | | **8/30** | **>= 24** |
