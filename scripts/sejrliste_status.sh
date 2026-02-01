#!/usr/bin/env bash
# ============================================================================
# SEJRLISTE STATUS — Unified system overview
# Shows: app status, URLs, active sejr, patterns, learning stats
# ============================================================================

set -euo pipefail

SYSTEM_PATH="/home/rasmus/Desktop/sejrliste systemet"
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}================================================================${NC}"
echo -e "${BOLD}           SEJRLISTE SYSTEM — STATUS OVERSIGT${NC}"
echo -e "${BOLD}================================================================${NC}"
echo ""

# --- SERVICES ---
echo -e "${BOLD}SERVICES${NC}"
echo "--------"

# Web app (systemd)
if systemctl --user is-active sejrliste-web.service &>/dev/null; then
    echo -e "  Web App (Streamlit):  ${GREEN}RUNNING${NC} (systemd auto-start)"
else
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8501/ 2>/dev/null | grep -q "200"; then
        echo -e "  Web App (Streamlit):  ${YELLOW}RUNNING (manual)${NC}"
    else
        echo -e "  Web App (Streamlit):  ${RED}STOPPED${NC}"
    fi
fi

# GTK4 app
if pgrep -f "masterpiece" &>/dev/null; then
    echo -e "  GTK4 Desktop App:     ${GREEN}RUNNING${NC}"
else
    echo -e "  GTK4 Desktop App:     ${BLUE}READY (launch from desktop)${NC}"
fi

echo ""

# --- ACCESS URLS ---
echo -e "${BOLD}ACCESS${NC}"
echo "------"
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
echo "  Desktop:   http://localhost:8501"
echo "  Phone:     http://${LOCAL_IP}:8501"

# Check Tailscale
if command -v tailscale &>/dev/null; then
    TS_IP=$(tailscale ip -4 2>/dev/null || echo "not connected")
    echo "  Anywhere:  http://${TS_IP}:8501 (Tailscale)"
else
    echo -e "  Anywhere:  ${YELLOW}Install Tailscale for remote access${NC}"
fi

echo ""

# --- ACTIVE SEJR ---
echo -e "${BOLD}ACTIVE SEJR${NC}"
echo "-----------"
ACTIVE_DIR="${SYSTEM_PATH}/10_ACTIVE"
if [ -d "$ACTIVE_DIR" ]; then
    active_count=0
    for sejr_dir in "$ACTIVE_DIR"/*/; do
        [ -d "$sejr_dir" ] || continue
        sejr_name=$(basename "$sejr_dir")
        status_file="${sejr_dir}STATUS.yaml"
        if [ -f "$status_file" ]; then
            score=$(grep "total_score:" "$status_file" 2>/dev/null | head -1 | awk '{print $2}' || echo "0")
            pass=$(grep "current_pass:" "$status_file" 2>/dev/null | head -1 | awk '{print $2}' || echo "1")
            echo "  ${sejr_name}"
            echo "    Pass: ${pass}/3 | Score: ${score}/30"
        else
            echo "  ${sejr_name} (no STATUS.yaml)"
        fi
        active_count=$((active_count + 1))
    done
    if [ "$active_count" -eq 0 ]; then
        echo "  (ingen aktive sejr)"
    fi
else
    echo "  (10_ACTIVE/ not found)"
fi

echo ""

# --- ARCHIVE STATS ---
echo -e "${BOLD}ARCHIVE${NC}"
echo "-------"
ARCHIVE_DIR="${SYSTEM_PATH}/90_ARCHIVE"
if [ -d "$ARCHIVE_DIR" ]; then
    archive_count=$(find "$ARCHIVE_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
    grand_count=$(find "$ARCHIVE_DIR" -name "STATUS.yaml" -exec grep -l "total_score: [2-9][7-9]\|total_score: 30" {} \; 2>/dev/null | wc -l)
    echo "  Archived: ${archive_count} sejr"
    echo "  Grand Admirals: ${grand_count}"
fi

echo ""

# --- LEARNING ---
echo -e "${BOLD}LEARNING (DNA Layer 7)${NC}"
echo "---------------------"
PATTERNS_FILE="${SYSTEM_PATH}/_CURRENT/PATTERNS.json"
if [ -f "$PATTERNS_FILE" ]; then
    total=$(python3 -c "import json; d=json.load(open('${PATTERNS_FILE}')); print(d.get('system',{}).get('total_patterns',0))" 2>/dev/null || echo "?")
    applied=$(python3 -c "import json; d=json.load(open('${PATTERNS_FILE}')); ps=d.get('learned_patterns',[]); print(sum(1 for p in ps if p.get('applied_count',0)>0))" 2>/dev/null || echo "?")
    last=$(python3 -c "import json; d=json.load(open('${PATTERNS_FILE}')); print(d.get('system',{}).get('last_learned','?'))" 2>/dev/null || echo "?")
    echo "  Patterns: ${total} total, ${applied} applied"
    echo "  Last learned: ${last}"
    echo "  Feedback loop: CLOSED (generate_sejr reads patterns)"
    # Check cron
    if crontab -l 2>/dev/null | grep -q "auto_learn"; then
        echo -e "  Auto-learn cron: ${GREEN}ACTIVE (daily 08:00)${NC}"
    else
        echo -e "  Auto-learn cron: ${RED}NOT SET${NC}"
    fi
else
    echo "  PATTERNS.json not found"
fi

# --- ADMIRAL SCANNER BRIEFING ---
echo -e "${BOLD}ADMIRAL SCANNER${NC}"
echo "---------------"
BRIEFING_FILE="${SYSTEM_PATH}/_CURRENT/MORNING_BRIEFING.md"
if [ -f "$BRIEFING_FILE" ]; then
    briefing_age=$(( ($(date +%s) - $(stat -c %Y "$BRIEFING_FILE")) / 3600 ))
    critical=$(grep -c "🔴" "$BRIEFING_FILE" 2>/dev/null || echo "0")
    medium=$(grep -c "🟡" "$BRIEFING_FILE" 2>/dev/null || echo "0")
    echo "  Last scan: ${briefing_age}h ago"
    if [ "$critical" -gt 1 ]; then
        echo -e "  ${RED}${critical} CRITICAL issues across systems${NC}"
    fi
    if [ "$medium" -gt 1 ]; then
        echo -e "  ${YELLOW}${medium} MEDIUM issues across systems${NC}"
    fi
    if [ "$critical" -le 1 ] && [ "$medium" -le 1 ]; then
        echo -e "  ${GREEN}All systems healthy${NC}"
    fi
    echo "  Full briefing: cat _CURRENT/MORNING_BRIEFING.md"
else
    echo -e "  ${YELLOW}No briefing yet — run: python3 scripts/admiral_scanner.py${NC}"
fi
if crontab -l 2>/dev/null | grep -q "admiral_scanner"; then
    echo -e "  Scanner cron: ${GREEN}ACTIVE (daily 07:50)${NC}"
else
    echo -e "  Scanner cron: ${RED}NOT SET${NC}"
fi

echo ""
echo -e "${BOLD}================================================================${NC}"
echo -e "  ${BOLD}sejrliste${NC} — run this command anytime for status"
echo -e "${BOLD}================================================================${NC}"
echo ""
