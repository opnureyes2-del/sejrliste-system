#!/usr/bin/env python3
"""
SEJRLISTE WEB APP - FULL FUNCTIONALITY
Alt synligt, redigérbart, kørbart
Built for Rasmus by Kv1nt
"""
import streamlit as st
from pathlib import Path
from datetime import datetime
import re
import subprocess
import os

# Configuration
SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
SCRIPTS_DIR = SYSTEM_PATH / "scripts"
TEMPLATES_DIR = SYSTEM_PATH / "00_TEMPLATES"
CURRENT_DIR = SYSTEM_PATH / "_CURRENT"

st.set_page_config(
    page_title="Sejrliste System",
    page_icon="🏆",
    layout="wide"
)

# === HELPER FUNCTIONS ===

def count_checkboxes(content: str) -> tuple:
    """Count checkboxes in content."""
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked

def get_sejr_status(sejr_path: Path) -> dict:
    """Get status for a sejr folder."""
    sejr_file = sejr_path / "SEJR_LISTE.md"
    status_file = sejr_path / "STATUS.yaml"

    result = {
        "name": sejr_path.name,
        "path": str(sejr_path),
        "checkboxes_done": 0,
        "checkboxes_total": 0,
        "completion_pct": 0,
        "score": 0,
        "status": "unknown",
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
                if "status:" in line:
                    result["status"] = line.split(":")[1].strip().strip('"')
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
    """Get rank name and emoji from score."""
    if score >= 27:
        return "GRAND ADMIRAL", "🏅"
    elif score >= 24:
        return "ADMIRAL", "🎖️"
    elif score >= 21:
        return "KAPTAJN", "⭐"
    elif score >= 18:
        return "LØJTNANT", "📊"
    else:
        return "KADET", "🔰"

def run_script(script_name: str, args: list = None) -> str:
    """Run a Python script and return output."""
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

# === SIDEBAR ===
with st.sidebar:
    st.title("🏆 Sejrliste")
    st.caption("7 DNA Layers Architecture")

    st.divider()

    view = st.radio("Navigation", [
        "📊 Dashboard",
        "📂 Active Sejr",
        "📦 Archive",
        "➕ Create New",
        "🔧 Run Scripts",
        "📝 Edit Files",
        "📈 Statistics",
        "🧬 7 DNA Layers"
    ])

    st.divider()

    # Quick stats
    active_count = len(list(ACTIVE_DIR.iterdir())) if ACTIVE_DIR.exists() else 0
    archive_count = len(list(ARCHIVE_DIR.iterdir())) if ARCHIVE_DIR.exists() else 0
    st.metric("Active", active_count)
    st.metric("Archived", archive_count)

# === MAIN CONTENT ===

if view == "📊 Dashboard":
    st.title("📊 Dashboard")
    st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Active Sejr", active_count)
    with col2:
        st.metric("Archived Sejr", archive_count)
    with col3:
        st.metric("Total", active_count + archive_count)
    with col4:
        # Calculate average score
        scores = []
        if ARCHIVE_DIR.exists():
            for a in ARCHIVE_DIR.iterdir():
                if a.is_dir():
                    sf = a / "STATUS.yaml"
                    if sf.exists():
                        try:
                            for line in sf.read_text().split("\n"):
                                if "total_score:" in line:
                                    scores.append(int(line.split(":")[1].strip()))
                        except:
                            pass
        avg = sum(scores)/len(scores) if scores else 0
        st.metric("Avg Score", f"{avg:.1f}/30")

    st.divider()

    # Active sejr overview
    st.subheader("📂 Active Sejr")
    if ACTIVE_DIR.exists() and list(ACTIVE_DIR.iterdir()):
        for sejr_path in sorted(ACTIVE_DIR.iterdir(), reverse=True):
            if sejr_path.is_dir():
                status = get_sejr_status(sejr_path)
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(f"**{status['name']}**")
                    with col2:
                        st.progress(status['completion_pct'] / 100)
                    with col3:
                        st.write(f"{status['completion_pct']}%")
                    with col4:
                        rank_name, rank_emoji = get_rank(status['score'])
                        st.write(f"{rank_emoji}")
    else:
        st.info("No active sejr - Create one!")
        if st.button("➕ Create New Sejr"):
            st.session_state['create_new'] = True

    st.divider()

    # Recent archives
    st.subheader("📦 Recent Archives")
    if ARCHIVE_DIR.exists():
        archives = sorted(ARCHIVE_DIR.iterdir(), reverse=True)[:5]
        for archive_path in archives:
            if archive_path.is_dir():
                status = get_sejr_status(archive_path)
                rank_name, rank_emoji = get_rank(status['score'])
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(archive_path.name[:40])
                with col2:
                    st.write(f"{status['score']}/30")
                with col3:
                    st.write(f"{rank_emoji} {rank_name}")

elif view == "📂 Active Sejr":
    st.title("📂 Active Sejr")

    if ACTIVE_DIR.exists():
        sejr_folders = [f for f in ACTIVE_DIR.iterdir() if f.is_dir()]

        if sejr_folders:
            tabs = st.tabs([f.name[:30] for f in sejr_folders])

            for i, sejr_path in enumerate(sejr_folders):
                with tabs[i]:
                    status = get_sejr_status(sejr_path)

                    # Status header
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Progress", f"{status['completion_pct']}%")
                    with col2:
                        st.metric("Checkboxes", f"{status['checkboxes_done']}/{status['checkboxes_total']}")
                    with col3:
                        st.metric("Score", f"{status['score']}/30")
                    with col4:
                        rank_name, rank_emoji = get_rank(status['score'])
                        st.metric("Rank", f"{rank_emoji} {rank_name}")

                    st.divider()

                    # 3-Pass scores
                    st.subheader("3-Pass Scores")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Pass 1", f"{status['pass_1_score']}/10")
                    with col2:
                        st.metric("Pass 2", f"{status['pass_2_score']}/10")
                    with col3:
                        st.metric("Pass 3", f"{status['pass_3_score']}/10")

                    st.divider()

                    # Actions
                    st.subheader("Actions")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("🔍 Verify", key=f"verify_{i}"):
                            output = run_script("auto_verify.py", ["--sejr", sejr_path.name])
                            st.code(output)
                    with col2:
                        if st.button("📦 Archive", key=f"archive_{i}"):
                            output = run_script("auto_archive.py", ["--sejr", sejr_path.name])
                            st.code(output)
                    with col3:
                        if st.button("📊 Track", key=f"track_{i}"):
                            output = run_script("auto_track.py")
                            st.code(output)
                    with col4:
                        if st.button("🔮 Predict", key=f"predict_{i}"):
                            output = run_script("auto_predict.py")
                            st.code(output)

                    st.divider()

                    # File editor
                    st.subheader("📝 Edit SEJR_LISTE.md")
                    sejr_file = sejr_path / "SEJR_LISTE.md"
                    if sejr_file.exists():
                        content = sejr_file.read_text(encoding="utf-8")
                        new_content = st.text_area("Content", content, height=400, key=f"content_{i}")
                        if st.button("💾 Save Changes", key=f"save_{i}"):
                            sejr_file.write_text(new_content, encoding="utf-8")
                            st.success("Saved!")
                            st.rerun()
        else:
            st.info("No active sejr")
    else:
        st.warning("10_ACTIVE directory not found")

elif view == "📦 Archive":
    st.title("📦 Archived Sejr")

    if ARCHIVE_DIR.exists():
        archives = sorted(ARCHIVE_DIR.iterdir(), reverse=True)

        for archive_path in archives:
            if archive_path.is_dir():
                status = get_sejr_status(archive_path)
                rank_name, rank_emoji = get_rank(status['score'])

                with st.expander(f"{rank_emoji} {archive_path.name} - {status['score']}/30"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Score", f"{status['score']}/30")
                    with col2:
                        st.metric("Rank", rank_name)
                    with col3:
                        st.metric("Checkboxes", f"{status['checkboxes_done']}/{status['checkboxes_total']}")

                    # Show diplom if exists
                    diplom_file = archive_path / "SEJR_DIPLOM.md"
                    if diplom_file.exists():
                        st.subheader("🏆 Diplom")
                        st.markdown(diplom_file.read_text(encoding="utf-8"))

                    # Show conclusion if exists
                    conclusion_file = archive_path / "CONCLUSION.md"
                    if conclusion_file.exists():
                        st.subheader("📋 Conclusion")
                        st.markdown(conclusion_file.read_text(encoding="utf-8"))
    else:
        st.warning("90_ARCHIVE directory not found")

elif view == "➕ Create New":
    st.title("➕ Create New Sejr")

    with st.form("create_sejr"):
        name = st.text_input("Sejr Name (no spaces)", placeholder="MY_NEW_PROJECT")
        goal = st.text_area("Goal", placeholder="What are you trying to achieve?")
        tech = st.text_input("Technology", placeholder="Python, JavaScript, etc.")
        scope = st.selectbox("Scope", ["day", "week", "sprint"])

        submitted = st.form_submit_button("🚀 Create Sejr")

        if submitted:
            if name:
                # Clean name
                clean_name = name.replace(" ", "_").upper()
                output = run_script("generate_sejr.py", [
                    "--name", clean_name,
                    "--goal", goal or "No goal specified",
                    "--tech", tech or "Not specified",
                    "--scope", scope
                ])
                st.code(output)
                if "Created:" in output or "✅" in output:
                    st.success(f"Sejr '{clean_name}' created!")
                    st.balloons()
            else:
                st.error("Please enter a name")

elif view == "🔧 Run Scripts":
    st.title("🔧 Run Scripts")

    st.subheader("Available Scripts")

    scripts = {
        "auto_verify.py": "Verify all active sejr (3-pass system)",
        "auto_track.py": "Update STATE.md with current status",
        "auto_learn.py": "Extract patterns from archives",
        "auto_predict.py": "Generate predictions for next steps",
        "auto_archive.py": "Archive completed sejr",
    }

    for script, desc in scripts.items():
        col1, col2, col3 = st.columns([2, 4, 1])
        with col1:
            st.write(f"**{script}**")
        with col2:
            st.write(desc)
        with col3:
            if st.button("▶️ Run", key=f"run_{script}"):
                with st.spinner(f"Running {script}..."):
                    output = run_script(script)
                    st.code(output)

    st.divider()

    st.subheader("Custom Command")
    custom_args = st.text_input("Additional arguments", placeholder="--sejr MY_SEJR")
    selected_script = st.selectbox("Script", list(scripts.keys()))
    if st.button("▶️ Run Custom"):
        args = custom_args.split() if custom_args else []
        output = run_script(selected_script, args)
        st.code(output)

elif view == "📝 Edit Files":
    st.title("📝 Edit Files")

    # File browser
    st.subheader("System Files")

    file_options = {
        "DNA.yaml": SYSTEM_PATH / "DNA.yaml",
        "README.md": SYSTEM_PATH / "README.md",
        "_CURRENT/STATE.md": CURRENT_DIR / "STATE.md",
        "_CURRENT/NEXT.md": CURRENT_DIR / "NEXT.md",
        "_CURRENT/PATTERNS.yaml": CURRENT_DIR / "PATTERNS.yaml",
    }

    # Add active sejr files
    if ACTIVE_DIR.exists():
        for sejr_path in ACTIVE_DIR.iterdir():
            if sejr_path.is_dir():
                file_options[f"ACTIVE/{sejr_path.name}/SEJR_LISTE.md"] = sejr_path / "SEJR_LISTE.md"
                file_options[f"ACTIVE/{sejr_path.name}/STATUS.yaml"] = sejr_path / "STATUS.yaml"

    selected_file = st.selectbox("Select File", list(file_options.keys()))

    if selected_file:
        file_path = file_options[selected_file]
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            new_content = st.text_area("Edit Content", content, height=500)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save"):
                    file_path.write_text(new_content, encoding="utf-8")
                    st.success(f"Saved {selected_file}")
            with col2:
                if st.button("🔄 Reload"):
                    st.rerun()
        else:
            st.warning(f"File not found: {file_path}")

elif view == "📈 Statistics":
    st.title("📈 Statistics")

    if ARCHIVE_DIR.exists():
        archives = list(ARCHIVE_DIR.iterdir())
        total_sejr = len([a for a in archives if a.is_dir()])

        scores = []
        ranks = {"GRAND ADMIRAL": 0, "ADMIRAL": 0, "KAPTAJN": 0, "LØJTNANT": 0, "KADET": 0}

        for archive_path in archives:
            if archive_path.is_dir():
                status = get_sejr_status(archive_path)
                if status['score'] > 0:
                    scores.append(status['score'])
                    rank_name, _ = get_rank(status['score'])
                    ranks[rank_name] += 1

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Archived", total_sejr)
        with col2:
            st.metric("Average Score", f"{sum(scores)/len(scores):.1f}/30" if scores else "N/A")
        with col3:
            st.metric("Highest Score", f"{max(scores)}/30" if scores else "N/A")
        with col4:
            st.metric("Grand Admirals", ranks["GRAND ADMIRAL"])

        st.divider()

        # Rank distribution
        st.subheader("Rank Distribution")
        col1, col2 = st.columns(2)
        with col1:
            for rank, count in ranks.items():
                if count > 0:
                    _, emoji = get_rank(27 if rank == "GRAND ADMIRAL" else 24 if rank == "ADMIRAL" else 21 if rank == "KAPTAJN" else 18 if rank == "LØJTNANT" else 0)
                    st.write(f"{emoji} **{rank}**: {count}")
        with col2:
            # Bar chart
            import pandas as pd
            df = pd.DataFrame({"Rank": list(ranks.keys()), "Count": list(ranks.values())})
            st.bar_chart(df.set_index("Rank"))

        st.divider()

        # Score trend
        if scores:
            st.subheader("Score History")
            st.line_chart(scores)
    else:
        st.warning("No archives found")

elif view == "🧬 7 DNA Layers":
    st.title("🧬 7 DNA Layers")

    layers = [
        ("1️⃣", "SELF-AWARE", "System knows its own state and identity", "DNA.yaml"),
        ("2️⃣", "SELF-DOCUMENTING", "Auto-logs all actions", "auto_track.py → STATE.md"),
        ("3️⃣", "SELF-VERIFYING", "Auto-tests and validates", "auto_verify.py → STATUS.yaml"),
        ("4️⃣", "SELF-IMPROVING", "Learns from patterns", "auto_learn.py → PATTERNS.yaml"),
        ("5️⃣", "SELF-ARCHIVING", "Extracts semantic essence", "auto_archive.py → CONCLUSION.md"),
        ("6️⃣", "PREDICTIVE", "Suggests next steps", "auto_predict.py → NEXT.md"),
        ("7️⃣", "SELF-OPTIMIZING", "Research before building", "PHASE 0 in SEJR_LISTE.md"),
    ]

    for emoji, name, desc, impl in layers:
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.subheader(f"{emoji}")
            with col2:
                st.subheader(name)
                st.write(desc)
                st.caption(f"Implementation: `{impl}`")
            st.divider()

    # Show DNA.yaml
    st.subheader("DNA.yaml Content")
    dna_file = SYSTEM_PATH / "DNA.yaml"
    if dna_file.exists():
        st.code(dna_file.read_text(encoding="utf-8"), language="yaml")

# === FOOTER ===
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("Sejrliste System v1.0")
with col2:
    st.caption("Built by Kv1nt for Rasmus")
with col3:
    st.caption(f"Last refresh: {datetime.now().strftime('%H:%M:%S')}")
