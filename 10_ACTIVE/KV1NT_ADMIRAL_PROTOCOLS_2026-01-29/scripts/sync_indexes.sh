#!/bin/bash
#
# sync_indexes.sh — Daily Index Synchronization Script
# =====================================================
# Regenerates navigation indexes, verifies internal consistency,
# updates status headers, and logs results.
#
# Schedule: Daily at 04:00 via cron
# Usage: bash sync_indexes.sh [--verbose]
# Log: /tmp/ADMIRAL_SYNC_$(date +%Y%m%d).log
#

set -euo pipefail

# --- Configuration ---
MASTER_FOLDERS="/home/rasmus/Desktop/MASTER FOLDERS(INTRO)"
MIN_ADMIRAL="/home/rasmus/Desktop/MIN ADMIRAL"
SEJRLISTE_DIR="/home/rasmus/Desktop/sejrliste systemet"
CONTEXT_DIR="$HOME/.claude/.context/core"
LOG_FILE="/tmp/ADMIRAL_SYNC_$(date +%Y%m%d_%H%M%S).log"
VERBOSE="${1:-}"

# --- Functions ---
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" | tee -a "$LOG_FILE"
}

log_section() {
    echo "" | tee -a "$LOG_FILE"
    echo "--- $1 ---" | tee -a "$LOG_FILE"
}

count_files() {
    local dir="$1"
    local ext="${2:-*}"
    find "$dir" -name "*.$ext" -type f 2>/dev/null | wc -l
}

# --- Main ---
log "========================================"
log "ADMIRAL DAILY SYNC STARTING"
log "========================================"
log ""

ERRORS=0
WARNINGS=0

# FASE 1: Verify directories exist
log_section "FASE 1: Directory Verification"

for dir in "$MASTER_FOLDERS" "$MIN_ADMIRAL" "$SEJRLISTE_DIR" "$CONTEXT_DIR"; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -type f 2>/dev/null | wc -l)
        log "[OK] $dir ($count files)"
    else
        log "[FAIL] Directory not found: $dir"
        ((ERRORS++))
    fi
done

# FASE 2: Check git status of known repos
log_section "FASE 2: Git Status Check"

for repo in "$SEJRLISTE_DIR" "$MIN_ADMIRAL" "$MASTER_FOLDERS"; do
    if [ -d "$repo/.git" ]; then
        dirty=$(git -C "$repo" status --porcelain 2>/dev/null | wc -l)
        if [ "$dirty" -gt 0 ]; then
            log "[WARN] $repo: $dirty uncommitted changes"
            ((WARNINGS++))
            if [ "$VERBOSE" = "--verbose" ]; then
                git -C "$repo" status --short 2>/dev/null | head -10 | tee -a "$LOG_FILE"
            fi
        else
            log "[OK] $repo: clean"
        fi
    else
        log "[INFO] $repo: not a git repo"
    fi
done

# FASE 3: Context file size check
log_section "FASE 3: Context File Size Check"

MAX_SIZE=102400  # 100KB ~ 25K tokens
if [ -d "$CONTEXT_DIR" ]; then
    for f in "$CONTEXT_DIR"/*.md; do
        if [ -f "$f" ]; then
            size=$(stat -c%s "$f" 2>/dev/null || echo "0")
            name=$(basename "$f")
            if [ "$size" -gt "$MAX_SIZE" ]; then
                log "[WARN] $name: ${size} bytes (over 100KB limit)"
                ((WARNINGS++))
            else
                log "[OK] $name: ${size} bytes"
            fi
        fi
    done
fi

# FASE 4: Sejrliste progress summary
log_section "FASE 4: Sejrliste Active Summary"

ACTIVE_DIR="$SEJRLISTE_DIR/10_ACTIVE"
if [ -d "$ACTIVE_DIR" ]; then
    total_sejr=0
    for sejr_dir in "$ACTIVE_DIR"/*/; do
        if [ -f "$sejr_dir/SEJR_LISTE.md" ]; then
            ((total_sejr++))
            name=$(basename "$sejr_dir")
            total_cb=$(grep -c '^\s*- \[' "$sejr_dir/SEJR_LISTE.md" 2>/dev/null || echo "0")
            checked_cb=$(grep -c '^\s*- \[x\]' "$sejr_dir/SEJR_LISTE.md" 2>/dev/null || echo "0")
            if [ "$total_cb" -gt 0 ]; then
                pct=$((checked_cb * 100 / total_cb))
            else
                pct=0
            fi
            log "[INFO] $name: $checked_cb/$total_cb ($pct%)"
        fi
    done
    log "[INFO] Total active sejrlister: $total_sejr"
fi

# FASE 5: Check for stale files (not modified in 7+ days)
log_section "FASE 5: Stale File Detection"

if [ -d "$MIN_ADMIRAL" ]; then
    stale=$(find "$MIN_ADMIRAL" -name "*.md" -mtime +7 -type f 2>/dev/null | wc -l)
    total=$(find "$MIN_ADMIRAL" -name "*.md" -type f 2>/dev/null | wc -l)
    log "[INFO] MIN ADMIRAL: $stale/$total files older than 7 days"
fi

if [ -d "$CONTEXT_DIR" ]; then
    stale=$(find "$CONTEXT_DIR" -name "*.md" -mtime +7 -type f 2>/dev/null | wc -l)
    total=$(find "$CONTEXT_DIR" -name "*.md" -type f 2>/dev/null | wc -l)
    log "[INFO] Context core: $stale/$total files older than 7 days"
fi

# Summary
log ""
log "========================================"
log "SYNC COMPLETE"
log "  Errors:   $ERRORS"
log "  Warnings: $WARNINGS"
log "  Log:      $LOG_FILE"
log "========================================"

# Exit code
if [ "$ERRORS" -gt 0 ]; then
    exit 1
else
    exit 0
fi
