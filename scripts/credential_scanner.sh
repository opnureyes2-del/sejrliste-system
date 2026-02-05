#!/bin/bash
# ═══════════════════════════════════════════════════════════
# CREDENTIAL SCANNER — Automated weekly security audit
# Scans entire Desktop for exposed credentials
# Part of: SIKKERHED_ENV_KEYS_OPRYDNING Pass 3
# Install: Add to cron (weekly Sunday 05:00)
#   0 5 * * 0 bash ~/Desktop/sejrliste\ systemet/scripts/credential_scanner.sh
# Created: 2026-02-05
# ═══════════════════════════════════════════════════════════

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

LOG_DIR="$HOME/Desktop/sejrliste systemet/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/credential_scan_$(date +%Y-%m-%d).log"
SCAN_DIRS=(
    "$HOME/Desktop"
    "$HOME/Pictures/Admiral"
    "$HOME/.claude"
    "$HOME/.config"
)

FOUND=0
TOTAL=0

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

scan_env_files() {
    log "═══ SCAN 1: .env files ═══"
    for dir in "${SCAN_DIRS[@]}"; do
        while IFS= read -r -d '' f; do
            ((TOTAL++))
            log "  ⚠️  FOUND .env: $f ($(stat -c%s "$f") bytes)"
            ((FOUND++))
        done < <(find "$dir" -maxdepth 5 -name ".env" -o -name ".env.local" \
                 -o -name ".env.production" -o -name ".env.staging" \
                 -print0 2>/dev/null | grep -z '\.env' || true)
    done
}

scan_credential_patterns() {
    log "═══ SCAN 2: Credential patterns in files ═══"
    local patterns=(
        'sk-proj-[A-Za-z0-9]'     # OpenAI keys
        'sk-ant-[A-Za-z0-9]'       # Anthropic keys
        'gsk_[A-Za-z0-9]'          # Groq keys
        'BSA[A-Za-z0-9]{8,}'       # Brave keys
        'hf_[A-Za-z0-9]'           # HuggingFace tokens
        'ghp_[A-Za-z0-9]'          # GitHub PATs
        'PRIVATE KEY'               # PEM private keys
    )

    for dir in "${SCAN_DIRS[@]}"; do
        for pattern in "${patterns[@]}"; do
            while IFS= read -r match; do
                # Skip .git internals, node_modules, .env files (already scanned)
                if echo "$match" | grep -qE '(\.git/|node_modules/|\.env|__pycache__|\.pyc)'; then
                    continue
                fi
                ((TOTAL++))
                local file_path="${match%%:*}"
                log "  ⚠️  CREDENTIAL PATTERN in: $file_path (pattern: ${pattern:0:10}...)"
                ((FOUND++))
            done < <(grep -rn "$pattern" "$dir" --include="*.md" --include="*.txt" \
                     --include="*.json" --include="*.yaml" --include="*.yml" \
                     --include="*.sh" --include="*.py" --include="*.js" \
                     --include="*.ts" 2>/dev/null | head -20 || true)
        done
    done
}

scan_git_staged() {
    log "═══ SCAN 3: Git repos — .env in history ═══"
    for dir in "${SCAN_DIRS[@]}"; do
        while IFS= read -r -d '' gitdir; do
            local repo="${gitdir%/.git}"
            local env_in_history
            env_in_history=$(cd "$repo" && git log --all --diff-filter=A --name-only --format="" 2>/dev/null | grep -iE '\.env' | head -5 || true)
            if [ -n "$env_in_history" ]; then
                ((TOTAL++))
                log "  ⚠️  .env in git HISTORY: $repo"
                log "      Files: $env_in_history"
                ((FOUND++))
            fi
        done < <(find "$dir" -maxdepth 4 -name ".git" -type d -print0 2>/dev/null)
    done
}

# ─── MAIN ───
log "═══════════════════════════════════════════"
log "  CREDENTIAL SCANNER — Weekly Audit"
log "  Scanning ${#SCAN_DIRS[@]} directories"
log "═══════════════════════════════════════════"

scan_env_files
scan_credential_patterns
scan_git_staged

log ""
log "═══════════════════════════════════════════"
log "  RESULTS: $FOUND findings in $TOTAL checks"
if [ "$FOUND" -eq 0 ]; then
    log "  ✅ CLEAN — No exposed credentials found"
else
    log "  ⚠️  ACTION NEEDED — Review $LOG_FILE"
fi
log "═══════════════════════════════════════════"

# Send desktop notification if issues found
if [ "$FOUND" -gt 0 ] && command -v notify-send &>/dev/null; then
    DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus \
    notify-send -u critical "🔒 Credential Scanner" "$FOUND exposed credentials found! Check $LOG_FILE"
fi

exit 0
