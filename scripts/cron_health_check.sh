#!/bin/bash
set -euo pipefail
# Cron wrapper for health check — log rotation + desktop notification
cd "/home/rasmus/Desktop/sejrliste systemet"

# Run health check, keep only last 50 lines
venv/bin/python3 scripts/auto_health_check.py --repair --quiet 2>&1 | tail -50 > /tmp/sejrliste-health.log

# Desktop notification if failures found
if grep -q "\[FAIL\]" /tmp/sejrliste-health.log; then
    FAILS=$(grep -c "\[FAIL\]" /tmp/sejrliste-health.log)
    DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus" \
        notify-send -u critical "🚨 Sejrliste: $FAILS FEJL" \
        "$(grep '\[FAIL\]' /tmp/sejrliste-health.log | head -3)" 2>/dev/null
fi
