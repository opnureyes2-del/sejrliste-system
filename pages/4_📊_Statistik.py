#!/usr/bin/env python3
"""
STATISTIK PAGE - Overview of all stats and patterns
"""
import streamlit as st
from pathlib import Path
from datetime import datetime
import json

st.set_page_config(page_title="Statistik", page_icon="📊", layout="wide")

SYSTEM_PATH = Path(__file__).parent.parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
CURRENT_DIR = SYSTEM_PATH / "_CURRENT"

st.title("📊 Statistik & Patterns")
st.caption("Overblik over alt - lær fra historien")

# Quick stats
col1, col2, col3, col4 = st.columns(4)

active_count = len(list(ACTIVE_DIR.iterdir())) if ACTIVE_DIR.exists() else 0
archive_count = len(list(ARCHIVE_DIR.iterdir())) if ARCHIVE_DIR.exists() else 0

with col1:
    st.metric("📂 Aktive", active_count)
with col2:
    st.metric("📦 Arkiverede", archive_count)
with col3:
    st.metric("🏆 Total", active_count + archive_count)
with col4:
    if 'session_start' in st.session_state:
        delta = datetime.now() - st.session_state.session_start
        st.metric("⏱️ Session", f"{int(delta.total_seconds()//60)} min")
    else:
        st.metric("⏱️ Session", "0 min")

st.divider()

# Patterns
st.subheader("🔮 Learned Patterns")
patterns_file = CURRENT_DIR / "PATTERNS.yaml"
if patterns_file.exists():
    content = patterns_file.read_text()
    st.code(content, language="yaml")
else:
    st.info("Ingen patterns endnu - kør auto_learn.py")

# Predictions
st.subheader("🎯 Next Steps")
next_file = CURRENT_DIR / "NEXT.md"
if next_file.exists():
    content = next_file.read_text()
    st.markdown(content)
else:
    st.info("Ingen predictions endnu - kør auto_predict.py")

# DNA Layer Activity
st.subheader("🧬 7 DNA Layers")
layers = [
    ("1. SELF-AWARE", "System identity", "DNA.yaml"),
    ("2. SELF-DOCUMENTING", "Auto-logging", "Haiku"),
    ("3. SELF-VERIFYING", "Test & verify", "Haiku"),
    ("4. SELF-IMPROVING", "Learn patterns", "Opus"),
    ("5. SELF-ARCHIVING", "Archive completed", "Sonnet"),
    ("6. PREDICTIVE", "Next steps", "Opus"),
    ("7. SELF-OPTIMIZING", "Research alternatives", "Opus"),
]

for name, desc, model in layers:
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.write(f"✅ {name}")
    with col2:
        st.caption(desc)
    with col3:
        if model != "DNA.yaml":
            st.caption(f"🤖 {model}")

# Archive stats
st.divider()
st.subheader("📈 Archive Performance")

if ARCHIVE_DIR.exists():
    archives = list(ARCHIVE_DIR.iterdir())
    scores = []
    for a in archives:
        if a.is_dir():
            status_file = a / "STATUS.yaml"
            if status_file.exists():
                content = status_file.read_text()
                for line in content.split("\n"):
                    if "total_score:" in line:
                        scores.append(int(line.split(":")[1].strip()))

    if scores:
        import pandas as pd
        df = pd.DataFrame({"Score": scores})
        st.bar_chart(df)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Højeste", f"{max(scores)}/30")
        with col2:
            st.metric("Gennemsnit", f"{sum(scores)/len(scores):.1f}/30")
        with col3:
            st.metric("Grand Admirals", sum(1 for s in scores if s >= 27))
