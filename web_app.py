#!/usr/bin/env python3
"""
SEJRLISTE WEB APP - Deployable version
Built for Rasmus by Kv1nt
"""
import streamlit as st
from pathlib import Path
from datetime import datetime
import re
import json

# Configuration
SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"

st.set_page_config(
    page_title="Sejrliste System",
    page_icon="🏆",
    layout="wide"
)

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
        "checkboxes_done": 0,
        "checkboxes_total": 0,
        "completion_pct": 0,
        "score": 0,
        "status": "unknown"
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

# Header
st.title("🏆 Sejrliste System")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    view = st.radio("View", ["Dashboard", "Active Sejr", "Archive", "Statistics"])

    st.divider()
    st.header("7 DNA Layers")
    for i, name in enumerate([
        "SELF-AWARE", "SELF-DOCUMENTING", "SELF-VERIFYING",
        "SELF-IMPROVING", "SELF-ARCHIVING", "PREDICTIVE", "SELF-OPTIMIZING"
    ], 1):
        st.write(f"[{i}] {name}")

# Main content
if view == "Dashboard":
    col1, col2, col3 = st.columns(3)

    # Count active and archived
    active_count = len(list(ACTIVE_DIR.iterdir())) if ACTIVE_DIR.exists() else 0
    archive_count = len(list(ARCHIVE_DIR.iterdir())) if ARCHIVE_DIR.exists() else 0

    with col1:
        st.metric("Active Sejr", active_count)
    with col2:
        st.metric("Archived Sejr", archive_count)
    with col3:
        st.metric("Total", active_count + archive_count)

    st.divider()

    # Active sejr list
    st.subheader("📂 Active Sejr")
    if ACTIVE_DIR.exists():
        for sejr_path in sorted(ACTIVE_DIR.iterdir(), reverse=True):
            if sejr_path.is_dir():
                status = get_sejr_status(sejr_path)
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{status['name']}**")
                with col2:
                    st.progress(status['completion_pct'] / 100)
                with col3:
                    st.write(f"{status['completion_pct']}%")
    else:
        st.info("No active sejr")

elif view == "Active Sejr":
    st.subheader("📂 Active Sejr Details")

    if ACTIVE_DIR.exists():
        sejr_folders = [f for f in ACTIVE_DIR.iterdir() if f.is_dir()]
        if sejr_folders:
            selected = st.selectbox("Select Sejr", [f.name for f in sejr_folders])
            if selected:
                sejr_path = ACTIVE_DIR / selected
                status = get_sejr_status(sejr_path)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Progress", f"{status['completion_pct']}%")
                    st.metric("Checkboxes", f"{status['checkboxes_done']}/{status['checkboxes_total']}")
                with col2:
                    st.metric("Score", f"{status['score']}/30")
                    rank_name, rank_emoji = get_rank(status['score'])
                    st.metric("Rank", f"{rank_emoji} {rank_name}")

                # Show SEJR_LISTE.md content
                sejr_file = sejr_path / "SEJR_LISTE.md"
                if sejr_file.exists():
                    with st.expander("View SEJR_LISTE.md", expanded=False):
                        st.markdown(sejr_file.read_text(encoding="utf-8"))
        else:
            st.info("No active sejr found")
    else:
        st.warning("10_ACTIVE directory not found")

elif view == "Archive":
    st.subheader("📦 Archived Sejr")

    if ARCHIVE_DIR.exists():
        archives = sorted(ARCHIVE_DIR.iterdir(), reverse=True)

        for archive_path in archives:
            if archive_path.is_dir():
                # Try to read diplom
                diplom_file = archive_path / "SEJR_DIPLOM.md"
                status_file = archive_path / "STATUS.yaml"

                score = 0
                if status_file.exists():
                    try:
                        content = status_file.read_text(encoding="utf-8")
                        for line in content.split("\n"):
                            if "total_score:" in line:
                                score = int(line.split(":")[1].strip())
                    except:
                        pass

                rank_name, rank_emoji = get_rank(score)

                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{archive_path.name}**")
                    with col2:
                        st.write(f"{score}/30")
                    with col3:
                        st.write(f"{rank_emoji} {rank_name}")

                    if diplom_file.exists():
                        with st.expander("View Diplom"):
                            st.markdown(diplom_file.read_text(encoding="utf-8"))

                    st.divider()
    else:
        st.warning("90_ARCHIVE directory not found")

elif view == "Statistics":
    st.subheader("📊 Statistics")

    if ARCHIVE_DIR.exists():
        archives = list(ARCHIVE_DIR.iterdir())
        total_sejr = len(archives)

        scores = []
        ranks = {"GRAND ADMIRAL": 0, "ADMIRAL": 0, "KAPTAJN": 0, "LØJTNANT": 0, "KADET": 0}

        for archive_path in archives:
            if archive_path.is_dir():
                status_file = archive_path / "STATUS.yaml"
                if status_file.exists():
                    try:
                        content = status_file.read_text(encoding="utf-8")
                        for line in content.split("\n"):
                            if "total_score:" in line:
                                score = int(line.split(":")[1].strip())
                                scores.append(score)
                                rank_name, _ = get_rank(score)
                                ranks[rank_name] += 1
                    except:
                        pass

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Archived Sejr", total_sejr)
            if scores:
                st.metric("Average Score", f"{sum(scores)/len(scores):.1f}/30")
                st.metric("Highest Score", f"{max(scores)}/30")

        with col2:
            st.write("**Rank Distribution:**")
            for rank, count in ranks.items():
                if count > 0:
                    st.write(f"- {rank}: {count}")

        # Score chart
        if scores:
            st.divider()
            st.subheader("Score History")
            st.bar_chart(scores)
    else:
        st.warning("90_ARCHIVE directory not found")

# Footer
st.divider()
st.caption("Sejrliste System - Built by Kv1nt for Rasmus | 7 DNA Layers Architecture")
