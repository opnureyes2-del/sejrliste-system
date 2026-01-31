#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
              SEJRLISTE ENTERPRISE - PROFESSIONAL PROJECT TRACKING
═══════════════════════════════════════════════════════════════════════════════

FEATURES:
  - Project Library: All projects with status tracking
  - Production Workspace: Active project management
  - File Management: Browse, view, copy files
  - 7 DNA Layers: Automated quality processes
  - 3-Pass System: Planning → Execution → Review

PROFESSIONAL DESIGN:
  - Clean enterprise aesthetics
  - Minimal visual noise
  - Focus on data and metrics
  - Accessibility-compliant

═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
from pathlib import Path
from datetime import datetime
import re
import subprocess
import json
import shutil
import os
from typing import List, Dict, Any, Optional

# Import Enforcement Engine
try:
    from enforcement_engine import EnforcementEngine, get_enforcement_for_sejr, EnforcementState
    ENFORCEMENT_AVAILABLE = True
except ImportError:
    ENFORCEMENT_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════
# INLINE YAML PARSER - ZERO DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════

def parse_yaml_simple(content: str) -> dict:
    """
    Simple YAML parser for key: value files.
    Handles VERIFY_STATUS.yaml format - NO external dependencies.
    """
    result = {}
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Parse value types
            if value.lower() == 'true':
                result[key] = True
            elif value.lower() == 'false':
                result[key] = False
            elif value.isdigit():
                result[key] = int(value)
            elif value.replace('.', '').isdigit():
                result[key] = float(value)
            elif value.startswith('"') and value.endswith('"'):
                result[key] = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                result[key] = value[1:-1]
            else:
                result[key] = value
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
SCRIPTS_DIR = SYSTEM_PATH / "scripts"
CURRENT_DIR = SYSTEM_PATH / "_CURRENT"
TEMPLATES_DIR = SYSTEM_PATH / "00_TEMPLATES"

