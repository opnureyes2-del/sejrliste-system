#!/bin/bash
set -euo pipefail
# REALTIDS OVERVÅGNING - Følg med i ændringer

cd "/home/rasmus/Desktop/sejrliste systemet"

echo "[ERROR] REALTIDS OVERVÅGNING STARTET"
echo "   Tryk Ctrl+C for at stoppe"
echo ""

# Brug inotifywait til at overvåge ændringer
if command -v inotifywait &> /dev/null; then
    inotifywait -m -r -e modify,create,delete 10_ACTIVE/ 2>/dev/null | while read path action file; do
        echo "[$(date +%H:%M:%S)] $action: $path$file"
        # Opdater status automatisk
        python3 scripts/auto_track.py --status 2>/dev/null | head -5
        echo "---"
    done
else
    # Fallback til watch
    watch -n 2 -c 'echo "[VICTORY] SEJRLISTE STATUS (opdateres hvert 2. sekund)"
    echo "═══════════════════════════════════════════════"
    echo ""
    echo "[LIST] AKTIVE SEJR:"
    ls -1 10_ACTIVE/ 2>/dev/null || echo "   (ingen)"
    echo ""
    for sejr in 10_ACTIVE/*/; do
        if [ -d "$sejr" ]; then
            name=$(basename "$sejr")
            done=$(grep -c "^\- \[x\]" "$sejr/SEJR_LISTE.md" 2>/dev/null || echo 0)
            total=$(grep -c "^\- \[" "$sejr/SEJR_LISTE.md" 2>/dev/null || echo 0)
            echo "   $name: $done/$total"
        fi
    done
    echo ""
    echo " ARKIVEREDE: $(ls -1 90_ARCHIVE/ 2>/dev/null | grep -v INDEX | wc -l)"
    '
fi
