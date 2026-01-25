# SEJR RULES - Obligatoriske Regler Per Sejr

**Formål:** Disse regler injiceres i model context når du arbejder på en sejr.
**Håndhævelse:** OBLIGATORISK - Ingen undtagelser.

---

## RULE 1: PHASE COMPLETION (Færdiggør Før Næste)

**ALDRIG** skip en phase. Hver phase SKAL være 100% komplet før næste starter.

```
FORBUDT:
- Starte PASS 2 før PASS 1 er 100%
- Skippe checkboxes du "kan tage senere"
- Lukke sejr uden FINAL VERIFICATION

TILLADT:
- Arbejde systematisk gennem hver checkbox
- Bede om pause og fortsætte senere (progress bevares)
- Opdele stor checkbox i mindre sub-tasks
```

---

## RULE 2: EVIDENCE-BASED COMPLETION (Bevis Alt)

**ALDRIG** mark en checkbox uden fysisk bevis.

```
FOR HVER CHECKBOX:
1. Udfør handlingen
2. Verificer resultatet (test, output, fil eksisterer)
3. Log beviset i AUTO_LOG.jsonl
4. FØRST DEREFTER marker checkbox

EKSEMPLER PÅ BEVIS:
- Fil oprettet: ls -la viser fil
- Test passed: pytest output
- Script virker: Faktisk output
- Build successful: Build log uden errors
```

---

## RULE 3: NO SILENT FAILURES (Rapportér Alt)

**ALDRIG** ignorer fejl eller fortsæt uden at dokumentere.

```
VED FEJL:
1. STOP med det samme
2. Dokumentér fejlen i AUTO_LOG.jsonl
3. Analysér root cause
4. Fix eller eskalér til bruger
5. Genoptag først når resolved

FORBUDT:
- "Det virker nok" antagelser
- Skip fejl og håb det fikser sig selv
- Skjule problemer fra bruger
```

---

## RULE 4: DNA LAG AWARENESS (Forstå Systemet)

Du arbejder i et 7-lag DNA system. KEND din rolle i hvert lag:

| DNA Lag | Dit Ansvar |
|---------|------------|
| 1. SELF-AWARE | Notér hvad du gør |
| 2. SELF-DOCUMENTING | Log ALT til AUTO_LOG.jsonl |
| 3. SELF-VERIFYING | Kør tests, verificer checkboxes |
| 4. SELF-IMPROVING | Notér patterns i PATTERNS.yaml |
| 5. SELF-ARCHIVING | Ekstrahér kun semantisk essens |
| 6. PREDICTIVE | Generér data-drevet NEXT.md |
| 7. SELF-OPTIMIZING | Altid 3 alternativer før bygning |

---

## RULE 5: TOKEN EFFICIENCY (Respektér Budgets)

Hvert DNA lag har et token budget. OVERHOLD dem.

Se `MODEL_CONSTRAINTS.yaml` for specifikke limits.

```
VED BUDGET OVERSKRIDELSE:
1. STOP umiddelbart
2. Rapportér til bruger
3. Vent på guidance
4. ALDRIG auto-opsummér for at spare tokens
```

---

## RULE 6: FOCUS LOCK (Ingen Distraktioner)

Når en sejr er aktiv, ER DET DIN ENESTE OPGAVE.

```
FORBUDT:
- Starte anden sejr før denne er arkiveret
- "Lige hurtigt" side-tasks
- Afvige fra plan uden bruger-godkendelse

TILLADT:
- Pause og genoptag samme sejr
- Bede bruger om afklaring
- Eskalere blockers
```

---

## RULE 7: SEMANTIC ARCHIVING (Bevar Essens)

Ved arkivering: ALDRIG auto-compact. Brug struktureret extraction.

```
BEVAR:
- Hvad lærte vi (patterns)
- Hvad kan genbruges (komponenter)
- Metrics (tid, checkboxes, score)
- Decision rationale (hvorfor valg)

FJERN:
- Process detaljer (hvordan vi kom derhen)
- Fejlforsøg (kun final solution)
- Verbose logs (kun semantisk summary)
```

---

## ADMIRAL VERIFICATION CHECKLIST

Før du afslutter NOGET arbejde på en sejr:

- [ ] Alle checkboxes har fysisk bevis
- [ ] AUTO_LOG.jsonl er opdateret
- [ ] Ingen skjulte fejl
- [ ] Token budget overholdt
- [ ] Focus maintained (ingen side-tracks)
- [ ] Klar til næste phase ELLER arkivering

---

**Disse regler er IKKE guidelines. De er KRAV.**
**Overtrædelse = Korrigering i rules.md = Permanent fix.**
