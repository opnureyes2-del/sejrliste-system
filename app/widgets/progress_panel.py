#!/usr/bin/env python3
"""
PROGRESS PANEL WIDGET - Progress bars and scores
"""
from pathlib import Path
from typing import Tuple

class ProgressPanel:
    """Widget for displaying progress and scores"""

    def __init__(self, sejr_path: Path):
        self.sejr_path = sejr_path
        self.status_file = sejr_path / "STATUS.yaml"
        self.scores = {"pass_1": 0, "pass_2": 0, "pass_3": 0, "total": 0}
        self.completion_pct = 0

    def load(self) -> None:
        """Load scores from STATUS.yaml"""
        if self.status_file.exists():
            content = self.status_file.read_text(encoding="utf-8")
            for line in content.split("\n"):
                if "pass_1_score:" in line:
                    self.scores["pass_1"] = int(line.split(":")[1].strip())
                elif "pass_2_score:" in line:
                    self.scores["pass_2"] = int(line.split(":")[1].strip())
                elif "pass_3_score:" in line:
                    self.scores["pass_3"] = int(line.split(":")[1].strip())
                elif "total_score:" in line:
                    self.scores["total"] = int(line.split(":")[1].strip())
                elif "completion_pct:" in line:
                    self.completion_pct = int(line.split(":")[1].strip())

    def get_rank(self) -> Tuple[str, str]:
        """Get rank name and emoji"""
        score = self.scores["total"]
        if score >= 27:
            return "GRAND ADMIRAL", ""
        elif score >= 24:
            return "ADMIRAL", ""
        elif score >= 21:
            return "KAPTAJN", ""
        elif score >= 18:
            return "LØJTNANT", ""
        else:
            return "KADET", ""
