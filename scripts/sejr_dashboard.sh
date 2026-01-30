#!/bin/bash
# ============================================================================
# SEJRLISTE ENFORCEMENT DASHBOARD
# ============================================================================
# A one-shot formatted terminal display showing the complete state of
# the Sejrliste System: active tasks, archive stats, enforcement status,
# and next recommended actions.
#
# Usage: sejrstatus  (via symlink)
#    or: bash scripts/sejr_dashboard.sh
#
# No dependencies beyond bash + standard coreutils (grep, wc, find, date, stat)
# ============================================================================

set -euo pipefail

# ── Base path ────────────────────────────────────────────────────────────────
BASE="/home/rasmus/Desktop/sejrliste systemet"
ACTIVE_DIR="$BASE/10_ACTIVE"
ARCHIVE_DIR="$BASE/90_ARCHIVE"
CURRENT_DIR="$BASE/_CURRENT"

# ── ANSI Color Codes ────────────────────────────────────────────────────────
RST=$'\033[0m'
BOLD=$'\033[1m'
DIM=$'\033[2m'

# Foreground
GREEN=$'\033[0;32m'
WHITE=$'\033[0;37m'

# Bold foreground
BRED=$'\033[1;31m'
BGREEN=$'\033[1;32m'
BYELLOW=$'\033[1;33m'
BBLUE=$'\033[1;34m'
BMAGENTA=$'\033[1;35m'
BCYAN=$'\033[1;36m'
BWHITE=$'\033[1;37m'

# Background accents
BG_GREEN=$'\033[42m'
BG_RED=$'\033[41m'

# ── Terminal width detection ─────────────────────────────────────────────────
COLS=$(tput cols 2>/dev/null || echo 80)
if [ "$COLS" -gt 120 ]; then
    COLS=120
fi

# ── Helper functions ─────────────────────────────────────────────────────────

hr() {
    local char="${1:--}"
    local color="${2:-$DIM}"
    printf "%s" "$color"
    printf '%*s' "$COLS" '' | tr ' ' "$char"
    printf "%s\n" "$RST"
}

