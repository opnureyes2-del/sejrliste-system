#!/bin/bash
# GIT COMPLIANCE CHECKER — Admiral Standard
# Checker ALLE kendte git repos for: dirty files, unpushed commits, behind remote
# Kør: bash scripts/git_compliance_checker.sh
# Cron: */30 * * * * bash /home/rasmus/Desktop/sejrliste\ systemet/scripts/git_compliance_checker.sh --quiet
# Oprettet: 2026-02-05 af Kv1nt (DOKUMENTATION_TOTAL_ORDEN Pass 3)

REPOS=(
  "/home/rasmus/Desktop/MANUAL I TILFÆLDE AF HJERNESKADE"
  "/home/rasmus/Desktop/MIN ADMIRAL"
  "/home/rasmus/Desktop/ELLE.md"
  "/home/rasmus/Desktop/INTRO FOLDER SYSTEM"
  "/home/rasmus/Desktop/MASTER FOLDERS(INTRO)"
  "/home/rasmus/Desktop/sejrliste systemet"
  "/home/rasmus/Desktop/projekts/projects/integration-bridge"
  "/home/rasmus/Desktop/projekts/projects/commander-and-agent"
  "/home/rasmus/Desktop/projekts/projects/kommandor-og-agenter"
  "/home/rasmus/Desktop/projekts/projects/lib-admin"
  "/home/rasmus/Desktop/projekts/projects/cosmic-library"
  "/home/rasmus/Desktop/projekts/projects/cirkelline-consulting"
  "/home/rasmus/Desktop/projekts/projects/commando-center"
  "/home/rasmus/Pictures/Admiral"
)

QUIET=false
[[ "$1" == "--quiet" ]] && QUIET=true

TOTAL=0
DIRTY=0
AHEAD=0
BEHIND=0
PROBLEMS=()

for repo in "${REPOS[@]}"; do
  [ -d "$repo/.git" ] || continue
  TOTAL=$((TOTAL + 1))
  name=$(basename "$repo")

  cd "$repo" 2>/dev/null || continue

  # Check dirty
  dirty_count=$(git status --porcelain 2>/dev/null | wc -l)
  if [ "$dirty_count" -gt 0 ]; then
    DIRTY=$((DIRTY + 1))
    PROBLEMS+=("⚠️  $name: $dirty_count dirty files")
  fi

  # Check ahead (unpushed)
  branch=$(git branch --show-current 2>/dev/null)
  ahead_count=$(git log "origin/$branch..HEAD" --oneline 2>/dev/null | wc -l)
  if [ "$ahead_count" -gt 0 ]; then
    AHEAD=$((AHEAD + 1))
    PROBLEMS+=("📤 $name: $ahead_count unpushed commits")
  fi

  # Check behind (needs pull)
  git fetch --quiet 2>/dev/null
  behind_count=$(git log "HEAD..origin/$branch" --oneline 2>/dev/null | wc -l)
  if [ "$behind_count" -gt 0 ]; then
    BEHIND=$((BEHIND + 1))
    PROBLEMS+=("📥 $name: $behind_count behind remote")
  fi
done

# Calculate score
CLEAN=$((TOTAL - DIRTY - AHEAD - BEHIND))
ISSUES=${#PROBLEMS[@]}

if [ "$QUIET" = true ]; then
  # Quiet mode: only output if problems found
  if [ "$ISSUES" -gt 0 ]; then
    notify-send "⚠️ Admiral Git Compliance" "$ISSUES issues in $TOTAL repos" 2>/dev/null
    echo "[$(date '+%Y-%m-%d %H:%M')] GIT COMPLIANCE: $ISSUES issues found"
    for p in "${PROBLEMS[@]}"; do
      echo "  $p"
    done
  fi
else
  # Full output
  echo "═══════════════════════════════════════════════"
  echo "  ADMIRAL GIT COMPLIANCE CHECK"
  echo "  $(date '+%Y-%m-%d %H:%M:%S')"
  echo "═══════════════════════════════════════════════"
  echo ""
  echo "  Repos scanned:  $TOTAL"
  echo "  Clean:          $((TOTAL - DIRTY))"
  echo "  Dirty:          $DIRTY"
  echo "  Unpushed:       $AHEAD"
  echo "  Behind:         $BEHIND"
  echo ""

  if [ "$ISSUES" -eq 0 ]; then
    echo "  ✅ ALL REPOS COMPLIANT"
  else
    echo "  ⚠️  $ISSUES ISSUES FOUND:"
    echo ""
    for p in "${PROBLEMS[@]}"; do
      echo "  $p"
    done
  fi
  echo ""
  echo "═══════════════════════════════════════════════"
fi

exit $ISSUES
