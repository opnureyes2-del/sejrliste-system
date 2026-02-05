#!/bin/bash
# ENV GUARD — Pre-commit hook that blocks .env files from being committed
# Install: Copy to .git/hooks/pre-commit in target repos
# Created: 2026-02-05 by SIKKERHED_ENV_KEYS_OPRYDNING sejr

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Check staged files for .env patterns
BLOCKED_FILES=$(git diff --cached --name-only | grep -iE '^\.(env|env\.local|env\.production|env\.development|env\.staging)$' || true)

# Also check for common credential files
CRED_FILES=$(git diff --cached --name-only | grep -iE '(credentials\.json|secrets\.json|\.pem$|\.key$|githubtoken|api.?key)' || true)

if [ -n "$BLOCKED_FILES" ]; then
    echo -e "${RED}⛔ ENV GUARD: Blokeret! Disse .env filer må IKKE committes:${NC}"
    echo "$BLOCKED_FILES" | while read f; do echo "   ❌ $f"; done
    echo ""
    echo "Fjern med: git reset HEAD <fil>"
    echo "Eller tilføj til .gitignore"
    exit 1
fi

if [ -n "$CRED_FILES" ]; then
    echo -e "${RED}⚠️  ENV GUARD: Mulige credentials opdaget:${NC}"
    echo "$CRED_FILES" | while read f; do echo "   ⚠️  $f"; done
    echo ""
    echo "Verificer at disse IKKE indeholder reelle credentials."
    echo "Bypass med: git commit --no-verify (IKKE ANBEFALET)"
    exit 1
fi

echo -e "${GREEN}✅ ENV GUARD: Ingen credential filer i commit${NC}"