center() {
    local text="$1"
    local color="${2:-$RST}"
    local len=${#text}
    local pad=$(( (COLS - len) / 2 ))
    [ "$pad" -lt 0 ] && pad=0
    printf "%*s%s%s%s\n" "$pad" "" "$color" "$text" "$RST"
}

section_header() {
    local title="$1"
    local icon="${2:-}"
    echo ""
    hr "=" "$BCYAN"
    printf "  %s%s  %s%s\n" "$BCYAN" "$icon" "$title" "$RST"
    hr "=" "$BCYAN"
}

subsection() {
    local title="$1"
    printf "\n  %s%s%s%s\n" "$BOLD" "$WHITE" "$title" "$RST"
    printf "  %s" "$DIM"
    printf '%*s' $((COLS - 4)) '' | tr ' ' '-'
    printf "%s\n" "$RST"
}

# Read a value from a YAML file — matches first occurrence of key at line start
# (ignoring leading whitespace). Returns trimmed value without quotes.
yaml_val() {
    local file="$1"
    local key="$2"
    local default="${3:-}"
    if [ -f "$file" ]; then
        local val
        val=$(grep -m1 "^[[:space:]]*${key}:" "$file" 2>/dev/null \
            | sed 's/^[^:]*:[[:space:]]*//' \
            | sed 's/^["'"'"']//;s/["'"'"']$//' \
            | tr -d '\r' || true)
        val=$(echo "$val" | xargs 2>/dev/null || echo "$val")  # trim whitespace
        if [ -n "$val" ] && [ "$val" != "null" ] && [ "$val" != '""' ] && [ "$val" != "''" ]; then
            echo "$val"
        else
            echo "$default"
        fi
    else
        echo "$default"
    fi
}

# Extract the 3-pass total score from an archive folder.
# Uses the highest reliable score from all available sources.
# Rationale: some ARCHIVE_METADATA files have stale scores from before bug fixes.
get_archive_score() {
    local dir="$1"
    local meta="$dir/ARCHIVE_METADATA.yaml"
    local status="$dir/STATUS.yaml"

    local score_meta=0
    local score_status=0
    local score_passes=0

    # Source 1: ARCHIVE_METADATA.yaml total_score
    if [ -f "$meta" ]; then
        score_meta=$(safe_int "$(yaml_val "$meta" "total_score" "0")")
    fi

    # Source 2: STATUS.yaml total_score (cap at 30 — some have cumulative points)
    if [ -f "$status" ]; then
        score_status=$(safe_int "$(yaml_val "$status" "total_score" "0")")
        [ "$score_status" -gt 30 ] && score_status=30

        # Source 3: Sum of pass scores from STATUS.yaml
        local p1 p2 p3
        p1=$(safe_int "$(yaml_val "$status" "pass_1_score" "0")")
        p2=$(safe_int "$(yaml_val "$status" "pass_2_score" "0")")
        p3=$(safe_int "$(yaml_val "$status" "pass_3_score" "0")")
        score_passes=$((p1 + p2 + p3))
        [ "$score_passes" -gt 30 ] && score_passes=30
    fi

    # Cap metadata at 30 too
    [ "$score_meta" -gt 30 ] && score_meta=30

    # Use the highest valid score (handles stale metadata from pre-fix archives)
    local best="$score_meta"
    [ "$score_status" -gt "$best" ] && best="$score_status"
    [ "$score_passes" -gt "$best" ] && best="$score_passes"

    echo "$best"
}

# Derive rank from score when YAML rank is missing or unreliable
rank_from_score() {
    local score="$1"
    if [ "$score" -ge 27 ]; then
        echo "GRAND ADMIRAL"
    elif [ "$score" -ge 24 ]; then
        echo "ADMIRAL"
    elif [ "$score" -ge 18 ]; then
        echo "KAPTAJN"
    elif [ "$score" -ge 12 ]; then
        echo "OFFICER"
    else
        echo "KADET"
    fi
}

# Color a rank string appropriately
color_rank() {
    local rank="$1"
    case "$rank" in
        *GRAND*ADMIRAL*|*GRAND_ADMIRAL*)
            printf "%s%s %s %s" "$BG_GREEN" "$BWHITE" "$rank" "$RST" ;;
        *ADMIRAL*)
            printf "%s%s%s" "$BGREEN" "$rank" "$RST" ;;
        *KAPTAJN*|*CAPTAIN*)
            printf "%s%s%s" "$BCYAN" "$rank" "$RST" ;;
        *OFFICER*)
            printf "%s%s%s" "$BBLUE" "$rank" "$RST" ;;
        *KADET*)
            printf "%s%s%s" "$BYELLOW" "$rank" "$RST" ;;
        *REKRUT*|*RECRUIT*)
            printf "%s%s%s" "$BRED" "$rank" "$RST" ;;
        *)
            printf "%s%s%s" "$WHITE" "$rank" "$RST" ;;
    esac
}

# Color a status string
color_status() {
    local status="$1"
    case "$status" in
        *DONE*|*COMPLETE*|*ARKIVERET*|*ARCHIVED*|*pass_3_complete*)
            printf "%s%s%s" "$BGREEN" "$status" "$RST" ;;
        *PROGRESS*|*PENDING*|*IN_PROGRESS*|*pass_1*|*pass_2*)
            printf "%s%s%s" "$BYELLOW" "$status" "$RST" ;;
        *BLOCK*|*FAIL*|*ERROR*|*BLOKERET*)
            printf "%s%s%s" "$BRED" "$status" "$RST" ;;
        *)
            printf "%s%s%s" "$WHITE" "$status" "$RST" ;;
    esac
}

