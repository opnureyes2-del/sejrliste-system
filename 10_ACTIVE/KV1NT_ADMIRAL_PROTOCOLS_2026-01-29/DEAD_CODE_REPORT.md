# Dead Code Scanner Report

**Generated:** 2026-01-30 00:34:33

```
======================================================================
ADMIRAL DEAD CODE SCANNER
Timestamp: 2026-01-30 00:34:33
======================================================================

--- sejrliste systemet ---
  Files scanned: 287
  Python: 66 | Markdown: 104 | Shell: 6
  Issues found: 290

  [ORPHAN_FILE] (24 items)
    [MEDIUM] 4_Statistik.py
         File: /home/rasmus/Desktop/sejrliste systemet/pages/4_Statistik.py
         File '4_Statistik.py' is never referenced by other files in sejrliste systemet
    [MEDIUM] sejr_list.py
         File: /home/rasmus/Desktop/sejrliste systemet/app/widgets/sejr_list.py
         File 'sejr_list.py' is never referenced by other files in sejrliste systemet
    [MEDIUM] visual_polish.py
         File: /home/rasmus/Desktop/sejrliste systemet/app/widgets/visual_polish.py
         File 'visual_polish.py' is never referenced by other files in sejrliste systemet
    [MEDIUM] progress_panel.py
         File: /home/rasmus/Desktop/sejrliste systemet/app/widgets/progress_panel.py
         File 'progress_panel.py' is never referenced by other files in sejrliste systemet
    [MEDIUM] context_sync.py
         File: /home/rasmus/Desktop/sejrliste systemet/app/integrations/context_sync.py
         File 'context_sync.py' is never referenced by other files in sejrliste systemet
    [MEDIUM] todo_sync.py
         File: /home/rasmus/Desktop/sejrliste systemet/app/integrations/todo_sync.py
         File 'todo_sync.py' is never referenced by other files in sejrliste systemet
    [MEDIUM] log_stream.py
         File: /home/rasmus/Desktop/sejrliste systemet/app/widgets/log_stream.py
         File 'log_stream.py' is never referenced by other files in sejrliste systemet
    [MEDIUM] 5_Indstillinger.py
         File: /home/rasmus/Desktop/sejrliste systemet/pages/5_Indstillinger.py
         File '5_Indstillinger.py' is never referenced by other files in sejrliste systemet
    [MEDIUM] start_web_en.sh
         File: /home/rasmus/Desktop/sejrliste systemet/start_web_en.sh
         File 'start_web_en.sh' is never referenced by other files in sejrliste systemet
    [MEDIUM] 1_Aktiv_Sejr.py
         File: /home/rasmus/Desktop/sejrliste systemet/pages/1_Aktiv_Sejr.py
         File '1_Aktiv_Sejr.py' is never referenced by other files in sejrliste systemet
    ... and 14 more

  [STALE_REFERENCE] (73 items)
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/README.md:26
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/WORKING_CONDITIONS_EN.md:19
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/INCOMPLETE_CHECK.md:17
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/MODEL_ONBOARDING_EN.md:174
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/MODEL_ONBOARDING_EN.md:180
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/MODEL_ONBOARDING_EN.md:331
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/ARBEJDSFORHOLD.md:19
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/INCOMPLETE_CHECK_EN.md:17
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/README_EN.md:26
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/sejrliste systemet/EXAMPLES_EN.md:11
         References non-existent path: /home/rasmus/Desktop/sejrliste
    ... and 63 more

  [UNUSED_FUNCTION] (149 items)
    [MEDIUM] print_box
         File: /home/rasmus/Desktop/sejrliste systemet/view.py:93
         Function 'print_box' defined but never called in this file
    [MEDIUM] run_app
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:830
         Function 'run_app' defined but never called in this file
    [MEDIUM] load_recent_logs
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:457
         Function 'load_recent_logs' defined but never called in this file
    [MEDIUM] action_dismiss
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:553
         Function 'action_dismiss' defined but never called in this file
    [MEDIUM] on_mount
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:607
         Function 'on_mount' defined but never called in this file
    [MEDIUM] action_toggle_help
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:673
         Function 'action_toggle_help' defined but never called in this file
    [MEDIUM] action_move_down
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:677
         Function 'action_move_down' defined but never called in this file
    [MEDIUM] action_move_up
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:684
         Function 'action_move_up' defined but never called in this file
    [MEDIUM] action_select_sejr
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:691
         Function 'action_select_sejr' defined but never called in this file
    [MEDIUM] action_switch_panel
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:704
         Function 'action_switch_panel' defined but never called in this file
    ... and 139 more

  [UNUSED_IMPORT] (44 items)
    [LOW] json
         File: /home/rasmus/Desktop/sejrliste systemet/pages/4_Statistik.py:8
         Import 'json' appears to be unused
    [LOW] datetime
         File: /home/rasmus/Desktop/sejrliste systemet/pages/1_Aktiv_Sejr.py:8
         Import 'datetime' appears to be unused
    [LOW] datetime
         File: /home/rasmus/Desktop/sejrliste systemet/pages/3_Ny_Sejr.py:8
         Import 'datetime' appears to be unused
    [LOW] annotations
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:23
         Import 'annotations' appears to be unused
    [LOW] os
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:24
         Import 'os' appears to be unused
    [LOW] sys
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:25
         Import 'sys' appears to be unused
    [LOW] asyncio
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:28
         Import 'asyncio' appears to be unused
    [LOW] Dict
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:32
         Import 'Dict' appears to be unused
    [LOW] Any
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:32
         Import 'Any' appears to be unused
    [LOW] Message
         File: /home/rasmus/Desktop/sejrliste systemet/app/sejr_app.py:46
         Import 'Message' appears to be unused
    ... and 34 more

--- MIN ADMIRAL ---
  Files scanned: 60
  Python: 5 | Markdown: 48 | Shell: 4
  Issues found: 27

  [STALE_REFERENCE] (21 items)
    [LOW] /home/rasmus/Desktop/MIN
         File: /home/rasmus/Desktop/MIN ADMIRAL/00_MASTER_INDEX.md:168
         References non-existent path: /home/rasmus/Desktop/MIN
    [LOW] /home/rasmus/Desktop/MIN
         File: /home/rasmus/Desktop/MIN ADMIRAL/00_MASTER_INDEX.md:171
         References non-existent path: /home/rasmus/Desktop/MIN
    [LOW] /home/rasmus/Desktop/MIN
         File: /home/rasmus/Desktop/MIN ADMIRAL/00_MASTER_INDEX.md:174
         References non-existent path: /home/rasmus/Desktop/MIN
    [LOW] /home/rasmus/Desktop/MASTER
         File: /home/rasmus/Desktop/MIN ADMIRAL/FOLDER_ARCHITECTURE.md:252
         References non-existent path: /home/rasmus/Desktop/MASTER
    [LOW] /home/rasmus/Desktop/MANUAL
         File: /home/rasmus/Desktop/MIN ADMIRAL/FOLDER_ARCHITECTURE.md:253
         References non-existent path: /home/rasmus/Desktop/MANUAL
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/MIN ADMIRAL/SYSTEM_CAPABILITIES.md:194
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/MIN ADMIRAL/SYSTEM_CAPABILITIES.md:215
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/MASTER
         File: /home/rasmus/Desktop/MIN ADMIRAL/SYSTEM_CAPABILITIES.md:434
         References non-existent path: /home/rasmus/Desktop/MASTER
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/MIN ADMIRAL/SYSTEM_CAPABILITIES.md:503
         References non-existent path: /home/rasmus/Desktop/sejrliste
    [LOW] /home/rasmus/Desktop/sejrliste
         File: /home/rasmus/Desktop/MIN ADMIRAL/SYSTEM_CAPABILITIES.md:506
         References non-existent path: /home/rasmus/Desktop/sejrliste
    ... and 11 more

  [UNUSED_IMPORT] (6 items)
    [LOW] os
         File: /home/rasmus/Desktop/MIN ADMIRAL/SCRIPTS/verify_victory.py:10
         Import 'os' appears to be unused
    [LOW] re
         File: /home/rasmus/Desktop/MIN ADMIRAL/SCRIPTS/verify_victory.py:11
         Import 're' appears to be unused
    [LOW] Optional
         File: /home/rasmus/Desktop/MIN ADMIRAL/SCRIPTS/verify_victory.py:16
         Import 'Optional' appears to be unused
    [LOW] os
         File: /home/rasmus/Desktop/MIN ADMIRAL/SCRIPTS/compliance_check.py:23
         Import 'os' appears to be unused
    [LOW] Dict
         File: /home/rasmus/Desktop/MIN ADMIRAL/SCRIPTS/verify_index_content_sync.py:24
         Import 'Dict' appears to be unused
    [LOW] Set
         File: /home/rasmus/Desktop/MIN ADMIRAL/SCRIPTS/split_docs_finder.py:22
         Import 'Set' appears to be unused

----------------------------------------------------------------------
TOTAL ISSUES: 317

OBLIGATORY QUESTIONS (Rule -39):
  1. What was the vision for each dead item?
  2. What worked before it became dead?
  3. What went wrong (why abandoned)?
  4. How do we do it right (revive or archive)?

ACTION: Review each item. Revive or archive. Never delete blindly.
----------------------------------------------------------------------
Generated by admiral_dead_code_scanner.py
```
