#!/bin/bash
#
# install_precommit_hook.sh — Install Admiral Pre-Commit Hook
# ============================================================
# Installs a pre-commit hook that runs verify_index_content_sync.py
# before allowing commits in the sejrliste systemet repo.
#
# Usage: bash install_precommit_hook.sh
#

set -euo pipefail

REPO_DIR="/home/rasmus/Desktop/sejrliste systemet"
HOOK_PATH="$REPO_DIR/.git/hooks/pre-commit"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERIFY_SCRIPT="$SCRIPT_DIR/verify_index_content_sync.py"

echo "Admiral Pre-Commit Hook Installer"
echo "================================="
echo ""

# Check if repo exists
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "[FAIL] Not a git repo: $REPO_DIR"
    echo "       Initialize with: git init"
    exit 1
fi

# Check if verify script exists
if [ ! -f "$VERIFY_SCRIPT" ]; then
    echo "[FAIL] Verify script not found: $VERIFY_SCRIPT"
    exit 1
fi

# Backup existing hook
if [ -f "$HOOK_PATH" ]; then
    backup="$HOOK_PATH.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$HOOK_PATH" "$backup"
    echo "[INFO] Existing hook backed up to: $backup"
fi

# Create hook
cat > "$HOOK_PATH" << 'HOOK_CONTENT'
#!/bin/bash
#
# Admiral Pre-Commit Hook
# Runs index-content sync verification before commit.
#

SCRIPT_DIR="$(cd "$(dirname "$0")/../../10_ACTIVE/KV1NT_ADMIRAL_PROTOCOLS_2026-01-29/scripts" 2>/dev/null && pwd)"
VERIFY_SCRIPT="$SCRIPT_DIR/verify_index_content_sync.py"

if [ -f "$VERIFY_SCRIPT" ]; then
    echo "[ADMIRAL] Running index-content sync verification..."

    # Run verification but don't block on warnings, only on failures
    output=$(python3 "$VERIFY_SCRIPT" 2>&1)
    exit_code=$?

    fail_count=$(echo "$output" | grep -c "\[FAIL\]" || true)

    if [ "$fail_count" -gt 0 ]; then
        echo ""
        echo "[ADMIRAL] BLOCKED: $fail_count critical issues found"
        echo "$output" | grep "\[FAIL\]" | head -5
        echo ""
        echo "Fix issues before committing, or use --no-verify to bypass."
        exit 1
    fi

    echo "[ADMIRAL] Pre-commit check passed"
fi

exit 0
HOOK_CONTENT

chmod +x "$HOOK_PATH"

echo "[OK] Pre-commit hook installed at: $HOOK_PATH"
echo "[OK] Hook will run verify_index_content_sync.py before each commit"
echo ""
echo "To test: cd '$REPO_DIR' && git commit --allow-empty -m 'test hook'"
echo "To bypass: git commit --no-verify -m 'message'"