# Progress bar: progress_bar <done> <total> <width>
progress_bar() {
    local done="${1:-0}"
    local total="${2:-1}"
    local width="${3:-30}"

    [ "$total" -eq 0 ] && total=1
    local pct=$(( done * 100 / total ))
    local filled=$(( done * width / total ))
    local empty=$(( width - filled ))

    local color="$BRED"
    [ "$pct" -ge 25 ] && color="$BYELLOW"
    [ "$pct" -ge 50 ] && color="$BCYAN"
    [ "$pct" -ge 75 ] && color="$BBLUE"
    [ "$pct" -ge 100 ] && color="$BGREEN"

    printf "%s[" "$color"
    [ "$filled" -gt 0 ] && printf '%*s' "$filled" '' | tr ' ' '#'
    [ "$empty" -gt 0 ] && printf '%*s' "$empty" '' | tr ' ' '.'
    printf "]%s %s%3d%%%s" "$RST" "$BOLD" "$pct" "$RST"
}

# Safe integer from string (strip non-numeric)
safe_int() {
    local val="$1"
    val=$(echo "$val" | tr -dc '0-9')
    [ -z "$val" ] && val=0
    echo "$val"
}

# ── Gather data ──────────────────────────────────────────────────────────────
NOW=$(date '+%Y-%m-%d %H:%M:%S')
NOW_EPOCH=$(date +%s)

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          RENDER DASHBOARD                                ║
# ╚════════════════════════════════════════════════════════════════════════════╝

clear 2>/dev/null || true
echo ""

# ── HEADER ───────────────────────────────────────────────────────────────────
hr "=" "$BMAGENTA"
echo ""
center "S E J R L I S T E   S Y S T E M" "$BWHITE"
center "ENFORCEMENT DASHBOARD" "$BCYAN"
echo ""
printf "  %sTimestamp: %s%s%s" "$DIM" "$RST$WHITE" "$NOW" "$RST"
printf "    %sSystem: %s%sACTIVE%s" "$DIM" "$RST" "$BGREEN" "$RST"

# Check DNA version
DNA_VERSION=$(yaml_val "$BASE/DNA.yaml" "version" "?.?.?")
printf "    %sDNA: %s%sv%s%s\n" "$DIM" "$RST" "$WHITE" "$DNA_VERSION" "$RST"

echo ""
hr "=" "$BMAGENTA"


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: ACTIVE SEJRLISTER
# ══════════════════════════════════════════════════════════════════════════════

section_header "ACTIVE SEJRLISTER" ">>>"

