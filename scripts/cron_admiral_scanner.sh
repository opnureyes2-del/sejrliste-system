#!/bin/bash
set -euo pipefail
# WHAT: Daily Admiral Scanner cron wrapper
# WHY:  Generates morning briefing for Rasmus — know what needs fixing before asking
# WHEN: Daily at 07:50 (before health check at 07:55)

SYSTEM_PATH="/home/rasmus/Desktop/sejrliste systemet"
VENV_PYTHON="$SYSTEM_PATH/venv/bin/python3"
LOG_FILE="$SYSTEM_PATH/_CURRENT/cron_scanner.log"

# Run scanner
if "$VENV_PYTHON" "$SYSTEM_PATH/scripts/admiral_scanner.py" --brief >> "$LOG_FILE" 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M')] Scanner OK" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M')] Scanner found CRITICAL issues" >> "$LOG_FILE"
    # Desktop notification if available
    if command -v notify-send &>/dev/null; then
        notify-send -u critical "⚓ Admiral Scanner" "CRITICAL issues found! Check MORNING_BRIEFING.md"
    fi
fi

# Log rotation (keep last 100 lines)
if [ -f "$LOG_FILE" ] && [ "$(wc -l < "$LOG_FILE")" -gt 100 ]; then
    tail -50 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi
