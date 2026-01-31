#!/usr/bin/env bash
set -euo pipefail
# ═══════════════════════════════════════════════════════════════
# start-web.sh — Streamlit Web App Launcher
# ═══════════════════════════════════════════════════════════════
#
# WHAT:  Starter Sejrliste web app (Streamlit) paa port 8501
# WHY:   Wrapper for systemd service (sejrliste-web.service)
# WHO:   Kaldt af: systemctl --user start sejrliste-web.service
#        Auto-start: ved login (WantedBy=default.target)
# HOW:   Bruger exec (erstatter shell-processen) saa systemd
#        kan tracke PID korrekt og genstarte ved crash
#
# ADGANG EFTER START:
#   Desktop:  http://localhost:8501
#   Telefon:  https://rog.tailc9c1c5.ts.net (Tailscale HTTPS)
#   Lokal:    http://10.168.6.233:8501 (samme WiFi)
#
# VIGTIG: Denne fil SKAL ligge i project root!
#   systemd ExecStart peger direkte paa denne fil.
#   Flyt den IKKE uden at opdatere sejrliste-web.service.
#
# Version: 3.0.0 | Opdateret: 2026-01-31
# ═══════════════════════════════════════════════════════════════

cd "/home/rasmus/Desktop/sejrliste systemet"
exec "./venv/bin/streamlit" run web_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true
