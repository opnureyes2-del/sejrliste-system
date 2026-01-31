#!/bin/bash
set -euo pipefail
# Cron wrapper for auto_learn — log rotation
cd "/home/rasmus/Desktop/sejrliste systemet"
venv/bin/python3 scripts/auto_learn.py 2>&1 | tail -50 > /tmp/sejrliste_learn.log
