#!/usr/bin/env python3
"""
AKTIV SEJR PAGE - View and work on active sejr
Like continuing a conversation - each sejr is a page
"""
import streamlit as st
from pathlib import Path
from datetime import datetime
import json
import re
import subprocess

st.set_page_config(page_title="Aktiv Sejr", page_icon="[LIST]", layout="wide")

SYSTEM_PATH = Path(__file__).parent.parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
SCRIPTS_DIR = SYSTEM_PATH / "scripts"

def get_active_sejr():
    if ACTIVE_DIR.exists():
        return sorted([f for f in ACTIVE_DIR.iterdir() if f.is_dir()], reverse=True)
    return []

def count_checkboxes(content: str):
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked

def run_script(script_name: str, args=None):
    script_path = SCRIPTS_DIR / script_name
    cmd = ["python3", str(script_path)]
    if args:
        cmd.extend(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(SYSTEM_PATH))
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {e}"

# Header
st.title("[LIST] Aktiv Sejr")
st.caption("Vælg en sejr at arbejde på - som at fortsætte en samtale")

# Get active sejr
active_sejr = get_active_sejr()

if not active_sejr:
    st.warning("Ingen aktive sejr. Opret en ny!")
    if st.button("+ Opret Ny Sejr"):
        st.switch_page("pages/3_Ny_Sejr.py")
else:
    # Sejr selector
    sejr_names = [s.name for s in active_sejr]
    selected_name = st.selectbox("Vælg Sejr:", sejr_names)
    selected_sejr = ACTIVE_DIR / selected_name

    st.divider()

    # Two columns: Sejr content + Actions
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"[TEXT] {selected_name}")

        # Read SEJR_LISTE.md
        sejr_file = selected_sejr / "SEJR_LISTE.md"
        if sejr_file.exists():
            content = sejr_file.read_text(encoding="utf-8")

            # Show checkboxes
            st.markdown("### Checkboxes")
            for line in content.split("\n"):
                if "- [" in line:
                    if "- [x]" in line.lower():
                        text = line.split("]", 1)[1].strip()
                        st.markdown(f"[OK] ~~{text}~~")
                    else:
                        text = line.split("]", 1)[1].strip()
                        st.markdown(f"⬜ {text}")

            # Progress
            done, total = count_checkboxes(content)
            st.progress(done / total if total > 0 else 0)
            st.metric("Progress", f"{done}/{total} ({int(done/total*100) if total else 0}%)")

        # AUTO_LOG stream
        st.markdown("###  Live Log")
        log_file = selected_sejr / "AUTO_LOG.jsonl"
        if log_file.exists():
            lines = log_file.read_text().strip().split("\n")[-5:]
            for line in reversed(lines):
                try:
                    entry = json.loads(line)
                    ts = entry.get("timestamp", "")[:19]
                    action = entry.get("action", "")
                    st.code(f"[{ts}] {action}")
                except:
                    pass

    with col2:
        st.subheader(" Actions")

        if st.button("[SCAN] Verify", use_container_width=True):
            with st.spinner("Verifying..."):
                output = run_script("auto_verify.py", [str(selected_sejr)])
                st.code(output[:500])

        if st.button("[DATA] Track", use_container_width=True):
            with st.spinner("Tracking..."):
                output = run_script("auto_track.py")
                st.code(output[:500])

        if st.button(" Predict", use_container_width=True):
            with st.spinner("Predicting..."):
                output = run_script("auto_predict.py")
                st.code(output[:500])

        if st.button("[DOCS] Learn", use_container_width=True):
            with st.spinner("Learning..."):
                output = run_script("auto_learn.py")
                st.code(output[:500])

        st.divider()

        # Status
        status_file = selected_sejr / "STATUS.yaml"
        if status_file.exists():
            st.markdown("### [DATA] Status")
            status_content = status_file.read_text()
            for line in status_content.split("\n"):
                if "score" in line.lower():
                    st.write(line)

        # Archive button
        st.divider()
        if st.button(" Archive Sejr", use_container_width=True, type="primary"):
            with st.spinner("Archiving..."):
                output = run_script("auto_archive.py", [str(selected_sejr)])
                st.code(output[:500])
                if "[OK]" in output:
                    st.success("Arkiveret!")
                    st.rerun()
