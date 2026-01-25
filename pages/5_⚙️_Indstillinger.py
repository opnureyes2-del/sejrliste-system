#!/usr/bin/env python3
"""
INDSTILLINGER PAGE - System configuration
"""
import streamlit as st
from pathlib import Path
import subprocess

st.set_page_config(page_title="Indstillinger", page_icon="⚙️", layout="wide")

SYSTEM_PATH = Path(__file__).parent.parent

st.title("⚙️ Indstillinger")
st.caption("System konfiguration og vedligeholdelse")

# Auto-refresh
st.subheader("🔄 Auto-Refresh")
auto_refresh = st.toggle("Aktiver auto-refresh (5 sek)", value=True)
if auto_refresh:
    st.session_state.auto_refresh = True
else:
    st.session_state.auto_refresh = False

# Session
st.subheader("⏱️ Session")
if st.button("Reset Session Timer"):
    from datetime import datetime
    st.session_state.session_start = datetime.now()
    st.success("Session timer reset!")

# System info
st.subheader("📁 System Paths")
st.code(f"""
SYSTEM_PATH: {SYSTEM_PATH}
ACTIVE_DIR: {SYSTEM_PATH / "10_ACTIVE"}
ARCHIVE_DIR: {SYSTEM_PATH / "90_ARCHIVE"}
SCRIPTS_DIR: {SYSTEM_PATH / "scripts"}
APP_DIR: {SYSTEM_PATH / "app"}
""")

# Git status
st.subheader("📦 Git Status")
try:
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True,
        cwd=str(SYSTEM_PATH)
    )
    if result.stdout.strip():
        st.warning(f"Uncommitted changes:\n{result.stdout}")
    else:
        st.success("✅ Git clean - all committed")
except:
    st.error("Git not available")

# Maintenance
st.subheader("🔧 Vedligeholdelse")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Rebuild STATE.md"):
        result = subprocess.run(
            ["python3", str(SYSTEM_PATH / "scripts/auto_track.py"), "--rebuild-state"],
            capture_output=True,
            text=True,
            cwd=str(SYSTEM_PATH)
        )
        st.code(result.stdout + result.stderr)

with col2:
    if st.button("📚 Rebuild PATTERNS.yaml"):
        result = subprocess.run(
            ["python3", str(SYSTEM_PATH / "scripts/auto_learn.py")],
            capture_output=True,
            text=True,
            cwd=str(SYSTEM_PATH)
        )
        st.code(result.stdout + result.stderr)

# DNA.yaml
st.subheader("🧬 DNA.yaml")
dna_file = SYSTEM_PATH / "DNA.yaml"
if dna_file.exists():
    st.code(dna_file.read_text(), language="yaml")
