# SEJR RULES - Obligatoriske Regler Per Sejr

> Disse regler er OBLIGATORISKE når du arbejder på denne sejr.

## REGEL 1: EN TING AD GANGEN
- Færdiggør nuværende task HELT før du starter ny
- Ingen context switching
- Ingen "næsten færdig" - kun FÆRDIG

## REGEL 2: PHASE-LOCKED EXECUTION
- Du SKAL færdiggøre nuværende phase
- Ingen skip til næste phase
- Bevis completion før videre

## REGEL 3: TOKEN BUDGET
- Hold dig inden for DNA lag budget
- Haiku: 500-1000 tokens
- Sonnet: 1500 tokens
- Opus: 2000-4000 tokens

## REGEL 4: AUTO-LOG ALT
- Hver handling logges til AUTO_LOG.jsonl
- Ingen handling uden log
- Timestamp + action + details

## REGEL 5: VERIFICATION REQUIRED
- Kør auto_verify.py efter hver ændring
- Checkboxes SKAL matche virkelighed
- Scores SKAL være korrekte

## REGEL 6: GIT ON COMPLETE
- Commit når phase er færdig
- Push efter commit
- Verify remote matches local

## REGEL 7: NO COMPACTION
- Ingen auto-summarering
- Brug semantic archiving
- Bevar essens, ikke detaljer
