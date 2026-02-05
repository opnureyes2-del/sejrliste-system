#!/bin/bash
# DOCUMENTATION FRESHNESS CHECKER — Admiral Standard
# Checker kritiske dokumenter for forældelse (>7 dage siden ændring)
# Kør: bash scripts/doc_freshness_checker.sh
# Cron: 0 8 * * 1 bash /home/rasmus/Desktop/sejrliste\ systemet/scripts/doc_freshness_checker.sh
# Oprettet: 2026-02-05 af Kv1nt (DOKUMENTATION_TOTAL_ORDEN Pass 3)

CRITICAL_DOCS=(
  "/home/rasmus/Desktop/MASTER FOLDERS(INTRO)/00_UNIFIED_SYSTEM_DASHBOARD.md|Unified Dashboard"
  "/home/rasmus/Desktop/MASTER FOLDERS(INTRO)/I5_ADMIRAL_REALTIME_ALERTS.md|I5 Alerts"
  "/home/rasmus/Desktop/MASTER FOLDERS(INTRO)/FAMILY_API_REFERENCE.md|API Reference"
  "/home/rasmus/Desktop/projekts/projects/CLAUDE.md|Projekts CLAUDE.md"
  "/home/rasmus/.claude/.context/core/session.md|Session Context"
  "/home/rasmus/.claude/.context/core/projects.md|Projects Context"
  "/home/rasmus/Desktop/MANUAL I TILFÆLDE AF HJERNESKADE/00_START_HER.md|Recovery Manual"
  "/home/rasmus/Desktop/MIN ADMIRAL/00_MASTER_INDEX.md|Admiral Master Index"
)

STALE_DAYS=7
NOW=$(date +%s)
STALE=()
FRESH=()

for entry in "${CRITICAL_DOCS[@]}"; do
  IFS='|' read -r filepath label <<< "$entry"

  if [ ! -f "$filepath" ]; then
    STALE+=("❌ $label: FIL MANGLER")
    continue
  fi

  mod_time=$(stat -c %Y "$filepath" 2>/dev/null)
  if [ -z "$mod_time" ]; then
    STALE+=("❓ $label: Kan ikke læse dato")
    continue
  fi

  age_days=$(( (NOW - mod_time) / 86400 ))

  if [ "$age_days" -gt "$STALE_DAYS" ]; then
    STALE+=("⚠️  $label: $age_days dage gammel")
  else
    FRESH+=("✅ $label: $age_days dage")
  fi
done

ISSUES=${#STALE[@]}

echo "═══════════════════════════════════════════════"
echo "  ADMIRAL DOCUMENTATION FRESHNESS CHECK"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Stale threshold: $STALE_DAYS dage"
echo "═══════════════════════════════════════════════"
echo ""

if [ ${#FRESH[@]} -gt 0 ]; then
  echo "  FRISKE DOKUMENTER:"
  for f in "${FRESH[@]}"; do
    echo "  $f"
  done
  echo ""
fi

if [ "$ISSUES" -gt 0 ]; then
  echo "  ⚠️  FORÆLDEDE DOKUMENTER ($ISSUES):"
  for s in "${STALE[@]}"; do
    echo "  $s"
  done
  echo ""
  notify-send "⚠️ Admiral Doc Freshness" "$ISSUES dokumenter er forældede (>$STALE_DAYS dage)" 2>/dev/null
else
  echo "  ✅ ALLE KRITISKE DOKUMENTER ER FRISKE"
fi

echo ""
echo "═══════════════════════════════════════════════"

exit $ISSUES