if [ -d "$ACTIVE_DIR" ]; then
    active_count=0
    for sejr_dir in "$ACTIVE_DIR"/*/; do
        [ ! -d "$sejr_dir" ] && continue
        active_count=$((active_count + 1))

        sejr_name=$(basename "$sejr_dir")
        status_file="$sejr_dir/STATUS.yaml"
        sejr_file="$sejr_dir/SEJR_LISTE.md"

        # Extract data from STATUS.yaml
        total_score=$(safe_int "$(yaml_val "$status_file" "total_score" "0")")
        rank=$(yaml_val "$status_file" "rank" "")
        current_pass=$(safe_int "$(yaml_val "$status_file" "current_pass" "0")")
        status=$(yaml_val "$status_file" "status" "unknown")
        can_archive=$(yaml_val "$status_file" "can_archive" "false")
        archive_blocker=$(yaml_val "$status_file" "archive_blocker" "")
        required_score=$(safe_int "$(yaml_val "$status_file" "required_score" "24")")
        tests_passed=$(safe_int "$(yaml_val "$status_file" "tests_passed" "0")")
        tests_required=$(safe_int "$(yaml_val "$status_file" "tests_required" "5")")

        # Cap score at 30 for active too
        [ "$total_score" -gt 30 ] && total_score=30

        # Derive rank from score if empty
        if [ -z "$rank" ] || [ "$rank" = "UNKNOWN" ]; then
            rank=$(rank_from_score "$total_score")
        fi

        # Pass scores
        p1_score=$(safe_int "$(yaml_val "$status_file" "pass_1_score" "0")")
        p1_pct=$(safe_int "$(yaml_val "$status_file" "pass_1_pct" "0")")
        p1_done=$(yaml_val "$status_file" "pass_1_complete" "false")
        p2_score=$(safe_int "$(yaml_val "$status_file" "pass_2_score" "0")")
        p2_pct=$(safe_int "$(yaml_val "$status_file" "pass_2_pct" "0")")
        p2_done=$(yaml_val "$status_file" "pass_2_complete" "false")
        p3_score=$(safe_int "$(yaml_val "$status_file" "pass_3_score" "0")")
        p3_pct=$(safe_int "$(yaml_val "$status_file" "pass_3_pct" "0")")
        p3_done=$(yaml_val "$status_file" "pass_3_complete" "false")

        # Count checkboxes from SEJR_LISTE.md
        cb_total=0
        cb_done=0
        if [ -f "$sejr_file" ]; then
            cb_total=$(grep -c '^\- \[' "$sejr_file" 2>/dev/null || true)
            cb_total=$(safe_int "$cb_total")
            cb_done=$(grep -c '^\- \[x\]' "$sejr_file" 2>/dev/null || true)
            cb_done=$(safe_int "$cb_done")
        fi

        # Display name (remove date suffix, underscores to spaces)
        display_name=$(echo "$sejr_name" | sed 's/_2026-01-[0-9]*//' | tr '_' ' ')

        subsection "$display_name"

        # Line 1: Score + Rank + Pass + Status
        printf "    %sScore:%s  %s%d%s%s/%d%s" "$DIM" "$RST" "$BOLD" "$total_score" "$RST" "$DIM" "$required_score" "$RST"
        printf "    %sRank:%s  " "$DIM" "$RST"
        color_rank "$rank"
        printf "    %sPass:%s  %s%d%s%s/3%s" "$DIM" "$RST" "$BOLD" "$current_pass" "$RST" "$DIM" "$RST"
        printf "    %sStatus:%s  " "$DIM" "$RST"
        color_status "$status"
        echo ""

        # Line 2: 3-Pass breakdown
        printf "    %sPass 1:%s " "$DIM" "$RST"
        if [ "$p1_done" = "true" ]; then
            printf "%s%d/10 DONE%s" "$BGREEN" "$p1_score" "$RST"
        else
            printf "%s%d/10 (%d%%)%s" "$BYELLOW" "$p1_score" "$p1_pct" "$RST"
        fi
        printf "   %sPass 2:%s " "$DIM" "$RST"
        if [ "$p2_done" = "true" ]; then
            printf "%s%d/10 DONE%s" "$BGREEN" "$p2_score" "$RST"
        else
            printf "%s%d/10 (%d%%)%s" "$BYELLOW" "$p2_score" "$p2_pct" "$RST"
        fi
        printf "   %sPass 3:%s " "$DIM" "$RST"
        if [ "$p3_done" = "true" ]; then
            printf "%s%d/10 DONE%s" "$BGREEN" "$p3_score" "$RST"
        else
            printf "%s%d/10 (%d%%)%s" "$BYELLOW" "$p3_score" "$p3_pct" "$RST"
        fi
        echo ""

        # Line 3: Checkbox progress bar
        printf "    %sCheckboxes:%s %d/%d  " "$DIM" "$RST" "$cb_done" "$cb_total"
        progress_bar "$cb_done" "$cb_total" 25
        echo ""

        # Line 4: Tests + Archive status
        printf "    %sTests:%s %d/%d" "$DIM" "$RST" "$tests_passed" "$tests_required"
        if [ "$can_archive" = "true" ]; then
            printf "    %s%s READY TO ARCHIVE %s" "$BG_GREEN" "$BWHITE" "$RST"
        elif [ -n "$archive_blocker" ]; then
            printf "    %sArchive blocker:%s %s%s%s" "$DIM" "$RST" "$BRED" "$archive_blocker" "$RST"
        fi
        echo ""

    done

    if [ "$active_count" -eq 0 ]; then
        printf "\n    %sNo active sejrlister -- all work archived!%s\n" "$BGREEN" "$RST"
    fi
