# _unused/ — Kode der ikke er i aktiv brug

Disse filer blev flyttet hertil ved oprydning 2026-01-28.

## Indhold

| Fil/Mappe | Oprindelse | Hvorfor ubrugt |
|-----------|-----------|----------------|
| `services/unified_sync.py` | Planlagt sync-service | Aldrig integreret i nogen script |
| `services/complete_timeline.py` | Planlagt timeline-generator | auto_live_status importerede den, men den var aldrig færdig |
| `services/active_workflow.py` | Planlagt workflow-engine | Aldrig importeret af noget |
| `desktop_app.py` | Ældre GTK desktop app | Erstattet af masterpiece.py og masterpiece_en.py |

## Kan de genbruges?

- **unified_sync.py** (26 KB) — Har ideer til sync-funktioner. Kan bruges som reference.
- **complete_timeline.py** (22 KB) — Har timeline-visualisering. Kan integreres i TUI-appen.
- **active_workflow.py** (11 KB) — Har workflow-state machine. Kan integreres.
- **desktop_app.py** (23 KB) — Gammel version. Ikke relevant længere.

## Regler

- Flyt IKKE filer tilbage uden at integrere dem ordentligt
- Hvis en fil genbruges, SLET den herfra
- Denne mappe er IKKE i .gitignore — den trackes stadig
