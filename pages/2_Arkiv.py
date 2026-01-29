#!/usr/bin/env python3
"""
ARKIV PAGE - Browse all archived sejr with diplomas
"""
import streamlit as st
from pathlib import Path
import re

st.set_page_config(page_title="Sejr Arkiv", page_icon="", layout="wide")

SYSTEM_PATH = Path(__file__).parent.parent
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"

def get_rank(score: int):
 if score >= 27: return "[MEDAL] GRAND ADMIRAL", "gold"
 elif score >= 24: return "[ADMIRAL] ADMIRAL", "silver"
 elif score >= 21: return " KAPTAJN", "bronze"
 elif score >= 18: return "[DATA] LØJTNANT", "blue"
 else: return " KADET", "gray"

def get_sejr_status(sejr_path: Path):
 status_file = sejr_path / "STATUS.yaml"
 result = {"score": 0, "p1": 0, "p2": 0, "p3": 0}
 if status_file.exists():
 content = status_file.read_text()
 for line in content.split("\n"):
 if "total_score:" in line:
 result["score"] = int(line.split(":")[1].strip())
 elif "pass_1_score:" in line:
 result["p1"] = int(line.split(":")[1].strip())
 elif "pass_2_score:" in line:
 result["p2"] = int(line.split(":")[1].strip())
 elif "pass_3_score:" in line:
 result["p3"] = int(line.split(":")[1].strip())
 return result

st.title(" Sejr Arkiv")
st.caption("Alle færdige sejr med diplomer - permanent bevis")

if not ARCHIVE_DIR.exists():
 st.warning("Ingen arkiverede sejr endnu")
else:
 archives = sorted([f for f in ARCHIVE_DIR.iterdir() if f.is_dir()], reverse=True)

 # Stats
 col1, col2, col3, col4 = st.columns(4)
 ga_count = sum(1 for a in archives if get_sejr_status(a)["score"] >= 27)

 with col1:
 st.metric("Total", len(archives))
 with col2:
 st.metric("[MEDAL] Grand Admiral", ga_count)
 with col3:
 avg_score = sum(get_sejr_status(a)["score"] for a in archives) / len(archives) if archives else 0
 st.metric("Gns. Score", f"{avg_score:.1f}/30")
 with col4:
 st.metric("Success Rate", f"{ga_count/len(archives)*100:.0f}%" if archives else "0%")

 st.divider()

 # Archive list
 for archive in archives:
 status = get_sejr_status(archive)
 rank, color = get_rank(status["score"])

 with st.expander(f"{rank} **{archive.name[:40]}...** ({status['score']}/30)"):
 col1, col2 = st.columns([2, 1])

 with col1:
 # Diploma
 diploma_file = archive / "SEJR_DIPLOM.md"
 if diploma_file.exists():
 diploma = diploma_file.read_text()
 st.markdown(diploma[:2000])
 else:
 st.info("Intet diplom fundet")

 with col2:
 st.markdown("### Scores")
 st.metric("Pass 1", f"{status['p1']}/10")
 st.metric("Pass 2", f"{status['p2']}/10")
 st.metric("Pass 3", f"{status['p3']}/10")
 st.metric("Total", f"{status['score']}/30")

 # Conclusion
 conclusion_file = archive / "CONCLUSION.md"
 if conclusion_file.exists():
 st.markdown("### Konklusion")
 st.text(conclusion_file.read_text()[:500])
