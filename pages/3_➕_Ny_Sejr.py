#!/usr/bin/env python3
"""
NY SEJR PAGE - Create new sejr with full wizard
"""
import streamlit as st
from pathlib import Path
import subprocess
from datetime import datetime

st.set_page_config(page_title="Ny Sejr", page_icon="➕", layout="wide")

SYSTEM_PATH = Path(__file__).parent.parent
SCRIPTS_DIR = SYSTEM_PATH / "scripts"

st.title("➕ Opret Ny Sejr")
st.caption("Start et nyt projekt - definer mål, teknologi og scope")

# Wizard form
with st.form("create_sejr"):
    st.markdown("### 📝 Projekt Info")

    name = st.text_input(
        "Navn (ingen mellemrum)",
        placeholder="MIT_PROJEKT",
        help="Brug underscore i stedet for mellemrum"
    )

    goal = st.text_area(
        "Mål - Hvad vil du opnå?",
        placeholder="Beskriv hvad du vil bygge og hvorfor...",
        height=100
    )

    tech = st.text_input(
        "Teknologi",
        placeholder="Python, React, PostgreSQL, etc."
    )

    scope = st.selectbox(
        "Scope",
        ["day", "week", "sprint"],
        help="day = 1 dag, week = 1 uge, sprint = 2 uger"
    )

    st.markdown("### 🧬 DNA Layer 7: SELF-OPTIMIZING")
    st.info("Før du starter, søg efter alternativer!")

    alternatives = st.text_area(
        "3 Alternativer (fra research)",
        placeholder="1. Alternativ A: ...\n2. Alternativ B: ...\n3. Alternativ C: ...",
        height=100
    )

    chosen = st.text_input(
        "Valgt tilgang og hvorfor",
        placeholder="Jeg vælger X fordi..."
    )

    submitted = st.form_submit_button("🚀 Opret Sejr", type="primary", use_container_width=True)

    if submitted:
        if not name:
            st.error("Navn er påkrævet!")
        else:
            clean_name = name.replace(" ", "_").upper()

            # Run generate_sejr.py
            script_path = SCRIPTS_DIR / "generate_sejr.py"
            cmd = [
                "python3", str(script_path),
                "--name", clean_name,
                "--goal", goal or "Ikke specificeret",
                "--tech", tech or "Ikke specificeret",
                "--scope", scope
            ]

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(SYSTEM_PATH)
                )
                output = result.stdout + result.stderr

                if "✅" in output or "Created" in output:
                    st.success(f"✅ Sejr '{clean_name}' oprettet!")
                    st.balloons()

                    # Add alternatives to PROJECT_BRIEF.md if provided
                    if alternatives or chosen:
                        brief_content = f"\n\n## DNA Layer 7: Research\n\n### Alternativer\n{alternatives}\n\n### Valgt\n{chosen}"
                        # Find the new sejr folder
                        from pathlib import Path
                        active_dir = SYSTEM_PATH / "10_ACTIVE"
                        for folder in active_dir.iterdir():
                            if clean_name in folder.name:
                                brief_file = folder / "PROJECT_BRIEF.md"
                                if brief_file.exists():
                                    current = brief_file.read_text()
                                    brief_file.write_text(current + brief_content)

                    st.info("Gå til 📋 Aktiv Sejr for at arbejde på den!")
                else:
                    st.error("Fejl ved oprettelse")
                    st.code(output)

            except Exception as e:
                st.error(f"Fejl: {e}")

# Tips
st.divider()
st.markdown("### 💡 Tips")
st.markdown("""
1. **Navn**: Brug beskrivende navn uden mellemrum (MY_PROJECT)
2. **Mål**: Vær specifik - hvad er success criteria?
3. **Teknologi**: List alle relevante teknologier
4. **Scope**: Vælg realistisk - hellere small og færdig
5. **Alternativer**: DNA Layer 7 kræver research før building!
""")
