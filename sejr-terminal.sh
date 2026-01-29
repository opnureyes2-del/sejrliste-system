#!/bin/bash
# SEJRLISTE TERMINAL - Direkte forbindelse til systemet

cd "/home/rasmus/Desktop/sejrliste systemet"

echo "═══════════════════════════════════════════════════════════════════"
echo "     [VICTORY] SEJRLISTE TERMINAL - REALTIDS KONTROL"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "[LIST] KOMMANDOER:"
echo "   verify    - Kør verifikation"
echo "   track     - Opdater status"
echo "   predict   - Generér forudsigelser"
echo "   learn     - Lær mønstre"
echo "   archive   - Arkiver færdig sejr"
echo "   new NAME  - Opret ny sejr"
echo "   status    - Vis nuværende status"
echo "   web       - Start web app"
echo "   watch     - Følg ændringer i realtid"
echo ""

# Definer aliaser
alias verify="python3 scripts/auto_verify.py"
alias track="python3 scripts/auto_track.py"
alias predict="python3 scripts/auto_predict.py"
alias learn="python3 scripts/auto_learn.py"
alias archive="python3 scripts/auto_archive.py"
alias new="python3 scripts/generate_sejr.py --name"
alias status="python3 scripts/auto_track.py --status"
alias web="source venv/bin/activate && streamlit run web_app.py --server.port 8501"
alias watch="watch -n 2 'python3 scripts/auto_track.py --status'"

echo "═══════════════════════════════════════════════════════════════════"
echo "[TARGET] AKTIVE SEJR:"
ls -1 10_ACTIVE/ 2>/dev/null || echo "   (ingen aktive)"
echo ""
echo " ARKIVEREDE: $(ls -1 90_ARCHIVE/ 2>/dev/null | grep -v INDEX | wc -l) sejr"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Start interaktiv shell
exec bash --rcfile <(echo "
source ~/.bashrc
cd '/home/rasmus/Desktop/sejrliste systemet'
alias verify='python3 scripts/auto_verify.py'
alias track='python3 scripts/auto_track.py'
alias predict='python3 scripts/auto_predict.py'
alias learn='python3 scripts/auto_learn.py'
alias archive='python3 scripts/auto_archive.py'
alias new='python3 scripts/generate_sejr.py --name'
alias status='python3 scripts/auto_track.py --status'
alias web='source venv/bin/activate && streamlit run web_app.py --server.port 8501'
alias watch=\"watch -n 2 'python3 scripts/auto_track.py --status'\"
PS1='[VICTORY] sejrliste > '
")
