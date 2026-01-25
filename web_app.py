#!/usr/bin/env python3
"""
SEJRLISTE VISUAL APP - ADMIRAL DESIGN
Matching the plan: 3-panel layout + live AUTO_LOG stream
Built for Rasmus by Kv1nt

FEATURES:
- Auto-refresh every 5 seconds
- Session timer (how long working)
- 3-panel layout
- Live AUTO_LOG stream
- 7 DNA layers display
"""
import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta
import re
import subprocess
import json
import time

# Configuration
SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
SCRIPTS_DIR = SYSTEM_PATH / "scripts"
CURRENT_DIR = SYSTEM_PATH / "_CURRENT"
APP_DIR = SYSTEM_PATH / "app"

st.set_page_config(
    page_title="Sejrliste Visual System",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === SESSION STATE INIT ===
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# === SESSION TIMER FUNCTION ===
def get_session_duration() -> str:
    """Returns formatted session duration"""
    delta = datetime.now() - st.session_state.session_start
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

# === HELPER FUNCTIONS ===

def count_checkboxes(content: str) -> tuple:
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked

def get_sejr_status(sejr_path: Path) -> dict:
    sejr_file = sejr_path / "SEJR_LISTE.md"
    status_file = sejr_path / "STATUS.yaml"
    result = {
        "name": sejr_path.name,
        "checkboxes_done": 0,
        "checkboxes_total": 0,
        "completion_pct": 0,
        "score": 0,
        "pass_1_score": 0,
        "pass_2_score": 0,
        "pass_3_score": 0,
    }
    if sejr_file.exists():
        content = sejr_file.read_text(encoding="utf-8")
        done, total = count_checkboxes(content)
        result["checkboxes_done"] = done
        result["checkboxes_total"] = total
        result["completion_pct"] = int((done / total * 100)) if total > 0 else 0
    if status_file.exists():
        try:
            content = status_file.read_text(encoding="utf-8")
            for line in content.split("\n"):
                if "total_score:" in line:
                    result["score"] = int(line.split(":")[1].strip())
                if "pass_1_score:" in line:
                    result["pass_1_score"] = int(line.split(":")[1].strip())
                if "pass_2_score:" in line:
                    result["pass_2_score"] = int(line.split(":")[1].strip())
                if "pass_3_score:" in line:
                    result["pass_3_score"] = int(line.split(":")[1].strip())
        except:
            pass
    return result

def get_rank(score: int) -> tuple:
    if score >= 27: return "GRAND ADMIRAL", "🏅"
    elif score >= 24: return "ADMIRAL", "🎖️"
    elif score >= 21: return "KAPTAJN", "⭐"
    elif score >= 18: return "LØJTNANT", "📊"
    else: return "KADET", "🔰"

def get_patterns() -> list:
    patterns_file = CURRENT_DIR / "PATTERNS.yaml"
    if patterns_file.exists():
        try:
            content = patterns_file.read_text(encoding="utf-8")
            patterns = []
            for line in content.split("\n"):
                if line.strip().startswith("- "):
                    patterns.append(line.strip()[2:])
            return patterns[:5]  # Top 5
        except:
            pass
    return []

def get_predictions() -> str:
    next_file = CURRENT_DIR / "NEXT.md"
    if next_file.exists():
        try:
            content = next_file.read_text(encoding="utf-8")
            # Get first meaningful line
            for line in content.split("\n"):
                if line.strip() and not line.startswith("#"):
                    return line.strip()[:100]
        except:
            pass
    return "No predictions yet"

def get_auto_log(sejr_path: Path, limit: int = 10) -> list:
    log_file = sejr_path / "AUTO_LOG.jsonl"
    if log_file.exists():
        try:
            lines = log_file.read_text(encoding="utf-8").strip().split("\n")
            entries = []
            for line in lines[-limit:]:
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                except:
                    pass
            return entries
        except:
            pass
    return []

def run_script(script_name: str, args: list = None) -> str:
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        return f"Script not found: {script_name}"
    cmd = ["python3", str(script_path)]
    if args:
        cmd.extend(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(SYSTEM_PATH))
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {str(e)}"

# === AUTO-REFRESH (JavaScript) ===
if st.session_state.auto_refresh:
    st.markdown(
        """
        <script>
            setTimeout(function(){
                window.location.reload();
            }, 5000);
        </script>
        """,
        unsafe_allow_html=True
    )

# === CUSTOM CSS ===
st.markdown("""
<style>
    .session-timer {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #1a1a2e;
        color: #4da6ff;
        padding: 5px 15px;
        border-radius: 20px;
        font-family: monospace;
        font-size: 0.9rem;
        z-index: 9999;
        border: 1px solid #333;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
        color: #eee;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .panel {
        background: #0e1117;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 1rem;
        min-height: 300px;
    }
    .panel-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #4da6ff;
        border-bottom: 1px solid #333;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .log-stream {
        background: #0a0a0a;
        border: 1px solid #222;
        border-radius: 5px;
        padding: 0.5rem;
        font-family: monospace;
        font-size: 0.85rem;
        max-height: 150px;
        overflow-y: auto;
    }
    .checkbox-done { color: #00ff00; }
    .checkbox-pending { color: #ffaa00; }
    .metric-big { font-size: 2rem; font-weight: bold; }
    .rank-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .rank-grand-admiral { background: gold; color: black; }
    .rank-admiral { background: silver; color: black; }
    .rank-kaptajn { background: #cd7f32; color: white; }
</style>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown('<div class="main-header">🏆 SEJRLISTE VISUAL SYSTEM</div>', unsafe_allow_html=True)

# === SESSION TIMER DISPLAY ===
session_time = get_session_duration()
st.markdown(f'<div class="session-timer">⏱️ Session: {session_time}</div>', unsafe_allow_html=True)

# Quick stats row
col1, col2, col3, col4, col5 = st.columns(5)
active_count = len([f for f in ACTIVE_DIR.iterdir() if f.is_dir()]) if ACTIVE_DIR.exists() else 0
archive_count = len([f for f in ARCHIVE_DIR.iterdir() if f.is_dir()]) if ARCHIVE_DIR.exists() else 0

with col1:
    st.metric("📂 Active", active_count)
with col2:
    st.metric("📦 Archived", archive_count)
with col3:
    st.metric("🏆 Total", active_count + archive_count)
with col4:
    # Count Grand Admirals
    ga_count = 0
    if ARCHIVE_DIR.exists():
        for a in ARCHIVE_DIR.iterdir():
            if a.is_dir():
                s = get_sejr_status(a)
                if s['score'] >= 27:
                    ga_count += 1
    st.metric("🏅 Grand Admirals", ga_count)
with col5:
    st.metric("⏱️ Updated", datetime.now().strftime("%H:%M:%S"))

st.divider()

# === SIDEBAR - Navigation & Actions ===
with st.sidebar:
    st.title("⚙️ Actions")

    # Auto-refresh toggle
    st.session_state.auto_refresh = st.toggle("🔄 Auto-Refresh (5s)", value=st.session_state.auto_refresh)

    if st.button("🔄 Manual Refresh", use_container_width=True):
        st.rerun()

    st.divider()

    # Session info
    st.write(f"⏱️ **Session:** {get_session_duration()}")
    st.write(f"🕐 **Started:** {st.session_state.session_start.strftime('%H:%M:%S')}")

    st.divider()

    if st.button("➕ New Sejr", use_container_width=True):
        st.session_state['show_create'] = True

    if st.button("🔍 Verify All", use_container_width=True):
        with st.spinner("Verifying..."):
            output = run_script("auto_verify.py", ["--all"])
            st.code(output)

    if st.button("📊 Update Tracking", use_container_width=True):
        with st.spinner("Tracking..."):
            output = run_script("auto_track.py")
            st.code(output)

    if st.button("🔮 Generate Predictions", use_container_width=True):
        with st.spinner("Predicting..."):
            output = run_script("auto_predict.py")
            st.code(output)

    if st.button("📚 Learn Patterns", use_container_width=True):
        with st.spinner("Learning..."):
            output = run_script("auto_learn.py")
            st.code(output)

    st.divider()

    # 7 DNA Layers indicator
    st.subheader("🧬 7 DNA Layers")
    dna_status = ["✅"] * 7  # All active
    for i, name in enumerate(["AWARE", "DOC", "VERIFY", "IMPROVE", "ARCHIVE", "PREDICT", "OPTIMIZE"]):
        st.write(f"{dna_status[i]} {i+1}. {name}")

# === MAIN 3-PANEL LAYOUT ===

# Get active sejr for display
active_sejr = []
if ACTIVE_DIR.exists():
    active_sejr = [f for f in sorted(ACTIVE_DIR.iterdir(), reverse=True) if f.is_dir()]

# Create 3 columns matching the plan
col_status, col_sejr, col_patterns = st.columns([1, 2, 1])

# === PANEL 1: LIVE STATUS ===
with col_status:
    st.markdown('<div class="panel-title">📊 LIVE STATUS</div>', unsafe_allow_html=True)

    if active_sejr:
        current = active_sejr[0]
        status = get_sejr_status(current)

        st.write(f"**Current:** {current.name[:20]}...")
        st.progress(status['completion_pct'] / 100)
        st.write(f"Progress: **{status['completion_pct']}%**")

        st.divider()

        st.write("**3-Pass Scores:**")
        cols = st.columns(3)
        with cols[0]:
            st.metric("P1", f"{status['pass_1_score']}/10")
        with cols[1]:
            st.metric("P2", f"{status['pass_2_score']}/10")
        with cols[2]:
            st.metric("P3", f"{status['pass_3_score']}/10")

        rank_name, rank_emoji = get_rank(status['score'])
        st.write(f"**Rank:** {rank_emoji} {rank_name}")
        st.write(f"**Total:** {status['score']}/30")
    else:
        st.info("No active sejr")
        st.write("Click **➕ New Sejr** to start")

    st.divider()
    st.write(f"📂 **{active_count}** active")
    st.write(f"📦 **{archive_count}** archived")

# === PANEL 2: SEJR LISTE VIEW ===
with col_sejr:
    st.markdown('<div class="panel-title">📋 SEJR LISTE</div>', unsafe_allow_html=True)

    if active_sejr:
        current = active_sejr[0]
        sejr_file = current / "SEJR_LISTE.md"

        if sejr_file.exists():
            content = sejr_file.read_text(encoding="utf-8")

            # Extract and display checkboxes
            checkbox_lines = []
            for line in content.split("\n"):
                if "- [" in line:
                    checkbox_lines.append(line)

            # Show first 15 checkboxes
            for line in checkbox_lines[:15]:
                if "- [x]" in line.lower():
                    checkbox_text = line.split("]", 1)[1].strip()[:50]
                    st.markdown(f"✅ ~~{checkbox_text}~~")
                else:
                    checkbox_text = line.split("]", 1)[1].strip()[:50]
                    st.markdown(f"⬜ {checkbox_text}")

            if len(checkbox_lines) > 15:
                st.write(f"*...and {len(checkbox_lines) - 15} more*")

            st.divider()
            done, total = count_checkboxes(content)
            st.progress(done / total if total > 0 else 0)
            st.write(f"**{done}/{total}** checkboxes complete")
    else:
        st.write("No active sejr to display")

        st.divider()
        st.subheader("Recent Archives")
        if ARCHIVE_DIR.exists():
            archives = sorted([f for f in ARCHIVE_DIR.iterdir() if f.is_dir()], reverse=True)[:5]
            for a in archives:
                s = get_sejr_status(a)
                rank_name, rank_emoji = get_rank(s['score'])
                st.write(f"{rank_emoji} {a.name[:25]}... ({s['score']}/30)")

# === PANEL 3: PATTERNS & PREDICTIONS ===
with col_patterns:
    st.markdown('<div class="panel-title">🔮 PATTERNS & PREDICTIONS</div>', unsafe_allow_html=True)

    # Patterns
    st.write("**Learned Patterns:**")
    patterns = get_patterns()
    if patterns:
        for p in patterns[:5]:
            st.write(f"• {p[:40]}...")
    else:
        st.write("*No patterns yet*")

    st.divider()

    # Predictions
    st.write("**Next Steps:**")
    prediction = get_predictions()
    st.info(prediction)

    st.divider()

    # DNA Layer status
    st.write("**7 DNA Layers:**")
    layers_short = ["AWARE", "DOC", "VERIFY", "IMPROVE", "ARCHIVE", "PREDICT", "OPTIMIZE"]
    for i, name in enumerate(layers_short, 1):
        st.write(f"✅ {i}. {name}")

# === AUTO_LOG STREAM ===
st.divider()
st.markdown('<div class="panel-title">📜 AUTO_LOG STREAM</div>', unsafe_allow_html=True)

log_container = st.container()
with log_container:
    if active_sejr:
        current = active_sejr[0]
        log_entries = get_auto_log(current, 5)
        if log_entries:
            for entry in reversed(log_entries):
                timestamp = entry.get('timestamp', 'N/A')[:19]
                action = entry.get('action', 'unknown')
                details = entry.get('details', {})
                st.code(f"[{timestamp}] {action}: {str(details)[:60]}", language=None)
        else:
            st.code("[No log entries yet]", language=None)
    else:
        # Show from _CURRENT/STATE.md
        state_file = CURRENT_DIR / "STATE.md"
        if state_file.exists():
            content = state_file.read_text(encoding="utf-8")
            lines = [l for l in content.split("\n") if l.strip()][:5]
            for line in lines:
                st.code(line[:80], language=None)
        else:
            st.code("[No active log stream]", language=None)

# === CREATE NEW SEJR MODAL ===
if st.session_state.get('show_create', False):
    st.divider()
    st.subheader("➕ Create New Sejr")
    with st.form("create_form"):
        name = st.text_input("Name (no spaces)", placeholder="MY_PROJECT")
        goal = st.text_area("Goal", placeholder="What are you building?")
        tech = st.text_input("Technology", placeholder="Python, JavaScript, etc.")

        if st.form_submit_button("🚀 Create"):
            if name:
                clean_name = name.replace(" ", "_").upper()
                output = run_script("generate_sejr.py", [
                    "--name", clean_name,
                    "--goal", goal or "No goal",
                    "--tech", tech or "Unknown",
                    "--scope", "day"
                ])
                st.code(output)
                if "✅" in output:
                    st.success("Sejr created!")
                    st.session_state['show_create'] = False
                    st.rerun()
            else:
                st.error("Name required")

    if st.button("Cancel"):
        st.session_state['show_create'] = False
        st.rerun()

# === FOOTER ===
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("Sejrliste Visual System v2.0")
with col2:
    st.caption("ADMIRAL DESIGN - 3-Panel Layout")
with col3:
    st.caption(f"Built by Kv1nt | {datetime.now().strftime('%Y-%m-%d')}")