st.set_page_config(
    page_title="Victory List Enterprise",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# PREMIUM MODERNE CSS - Glassmorphism + Animationer + Dark Theme
# ═══════════════════════════════════════════════════════════════════════════════

ENTERPRISE_CSS = """
<style>
/* Premium fonts */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/*  PREMIUM DARK THEME - Cirkelline Chakra Colors */
:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #0f1424;
    --bg-tertiary: #151b2e;
    --bg-elevated: #1a2236;
    --border-color: rgba(99, 102, 241, 0.15);
    --border-glow: rgba(139, 92, 246, 0.3);
    --text-primary: #ff9f43;      /* ORANGE-MANGO - visible on dark background */
    --text-secondary: #feca57;    /* MORNING-SUN-YELLOW - secondary text */
    --text-muted: #64748b;
    --accent-violet: #8b5cf6;
    --accent-indigo: #6366f1;
    --accent-cyan: #22d3ee;
    --accent-emerald: #10b981;
    --accent-orange: #f97316;
    --accent-pink: #ec4899;
    --accent-gold: #fbbf24;
    --accent-red: #ef4444;
    --glow-violet: 0 0 30px rgba(139, 92, 246, 0.3);
    --glow-indigo: 0 0 30px rgba(99, 102, 241, 0.3);
    --glow-cyan: 0 0 20px rgba(34, 211, 238, 0.2);
    --glass-bg: rgba(15, 20, 36, 0.8);
    --glass-border: rgba(255, 255, 255, 0.08);
}

/*  ANIMATED GRADIENT BACKGROUND */
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse 60% 40% at 100% 100%, rgba(99, 102, 241, 0.1) 0%, transparent 40%),
        radial-gradient(ellipse 50% 30% at 0% 50%, rgba(34, 211, 238, 0.08) 0%, transparent 30%),
        linear-gradient(180deg, var(--bg-primary) 0%, #0d1220 100%);
    font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
    min-height: 100vh;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/*  PREMIUM HEADER WITH GLOW */
.premium-header {
    background: linear-gradient(135deg, var(--glass-bg) 0%, rgba(20, 25, 45, 0.9) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--glass-border);
    border-radius: 0 0 20px 20px;
    margin: -1rem -1rem 1.5rem -1rem;
    box-shadow: var(--glow-indigo);
}

.premium-header h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    background: linear-gradient(135deg, var(--accent-violet) 0%, var(--accent-cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    font-size: 1.75rem;
    letter-spacing: -0.03em;
}

/*  GLASSMORPHISM SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15, 20, 36, 0.95) 0%, rgba(10, 14, 26, 0.98) 100%) !important;
    border-right: 1px solid var(--glass-border) !important;
    box-shadow: 4px 0 30px rgba(0, 0, 0, 0.3) !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

section[data-testid="stSidebar"] .stMarkdown {
    color: var(--text-primary);
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    background: linear-gradient(135deg, var(--accent-violet) 0%, var(--accent-indigo) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 600;
}

/*  PREMIUM PROJECT CARDS - Glassmorphism + Glow */
.sejr-card {
    background: linear-gradient(145deg, var(--glass-bg) 0%, rgba(20, 26, 46, 0.7) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin: 0.75rem 0;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.sejr-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-violet), var(--accent-cyan), var(--accent-violet));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.sejr-card:hover {
    border-color: var(--border-glow);
    box-shadow: var(--glow-violet), inset 0 1px 0 rgba(255,255,255,0.05);
    transform: translateY(-2px);
}

.sejr-card:hover::before {
    opacity: 1;
}

.sejr-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.35rem;
    letter-spacing: -0.01em;
}

.sejr-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.02em;
}

/*  PREMIUM ANIMATED PROGRESS BARS */
.progress-bar-container {
    background: linear-gradient(90deg, rgba(15, 20, 36, 0.8) 0%, rgba(20, 27, 46, 0.6) 100%);
    border-radius: 10px;
    height: 10px;
    overflow: hidden;
    margin: 0.75rem 0;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--glass-border);
}

.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-violet) 0%, var(--accent-indigo) 50%, var(--accent-cyan) 100%);
    border-radius: 10px;
    transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.4), inset 0 1px 0 rgba(255,255,255,0.2);
    position: relative;
}

.progress-bar-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.progress-bar-fill.complete {
    background: linear-gradient(90deg, var(--accent-emerald) 0%, var(--accent-cyan) 100%);
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.4), inset 0 1px 0 rgba(255,255,255,0.2);
}

/*  PREMIUM WORKSPACE SECTIONS - Glass Panels */
.workspace-section {
    background: linear-gradient(180deg, var(--glass-bg) 0%, rgba(10, 14, 26, 0.85) 100%);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1.75rem 2rem;
    margin: 1.25rem 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.04);
    position: relative;
}

.workspace-section::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 20%;
    right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-violet), transparent);
}

.workspace-header {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    color: var(--text-primary);
    font-size: 1.2rem;
    border-bottom: 1px solid var(--glass-border);
    padding-bottom: 1rem;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.workspace-header::before {
    content: '◆';
    color: var(--accent-violet);
    font-size: 0.8rem;
}

/*  PREMIUM FILE MANAGER - Neon Dropzone */
.file-manager {
    background: linear-gradient(180deg, rgba(15, 20, 36, 0.6) 0%, rgba(10, 14, 26, 0.8) 100%);
    border: 2px dashed var(--border-glow);
    border-radius: 16px;
    padding: 2rem;
    min-height: 220px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}

.file-manager::after {
    content: ' Drop files here';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: var(--text-muted);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.9rem;
    opacity: 0.5;
    pointer-events: none;
}

.file-manager.drag-over {
    border-color: var(--accent-cyan);
    background: rgba(34, 211, 238, 0.05);
    box-shadow: var(--glow-cyan), inset 0 0 30px rgba(34, 211, 238, 0.1);
}

.file-item {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    margin: 0.5rem;
    background: linear-gradient(145deg, var(--glass-bg) 0%, rgba(20, 26, 46, 0.8) 100%);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    cursor: grab;
    transition: all 0.25s ease;
    min-width: 100px;
    backdrop-filter: blur(8px);
}

.file-item:hover {
    border-color: var(--accent-violet);
    box-shadow: var(--glow-violet);
    transform: translateY(-4px) scale(1.02);
}

.file-item.dragging {
    opacity: 0.6;
    cursor: grabbing;
    transform: scale(1.05);
    box-shadow: var(--glow-indigo);
}

.file-icon {
    font-size: 2rem;
    margin-bottom: 0.6rem;
    filter: drop-shadow(0 0 8px rgba(139, 92, 246, 0.4));
}

.file-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-secondary);
    text-align: center;
    word-break: break-word;
    max-width: 85px;
    font-weight: 500;
}

/*  PREMIUM DNA LAYER BADGES - Glowing Pills */
.dna-layer {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.9rem;
    margin: 0.3rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
}

.dna-active {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(34, 211, 238, 0.1) 100%);
    color: var(--accent-emerald);
    border: 1px solid rgba(16, 185, 129, 0.3);
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
}

.dna-active::before {
    content: '●';
    font-size: 0.5rem;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.dna-pending {
    background: rgba(21, 27, 46, 0.6);
    color: var(--text-muted);
    border: 1px solid var(--glass-border);
}

.dna-pending::before {
    content: '○';
    font-size: 0.5rem;
}

.dna-running {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%);
    color: var(--accent-indigo);
    border: 1px solid rgba(99, 102, 241, 0.3);
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.2);
    animation: glow-pulse 2s infinite;
}

.dna-running::before {
    content: '◉';
    font-size: 0.5rem;
}

@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 15px rgba(99, 102, 241, 0.2); }
    50% { box-shadow: 0 0 25px rgba(99, 102, 241, 0.4); }
}

/*  PREMIUM ACTION BUTTONS - Gradient + Glow */
.action-btn {
    background: linear-gradient(135deg, var(--accent-violet) 0%, var(--accent-indigo) 100%);
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.25rem;
    color: white;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
}

.action-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s ease;
}

.action-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(139, 92, 246, 0.5);
}

.action-btn:hover::before {
    left: 100%;
}

.action-btn-success {
    background: linear-gradient(135deg, var(--accent-emerald) 0%, var(--accent-cyan) 100%);
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.action-btn-success:hover {
    box-shadow: 0 6px 25px rgba(16, 185, 129, 0.5);
}

.action-btn-danger {
    background: linear-gradient(135deg, var(--accent-red) 0%, var(--accent-orange) 100%);
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
}

.action-btn-danger:hover {
    box-shadow: 0 6px 25px rgba(239, 68, 68, 0.5);
}

/*  PREMIUM LOG STREAM - Terminal Style */
.log-stream {
    background: linear-gradient(180deg, rgba(10, 14, 26, 0.95) 0%, rgba(5, 7, 13, 0.98) 100%);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 1.25rem;
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 0.8rem;
    max-height: 250px;
    overflow-y: auto;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
    position: relative;
}

.log-stream::before {
    content: '● ● ●';
    position: absolute;
    top: 0.5rem;
    left: 1rem;
    color: var(--text-muted);
    font-size: 0.5rem;
    letter-spacing: 0.3rem;
}

.log-stream::-webkit-scrollbar {
    width: 6px;
}

.log-stream::-webkit-scrollbar-track {
    background: var(--bg-primary);
    border-radius: 3px;
}

.log-stream::-webkit-scrollbar-thumb {
    background: var(--accent-violet);
    border-radius: 3px;
}

.log-entry {
    color: var(--text-secondary);
    margin: 0.35rem 0;
    padding: 0.35rem 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    border-radius: 4px;
    transition: background 0.15s ease;
}

.log-entry:hover {
    background: rgba(139, 92, 246, 0.05);
}

.log-entry .timestamp {
    color: var(--accent-cyan);
    opacity: 0.7;
}

.log-entry .action {
    color: var(--accent-emerald);
    font-weight: 600;
    text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
}

/*  PREMIUM STAT CARDS - Glowing Metrics */
.stat-card {
    background: linear-gradient(145deg, var(--glass-bg) 0%, rgba(20, 26, 46, 0.7) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-violet), var(--accent-cyan));
    opacity: 0.6;
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--glow-indigo);
}

.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.25rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
}

.stat-label {
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-top: 0.5rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/*  PREMIUM SCORE BADGES - Neon Glow */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s ease;
}

.score-high {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(34, 211, 238, 0.1) 100%);
    color: var(--accent-emerald);
    border: 1px solid rgba(16, 185, 129, 0.3);
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
}

.score-high::before {
    content: '';
    font-size: 0.7rem;
}

.score-medium {
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(249, 115, 22, 0.1) 100%);
    color: var(--accent-gold);
    border: 1px solid rgba(251, 191, 36, 0.3);
    box-shadow: 0 0 15px rgba(251, 191, 36, 0.15);
}

.score-medium::before {
    content: '◆';
    font-size: 0.6rem;
}

.score-low {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(249, 115, 22, 0.1) 100%);
    color: var(--accent-red);
    border: 1px solid rgba(239, 68, 68, 0.3);
    box-shadow: 0 0 15px rgba(239, 68, 68, 0.15);
}

.score-low::before {
    content: '▼';
    font-size: 0.5rem;
}

/*  STREAMLIT ELEMENTS - Premium Override */

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-violet) 0%, var(--accent-indigo) 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.5rem !important;
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Select boxes */
.stSelectbox > div > div {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--accent-violet) !important;
    box-shadow: var(--glow-violet) !important;
}

/* Text inputs */
.stTextInput > div > div > input {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 0.75rem 1rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-violet) !important;
    box-shadow: var(--glow-violet) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--accent-violet) !important;
    background: rgba(139, 92, 246, 0.1) !important;
}

.streamlit-expanderContent {
    background: rgba(15, 20, 36, 0.5) !important;
    border: 1px solid var(--glass-border) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 0.5rem !important;
}

.stTabs [data-baseweb="tab"] {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 0.6rem 1.25rem !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(139, 92, 246, 0.1) !important;
    border-color: var(--accent-violet) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent-violet) 0%, var(--accent-indigo) 100%) !important;
    color: white !important;
    border-color: transparent !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    padding: 1.25rem !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-cyan) 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-size: 0.75rem !important;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, rgba(15, 20, 36, 0.8) 0%, rgba(20, 27, 46, 0.6) 100%) !important;
    border-radius: 10px !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-violet) 0%, var(--accent-cyan) 100%) !important;
    border-radius: 10px !important;
}

/* Markdown text */
.stMarkdown {
    color: var(--text-secondary) !important;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Code blocks */
.stCodeBlock {
    background: rgba(10, 14, 26, 0.9) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
}

/* Radio buttons */
.stRadio > div {
    background: transparent !important;
}

.stRadio label {
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Checkboxes */
.stCheckbox > label {
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Toast messages */
[data-testid="stToast"] {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
}

/* Scrollbar global */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--accent-violet) 0%, var(--accent-indigo) 100%);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, var(--accent-indigo) 0%, var(--accent-violet) 100%);
}

/*  ANIMATED FLOATING PARTICLES */
.floating-particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: -1;
}

.particle {
    position: absolute;
    width: 4px;
    height: 4px;
    background: var(--accent-violet);
    border-radius: 50%;
    opacity: 0.3;
    animation: float 15s infinite ease-in-out;
}

@keyframes float {
    0%, 100% {
        transform: translateY(100vh) translateX(0);
        opacity: 0;
    }
    10% {
        opacity: 0.3;
    }
    90% {
        opacity: 0.3;
    }
    100% {
        transform: translateY(-100px) translateX(50px);
        opacity: 0;
    }
}

/* ═══════════════════════════════════════════════════════════════════════════════
   RESPONSIVE DESIGN — Mobile + Tablet Breakpoints
   ═══════════════════════════════════════════════════════════════════════════════ */

/* ── TABLET (≤1024px) ────────────────────────────────────────────────────── */
@media (max-width: 1024px) {
    .premium-header {
        padding: 1rem 1.25rem;
        margin: -0.5rem -0.5rem 1rem -0.5rem;
    }

    .premium-header h1 {
        font-size: 1.4rem;
    }

    .workspace-section {
        padding: 1.25rem 1.25rem;
        border-radius: 16px;
    }

    .stat-card {
        padding: 1rem;
    }

    .stat-value {
        font-size: 1.75rem;
    }

    .sejr-card {
        padding: 1rem 1.25rem;
    }

    .file-manager {
        padding: 1.5rem;
        min-height: 160px;
    }

    .log-stream {
        max-height: 250px;
    }
}

/* ── MOBILE (≤768px) ─────────────────────────────────────────────────────── */
@media (max-width: 768px) {
    /* Force Streamlit columns to stack vertically on mobile */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
        width: 100% !important;
    }

    /* Allow 2-column grid for stat cards and small items */
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:nth-child(4)) > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:nth-child(5)) > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:nth-child(6)) > [data-testid="stColumn"] {
        flex: 1 1 48% !important;
        min-width: 48% !important;
        width: 48% !important;
    }

    .premium-header {
        padding: 0.75rem 1rem;
        margin: -0.25rem -0.25rem 0.75rem -0.25rem;
        border-radius: 0 0 14px 14px;
    }

    .premium-header h1 {
        font-size: 1.2rem;
        letter-spacing: -0.02em;
    }

    .workspace-section {
        padding: 1rem;
        margin: 0.75rem 0;
        border-radius: 14px;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }

    .workspace-header {
        font-size: 1rem;
        padding-bottom: 0.75rem;
        margin-bottom: 0.75rem;
        gap: 0.5rem;
    }

    .sejr-card {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
    }

    .stat-card {
        padding: 0.75rem;
        border-radius: 12px;
    }

    .stat-value {
        font-size: 1.5rem;
    }

    .stat-label {
        font-size: 0.65rem;
    }

    .file-manager {
        padding: 1rem;
        min-height: 120px;
        border-radius: 12px;
    }

    .file-item {
        min-width: 70px;
        padding: 0.5rem;
        margin: 0.25rem;
        font-size: 0.7rem;
    }

    .file-item .icon {
        font-size: 1.5rem;
    }

    .log-stream {
        max-height: 200px;
        font-size: 0.7rem;
        padding: 0.75rem;
    }

    .score-badge {
        padding: 0.3rem 0.6rem;
        font-size: 0.75rem;
    }

    .dna-layer {
        padding: 0.3rem 0.6rem;
        font-size: 0.7rem;
    }

    .action-btn {
        padding: 0.5rem 0.8rem !important;
        font-size: 0.8rem !important;
        border-radius: 8px !important;
    }

    /* Streamlit button override for mobile */
    .stButton > button {
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
        border-radius: 10px !important;
    }

    /* Streamlit metrics on mobile */
    [data-testid="stMetric"] {
        padding: 0.75rem !important;
        border-radius: 12px !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.25rem !important;
    }

    /* Tabs on mobile */
    .stTabs [data-baseweb="tab"] {
        padding: 0.4rem 0.8rem !important;
        font-size: 0.8rem !important;
    }

    /* Disable particles on mobile for performance */
    .floating-particles,
    .particles-container {
        display: none !important;
    }

    /* Sidebar auto-collapse hint */
    section[data-testid="stSidebar"] {
        box-shadow: 2px 0 15px rgba(0, 0, 0, 0.4) !important;
    }

    /* Reduce backdrop-filter for mobile performance */
    .sejr-card,
    .stat-card {
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
    }
}

/* ── SMALL MOBILE (≤480px) ───────────────────────────────────────────────── */
@media (max-width: 480px) {
    /* All columns fully stack */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
        width: 100% !important;
    }

    .premium-header {
        padding: 0.5rem 0.75rem;
    }

    .premium-header h1 {
        font-size: 1rem;
    }

    .workspace-section {
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 12px;
    }

    .workspace-header {
        font-size: 0.9rem;
    }

    .stat-value {
        font-size: 1.25rem;
    }

    .stat-label {
        font-size: 0.6rem;
    }

    .sejr-card {
        padding: 0.5rem 0.75rem;
    }

    .file-manager {
        min-height: 80px;
        padding: 0.75rem;
    }

    .log-stream {
        max-height: 150px;
        font-size: 0.65rem;
    }

    /* Reduce heavy box shadows on small screens */
    .workspace-section,
    .sejr-card,
    .stat-card {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
    }

    /* Full width buttons */
    .stButton > button {
        width: 100% !important;
    }
}

/* ── TOUCH-FRIENDLY ENHANCEMENTS ─────────────────────────────────────────── */
@media (pointer: coarse) {
    /* Larger touch targets */
    .stButton > button {
        min-height: 44px !important;
    }

    .file-item {
        min-width: 80px;
        min-height: 80px;
    }

    .action-btn {
        min-height: 44px !important;
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 44px !important;
    }

    /* Disable hover effects on touch devices */
    .sejr-card:hover,
    .stat-card:hover {
        transform: none;
    }
}

/* ── LANDSCAPE MOBILE ────────────────────────────────────────────────────── */
@media (max-width: 768px) and (orientation: landscape) {
    .premium-header {
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
    }

    .workspace-section {
        margin: 0.5rem 0;
        padding: 0.75rem 1rem;
    }

    /* Allow 2 columns in landscape */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 1 1 48% !important;
        min-width: 48% !important;
        width: 48% !important;
    }
}
</style>

<script>
// Drag and Drop functionality
document.addEventListener('DOMContentLoaded', function() {
    const fileItems = document.querySelectorAll('.file-item');
    const dropZones = document.querySelectorAll('.file-manager');

    fileItems.forEach(item => {
        item.draggable = true;

        item.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', item.dataset.path);
            item.classList.add('dragging');
        });

        item.addEventListener('dragend', () => {
            item.classList.remove('dragging');
        });
    });

    dropZones.forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('drag-over');
        });

        zone.addEventListener('dragleave', () => {
            zone.classList.remove('drag-over');
        });

        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('drag-over');
            const sourcePath = e.dataTransfer.getData('text/plain');
            const targetPath = zone.dataset.path;

            // Send to Streamlit
            if (window.parent.postMessage) {
                window.parent.postMessage({
                    type: 'FILE_DROP',
                    source: sourcePath,
                    target: targetPath
                }, '*');
            }
        });
    });
});
</script>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

def count_checkboxes(content: str) -> tuple:
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked

def get_sejr_status(sejr_path: Path) -> dict:
    """Get complete status for a sejr"""
    sejr_file = sejr_path / "SEJR_LISTE.md"
    status_file = sejr_path / "STATUS.yaml"  # FIXED: Was VERIFY_STATUS.yaml

    result = {
        "name": sejr_path.name,
        "path": str(sejr_path),
        "checkboxes_done": 0,
        "checkboxes_total": 0,
        "progress": 0,
        "score": "0/30",
        "phase": "UNKNOWN",
        "is_archived": "90_ARCHIVE" in str(sejr_path),
        "files": [],
        "last_modified": datetime.fromtimestamp(sejr_path.stat().st_mtime) if sejr_path.exists() else datetime.now()
    }

    # Count checkboxes
    if sejr_file.exists():
        content = sejr_file.read_text()
        done, total = count_checkboxes(content)
        result["checkboxes_done"] = done
        result["checkboxes_total"] = total
        result["progress"] = int((done / total * 100) if total > 0 else 0)

    # Get verify status - FIXED: Read correct fields from STATUS.yaml
    if status_file.exists():
        try:
            data = parse_yaml_simple(status_file.read_text())
            # total_score is the correct field name
            score = data.get('total_score', 0)
            if score == 0:
                # Fallback: Calculate from pass scores
                p1 = data.get('pass_1_score', 0)
                p2 = data.get('pass_2_score', 0)
                p3 = data.get('pass_3_score', 0)
                score = p1 + p2 + p3
            result["score"] = f"{score}/30"
            # Determine phase from pass status
            if data.get('pass_3_complete'):
                result["phase"] = "COMPLETE"
            elif data.get('pass_2_complete'):
                result["phase"] = "PASS 3"
            elif data.get('pass_1_complete'):
                result["phase"] = "PASS 2"
            else:
                result["phase"] = "PASS 1"
        except:
            pass

    # List files in folder
    if sejr_path.exists():
        result["files"] = [f.name for f in sejr_path.iterdir() if f.is_file()]

    return result

def get_all_sejrs() -> List[dict]:
    """Get all active and archived sejrs"""
    sejrs = []

    # Active
    if ACTIVE_DIR.exists():
        for folder in sorted(ACTIVE_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if folder.is_dir() and not folder.name.startswith("."):
                sejrs.append(get_sejr_status(folder))

    # Archived (last 10)
    if ARCHIVE_DIR.exists():
        for folder in sorted(ARCHIVE_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
            if folder.is_dir() and not folder.name.startswith("."):
                sejrs.append(get_sejr_status(folder))

    return sejrs

def run_script(script_name: str) -> tuple:
    """Run a DNA layer script"""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        return False, f"Script not found: {script_name}"

    try:
        result = subprocess.run(
            ["python3", str(script_path)],
            cwd=str(SYSTEM_PATH),
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout or result.stderr
    except Exception as e:
        return False, str(e)

def copy_file(source: str, target_dir: str) -> bool:
    """Copy a file to target directory"""
    try:
        src = Path(source)
        dst = Path(target_dir) / src.name
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        st.error(f"Copy failed: {e}")
        return False

def move_file(source: str, target_dir: str) -> bool:
    """Move a file to target directory"""
    try:
        src = Path(source)
        dst = Path(target_dir) / src.name
        shutil.move(src, dst)
        return True
    except Exception as e:
        st.error(f"Move failed: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

if 'selected_sejr' not in st.session_state:
    st.session_state.selected_sejr = None
if 'view' not in st.session_state:
    st.session_state.view = 'library'  # library, production, files
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()

def get_session_duration() -> str:
    delta = datetime.now() - st.session_state.session_start
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m {seconds}s"

# ═══════════════════════════════════════════════════════════════════════════════
# INJECT CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ANIMATED PARTICLES BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="particles-container">
    <div class="particle" style="left: 5%; animation-delay: 0s; animation-duration: 20s;"></div>
    <div class="particle" style="left: 15%; animation-delay: 2s; animation-duration: 25s;"></div>
    <div class="particle" style="left: 25%; animation-delay: 4s; animation-duration: 18s;"></div>
    <div class="particle" style="left: 35%; animation-delay: 1s; animation-duration: 22s;"></div>
    <div class="particle" style="left: 45%; animation-delay: 3s; animation-duration: 19s;"></div>
    <div class="particle" style="left: 55%; animation-delay: 5s; animation-duration: 24s;"></div>
    <div class="particle" style="left: 65%; animation-delay: 2.5s; animation-duration: 21s;"></div>
    <div class="particle" style="left: 75%; animation-delay: 4.5s; animation-duration: 17s;"></div>
    <div class="particle" style="left: 85%; animation-delay: 1.5s; animation-duration: 23s;"></div>
    <div class="particle" style="left: 95%; animation-delay: 3.5s; animation-duration: 26s;"></div>
    <div class="particle large" style="left: 10%; animation-delay: 0.5s; animation-duration: 30s;"></div>
    <div class="particle large" style="left: 40%; animation-delay: 2s; animation-duration: 28s;"></div>
    <div class="particle large" style="left: 70%; animation-delay: 4s; animation-duration: 32s;"></div>
    <div class="particle large" style="left: 90%; animation-delay: 1s; animation-duration: 27s;"></div>
</div>
<style>
    .particles-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: -1;
    }
    .particle {
        position: absolute;
        width: 6px;
        height: 6px;
        background: linear-gradient(135deg, var(--accent-violet) 0%, var(--accent-cyan) 100%);
        border-radius: 50%;
        opacity: 0.4;
        animation: particle-float linear infinite;
        box-shadow: 0 0 10px var(--accent-violet), 0 0 20px var(--accent-indigo);
    }
    .particle.large {
        width: 12px;
        height: 12px;
        opacity: 0.2;
        box-shadow: 0 0 20px var(--accent-violet), 0 0 40px var(--accent-indigo);
    }
    @keyframes particle-float {
        0% {
            transform: translateY(100vh) translateX(0) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 0.4;
        }
        90% {
            opacity: 0.4;
        }
        100% {
            transform: translateY(-100px) translateX(100px) rotate(360deg);
            opacity: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="premium-header">
    <h1> Victory List Enterprise </h1>
    <div style="color: var(--text-secondary); font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">
         Session: """ + get_session_duration() + """ |  DNA: 7 Layers Active |  Premium Edition
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR - PROJECT LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid var(--border-color);">
        <span style="font-family: 'Inter', sans-serif; font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">
             PROJECTS
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Active", use_container_width=True):
            st.session_state.view = 'library'
            st.session_state.filter = 'active'
    with col2:
        if st.button(" Archive", use_container_width=True):
            st.session_state.view = 'library'
            st.session_state.filter = 'archived'

    st.markdown("---")

    # Sejr list
    sejrs = get_all_sejrs()
    active_sejrs = [s for s in sejrs if not s['is_archived']]
    archived_sejrs = [s for s in sejrs if s['is_archived']]

    st.markdown(f"**Active ({len(active_sejrs)})**")
    for sejr in active_sejrs:
        progress_bar = f"{'█' * (sejr['progress'] // 10)}{'░' * (10 - sejr['progress'] // 10)}"
        if st.button(
            f" {sejr['name'][:20]}\n{progress_bar} {sejr['progress']}%",
            key=f"sejr_{sejr['name']}",
            use_container_width=True
        ):
            st.session_state.selected_sejr = sejr
            st.session_state.view = 'production'
            st.rerun()

    if archived_sejrs:
        st.markdown(f"** Archived ({len(archived_sejrs)})**")
        for sejr in archived_sejrs[:5]:
            if st.button(f" {sejr['name'][:20]}", key=f"arch_{sejr['name']}", use_container_width=True):
                st.session_state.selected_sejr = sejr
                st.session_state.view = 'production'
                st.rerun()

    st.markdown("---")

    # Quick actions
    st.markdown("** Quick Actions**")
    if st.button(" New Victory", use_container_width=True):
        success, output = run_script("generate_sejr.py")
        if success:
            st.success("New victory created!")
            st.rerun()
        else:
            st.error(output)

    if st.button(" Refresh", use_container_width=True):
        st.rerun()

    # 7 Days Ahead - KLARSYN
    st.markdown("---")
    st.markdown("** 7 Dage Frem**")

    try:
        import sys
        timeline_path = SYSTEM_PATH / "services"
        if str(timeline_path) not in sys.path:
            sys.path.insert(0, str(timeline_path))

        from unified_sync import PredictiveEngine
        engine = PredictiveEngine()
        visions = engine.analyze_week_ahead()

        for i, vision in enumerate(visions[:3]):  # Show first 3 days
            from datetime import datetime
            date = datetime.strptime(vision.date, "%Y-%m-%d")
            weekday = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"][date.weekday()]

            if i == 0:
                icon = ""
                label = "I dag"
            elif i == 1:
                icon = "⏳"
                label = "I morgen"
            else:
                icon = ""
                label = f"{weekday}"

            sejrs = ", ".join(vision.predicted_sejrs[:2]) if vision.predicted_sejrs else "Ingen planlagt"
            st.markdown(f"{icon} **{label}:** {sejrs[:25]}")

    except Exception as e:
        st.caption(f"Forudsigelser: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

if st.session_state.view == 'library' or st.session_state.selected_sejr is None:
    # LIBRARY VIEW - Grid of sejr cards
    st.markdown("""
    <div class="production-room">
        <div class="production-header">Select Project</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(active_sejrs)}</div>
            <div class="stat-label">Active</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(archived_sejrs)}</div>
            <div class="stat-label">Archived</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        avg_progress = sum(s['progress'] for s in active_sejrs) // len(active_sejrs) if active_sejrs else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{avg_progress}%</div>
            <div class="stat-label">Avg Progress</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{get_session_duration()}</div>
            <div class="stat-label">Session</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sejr grid
    cols = st.columns(3)
    for i, sejr in enumerate(active_sejrs):
        with cols[i % 3]:
            progress_bar = f"{'█' * (sejr['progress'] // 10)}{'░' * (10 - sejr['progress'] // 10)}"
            status_color = "#5ba32b" if sejr['progress'] >= 80 else "#f7b93e" if sejr['progress'] >= 50 else "#c23b23"

            st.markdown(f"""
            <div class="sejr-card" onclick="selectSejr('{sejr['name']}')">
                <div class="sejr-title">{sejr['name']}</div>
                <div class="progress-bar-container">
                    <div class="progress-bar-container-bar" style="width: {sejr['progress']}%"></div>
                </div>
                <div class="sejr-meta">
                    <span style="color: {status_color}">■</span> {sejr['progress']}% | Score: {sejr['score']}
                </div>
                <div class="sejr-meta">Phase: {sejr['phase']} | Tasks: {sejr['checkboxes_done']}/{sejr['checkboxes_total']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"▶ Open", key=f"open_{sejr['name']}", use_container_width=True):
                st.session_state.selected_sejr = sejr
                st.session_state.view = 'production'
                st.rerun()

else:
    # PRODUCTION ROOM - Active workspace
    sejr = st.session_state.selected_sejr
    sejr_path = Path(sejr['path'])

    # Refresh sejr data
    sejr = get_sejr_status(sejr_path)
    st.session_state.selected_sejr = sejr

    st.markdown(f"""
    <div class="production-room">
        <div class="production-header"> PRODUCTION ROOM: {sejr['name']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    #  ENFORCEMENT PANEL - IMPOSSIBLE TO FAIL
    # ═══════════════════════════════════════════════════════════════════════════
    if ENFORCEMENT_AVAILABLE:
        enforcement = get_enforcement_for_sejr(sejr_path)
        pos = enforcement.get_current_position()

        # ALWAYS VISIBLE POSITION INDICATOR
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 2px solid {'var(--accent-emerald)' if pos['can_complete'] else 'var(--accent-orange)' if pos['skipped_must_return'] == 0 else 'var(--accent-red)'};
            border-radius: 16px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <span style="font-size: 1.5rem; font-weight: bold; color: var(--text-primary);">
                         YOU ARE HERE:
                    </span>
                    <span style="font-size: 1.2rem; color: var(--accent-cyan); margin-left: 0.5rem;">
                        {pos['current_checkpoint']['name'][:40]}{'...' if len(pos['current_checkpoint']['name']) > 40 else ''}
                    </span>
                </div>
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <span style="
                        background: var(--glass-bg);
                        padding: 0.5rem 1rem;
                        border-radius: 20px;
                        font-family: 'JetBrains Mono', monospace;
                        font-weight: bold;
                        color: {'var(--accent-emerald)' if pos['progress_percent'] >= 80 else 'var(--accent-orange)' if pos['progress_percent'] >= 50 else 'var(--accent-red)'};
                    ">
                        {pos['verified']}/{pos['total']} ({pos['progress_percent']}%)
                    </span>
                </div>
            </div>
            {'<div style="color: var(--accent-red); margin-top: 0.75rem; font-weight: bold;">[WARN] ' + pos["blocking_reason"] + '</div>' if pos['blocking_reason'] else ''}
        </div>
        """, unsafe_allow_html=True)

        # SKIPPED CHECKPOINT WARNING - CANNOT BE IGNORED
        if pos['skipped_must_return'] > 0:
            st.error(f"""
             **BLOCKED!** You have {pos['skipped_must_return']} task(s) you MUST return to!

            These tasks MUST be completed before you can continue:
            """)
            for cp_id in enforcement.skipped_checkpoints:
                cp = enforcement.checkpoints.get(cp_id)
                if cp:
                    st.warning(f"⏸ **{cp.name}**")
                    if st.button(f" Return to {cp_id}", key=f"return_{cp_id}"):
                        enforcement.start_checkpoint(cp_id)
                        st.rerun()

        # CURRENT CHECKPOINT ACTIONS
        if pos['current_checkpoint']['id']:
            current_cp = enforcement.checkpoints.get(pos['current_checkpoint']['id'])
            if current_cp:
                col_verify, col_skip = st.columns([2, 1])

                with col_verify:
                    if current_cp.verification_type == "manual":
                        proof = st.text_input(
                            f" Proof for: {current_cp.name[:40]}",
                            key=f"proof_{current_cp.id}",
                            placeholder="What's your proof? (e.g., 'Tested locally, output: OK')"
                        )
                        if st.button("[OK] Confirm & Verify", key=f"verify_{current_cp.id}", type="primary"):
                            if proof:
                                success, msg = enforcement.verify_checkpoint(current_cp.id, proof)
                                if success:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                            else:
                                st.error(" YOU MUST PROVIDE PROOF!")
                    else:
                        if st.button("[OK] Run Verification", key=f"verify_{current_cp.id}", type="primary"):
                            success, msg = enforcement.verify_checkpoint(current_cp.id)
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)

                with col_skip:
                    with st.expander("⏸ Skip temporarily"):
                        skip_reason = st.text_input("Why are you skipping?", key=f"skip_reason_{current_cp.id}")
                        if st.button("⏸ Skip (you MUST return!)", key=f"skip_{current_cp.id}"):
                            if skip_reason:
                                success, msg = enforcement.skip_checkpoint(current_cp.id, skip_reason)
                                st.warning(msg)
                                st.rerun()
                            else:
                                st.error("You MUST provide a reason!")

        # ARCHIVE BLOCKING
        can_archive, archive_msg = enforcement.can_archive()
        if not can_archive:
            st.markdown(f"""
            <div style="
                background: rgba(239, 68, 68, 0.1);
                border: 2px solid var(--accent-red);
                border-radius: 12px;
                padding: 1rem;
                margin: 0.5rem 0;
            ">
                <span style="font-weight: bold; color: var(--accent-red);">
                     ARCHIVING BLOCKED
                </span>
                <p style="color: var(--text-secondary); margin-top: 0.5rem;">
                    {archive_msg.replace(chr(10), '<br>')}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Back button
    if st.button("⬅ Back to Library"):
        st.session_state.view = 'library'
        st.session_state.selected_sejr = None
        st.rerun()

    # Progress overview
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.progress(sejr['progress'] / 100, text=f"Progress: {sejr['progress']}%")
    with col2:
        st.metric("Score", sejr['score'])
    with col3:
        st.metric("Phase", sejr['phase'])

    st.markdown("---")

    # DNA Layer Actions
    st.markdown("###  DNA Layer Actions")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("[OK] Verify (v)", use_container_width=True, type="primary"):
            with st.spinner("Running verification..."):
                success, output = run_script("auto_verify.py")
                if success:
                    st.success("Verification complete!")
                    st.rerun()
                else:
                    st.error(output)

    with col2:
        if st.button(" Archive (a)", use_container_width=True):
            # ENFORCEMENT CHECK - BLOCKS IF NOT COMPLETE
            if ENFORCEMENT_AVAILABLE:
                enforcement = get_enforcement_for_sejr(sejr_path)
                can_archive, block_reason = enforcement.can_archive()
                if not can_archive:
                    st.error(f" **ARCHIVING BLOCKED!**\n\n{block_reason}")
                    st.stop()

            with st.spinner("Archiving..."):
                success, output = run_script("auto_archive.py")
                if success:
                    st.success("Archived successfully!")
                    st.session_state.selected_sejr = None
                    st.session_state.view = 'library'
                    st.rerun()
                else:
                    st.error(output)

    with col3:
        if st.button(" Predict (p)", use_container_width=True):
            with st.spinner("Generating predictions..."):
                success, output = run_script("auto_predict.py")
                if success:
                    st.success("Predictions generated!")
                else:
                    st.error(output)

    with col4:
        if st.button(" Learn (l)", use_container_width=True):
            with st.spinner("Learning patterns..."):
                success, output = run_script("auto_learn.py")
                if success:
                    st.success("Patterns learned!")
                else:
                    st.error(output)

    st.markdown("---")

    # Two column layout: Files + Tasks
    col_files, col_tasks = st.columns([1, 2])

    with col_files:
        st.markdown("###  File Manager")
        st.markdown(f"""
        <div class="file-manager" data-path="{sejr['path']}">
        """, unsafe_allow_html=True)

        # List files with icons
        if sejr_path.exists():
            for file in sorted(sejr_path.iterdir()):
                if file.is_file():
                    icon = ""
                    if file.suffix == ".md":
                        icon = ""
                    elif file.suffix == ".yaml":
                        icon = ""
                    elif file.suffix == ".jsonl":
                        icon = ""

                    st.markdown(f"""
                    <div class="file-item" data-path="{file}" draggable="true">
                        <div class="file-icon">{icon}</div>
                        <div class="file-name">{file.name[:15]}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # File actions
                    with st.expander(f"{icon} {file.name}", expanded=False):
                        if st.button(f" View", key=f"view_{file.name}"):
                            if file.suffix in ['.md', '.yaml', '.txt', '.json', '.jsonl']:
                                st.code(file.read_text()[:2000], language="markdown")
                        if st.button(f" Copy path", key=f"copy_{file.name}"):
                            st.code(str(file))
                        if st.button(f" Delete", key=f"del_{file.name}"):
                            if st.checkbox(f"Confirm delete {file.name}", key=f"confirm_{file.name}"):
                                file.unlink()
                                st.success(f"Deleted {file.name}")
                                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Copy from templates
        st.markdown("---")
        st.markdown("** Copy Template**")
        if TEMPLATES_DIR.exists():
            templates = list(TEMPLATES_DIR.glob("*.md"))
            if templates:
                selected_template = st.selectbox(
                    "Select template",
                    options=templates,
                    format_func=lambda x: x.name
                )
                if st.button(" Copy to Sejr"):
                    if copy_file(str(selected_template), str(sejr_path)):
                        st.success(f"Copied {selected_template.name}")
                        st.rerun()

    with col_tasks:
        st.markdown("###  Task List")

        sejr_file = sejr_path / "SEJR_LISTE.md"
        if sejr_file.exists():
            content = sejr_file.read_text()

            # Show tasks with checkboxes
            lines = content.split('\n')
            modified = False
            new_lines = []

            for i, line in enumerate(lines):
                if '- [ ]' in line:
                    task = line.replace('- [ ]', '').strip()
                    if st.checkbox(task, key=f"task_{i}", value=False):
                        new_lines.append(line.replace('- [ ]', '- [x]'))
                        modified = True
                    else:
                        new_lines.append(line)
                elif '- [x]' in line or '- [X]' in line:
                    task = line.replace('- [x]', '').replace('- [X]', '').strip()
                    if st.checkbox(task, key=f"task_{i}", value=True):
                        new_lines.append(line)
                    else:
                        new_lines.append(line.replace('- [x]', '- [ ]').replace('- [X]', '- [ ]'))
                        modified = True
                else:
                    new_lines.append(line)

            if modified:
                sejr_file.write_text('\n'.join(new_lines))
                st.success("Tasks updated!")
                st.rerun()

        # Show raw markdown option
        with st.expander(" View Raw SEJR_LISTE.md"):
            if sejr_file.exists():
                st.code(sejr_file.read_text(), language="markdown")

    st.markdown("---")

    # Log stream
    st.markdown("###  Live Activity Log")
    log_file = sejr_path / "AUTO_LOG.jsonl"
    if log_file.exists():
        st.markdown('<div class="log-stream">', unsafe_allow_html=True)
        logs = log_file.read_text().strip().split('\n')[-10:]
        for log_line in reversed(logs):
            try:
                entry = json.loads(log_line)
                ts = entry.get('timestamp', '')[:19]
                action = entry.get('action', 'unknown')
                st.markdown(f"""
                <div class="log-entry">
                    <span class="timestamp">{ts}</span> |
                    <span class="action">{action}</span>
                </div>
                """, unsafe_allow_html=True)
            except:
                pass
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No activity log yet")

    # ═══════════════════════════════════════════════════════════════════════════
    # COMPLETE TIMELINE - ALLE SKRIDT FRA NU TIL AFSLUTNING
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown("###  Komplet Tidslinje")
    st.markdown("*Se ALLE skridt fra nu til GRAND ADMIRAL*")

    # Import timeline functionality
    try:
        import sys
        timeline_path = SYSTEM_PATH / "services"
        if str(timeline_path) not in sys.path:
            sys.path.insert(0, str(timeline_path))

        from complete_timeline import TimelineGenerator, MASTER_STEPS

        generator = TimelineGenerator()
        timeline = generator.generate_sejr_timeline(sejr_path)

        # Progress overview
        col_prog1, col_prog2 = st.columns([3, 1])
        with col_prog1:
            st.progress(timeline.progress_percentage / 100)
        with col_prog2:
            st.markdown(f"**{timeline.progress_percentage}%**")

        # Timeline steps in expander
        with st.expander(" See all 20 steps", expanded=False):
            for step in timeline.steps:
                if step.status.value == "[OK]":
                    icon = "[OK]"
                    style = "color: #10b981;"
                elif step.status.value == "":
                    icon = ""
                    style = "color: #3b82f6; font-weight: bold;"
                else:
                    icon = "⏳"
                    style = "color: #64748b;"

                current_marker = " ← YOU ARE HERE" if step.status.value == "" else ""
                st.markdown(f"""
                <div style="{style}">
                    {icon} [{step.number:02d}] {step.name}{current_marker}
                </div>
                """, unsafe_allow_html=True)

        # Estimated completion
        try:
            from datetime import datetime
            est = datetime.fromisoformat(timeline.estimated_completion)
            st.info(f"⏱ Estimated completion: **{est.strftime('%Y-%m-%d %H:%M')}**")
        except:
            pass

        # Final outcome
        st.success(f" Expected result: {timeline.final_outcome}")

    except ImportError as e:
        st.warning(f"Timeline not available: {e}")
    except Exception as e:
        st.error(f"Timeline error: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
#  REAL-TIME MISSION CONTROL PANEL
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div class="workspace-section">
    <div class="workspace-header"> MISSION CONTROL - Live Activity Feed</div>
</div>
""", unsafe_allow_html=True)

col_realtime1, col_realtime2, col_realtime3 = st.columns([1, 1, 1])

#  LIVE ACTIVITY STREAM
with col_realtime1:
    st.markdown("####  Live Activity Stream")

    # Read latest actions from all active sejrs
    live_actions = []
    if ACTIVE_DIR.exists():
        for folder in ACTIVE_DIR.iterdir():
            if folder.is_dir():
                log_file = folder / "AUTO_LOG.jsonl"
                if log_file.exists():
                    try:
                        lines = log_file.read_text().strip().split('\n')[-10:]
                        for line in lines:
                            if line:
                                entry = json.loads(line)
                                entry['sejr'] = folder.name[:15]
                                live_actions.append(entry)
                    except:
                        pass

    # Sort by timestamp and show latest
    live_actions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    if live_actions:
        st.markdown("""
        <div class="log-stream" style="height: 200px; overflow-y: auto;">
        """, unsafe_allow_html=True)

        for action in live_actions[:8]:
            ts = action.get('timestamp', 'N/A')[:16]
            act = action.get('action', 'unknown')
            sjr = action.get('sejr', '')
            st.markdown(f"""
            <div class="log-entry">
                <span class="timestamp">{ts}</span>
                <span class="action">{act}</span>
                <span style="color: var(--accent-violet);">@{sjr}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No live activity yet...")

#  UPCOMING VICTORIES
with col_realtime2:
    st.markdown("####  Upcoming Victories")

    all_sejrs = get_all_sejrs()
    pending_sejrs = [s for s in all_sejrs if not s['is_archived'] and s['progress'] < 100]
    pending_sejrs.sort(key=lambda x: x['progress'], reverse=True)

    st.markdown("""
    <div style="background: var(--glass-bg); border-radius: 12px; padding: 1rem; border: 1px solid var(--glass-border);">
    """, unsafe_allow_html=True)

    for i, sjr in enumerate(pending_sejrs[:5]):
        progress_color = "#10b981" if sjr['progress'] >= 70 else "#fbbf24" if sjr['progress'] >= 40 else "#8b5cf6"
        st.markdown(f"""
        <div style="padding: 0.5rem 0; border-bottom: 1px solid var(--glass-border);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: var(--text-primary); font-weight: 500;">#{i+1} {sjr['name'][:18]}</span>
                <span style="color: {progress_color}; font-weight: bold;">{sjr['progress']}%</span>
            </div>
            <div style="background: rgba(15, 20, 36, 0.6); border-radius: 4px; height: 6px; margin-top: 0.3rem;">
                <div style="background: linear-gradient(90deg, var(--accent-violet), {progress_color}); height: 100%; width: {sjr['progress']}%; border-radius: 4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

#  LIVE CODE VIEWER
with col_realtime3:
    st.markdown("####  Live Code Viewer")

    # Check for recent file changes
    st.markdown("""
    <div style="background: rgba(10, 14, 26, 0.95); border-radius: 12px; padding: 1rem; border: 1px solid var(--glass-border); font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;">
        <div style="color: var(--text-muted); margin-bottom: 0.5rem;">● ● ● TERMINAL</div>
    """, unsafe_allow_html=True)

    # Show recently modified files
    recent_files = []
    if ACTIVE_DIR.exists():
        for folder in ACTIVE_DIR.iterdir():
            if folder.is_dir():
                for f in folder.iterdir():
                    if f.is_file() and f.suffix in ['.md', '.py', '.yaml']:
                        recent_files.append({
                            'path': f,
                            'mtime': f.stat().st_mtime,
                            'name': f.name
                        })

    recent_files.sort(key=lambda x: x['mtime'], reverse=True)

    for rf in recent_files[:5]:
        mtime_str = datetime.fromtimestamp(rf['mtime']).strftime('%H:%M:%S')
        st.markdown(f"""
        <div style="color: var(--accent-emerald); margin: 0.25rem 0;">
            [{mtime_str}] <span style="color: var(--accent-cyan);">MODIFIED</span> {rf['name'][:20]}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Option to watch a specific file
    if recent_files:
        st.markdown("---")
        selected_file = st.selectbox(
            " View file content:",
            options=[rf['path'] for rf in recent_files[:10]],
            format_func=lambda x: x.name,
            key="code_viewer_select"
        )

        if selected_file and st.button(" View Code", key="show_code_btn"):
            with st.expander(f" {selected_file.name}", expanded=True):
                try:
                    content = selected_file.read_text()[:3000]
                    lang = "python" if selected_file.suffix == ".py" else "yaml" if selected_file.suffix == ".yaml" else "markdown"
                    st.code(content, language=lang)
                except Exception as e:
                    st.error(f"Could not read file: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
#  AUTO-REFRESH OPTION
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
col_refresh1, col_refresh2 = st.columns([3, 1])
with col_refresh1:
    st.markdown("""
    <div style="color: var(--text-muted); font-size: 0.85rem;">
         Tip: Use the button to refresh live data or enable auto-refresh
    </div>
    """, unsafe_allow_html=True)
with col_refresh2:
    if st.button(" Refresh Now", use_container_width=True):
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1.5rem;">
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem;">
        <span style="background: linear-gradient(135deg, var(--accent-violet) 0%, var(--accent-cyan) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
             Victory List Enterprise 
        </span>
    </div>
    <div style="color: var(--text-muted); font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; margin-top: 0.5rem;">
         LIBRARY |  PRODUCTION |  FILES |  DNA |  LIVE
    </div>
    <div style="color: var(--text-muted); font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; margin-top: 0.3rem;">
        v=Verify | a=Archive | p=Predict | n=New | r=Refresh
    </div>
</div>
""", unsafe_allow_html=True)
