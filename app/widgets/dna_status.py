#!/usr/bin/env python3
"""
DNA STATUS WIDGET - 7 DNA Layer status display
"""
from typing import List, Dict

# DNA Layer definitions (from plan)
DNA_LAYERS = [
    {"num": 1, "name": "SELF-AWARE", "short": "AWARE", "model": None},
    {"num": 2, "name": "SELF-DOCUMENTING", "short": "DOC", "model": "Haiku"},
    {"num": 3, "name": "SELF-VERIFYING", "short": "VERIFY", "model": "Haiku"},
    {"num": 4, "name": "SELF-IMPROVING", "short": "IMPROVE", "model": "Opus"},
    {"num": 5, "name": "SELF-ARCHIVING", "short": "ARCHIVE", "model": "Sonnet"},
    {"num": 6, "name": "PREDICTIVE", "short": "PREDICT", "model": "Opus"},
    {"num": 7, "name": "SELF-OPTIMIZING", "short": "OPTIMIZE", "model": "Opus"},
]

class DNAStatus:
    """Widget for displaying 7 DNA layer status"""

    def __init__(self):
        self.layers = DNA_LAYERS.copy()
        self.active_layers: List[int] = []

    def set_active(self, layer_nums: List[int]) -> None:
        """Set which layers are active"""
        self.active_layers = layer_nums

    def get_display_items(self) -> List[Dict]:
        """Get layers formatted for display"""
        items = []
        for layer in self.layers:
            is_active = layer["num"] in self.active_layers
            items.append({
                "num": layer["num"],
                "name": layer["name"],
                "short": layer["short"],
                "model": layer["model"],
                "active": is_active,
                "icon": "[OK]" if is_active else "⬜",
            })
        return items

    def get_model_for_layer(self, layer_num: int) -> str:
        """Get model name for specific layer"""
        for layer in self.layers:
            if layer["num"] == layer_num:
                return layer["model"] or "None"
        return "None"