else
    printf "\n    %s10_ACTIVE/ directory not found%s\n" "$BRED" "$RST"
fi


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: ARCHIVE STATS
# ══════════════════════════════════════════════════════════════════════════════

section_header "ARCHIVE STATISTICS" "<<<"

if [ -d "$ARCHIVE_DIR" ]; then
    archive_total=0
    score_sum=0
    grand_admiral_count=0
    admiral_count=0
    captain_count=0
    kadet_count=0
    other_rank_count=0
    perfect_count=0
    highest_score=0
    lowest_score=999

    # Collect per-sejr data for the table
    declare -a arch_names=()
    declare -a arch_scores=()
    declare -a arch_ranks=()

    for arch_dir in "$ARCHIVE_DIR"/*/; do
        [ ! -d "$arch_dir" ] && continue
        arch_name=$(basename "$arch_dir")

        # Skip non-directories
        [ "$arch_name" = "INDEX.md" ] && continue

        archive_total=$((archive_total + 1))

        # Get proper 3-pass score (handles all YAML variants)
        score=$(get_archive_score "$arch_dir")

        # Get rank — derive from score for accuracy
        rank=$(rank_from_score "$score")

        score_sum=$((score_sum + score))
        [ "$score" -gt "$highest_score" ] && highest_score=$score
        [ "$score" -lt "$lowest_score" ] && lowest_score=$score
        [ "$score" -eq 30 ] && perfect_count=$((perfect_count + 1))

        # Count ranks
        case "$rank" in
            *GRAND*) grand_admiral_count=$((grand_admiral_count + 1)) ;;
            *ADMIRAL*) admiral_count=$((admiral_count + 1)) ;;
            *KAPTAJN*|*CAPTAIN*) captain_count=$((captain_count + 1)) ;;
            *KADET*) kadet_count=$((kadet_count + 1)) ;;
            *) other_rank_count=$((other_rank_count + 1)) ;;
        esac

        # Store for display (trim name for display)
        short_name=$(echo "$arch_name" | sed 's/_2026-01-[0-9_]*//' | tr '_' ' ')
        arch_names+=("$short_name")
        arch_scores+=("$score")
        arch_ranks+=("$rank")
    done

    # Summary line
    if [ "$archive_total" -gt 0 ]; then
        avg_score=$((score_sum * 10 / archive_total))
        avg_whole=$((avg_score / 10))
        avg_decimal=$((avg_score % 10))
    else
        avg_whole=0
        avg_decimal=0
    fi

    [ "$lowest_score" -eq 999 ] && lowest_score=0

    printf "\n"
    printf "    %s%sTotal Archived:%s   %s%d%s sejrlister\n" "$BOLD" "$WHITE" "$RST" "$BOLD" "$archive_total" "$RST"
    printf "    %s%sCombined Score:%s   %s%d%s%s/%d%s\n" "$BOLD" "$WHITE" "$RST" "$BOLD" "$score_sum" "$RST" "$DIM" "$((archive_total * 30))" "$RST"
    printf "    %s%sAverage Score:%s    %s%d.%d%s%s/30%s\n" "$BOLD" "$WHITE" "$RST" "$BOLD" "$avg_whole" "$avg_decimal" "$RST" "$DIM" "$RST"
    printf "    %s%sHighest / Lowest:%s %s%d%s / %s%d%s\n" "$BOLD" "$WHITE" "$RST" "$BGREEN" "$highest_score" "$RST" "$BYELLOW" "$lowest_score" "$RST"
    printf "    %s%sPerfect Scores:%s   %s%d%s %s(30/30)%s\n" "$BOLD" "$WHITE" "$RST" "$BGREEN" "$perfect_count" "$RST" "$DIM" "$RST"

    # Rank distribution
    subsection "RANK DISTRIBUTION"

    printf "    "
    if [ "$grand_admiral_count" -gt 0 ]; then
        printf "%s%s GRAND ADMIRAL %s %s%d%s  " "$BG_GREEN" "$BWHITE" "$RST" "$BOLD" "$grand_admiral_count" "$RST"
    fi
    if [ "$admiral_count" -gt 0 ]; then
        printf "%sADMIRAL%s %s%d%s  " "$BGREEN" "$RST" "$BOLD" "$admiral_count" "$RST"
    fi
    if [ "$captain_count" -gt 0 ]; then
        printf "%sKAPTAJN%s %s%d%s  " "$BCYAN" "$RST" "$BOLD" "$captain_count" "$RST"
    fi
    if [ "$kadet_count" -gt 0 ]; then
        printf "%sKADET%s %s%d%s  " "$BYELLOW" "$RST" "$BOLD" "$kadet_count" "$RST"
    fi
    if [ "$other_rank_count" -gt 0 ]; then
        printf "%sOTHER%s %s%d%s  " "$DIM" "$RST" "$BOLD" "$other_rank_count" "$RST"
    fi
    echo ""

    # Visual bar for grand admiral dominance
    if [ "$archive_total" -gt 0 ]; then
        printf "\n    %sGrand Admiral rate:%s " "$DIM" "$RST"
        progress_bar "$grand_admiral_count" "$archive_total" 25
        printf "  %s(%d/%d)%s\n" "$DIM" "$grand_admiral_count" "$archive_total" "$RST"
    fi

    # Top scores table (show up to 12 with highest scores first)
    subsection "TOP ARCHIVED SEJRLISTER"

    printf "    %s%-40s  %6s  %-16s%s\n" "$DIM" "Name" "Score" "Rank" "$RST"
    printf "    %s" "$DIM"
    printf '%*s' $((COLS - 8)) '' | tr ' ' '.'
    printf "%s\n" "$RST"

    # Build sortable list: index:score pairs
    sort_input=""
    for i in "${!arch_scores[@]}"; do
        sort_input+="$i:${arch_scores[$i]}"$'\n'
    done

    # Sort and display top entries
    displayed=0
    while IFS=: read -r idx sc; do
        [ -z "$idx" ] && continue
        [ "$displayed" -ge 12 ] && break

        name="${arch_names[$idx]}"
        rk="${arch_ranks[$idx]}"

        # Truncate name if needed
        if [ ${#name} -gt 38 ]; then
            name="${name:0:35}..."
        fi

        printf "    %-40s  " "$name"
        if [ "$sc" -eq 30 ]; then
            printf "%s%3d/30%s" "$BGREEN" "$sc" "$RST"
        elif [ "$sc" -ge 24 ]; then
            printf "%s%3d/30%s" "$BCYAN" "$sc" "$RST"
        elif [ "$sc" -ge 18 ]; then
            printf "%s%3d/30%s" "$BYELLOW" "$sc" "$RST"
        else
            printf "%s%3d/30%s" "$BRED" "$sc" "$RST"
        fi
        printf "  "
        color_rank "$rk"
        echo ""

        displayed=$((displayed + 1))
    done < <(echo "$sort_input" | sort -t: -k2 -nr)

    if [ "$archive_total" -gt 12 ]; then
        printf "    %s... and %d more%s\n" "$DIM" "$((archive_total - 12))" "$RST"
    fi

else
    printf "\n    %s90_ARCHIVE/ directory not found%s\n" "$BRED" "$RST"
fi


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: ENFORCEMENT STATUS
# ══════════════════════════════════════════════════════════════════════════════

section_header "ENFORCEMENT STATUS" "!!!"

# Git status
printf "\n"
if [ -d "$BASE/.git" ]; then
    git_clean=$(cd "$BASE" && git status --porcelain 2>/dev/null | wc -l)
    git_clean=$(safe_int "$git_clean")
    last_commit=$(cd "$BASE" && git log -1 --format='%ci' 2>/dev/null || echo "unknown")
    last_msg=$(cd "$BASE" && git log -1 --format='%s' 2>/dev/null || echo "unknown")
    commit_count=$(cd "$BASE" && git rev-list --count HEAD 2>/dev/null || echo "?")

    printf "    %s%sGit Repository:%s    " "$BOLD" "$WHITE" "$RST"
    if [ "$git_clean" -eq 0 ]; then
        printf "%s%s CLEAN %s\n" "$BG_GREEN" "$BWHITE" "$RST"
    else
        printf "%s%s %d UNCOMMITTED CHANGES %s\n" "$BG_RED" "$BWHITE" "$git_clean" "$RST"
    fi
    printf "    %s%sTotal Commits:%s     %s%s%s\n" "$BOLD" "$WHITE" "$RST" "$BOLD" "$commit_count" "$RST"
    printf "    %s%sLast Commit:%s       %s%s%s\n" "$BOLD" "$WHITE" "$RST" "$WHITE" "$last_commit" "$RST"
    printf "    %s%sLast Message:%s      %s%s%s\n" "$BOLD" "$WHITE" "$RST" "$DIM" "$last_msg" "$RST"
else
    printf "    %s%sGit Repository:%s    %sNOT A GIT REPO%s\n" "$BOLD" "$WHITE" "$RST" "$BYELLOW" "$RST"
fi

# LIVE_STATUS.md freshness
live_status="$CURRENT_DIR/LIVE_STATUS.md"
if [ -f "$live_status" ]; then
    ls_mod=$(stat -c '%Y' "$live_status" 2>/dev/null || stat -f '%m' "$live_status" 2>/dev/null || echo 0)
    ls_age_secs=$((NOW_EPOCH - ls_mod))
    ls_age_min=$((ls_age_secs / 60))
    ls_age_hrs=$((ls_age_secs / 3600))

    printf "    %s%sLIVE_STATUS.md:%s    " "$BOLD" "$WHITE" "$RST"
    if [ "$ls_age_hrs" -lt 1 ]; then
        printf "%sFRESH%s %s(%d min ago)%s\n" "$BGREEN" "$RST" "$DIM" "$ls_age_min" "$RST"
    elif [ "$ls_age_hrs" -lt 24 ]; then
        printf "%s%dh old%s\n" "$BYELLOW" "$ls_age_hrs" "$RST"
    else
        printf "%sSTALE%s %s(%d days old)%s\n" "$BRED" "$RST" "$DIM" "$((ls_age_hrs / 24))" "$RST"
    fi
else
    printf "    %s%sLIVE_STATUS.md:%s    %sMISSING%s\n" "$BOLD" "$WHITE" "$RST" "$BRED" "$RST"
fi

# Key files check
subsection "SYSTEM FILE INTEGRITY"

check_file() {
    local label="$1"
    local path="$2"
    printf "    %-30s" "$label"
    if [ -e "$path" ]; then
        printf "%sOK%s\n" "$BGREEN" "$RST"
    else
        printf "%sMISSING%s\n" "$BRED" "$RST"
    fi
}

check_file "DNA.yaml" "$BASE/DNA.yaml"
check_file "00_TEMPLATES/" "$BASE/00_TEMPLATES"
check_file "10_ACTIVE/" "$BASE/10_ACTIVE"
check_file "90_ARCHIVE/" "$BASE/90_ARCHIVE"
check_file "_CURRENT/" "$BASE/_CURRENT"
check_file "_CURRENT/NEXT.md" "$CURRENT_DIR/NEXT.md"
check_file "_CURRENT/LIVE_STATUS.md" "$CURRENT_DIR/LIVE_STATUS.md"
check_file "_CURRENT/LEADERBOARD.md" "$CURRENT_DIR/LEADERBOARD.md"
check_file "scripts/auto_verify.py" "$BASE/scripts/auto_verify.py"
check_file "scripts/auto_archive.py" "$BASE/scripts/auto_archive.py"
check_file "scripts/generate_sejr.py" "$BASE/scripts/generate_sejr.py"


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: NEXT ACTIONS
# ══════════════════════════════════════════════════════════════════════════════

section_header "NEXT RECOMMENDED ACTIONS" ">>>"

next_file="$CURRENT_DIR/NEXT.md"
if [ -f "$next_file" ]; then
    printf "\n"

    # Pull the status table from NEXT.md
    in_table=0
    table_lines=0
    while IFS= read -r line; do
        if echo "$line" | grep -q '^| Sejrliste\|^| Sejr'; then
            in_table=1
        fi
        if [ "$in_table" -eq 1 ]; then
            if echo "$line" | grep -q '^|'; then
                if echo "$line" | grep -qi 'score\|naeste\|Sejrliste'; then
                    printf "    %s%s%s\n" "$DIM" "$line" "$RST"
                elif echo "$line" | grep -qi 'DONE\|complete'; then
                    printf "    %s%s%s\n" "$GREEN" "$line" "$RST"
                else
                    printf "    %s%s%s\n" "$WHITE" "$line" "$RST"
                fi
                table_lines=$((table_lines + 1))
            else
                [ "$table_lines" -gt 0 ] && in_table=0
            fi
        fi
    done < "$next_file"

    # Recommendations
    printf "\n"
    while IFS= read -r rec; do
        clean_rec=$(echo "$rec" | sed 's/\*\*//g')
        printf "    %s>>> %s%s\n" "$BYELLOW" "$clean_rec" "$RST"
    done < <(grep -i '^\*\*Anbefaling' "$next_file" 2>/dev/null || true)

    # Risks
    while IFS= read -r risk; do
        [ -z "$risk" ] && continue
        clean_risk=$(echo "$risk" | sed 's/\*\*//g')
        printf "    %s!!! %s%s\n" "$BRED" "$clean_risk" "$RST"
    done < <(grep -i '^\*\*Risiko' "$next_file" 2>/dev/null || true)

    # Patterns / Observations
    while IFS= read -r pat; do
        [ -z "$pat" ] && continue
        clean_pat=$(echo "$pat" | sed 's/\*\*//g')
        printf "    %s    %s%s\n" "$BCYAN" "$clean_pat" "$RST"
    done < <(grep -i '^\*\*Pattern\|^\*\*Observation' "$next_file" 2>/dev/null || true)

else
    printf "\n    %s_CURRENT/NEXT.md not found%s\n" "$BRED" "$RST"
fi


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════

echo ""
hr "=" "$BMAGENTA"
echo ""

# System summary one-liner
active_n=0
[ -d "$ACTIVE_DIR" ] && active_n=$(find "$ACTIVE_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
active_n=$(safe_int "$active_n")
archive_n=0
[ -d "$ARCHIVE_DIR" ] && archive_n=$(find "$ARCHIVE_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
archive_n=$(safe_int "$archive_n")

printf "  %sSystem:%s %s%d active%s %s|%s %s%d archived%s" \
    "$DIM" "$RST" "$BYELLOW" "$active_n" "$RST" "$DIM" "$RST" "$BGREEN" "$archive_n" "$RST"
printf "  %s|%s  %sRun:%s %ssejrstatus%s" "$DIM" "$RST" "$DIM" "$RST" "$BOLD" "$RST"
printf "  %s|%s  %sSejrliste Systemet v%s%s\n" "$DIM" "$RST" "$DIM" "$DNA_VERSION" "$RST"

echo ""
center "DET SYSTEM DER BEVISER SIG SELV" "$DIM"
echo ""
hr "=" "$BMAGENTA"
echo ""
