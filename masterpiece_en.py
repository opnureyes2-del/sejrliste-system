#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║             VICTORY LIST MASTERPIECE - GTK4 + LIBADWAITA NATIVE (ENGLISH)                   ║
║                                                                               ║
║   A modern, native GNOME application for the Sejrliste system                 ║
║   Built with GTK4 and Libadwaita for a truly contemporary look                ║
║                                                                               ║
║   Features:                                                                   ║
║   • AdwNavigationSplitView - Modern sidebar navigation                        ║
║   • AdwStatusPage - Beautiful empty/welcome states                            ║
║   • AdwActionRow - Polished list items with progress                          ║
║   • 7 DNA Layers - Visual status indicators                                   ║
║   • Real-time updates - Auto-refresh from filesystem                          ║
║                                                                               ║
║   Author: Kv1nt (Claude Opus 4.5) for Rasmus                                  ║
║   Date: 2026-01-25                                                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Pango, Gdk
import cairo  # For konfetti drawing
from pathlib import Path
import re
import json
from datetime import datetime
import subprocess
import shutil
from typing import Dict, List, Any, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CIRKELLINE KV1NT ADMIRAL DESIGN SYSTEM - VF STANDARD
# ═══════════════════════════════════════════════════════════════════════════════

# VF Logo ASCII Art (for terminal/text display)
VF_LOGO_ASCII = """
██╗   ██╗███████╗
██║   ██║██╔════╝
██║   ██║█████╗
╚██╗ ██╔╝██╔══╝
 ╚████╔╝ ██║
  ╚═══╝  ╚═╝
  ADMIRAL
"""

MODERN_CSS = """
/* =============================================================================
   SEJRLISTE MESTERVÆRK - CIRKELLINE KV1NT ADMIRAL STANDARD

   ██╗   ██╗███████╗   VF = VICTORY FLEET
   ██║   ██║██╔════╝   Admiral Rasmus's Command Center
   ██║   ██║█████╗
   ╚██╗ ██╔╝██╔══╝     Cirkelline Chakra-Aligned Color System:
    ╚████╔╝ ██║        Divine → Wisdom → Heart → Intuition → Sacred
     ╚═══╝  ╚═╝

   Design Principper:
   - Cirkelline Chakra-Farver (spirituelt alignment)
   - 8px grid system for perfekt spacing
   - Ivory warmth med deep navy kontrast
   - Vindertavle: Visualiser hele rejsen
   - VF Logo: Admiral Standard

   Skabt til Kv1nt Admiral Standard.
   ============================================================================= */

/* === CIRKELLINE CHAKRA DESIGN TOKENS === */

/* Deep Navy Base (from Cirkelline Agents) */
@define-color surface_0 #0A0E27;
@define-color surface_1 #1A1F3A;
@define-color surface_2 #252B4D;
@define-color surface_3 #303860;
@define-color surface_elevated #3A4273;

/* Primary Orange - Main Brand (Cirkelline) */
@define-color primary_400 #fb923c;
@define-color primary_500 #F97316;
@define-color primary_600 #ea580c;

/* Divine Violet - Crown Chakra */
@define-color divine_400 #c084fc;
@define-color divine_500 #a855f7;

/* Wisdom Gold - Solar Plexus */
@define-color wisdom_400 #fcd34d;
@define-color wisdom_500 #f59e0b;

/* Heart Emerald - Heart Chakra */
@define-color heart_400 #34d399;
@define-color heart_500 #10b981;

/* Intuition Indigo - Third Eye */
@define-color intuition_400 #818cf8;
@define-color intuition_500 #6366f1;

/* Sacred Magenta - Divine Feminine */
@define-color sacred_400 #e879f9;
@define-color sacred_500 #d946ef;

/* Cyan (Chat/Action) */
@define-color cyan_400 #22d3ee;
@define-color cyan_500 #00D9FF;

/* Electric Pink (Important) */
@define-color pink_400 #fb7185;
@define-color pink_500 #FF006E;

/* Success/Error/Warning */
@define-color success_400 #4ade80;
@define-color success_500 #00FF88;
@define-color warning_400 #fbbf24;
@define-color warning_500 #FFB800;
@define-color error_400 #f87171;
@define-color error_500 #FF3366;

/* Text Colors */
@define-color text_primary rgba(255, 255, 255, 0.95);
@define-color text_secondary #B4C6E7;
@define-color text_tertiary rgba(255, 255, 255, 0.40);

/* Ivory (Warm Light Theme Elements) */
@define-color ivory_100 #FFF8F0;
@define-color ivory_200 #FFF5EB;

/* === BASE CANVAS - DEEP NAVY WITH CHAKRA GLOW === */
window.background {
    background:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(249, 115, 22, 0.12) 0%, transparent 50%),
        radial-gradient(ellipse 60% 40% at 100% 100%, rgba(168, 85, 247, 0.08) 0%, transparent 40%),
        radial-gradient(ellipse 40% 30% at 0% 50%, rgba(0, 217, 255, 0.06) 0%, transparent 30%),
        linear-gradient(180deg, #0A0E27 0%, #0f1229 100%);
}

/* === HEADERBAR - SLEEK PREMIUM GLASS === */
headerbar {
    background: linear-gradient(180deg,
        rgba(20, 20, 32, 0.95) 0%,
        rgba(15, 15, 24, 0.90) 100%);
    border-bottom: 1px solid rgba(99, 102, 241, 0.08);
    box-shadow:
        0 1px 0 0 rgba(255, 255, 255, 0.02) inset,
        0 8px 32px -8px rgba(0, 0, 0, 0.6),
        0 0 80px -20px rgba(99, 102, 241, 0.10);
    min-height: 56px;
    padding: 0 8px;
}

headerbar title {
    font-weight: 700;
    font-size: 15px;
    letter-spacing: -0.02em;
    color: rgba(255, 255, 255, 0.95);
}

headerbar button {
    min-height: 36px;
    min-width: 36px;
    border-radius: 10px;
    margin: 6px 4px;
}

/* === NAVIGATION SIDEBAR - LAYERED DEPTH + BREATHING ROOM === */
.navigation-sidebar {
    background: linear-gradient(180deg,
        rgba(15, 15, 23, 0.98) 0%,
        rgba(10, 10, 15, 0.95) 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.03);
    padding: 16px 12px;
}

.navigation-sidebar row {
    margin: 8px 4px;
    padding: 16px 20px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    transition: all 250ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.navigation-sidebar row:hover {
    background: rgba(99, 102, 241, 0.08);
    border-color: rgba(99, 102, 241, 0.15);
    transform: translateX(6px) scale(1.01);
    box-shadow:
        0 4px 20px -4px rgba(99, 102, 241, 0.25),
        0 0 0 1px rgba(99, 102, 241, 0.1) inset;
}

.navigation-sidebar row:selected {
    background: linear-gradient(135deg,
        rgba(99, 102, 241, 0.18) 0%,
        rgba(139, 92, 246, 0.12) 100%);
    border-color: rgba(99, 102, 241, 0.30);
    transform: translateX(4px);
    box-shadow:
        0 0 0 1px rgba(99, 102, 241, 0.15) inset,
        0 8px 24px -8px rgba(99, 102, 241, 0.35),
        0 0 40px -10px rgba(139, 92, 246, 0.20);
}

.navigation-sidebar row:selected:hover {
    background: linear-gradient(135deg,
        rgba(99, 102, 241, 0.25) 0%,
        rgba(139, 92, 246, 0.18) 100%);
    transform: translateX(8px) scale(1.01);
}

/* === CARDS - ELEVATED SURFACES WITH SMOOTH ANIMATIONS === */
.card, preferencesgroup {
    background: linear-gradient(180deg,
        rgba(36, 36, 51, 0.90) 0%,
        rgba(26, 26, 38, 0.85) 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    box-shadow:
        0 0 0 1px rgba(0, 0, 0, 0.4),
        0 4px 8px -2px rgba(0, 0, 0, 0.25),
        0 12px 32px -8px rgba(0, 0, 0, 0.30);
    padding: 24px;
    margin: 16px 0;
    transition: all 280ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card:hover, preferencesgroup:hover {
    transform: translateY(-4px) scale(1.005);
    border-color: rgba(99, 102, 241, 0.12);
    box-shadow:
        0 0 0 1px rgba(99, 102, 241, 0.08),
        0 8px 16px -4px rgba(0, 0, 0, 0.30),
        0 20px 48px -12px rgba(99, 102, 241, 0.15);
}

preferencesgroup > box > label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.5);
    margin-bottom: 12px;
}

/* === ACTION ROWS - SMOOTH INTERACTIVE === */
row.activatable {
    border-radius: 14px;
    margin: 8px 0;
    padding: 16px 20px;
    transition: all 220ms cubic-bezier(0.34, 1.56, 0.64, 1);
    background: rgba(255, 255, 255, 0.015);
    border: 1px solid transparent;
}

row.activatable:hover {
    background: rgba(99, 102, 241, 0.06);
    border-color: rgba(99, 102, 241, 0.10);
    transform: translateX(4px);
    box-shadow: 0 4px 16px -6px rgba(99, 102, 241, 0.20);
}

row.activatable:active {
    background: rgba(99, 102, 241, 0.10);
    transform: scale(0.98) translateX(4px);
    transition: all 80ms ease-out;
}

/* === PROGRESS BARS - SMOOTH ANIMATED INDICATORS === */
progressbar trough {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 10px;
    min-height: 8px;
    border: none;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
}

progressbar progress {
    background: linear-gradient(90deg,
        #6366f1 0%,
        #8b5cf6 50%,
        #a78bfa 100%);
    border-radius: 10px;
    box-shadow:
        0 0 20px -4px rgba(99, 102, 241, 0.7),
        0 0 8px -2px rgba(139, 92, 246, 0.5);
    transition: all 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

progressbar.success progress {
    background: linear-gradient(90deg,
        #22c55e 0%,
        #4ade80 100%);
    box-shadow: 0 0 12px -2px rgba(34, 197, 94, 0.6);
}

progressbar.warning progress {
    background: linear-gradient(90deg,
        #f59e0b 0%,
        #fbbf24 100%);
    box-shadow: 0 0 12px -2px rgba(245, 158, 11, 0.6);
}

progressbar.error progress {
    background: linear-gradient(90deg,
        #ef4444 0%,
        #f87171 100%);
    box-shadow: 0 0 12px -2px rgba(239, 68, 68, 0.6);
}

/* === DNA LAYER BADGES === */
.heading {
    color: #f8fafc;
    font-weight: 700;
}

.caption {
    color: #94a3b8;
    font-size: 11px;
    letter-spacing: 0.3px;
}

.accent {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 50%;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
}

.success {
    color: #22c55e;
    text-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

.warning {
    color: #f59e0b;
    text-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
}

/* === BUTTONS - SMOOTH PREMIUM INTERACTIONS === */
button {
    border-radius: 12px;
    padding: 12px 18px;
    min-height: 40px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    background: rgba(255, 255, 255, 0.03);
    font-weight: 500;
    font-size: 13px;
    letter-spacing: 0.01em;
    transition: all 220ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

button:hover {
    background: rgba(255, 255, 255, 0.07);
    border-color: rgba(255, 255, 255, 0.12);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px -4px rgba(0, 0, 0, 0.3);
}

button:active {
    background: rgba(255, 255, 255, 0.05);
    transform: scale(0.97) translateY(0);
    transition: all 80ms ease-out;
}

button.flat {
    background: transparent;
    border-color: transparent;
}

button.flat:hover {
    background: rgba(99, 102, 241, 0.08);
    transform: scale(1.05);
}

button.suggested-action {
    background: linear-gradient(135deg,
        #6366f1 0%,
        #7c3aed 100%);
    border: none;
    color: white;
    font-weight: 600;
    box-shadow:
        0 2px 4px rgba(0, 0, 0, 0.25),
        0 8px 20px -6px rgba(99, 102, 241, 0.50),
        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
}

button.suggested-action:hover {
    background: linear-gradient(135deg,
        #818cf8 0%,
        #8b5cf6 100%);
    transform: translateY(-3px) scale(1.02);
    box-shadow:
        0 4px 8px rgba(0, 0, 0, 0.25),
        0 16px 32px -8px rgba(99, 102, 241, 0.55),
        0 0 40px -10px rgba(139, 92, 246, 0.40),
        0 0 0 1px rgba(255, 255, 255, 0.15) inset;
}

button.suggested-action:active {
    transform: scale(0.96) translateY(0);
    box-shadow:
        0 1px 2px rgba(0, 0, 0, 0.4),
        0 4px 12px -4px rgba(99, 102, 241, 0.4);
    transition: all 80ms ease-out;
}

button.destructive-action {
    background: linear-gradient(180deg,
        #ef4444 0%,
        #dc2626 100%);
    border: none;
    color: white;
    box-shadow: 0 4px 12px -2px rgba(239, 68, 68, 0.4);
}

button.pill {
    border-radius: 100px;
    padding: 10px 20px;
}

button.circular {
    border-radius: 50%;
    padding: 8px;
    min-width: 36px;
    min-height: 36px;
}

/* === SEARCH BAR === */
searchbar {
    background: rgba(15, 15, 35, 0.9);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

searchentry {
    background: rgba(30, 30, 60, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 10px 16px;
    color: #f8fafc;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

searchentry:focus {
    border-color: rgba(139, 92, 246, 0.6);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2),
                0 4px 15px rgba(0, 0, 0, 0.2);
}

/* === STATUS PAGE === */
statuspage {
    background: transparent;
}

statuspage .icon-dropshadow {
    color: #8b5cf6;
}

statuspage .title {
    font-size: 28px;
    font-weight: 800;
    color: #c4b5fd;
}

/* === SCROLLBAR - MINIMAL === */
scrollbar {
    background: transparent;
}

scrollbar slider {
    background: rgba(139, 92, 246, 0.3);
    border-radius: 4px;
    min-width: 6px;
}

scrollbar slider:hover {
    background: rgba(139, 92, 246, 0.5);
}

/* === SEPARATORS === */
separator {
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(139, 92, 246, 0.3) 50%,
        transparent 100%);
    min-height: 1px;
}

/* === TYPOGRAPHY - CONFIDENT HIERARCHY === */
.title-1 {
    font-size: 32px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.98);
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.title-2 {
    font-size: 24px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    letter-spacing: -0.01em;
}

.title-3 {
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.90);
}

.body {
    font-size: 14px;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.75);
    line-height: 1.5;
}

.monospace {
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-size: 13px;
}

.dim-label {
    color: rgba(255, 255, 255, 0.40);
}

/* === BOXED LIST - HARMONIC FLOW === */
.boxed-list {
    background: rgba(26, 26, 38, 0.6);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    overflow: hidden;
}

.boxed-list row {
    padding: 14px 18px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    transition: background 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

.boxed-list row:last-child {
    border-bottom: none;
}

.boxed-list row:hover {
    background: rgba(255, 255, 255, 0.03);
}

/* === PRIORITY DASHBOARD - COMMAND & CONTROL CENTER === */
.priority-section {
    margin: 16px 0;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.priority-urgent {
    background: linear-gradient(135deg,
        rgba(239, 68, 68, 0.12) 0%,
        rgba(185, 28, 28, 0.06) 100%);
    border-left: 3px solid #ef4444;
    box-shadow:
        0 0 0 1px rgba(239, 68, 68, 0.1) inset,
        0 4px 20px -4px rgba(239, 68, 68, 0.2);
}

.priority-attention {
    background: linear-gradient(135deg,
        rgba(245, 158, 11, 0.12) 0%,
        rgba(180, 83, 9, 0.06) 100%);
    border-left: 3px solid #f59e0b;
    box-shadow:
        0 0 0 1px rgba(245, 158, 11, 0.1) inset,
        0 4px 20px -4px rgba(245, 158, 11, 0.15);
}

.priority-next {
    background: linear-gradient(135deg,
        rgba(99, 102, 241, 0.12) 0%,
        rgba(79, 70, 229, 0.06) 100%);
    border-left: 3px solid #6366f1;
    box-shadow:
        0 0 0 1px rgba(99, 102, 241, 0.1) inset,
        0 4px 20px -4px rgba(99, 102, 241, 0.15);
}

.priority-card {
    border-radius: 12px;
    padding: 14px 16px;
    margin: 6px 0;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.priority-card:hover {
    transform: translateX(6px);
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.08);
    box-shadow: 0 4px 16px -4px rgba(0, 0, 0, 0.4);
}

/* === STATUS INDICATORS - STRENGTH & CONFIDENCE === */
.success {
    color: #4ade80;
}

.warning {
    color: #fbbf24;
}

.error {
    color: #f87171;
}

.accent {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border-radius: 6px;
    font-weight: 600;
    padding: 4px 8px;
    box-shadow: 0 2px 8px -2px rgba(99, 102, 241, 0.5);
}

/* === GLOW EFFECTS - CONTROLLED POWER === */
.glow-purple {
    box-shadow: 0 0 20px -4px rgba(139, 92, 246, 0.5);
}

.glow-green {
    box-shadow: 0 0 20px -4px rgba(74, 222, 128, 0.5);
}

.glow-amber {
    box-shadow: 0 0 20px -4px rgba(251, 191, 36, 0.5);
}

.glow-red {
    box-shadow: 0 0 20px -4px rgba(248, 113, 113, 0.5);
}

/* === CHAT STREAM - FLOWING CONVERSATION === */
.chat-stream-messages {
    background: linear-gradient(180deg,
        rgba(10, 10, 15, 0.4) 0%,
        rgba(15, 15, 23, 0.6) 100%);
    padding: 12px;
    border-radius: 12px;
}

.chat-bubble {
    background: rgba(36, 36, 51, 0.8);
    border-radius: 16px;
    padding: 12px 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow:
        0 1px 2px rgba(0, 0, 0, 0.2),
        0 4px 12px -4px rgba(0, 0, 0, 0.15);
    transition: all 180ms cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-bubble:hover {
    background: rgba(42, 42, 60, 0.9);
    border-color: rgba(255, 255, 255, 0.08);
}

.chat-bubble-system {
    border-radius: 6px 16px 16px 16px;
    background: linear-gradient(135deg,
        rgba(99, 102, 241, 0.10) 0%,
        rgba(36, 36, 51, 0.8) 100%);
    border-left: 2px solid rgba(99, 102, 241, 0.5);
}

.chat-bubble-user {
    border-radius: 16px 16px 6px 16px;
    background: linear-gradient(135deg,
        rgba(139, 92, 246, 0.20) 0%,
        rgba(99, 102, 241, 0.15) 100%);
    border-right: 2px solid rgba(139, 92, 246, 0.6);
}

.chat-sender {
    font-weight: 600;
    font-size: 11px;
    color: #a78bfa;
    letter-spacing: 0.02em;
    margin-bottom: 4px;
}

.chat-timestamp {
    font-size: 10px;
    color: rgba(255, 255, 255, 0.35);
    margin-top: 6px;
}

.chat-link {
    margin-top: 8px;
    padding: 6px 12px;
    border-radius: 8px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.2);
    transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-link:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.35);
}

.chat-verification {
    margin-top: 8px;
    padding: 6px 12px;
    border-radius: 8px;
    background: rgba(74, 222, 128, 0.08);
    border: 1px solid rgba(74, 222, 128, 0.15);
}

.chat-verification.failed {
    background: rgba(248, 113, 113, 0.08);
    border-color: rgba(248, 113, 113, 0.15);
}

/* === DRAG & DROP ACTIVE STATE === */
window.drop-active {
    background: rgba(99, 102, 241, 0.08);
    border: 3px dashed @primary_500;
    box-shadow: inset 0 0 80px rgba(99, 102, 241, 0.15);
}

window.drop-active * {
    opacity: 0.7;
}

/* === ZOOM SLIDER === */
.zoom-slider {
    min-width: 100px;
    margin: 0 8px;
}

.zoom-slider trough {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    min-height: 4px;
}

.zoom-slider highlight {
    background: @primary_500;
    border-radius: 4px;
}

.zoom-slider slider {
    background: @primary_400;
    border-radius: 50%;
    min-width: 14px;
    min-height: 14px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.zoom-label {
    font-size: 11px;
    color: @text_secondary;
    min-width: 35px;
    text-align: center;
}

/* === DNA LAYER ROWS === */
.dna-layer-row {
    padding: 12px 16px;
    border-radius: 12px;
    background: transparent;
    transition: all 200ms ease;
}

.dna-layer-row:hover {
    background: rgba(99, 102, 241, 0.08);
}

.dna-layer-active {
    background: rgba(74, 222, 128, 0.1);
    border-left: 3px solid @success_400;
}

.dna-layer-running {
    background: rgba(99, 102, 241, 0.15);
    border-left: 3px solid @primary_400;
    box-shadow: inset 0 0 20px rgba(99, 102, 241, 0.1);
}

.dna-badge {
    background: @surface_3;
    border-radius: 50%;
    padding: 2px;
}

.dna-badge-active {
    background: @success_500;
    box-shadow: 0 0 12px rgba(74, 222, 128, 0.4);
}

.dna-progress {
    min-height: 3px;
    border-radius: 2px;
}

.dna-progress trough {
    background: rgba(255, 255, 255, 0.1);
    min-height: 3px;
}

.dna-progress progress {
    background: linear-gradient(90deg, @primary_500, @accent_400);
    border-radius: 2px;
}

/* === KEYBOARD HINTS === */
.keyboard-hint {
    font-size: 10px;
    color: @text_tertiary;
    background: rgba(255, 255, 255, 0.08);
    padding: 2px 6px;
    border-radius: 4px;
    margin-left: 8px;
}

/* === COPY BUTTON === */
.copy-btn {
    opacity: 0;
    transition: opacity 150ms ease;
}

*:hover > .copy-btn {
    opacity: 1;
}

.copy-btn:active {
    background: @success_500;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   VF LOGO - KV1NT ADMIRAL STANDARD
   ═══════════════════════════════════════════════════════════════════════════════ */

.vf-logo {
    padding: 8px;
}

.vf-logo-frame {
    background: linear-gradient(135deg,
        @divine_500 0%,
        @wisdom_500 25%,
        @heart_500 50%,
        @intuition_500 75%,
        @sacred_500 100%);
    border-radius: 16px;
    padding: 3px;
    box-shadow:
        0 0 30px rgba(168, 85, 247, 0.4),
        0 0 60px rgba(249, 115, 22, 0.2),
        0 8px 32px rgba(0, 0, 0, 0.4);
}

.vf-logo-frame > * {
    background: @surface_0;
    border-radius: 13px;
    padding: 12px 20px;
}

.vf-logo-text {
    font-size: 32px;
    font-weight: 900;
    letter-spacing: 4px;
    background: linear-gradient(135deg,
        @cyan_500 0%,
        @primary_500 50%,
        @pink_500 100%);
    -gtk-icon-filter: none;
    color: @cyan_500;
}

.vf-logo-subtitle {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 6px;
    color: @text_secondary;
    margin-top: 4px;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   VINDERTAVLE - VICTORY JOURNEY BOARD
   ═══════════════════════════════════════════════════════════════════════════════ */

.vindertavle {
    background: linear-gradient(180deg,
        rgba(26, 31, 58, 0.95) 0%,
        rgba(10, 14, 39, 0.98) 100%);
    border-radius: 20px;
    border: 1px solid rgba(99, 102, 241, 0.15);
    box-shadow:
        0 0 60px rgba(168, 85, 247, 0.08),
        0 20px 60px rgba(0, 0, 0, 0.4);
    margin: 16px;
}

.vindertavle-header {
    background: linear-gradient(90deg,
        rgba(249, 115, 22, 0.1) 0%,
        rgba(168, 85, 247, 0.1) 100%);
    border-radius: 20px 20px 0 0;
    padding: 20px;
}

.vindertavle-title {
    color: @ivory_100;
    letter-spacing: 4px;
    font-weight: 800;
}

.vindertavle-stats {
    background: @divine_500;
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 13px;
}

.vindertavle-timeline {
    padding: 8px 0;
}

/* Victory Cards */
.victory-card {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 12px;
    padding: 12px;
    transition: all 200ms ease;
    border-left: 3px solid transparent;
}

.victory-card:hover {
    background: rgba(255, 255, 255, 0.05);
    transform: translateX(4px);
}

/* Chakra Colors for Victory Cards */
.chakra-divine {
    border-left-color: @divine_500;
}
.chakra-divine .victory-node {
    background: @divine_500;
    box-shadow: 0 0 12px @divine_500;
}
.chakra-divine-text {
    color: @divine_400;
}

.chakra-wisdom {
    border-left-color: @wisdom_500;
}
.chakra-wisdom .victory-node {
    background: @wisdom_500;
    box-shadow: 0 0 12px @wisdom_500;
}
.chakra-wisdom-text {
    color: @wisdom_400;
}

.chakra-heart {
    border-left-color: @heart_500;
}
.chakra-heart .victory-node {
    background: @heart_500;
    box-shadow: 0 0 12px @heart_500;
}
.chakra-heart-text {
    color: @heart_400;
}

.chakra-intuition {
    border-left-color: @intuition_500;
}
.chakra-intuition .victory-node {
    background: @intuition_500;
    box-shadow: 0 0 12px @intuition_500;
}
.chakra-intuition-text {
    color: @intuition_400;
}

.chakra-sacred {
    border-left-color: @sacred_500;
}
.chakra-sacred .victory-node {
    background: @sacred_500;
    box-shadow: 0 0 12px @sacred_500;
}
.chakra-sacred-text {
    color: @sacred_400;
}

.chakra-primary {
    border-left-color: @primary_500;
}
.chakra-primary .victory-node {
    background: @primary_500;
    box-shadow: 0 0 12px @primary_500;
}
.chakra-primary-text {
    color: @primary_400;
}

/* Victory Node (Timeline circles) */
.victory-node {
    border-radius: 50%;
    min-width: 12px;
    min-height: 12px;
}

/* Timeline Line */
.timeline-line {
    background: rgba(99, 102, 241, 0.3);
    min-width: 2px;
    margin-left: 5px;
    margin-right: 5px;
}

/* NOW Marker */
.now-marker {
    background: linear-gradient(90deg,
        rgba(0, 217, 255, 0.15) 0%,
        rgba(0, 255, 136, 0.10) 100%);
    border-radius: 12px;
    padding: 12px 16px;
    border: 1px solid rgba(0, 217, 255, 0.3);
    box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
}

.now-marker-text {
    color: @cyan_500;
    font-weight: 800;
    letter-spacing: 2px;
}

/* === WELCOME HEADER === */
.welcome-header {
    background: linear-gradient(180deg,
        rgba(249, 115, 22, 0.08) 0%,
        transparent 100%);
    padding: 32px;
    border-radius: 0 0 32px 32px;
}

/* === STAT BADGES === */
.stat-badge {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    padding: 12px 20px;
    min-width: 70px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: all 200ms ease;
}

.stat-badge:hover {
    background: rgba(255, 255, 255, 0.06);
    transform: translateY(-2px);
}

/* Give each stat badge a subtle chakra glow on hover */
.stat-badge.chakra-divine:hover {
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.2);
    border-color: rgba(168, 85, 247, 0.3);
}

.stat-badge.chakra-wisdom:hover {
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.2);
    border-color: rgba(245, 158, 11, 0.3);
}

.stat-badge.chakra-heart:hover {
    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.2);
    border-color: rgba(16, 185, 129, 0.3);
}

.stat-badge.chakra-intuition:hover {
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.3);
}

/* ═══════════════════════════════════════════════════════════════════════════════
   5W KONTROL PANEL - HVAD/HVOR/HVORFOR/HVORDAN/HVORNÅR
   Ordblind-venlig: Store ikoner, klar farvekodning, minimal tekst
   ═══════════════════════════════════════════════════════════════════════════════ */

/* Basis for alle 5W rows */
.w5-hvad, .w5-hvor, .w5-hvorfor, .w5-hvordan, .w5-hvornaar {
    padding: 12px 16px;
    border-radius: 12px;
    margin: 4px 0;
    border-left: 4px solid transparent;
    transition: all 200ms ease;
}

.w5-hvad:hover, .w5-hvor:hover, .w5-hvorfor:hover,
.w5-hvordan:hover, .w5-hvornaar:hover {
    background: rgba(255, 255, 255, 0.03);
}

/* HVAD - Divine Violet */
.w5-hvad {
    border-left-color: @divine_500;
    background: rgba(168, 85, 247, 0.05);
}

/* HVOR - Wisdom Gold */
.w5-hvor {
    border-left-color: @wisdom_500;
    background: rgba(245, 158, 11, 0.05);
}
.w5-hvor:hover {
    background: rgba(245, 158, 11, 0.1);
}

/* HVORFOR - Heart Emerald */
.w5-hvorfor {
    border-left-color: @heart_500;
    background: rgba(16, 185, 129, 0.05);
}

/* HVORDAN - Intuition Indigo */
.w5-hvordan {
    border-left-color: @intuition_500;
    background: rgba(99, 102, 241, 0.05);
}

/* HVORNÅR - Sacred Magenta */
.w5-hvornaar {
    border-left-color: @sacred_500;
    background: rgba(217, 70, 239, 0.05);
}

/* Pass Badges (1, 2, 3) */
.pass-badge {
    min-width: 28px;
    min-height: 28px;
    border-radius: 50%;
    background: @surface_3;
    color: @text_tertiary;
    font-weight: 700;
    font-size: 12px;
    padding: 4px;
}

.pass-badge.pass-complete {
    background: @heart_500;
    color: white;
    box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
}

.pass-badge.pass-active {
    background: @primary_500;
    color: white;
    box-shadow: 0 0 12px rgba(249, 115, 22, 0.5);
}

/* ═══════════════════════════════════════════════════════════════════════════════
   ORDBLIND-VENLIG NAVIGATION
   Store ikoner, klar farvekodning, synlige keyboard hints
   ═══════════════════════════════════════════════════════════════════════════════ */

/* Store knapper med synlige hints */
button.large-action {
    min-height: 48px;
    min-width: 48px;
    border-radius: 12px;
}

button.large-action image {
    -gtk-icon-size: 32px;
}

/* Keyboard shortcut hints synlige på hover */
.keyboard-shortcut {
    font-size: 10px;
    font-weight: 700;
    color: @text_tertiary;
    background: rgba(255, 255, 255, 0.08);
    padding: 2px 6px;
    border-radius: 4px;
    margin-left: 8px;
    opacity: 0;
    transition: opacity 150ms ease;
}

*:hover > .keyboard-shortcut {
    opacity: 1;
}

/* Altid synlige shortcuts i toolbar */
.shortcut-always-visible {
    opacity: 1;
}

/* Handlings-farver for knapper */
button.action-verify {
    background: rgba(16, 185, 129, 0.2);
    border: 1px solid @heart_500;
}

button.action-archive {
    background: rgba(168, 85, 247, 0.2);
    border: 1px solid @divine_500;
}

button.action-predict {
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid @intuition_500;
}

button.action-new {
    background: rgba(249, 115, 22, 0.2);
    border: 1px solid @primary_500;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   ACHIEVEMENT BADGES
   ═══════════════════════════════════════════════════════════════════════════════ */

.achievement-panel {
    background: linear-gradient(180deg,
        rgba(26, 31, 58, 0.8) 0%,
        rgba(10, 14, 39, 0.9) 100%);
    border-radius: 16px;
    border: 1px solid rgba(99, 102, 241, 0.1);
    margin: 12px;
}

.achievement-badge {
    padding: 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid transparent;
    min-width: 70px;
    transition: all 200ms ease;
}

.achievement-badge.unlocked {
    border-color: rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.achievement-badge.unlocked:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.achievement-badge.locked {
    opacity: 0.4;
}

.achievement-icon {
    font-size: 24px;
}

/* Chakra glow for unlocked achievements */
.achievement-badge.unlocked.chakra-divine {
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.3);
}

.achievement-badge.unlocked.chakra-wisdom {
    box-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
}

.achievement-badge.unlocked.chakra-heart {
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}

.achievement-badge.unlocked.chakra-sacred {
    box-shadow: 0 0 20px rgba(217, 70, 239, 0.3);
}

/* ═══════════════════════════════════════════════════════════════════════════════
   FILTRE & SORTERING
   ═══════════════════════════════════════════════════════════════════════════════ */

.filter-bar {
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.02);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.filter-chip {
    padding: 4px 12px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.05);
    font-size: 12px;
    transition: all 150ms ease;
}

.filter-chip:hover {
    background: rgba(255, 255, 255, 0.1);
}

.filter-chip.active {
    background: @primary_500;
    color: white;
}

.filter-chip.chakra-divine.active {
    background: @divine_500;
}

.filter-chip.chakra-wisdom.active {
    background: @wisdom_500;
}

.filter-chip.chakra-heart.active {
    background: @heart_500;
}

/* Sort dropdown */
.sort-dropdown {
    min-width: 120px;
    padding: 4px 8px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
}

/* ═══════════════════════════════════════════════════════════════════════════════
   LIVE AKTIVITETS MONITOR - WORLD CLASS REAL-TIME
   ═══════════════════════════════════════════════════════════════════════════════ */

.live-activity-monitor {
    background: linear-gradient(180deg,
        rgba(10, 14, 39, 0.95) 0%,
        rgba(15, 18, 41, 0.90) 100%);
    border-top: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 16px 16px 0 0;
    margin-top: 8px;
    box-shadow:
        0 -8px 32px -8px rgba(0, 0, 0, 0.5),
        0 0 60px -20px rgba(99, 102, 241, 0.15) inset;
}

.activity-header {
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 16px 16px 0 0;
}

.pulse-indicator {
    font-size: 12px;
    color: @success_400;
    opacity: 0.6;
    transition: all 300ms ease;
}

.pulse-indicator.pulse-on {
    color: @success_500;
    opacity: 1.0;
}

.activity-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: rgba(255, 255, 255, 0.9);
}

.status-badge-active {
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1));
    color: @success_400;
    border: 1px solid rgba(34, 197, 94, 0.3);
}

.activity-list {
    background: transparent;
}

.activity-row {
    background: transparent;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    transition: all 150ms ease;
}

.activity-row:hover {
    background: rgba(99, 102, 241, 0.05);
}

.activity-icon {
    font-size: 14px;
    min-width: 24px;
}

.activity-timestamp {
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.4);
    min-width: 70px;
}

.activity-source {
    font-size: 11px;
    font-weight: 600;
    color: @intuition_400;
    min-width: 100px;
}

.activity-message {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.75);
}

.five-w-bar {
    padding: 8px 16px;
    background: rgba(0, 0, 0, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.five-w-item {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.6);
    padding: 4px 8px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 6px;
}
"""

def load_custom_css():
    """Load modern CSS styling"""
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(MODERN_CSS.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

def send_notification(title: str, body: str, icon: str = "emblem-ok-symbolic"):
    """Send desktop notification"""
    try:
        subprocess.run([
            "notify-send",
            "-i", icon,
            "-a", "Victory List Masterpiece",
            title,
            body
        ], check=False)
    except:
        pass

def get_system_stats() -> dict:
    """Get overall system statistics"""
    stats = {
        "total_victorys": 0,
        "active": 0,
        "archived": 0,
        "total_checkboxes": 0,
        "completed_checkboxes": 0,
        "grand_admirals": 0,
    }

    if ACTIVE_DIR.exists():
        for folder in ACTIVE_DIR.iterdir():
            if folder.is_dir() and not folder.name.startswith("."):
                stats["active"] += 1
                stats["total_victorys"] += 1
                sejr_file = folder / "SEJR_LISTE.md"
                if sejr_file.exists():
                    done, total = count_checkboxes(sejr_file.read_text())
                    stats["total_checkboxes"] += total
                    stats["completed_checkboxes"] += done

    if ARCHIVE_DIR.exists():
        for folder in ARCHIVE_DIR.iterdir():
            if folder.is_dir() and not folder.name.startswith("."):
                stats["archived"] += 1
                stats["total_victorys"] += 1
                # Check for Grand Admiral (27+ score)
                conclusion = folder / "CONCLUSION.md"
                if conclusion.exists():
                    content = conclusion.read_text()
                    if "GRAND ADMIRAL" in content or "27/30" in content or "30/30" in content:
                        stats["grand_admirals"] += 1

    return stats

# ═══════════════════════════════════════════════════════════════════════════════
# INTELLIGENT SEARCH ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# UNIVERSAL SEJR CONVERTER - FRA ALT TIL SEJR STRUKTUR
# ═══════════════════════════════════════════════════════════════════════════════

class SejrConverter:
    """
    Universal converter: Enhver mappe, fil, PDF, tekst, kommando → SEJR struktur

    MULTI-KONTROLBART:
    - Manual mode: Rasmus styrer alt
    - Kv1nt mode: AI-assisteret med forslag
    - Admiral mode: Fuldt automatisk med verifikation

    5W KONTROL:
    - HVAD: Hvad konverteres
    - HVOR: Hvor gemmes det
    - HVORFOR: Formål med sejren
    - HVORDAN: Hvilken tilgang
    - HVORNÅR: Timeline og milestones
    """

    INPUT_TYPES = {
        "folder": "📁 Folder",
        "file": "📄 Fil",
        "pdf": "📕 PDF",
        "text": "📝 Tekst",
        "command": "💻 Kommando",
    }

    CONTROL_MODES = {
        "manual": "✋ Manuel - Du styrer ALT",
        "kv1nt": "🤖 Kv1nt - AI-assisteret med forslag",
        "admiral": "🎖️ Admiral - Fuld automatisk",
    }

    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.active_dir = system_path / "10_ACTIVE"
        self.templates_dir = system_path / "00_TEMPLATES"

    def analyze_input(self, input_path: str, input_type: str) -> dict:
        """Analyze input and suggest SEJR structure"""
        analysis = {
            "input_path": input_path,
            "input_type": input_type,
            "exists": False,
            "suggested_name": "",
            "suggested_tasks": [],
            "file_count": 0,
            "total_size": 0,
            "detected_sections": [],
        }

        path = Path(input_path)

        if input_type == "folder" and path.exists() and path.is_dir():
            analysis["exists"] = True
            analysis["suggested_name"] = path.name.upper().replace(" ", "_")
            files = list(path.rglob("*"))
            analysis["file_count"] = len([f for f in files if f.is_file()])
            analysis["total_size"] = sum(f.stat().st_size for f in files if f.is_file())

            # Detect structure
            for f in files[:20]:  # First 20 files
                if f.is_file():
                    analysis["suggested_tasks"].append(f"Behandl {f.name}")

        elif input_type == "file" and path.exists() and path.is_file():
            analysis["exists"] = True
            analysis["suggested_name"] = path.stem.upper().replace(" ", "_")
            analysis["file_count"] = 1
            analysis["total_size"] = path.stat().st_size

            # Read and analyze content
            if path.suffix in [".md", ".txt"]:
                try:
                    content = path.read_text()
                    # Find headers as tasks
                    for line in content.split("\n"):
                        if line.startswith("# ") or line.startswith("## "):
                            analysis["detected_sections"].append(line.strip("#").strip())
                except:
                    pass

        elif input_type == "text":
            analysis["exists"] = True
            analysis["suggested_name"] = "TEKST_PROJEKT"
            # Parse text for structure
            lines = input_path.split("\n")
            for line in lines:
                if line.strip():
                    analysis["suggested_tasks"].append(f"[ ] {line.strip()[:50]}")

        elif input_type == "command":
            analysis["exists"] = True
            analysis["suggested_name"] = "KOMMANDO_SEJR"
            analysis["suggested_tasks"] = [
                "[ ] Run command",
                "[ ] Verify output",
                "[ ] Dokumenter resultat",
            ]

        return analysis

    def create_sejr_from_input(self, config: dict) -> Path:
        """
        Create SEJR structure from analyzed input

        config = {
            "name": "PROJEKT_NAVN",
            "input_path": "/path/to/input",
            "input_type": "folder|file|pdf|text|command",
            "mode": "manual|kv1nt|admiral",
            "hvad": "Beskrivelse af hvad",
            "hvor": "Destination folder",
            "hvorfor": "Formål",
            "hvordan": "Tilgang",
            "hvornaar": "Timeline",
            "tasks": ["Task 1", "Task 2", ...],
        }
        """
        # Generate folder name with date
        date_str = datetime.now().strftime("%Y-%m-%d")
        folder_name = f"{config['name']}_{date_str}"
        sejr_path = self.active_dir / folder_name

        # Create folder
        sejr_path.mkdir(parents=True, exist_ok=True)

        # Generate SEJR_LISTE.md content
        victory_content = f"""# SEJR: {config['name']}

**Oprettet:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Status:** 🔵 PASS 1 - IN PROGRESS
**Ejer:** Rasmus + Kv1nt
**Current Pass:** 1/3

**Kilde:** {config.get('input_type', 'unknown')} → {config.get('input_path', 'N/A')}
**Mode:** {config.get('mode', 'manual')}

---

## 5W KONTROL

| Kontrol | Værdi |
|---------|-------|
| **HVAD** | {config.get('hvad', 'Konvertering til victory struktur')} |
| **HVOR** | {sejr_path} |
| **HVORFOR** | {config.get('hvorfor', 'Systematisk eksekvering')} |
| **HVORDAN** | {config.get('hvordan', '3-pass system')} |
| **HVORNÅR** | {config.get('hvornaar', 'Nu → Complete')} |

---

## ⚠️ 3-PASS KONKURRENCE SYSTEM (OBLIGATORISK)

```
PASS 1: FUNGERENDE     → "Get it working"      → REVIEW REQUIRED
PASS 2: FORBEDRET      → "Make it better"      → REVIEW REQUIRED
PASS 3: OPTIMERET      → "Make it best"        → FINAL VERIFICATION
                                                        ↓
                                               ✅ KAN ARKIVERES
```

---

# 🥉 PASS 1: FUNGERENDE ("Get It Working")

## Tasks

"""
        # Add tasks
        for task in config.get('tasks', []):
            if not task.startswith("- [ ]"):
                task = f"- [ ] {task}"
            sejr_content += f"{task}\n"

        victory_content += """
---

## Verification

- [ ] Alle tasks completeret
- [ ] Output verificeret
- [ ] Ready for Pass 2

---

# 🥈 PASS 2: FORBEDRET ("Make It Better")

*Udfyldes efter Pass 1 er færdig*

---

# 🥇 PASS 3: OPTIMERET ("Make It Best")

*Udfyldes efter Pass 2 er færdig*
"""

        # Write SEJR_LISTE.md
        (sejr_path / "SEJR_LISTE.md").write_text(sejr_content)

        # Create CLAUDE.md focus lock
        claude_content = f"""# CLAUDE FOKUS LOCK - LÆS DETTE FØRST

> **DU ER I EN SEJR LISTE MAPPE. DU HAR ÉN OPGAVE. FOKUSÉR.**

---

## 🔒 CURRENT STATE

**Sejr:** {config['name']}
**Current Pass:** 1/3
**Status:** Pass 1 - Fungerende
**Input:** {config.get('input_type', 'unknown')}

---

## 🎯 DIN ENESTE OPGAVE RIGHT NOW

```
Læs SEJR_LISTE.md og arbejd på første task
```

**INTET ANDET.** Færdiggør dette før du gør noget andet.
"""
        (sejr_path / "CLAUDE.md").write_text(claude_content)

        # Create STATUS.yaml
        status_content = f"""# SEJR STATUS
name: {config['name']}
created: {datetime.now().isoformat()}
current_pass: 1
status: in_progress

input:
  type: {config.get('input_type', 'unknown')}
  path: {config.get('input_path', 'N/A')}

control:
  mode: {config.get('mode', 'manual')}
  hvad: {config.get('hvad', '')}
  hvor: {str(sejr_path)}
  hvorfor: {config.get('hvorfor', '')}
  hvordan: {config.get('hvordan', '')}
  hvornaar: {config.get('hvornaar', '')}

passes:
  pass_1:
    status: in_progress
    score: 0
  pass_2:
    status: pending
    score: 0
  pass_3:
    status: pending
    score: 0
"""
        (sejr_path / "STATUS.yaml").write_text(status_content)

        # Initialize AUTO_LOG.jsonl
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "victory_created",
            "source": config.get('input_type', 'unknown'),
            "mode": config.get('mode', 'manual'),
            "detail": f"Oprettet fra {config.get('input_path', 'N/A')}"
        }
        (sejr_path / "AUTO_LOG.jsonl").write_text(json.dumps(log_entry) + "\n")

        return sejr_path


class IntelligentSearch:
    """
    Intelligent search across all sejr files, code, and details.
    Searches: filenames, file contents, checkboxes, logs, code patterns
    """

    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.active_dir = system_path / "10_ACTIVE"
        self.archive_dir = system_path / "90_ARCHIVE"

    def search(self, query: str, max_results: int = 50) -> list:
        """
        Search for query across all sejr folders.
        Returns list of dicts with: sejr, file, line_num, context, match_type
        """
        if not query or len(query) < 2:
            return []

        results = []
        query_lower = query.lower()

        # Search active victorys
        if self.active_dir.exists():
            for sejr_folder in self.active_dir.iterdir():
                if sejr_folder.is_dir() and not sejr_folder.name.startswith("."):
                    results.extend(self._search_sejr(sejr_folder, query_lower))

        # Search archived victorys
        if self.archive_dir.exists():
            for sejr_folder in self.archive_dir.iterdir():
                if sejr_folder.is_dir() and not sejr_folder.name.startswith("."):
                    results.extend(self._search_sejr(sejr_folder, query_lower))

        # Sort by relevance (exact matches first, then partial)
        results.sort(key=lambda x: (0 if query_lower in x["match"].lower() else 1, x["victory"]))

        return results[:max_results]

    def _search_sejr(self, sejr_folder: Path, query: str) -> list:
        """Search within a single victory folder"""
        results = []

        # Search folder name
        if query in sejr_folder.name.lower():
            results.append({
                "victory": sejr_folder.name,
                "file": "(folder name)",
                "line_num": 0,
                "context": sejr_folder.name,
                "match": sejr_folder.name,
                "match_type": "folder"
            })

        # Search files
        for file_path in sejr_folder.iterdir():
            if file_path.is_file():
                results.extend(self._search_file(file_path, sejr_folder.name, query))

        return results

    def _search_file(self, file_path: Path, sejr_name: str, query: str) -> list:
        """Search within a single file"""
        results = []

        # Search filename
        if query in file_path.name.lower():
            results.append({
                "victory": sejr_name,
                "file": file_path.name,
                "line_num": 0,
                "context": f"Filename: {file_path.name}",
                "match": file_path.name,
                "match_type": "filename"
            })

        # Search file contents
        try:
            if file_path.suffix in [".md", ".yaml", ".txt", ".py"]:
                content = file_path.read_text(errors="ignore")
                for i, line in enumerate(content.split("\n"), 1):
                    if query in line.lower():
                        # Get context (surrounding text)
                        context = line.strip()[:100]
                        if len(line.strip()) > 100:
                            context += "..."

                        results.append({
                            "victory": sejr_name,
                            "file": file_path.name,
                            "line_num": i,
                            "context": context,
                            "match": self._extract_match(line, query),
                            "match_type": "content"
                        })

            elif file_path.suffix == ".jsonl":
                # Parse JSONL logs
                content = file_path.read_text(errors="ignore")
                for i, line in enumerate(content.split("\n"), 1):
                    if line.strip() and query in line.lower():
                        try:
                            data = json.loads(line)
                            context = f"{data.get('action', 'unknown')}: {data.get('detail', line[:50])}"
                        except:
                            context = line[:100]

                        results.append({
                            "victory": sejr_name,
                            "file": file_path.name,
                            "line_num": i,
                            "context": context[:100],
                            "match": self._extract_match(line, query),
                            "match_type": "log"
                        })
        except Exception as e:
            pass

        return results

    def _extract_match(self, line: str, query: str) -> str:
        """Extract the matching portion with some context"""
        line_lower = line.lower()
        idx = line_lower.find(query)
        if idx == -1:
            return query

        start = max(0, idx - 10)
        end = min(len(line), idx + len(query) + 10)

        match = line[start:end]
        if start > 0:
            match = "..." + match
        if end < len(line):
            match = match + "..."

        return match

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PATH = Path(__file__).parent
ACTIVE_DIR = SYSTEM_PATH / "10_ACTIVE"
ARCHIVE_DIR = SYSTEM_PATH / "90_ARCHIVE"
SCRIPTS_DIR = SYSTEM_PATH / "scripts"

DNA_LAYERS = [
    ("1", "SELF-AWARE", "System kender sig selv", "emblem-system-symbolic"),
    ("2", "SELF-DOCUMENTING", "Auto-logger actioner", "document-edit-symbolic"),
    ("3", "SELF-VERIFYING", "Auto-verificerer", "emblem-ok-symbolic"),
    ("4", "SELF-IMPROVING", "Learning patterns", "view-refresh-symbolic"),
    ("5", "SELF-ARCHIVING", "Archiveer semantisk", "folder-symbolic"),
    ("6", "PREDICTIVE", "Predicter næste", "weather-clear-symbolic"),
    ("7", "SELF-OPTIMIZING", "3 alternativer", "applications-engineering-symbolic"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def count_checkboxes(content: str) -> tuple:
    """Count checked and total checkboxes"""
    checked = len(re.findall(r'- \[[xX]\]', content))
    unchecked = len(re.findall(r'- \[ \]', content))
    return checked, checked + unchecked

def get_sejr_info(path: Path) -> dict:
    """Get comprehensive info about a victory"""
    sejr_file = path / "SEJR_LISTE.md"
    status_file = path / "STATUS.yaml"

    info = {
        "name": path.name,
        "path": str(path),
        "display_name": path.name.split("_2026")[0].replace("_", " "),
        "progress": 0,
        "done": 0,
        "total": 0,
        "current_pass": "1",
        "is_archived": "90_ARCHIVE" in str(path),
        "files": [],
        "date": "Unknown",
    }

    # Extract date from folder name
    if "2026-01-" in path.name:
        try:
            date_part = path.name.split("2026-01-")[1][:2]
            info["date"] = f"Yesn {date_part}, 2026"
        except:
            pass

    # Count checkboxes
    if sejr_file.exists():
        content = sejr_file.read_text()
        done, total = count_checkboxes(content)
        info["done"] = done
        info["total"] = total
        info["progress"] = int((done / total * 100) if total > 0 else 0)

        # Find current pass
        if "Pass 3" in content and "PASS 3" in content.upper():
            info["current_pass"] = "3"
        elif "Pass 2" in content and "PASS 2" in content.upper():
            info["current_pass"] = "2"

    # List files
    if path.exists():
        info["files"] = [f.name for f in path.iterdir() if f.is_file()]

    return info

def get_all_sejrs() -> list:
    """Get all victorys sorted by date"""
    sejrs = []

    if ACTIVE_DIR.exists():
        for folder in sorted(ACTIVE_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if folder.is_dir() and not folder.name.startswith("."):
                sejrs.append(get_sejr_info(folder))

    if ARCHIVE_DIR.exists():
        for folder in sorted(ARCHIVE_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if folder.is_dir() and not folder.name.startswith("."):
                sejrs.append(get_sejr_info(folder))

    return sejrs

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM WIDGETS
# ═══════════════════════════════════════════════════════════════════════════════

class SejrRow(Adw.ActionRow):
    """A row representing a victory in the sidebar"""

    def __init__(self, sejr_info: dict):
        super().__init__()
        self.sejr_info = sejr_info

        self.set_title(sejr_info["display_name"])
        self.set_subtitle(f"Pass {sejr_info['current_pass']}/3 • {sejr_info['date']}")

        # Icon based on status
        if sejr_info["is_archived"]:
            icon = Gtk.Image.new_from_icon_name("emblem-ok-symbolic")
            icon.add_css_class("success")
        elif sejr_info["progress"] >= 80:
            icon = Gtk.Image.new_from_icon_name("emblem-important-symbolic")
            icon.add_css_class("warning")
        else:
            icon = Gtk.Image.new_from_icon_name("folder-open-symbolic")

        self.add_prefix(icon)

        # Progress indicator
        progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        progress_box.set_valign(Gtk.Align.CENTER)

        progress_label = Gtk.Label(label=f"{sejr_info['progress']}%")
        progress_label.add_css_class("caption")
        progress_box.append(progress_label)

        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(sejr_info["progress"] / 100)
        progress_bar.set_size_request(60, 4)

        if sejr_info["progress"] >= 80:
            progress_bar.add_css_class("success")
        elif sejr_info["progress"] >= 50:
            progress_bar.add_css_class("warning")

        progress_box.append(progress_bar)
        self.add_suffix(progress_box)

        # Make it activatable
        self.set_activatable(True)


# ═══════════════════════════════════════════════════════════════════════════════
# CHAT STREAM WIDGET - MESSENGER-STYLE INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

class ChatMessage(Gtk.Box):
    """A single chat message in the stream - like Messenger"""

    def __init__(self, sender: str, content: str, timestamp: str = None,
                 msg_type: str = "info", file_link: str = None, verification: dict = None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        self.file_link = file_link

        # Determine if this is user message (right side) or system (left side)
        is_user = sender.lower() in ["rasmus", "bruger", "dig", "user"]

        if is_user:
            self.set_halign(Gtk.Align.END)
        else:
            self.set_halign(Gtk.Align.START)

        self.set_margin_start(12 if not is_user else 60)
        self.set_margin_end(12 if is_user else 60)
        self.set_margin_top(4)
        self.set_margin_bottom(4)

        # Avatar (only for non-user messages)
        if not is_user:
            avatar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            avatar_box.set_valign(Gtk.Align.START)

            # Emoji avatar based on sender
            avatar_emojis = {
                "system": "🖥️",
                "kv1nt": "🤖",
                "admiral": "🎖️",
                "dna": "🧬",
                "verify": "✅",
                "error": "❌",
                "info": "💬",
            }
            emoji = avatar_emojis.get(sender.lower(), "💬")

            avatar_label = Gtk.Label(label=emoji)
            avatar_label.set_markup(f'<span size="large">{emoji}</span>')
            avatar_box.append(avatar_label)

            self.append(avatar_box)

        # Message bubble
        bubble = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        bubble.add_css_class("chat-bubble")
        if is_user:
            bubble.add_css_class("chat-bubble-user")
        else:
            bubble.add_css_class("chat-bubble-system")

        # Sender name (only for non-user)
        if not is_user:
            sender_label = Gtk.Label(label=sender.upper())
            sender_label.set_halign(Gtk.Align.START)
            sender_label.add_css_class("caption")
            sender_label.add_css_class("chat-sender")
            bubble.append(sender_label)

        # Main content
        content_label = Gtk.Label(label=content)
        content_label.set_halign(Gtk.Align.START if not is_user else Gtk.Align.END)
        content_label.set_wrap(True)
        content_label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        content_label.set_max_width_chars(50)
        content_label.set_selectable(True)
        bubble.append(content_label)

        # File link if provided
        if file_link:
            link_btn = Gtk.Button()
            link_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            link_box.append(Gtk.Image.new_from_icon_name("document-open-symbolic"))
            link_box.append(Gtk.Label(label=Path(file_link).name))
            link_btn.set_child(link_box)
            link_btn.add_css_class("flat")
            link_btn.add_css_class("chat-link")
            link_btn.connect("clicked", self._on_file_clicked)
            bubble.append(link_btn)

        # Verification status if provided
        if verification:
            verify_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            verify_box.add_css_class("chat-verification")

            status_icon = "emblem-ok-symbolic" if verification.get("passed") else "dialog-warning-symbolic"
            verify_box.append(Gtk.Image.new_from_icon_name(status_icon))

            verify_label = Gtk.Label(label=verification.get("message", "Verifyet"))
            verify_label.add_css_class("caption")
            if verification.get("passed"):
                verify_label.add_css_class("success")
            else:
                verify_label.add_css_class("warning")
            verify_box.append(verify_label)

            bubble.append(verify_box)

        # Timestamp
        if timestamp:
            time_label = Gtk.Label(label=timestamp)
            time_label.set_halign(Gtk.Align.END if is_user else Gtk.Align.START)
            time_label.add_css_class("caption")
            time_label.add_css_class("dim-label")
            time_label.add_css_class("chat-timestamp")
            bubble.append(time_label)

        self.append(bubble)

        # Avatar for user (on right side)
        if is_user:
            avatar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            avatar_box.set_valign(Gtk.Align.START)
            avatar_label = Gtk.Label()
            avatar_label.set_markup('<span size="large">👤</span>')
            avatar_box.append(avatar_label)
            self.append(avatar_box)

    def _on_file_clicked(self, button):
        """Open the linked file"""
        if self.file_link:
            try:
                subprocess.Popen(["xdg-open", self.file_link])
            except:
                pass


class ChatStream(Gtk.Box):
    """A scrollable chat stream showing activity like Messenger"""

    def __init__(self, sejr_path: Path = None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.sejr_path = sejr_path
        self.messages = []

        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header_box.set_margin_start(12)
        header_box.set_margin_end(12)
        header_box.set_margin_top(8)
        header_box.set_margin_bottom(8)

        chat_icon = Gtk.Image.new_from_icon_name("chat-symbolic")
        header_box.append(chat_icon)

        header_label = Gtk.Label(label="Activity Stream")
        header_label.add_css_class("heading")
        header_box.append(header_label)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        header_box.append(spacer)

        # Clear button
        clear_btn = Gtk.Button(icon_name="edit-clear-symbolic")
        clear_btn.add_css_class("flat")
        clear_btn.set_tooltip_text("Ryd stream")
        clear_btn.connect("clicked", lambda b: self.clear_messages())
        header_box.append(clear_btn)

        self.append(header_box)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(sep)

        # Scrollable message area
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_min_content_height(200)

        self.message_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.message_box.add_css_class("chat-stream-messages")
        scroll.set_child(self.message_box)

        self.append(scroll)
        self.scroll_window = scroll

        # Load existing messages from AUTO_LOG.jsonl if available
        if sejr_path:
            self._load_from_log(sejr_path)

    def _load_from_log(self, sejr_path: Path):
        """Load messages from AUTO_LOG.jsonl"""
        log_file = sejr_path / "AUTO_LOG.jsonl"
        if not log_file.exists():
            # Add welcome message
            self.add_message(
                sender="Kv1nt",
                content=f"Welcome to {victory_path.name.split('_2026')[0].replace('_', ' ')}! I am watching everything that happens here.",
                msg_type="info"
            )
            return

        try:
            content = log_file.read_text()
            for line in content.strip().split("\n")[-20:]:  # Last 20 entries
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)

                    # Determine sender based on action
                    action = data.get("action", "unknown")
                    if "verify" in action.lower():
                        sender = "Verify"
                    elif "dna" in action.lower():
                        sender = "DNA"
                    elif "user" in action.lower() or "rasmus" in action.lower():
                        sender = "Rasmus"
                    else:
                        sender = "System"

                    # Extract content
                    detail = data.get("detail", data.get("message", str(data)))
                    timestamp = data.get("timestamp", "")
                    if timestamp and len(timestamp) > 16:
                        timestamp = timestamp[11:16]  # Just HH:MM

                    # File link if present
                    file_link = data.get("file", data.get("path"))

                    # Verification if present
                    verification = None
                    if "verify" in action.lower() or "test" in action.lower():
                        verification = {
                            "passed": data.get("passed", data.get("success", True)),
                            "message": data.get("result", "Verifyet")
                        }

                    self.add_message(
                        sender=sender,
                        content=detail[:200],
                        timestamp=timestamp,
                        file_link=file_link,
                        verification=verification
                    )
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            self.add_message(
                sender="System",
                content=f"Could not read log: {e}",
                msg_type="error"
            )

    def add_message(self, sender: str, content: str, timestamp: str = None,
                    msg_type: str = "info", file_link: str = None, verification: dict = None):
        """Add a new message to the stream"""
        if not timestamp:
            timestamp = datetime.now().strftime("%H:%M")

        msg = ChatMessage(
            sender=sender,
            content=content,
            timestamp=timestamp,
            msg_type=msg_type,
            file_link=file_link,
            verification=verification
        )

        self.message_box.append(msg)
        self.messages.append(msg)

        # Auto-scroll to bottom
        GLib.idle_add(self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        adj = self.scroll_window.get_vadjustment()
        adj.set_value(adj.get_upper())
        return False

    def clear_messages(self):
        """Clear all messages"""
        while child := self.message_box.get_first_child():
            self.message_box.remove(child)
        self.messages = []

        # Add cleared message
        self.add_message(
            sender="System",
            content="Stream ryddet",
            msg_type="info"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# KONFETTI ANIMATION - CELEBRATION WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class KonfettiOverlay(Gtk.Overlay):
    """
    Konfetti animation overlay for celebrations.

    Triggers when:
    - A sejr reaches 100% completion
    - A Pass is completed (Pass 1→2→3)
    - Admiral status is achieved (30/30)

    Note: Uses GTK4 Snapshot API instead of cairo for compatibility.
    """

    def __init__(self):
        super().__init__()
        self.particles = []
        self.animation_active = False
        self.drawing_area = None

    def _ensure_drawing_area(self):
        """Create drawing area on demand"""
        if self.drawing_area is None:
            self.drawing_area = Gtk.DrawingArea()
            self.drawing_area.set_draw_func(self._draw_konfetti)
            self.drawing_area.set_can_target(False)  # Click-through
            self.add_overlay(self.drawing_area)

    def celebrate(self, level: str = "normal"):
        """Trigger celebration animation"""
        import random

        if self.animation_active:
            return

        # Create drawing area on first celebration
        try:
            self._ensure_drawing_area()
        except Exception as e:
            print(f"🎉 Celebration! (konfetti fejlede: {e})")
            return

        self.animation_active = True

        # Generate particles
        colors = [
            (168/255, 85/255, 247/255),   # Divine violet
            (249/255, 115/255, 22/255),   # Primary orange
            (16/255, 185/255, 129/255),   # Heart emerald
            (99/255, 102/255, 241/255),   # Intuition indigo
            (245/255, 158/255, 11/255),   # Wisdom gold
        ]

        num_particles = 50 if level == "normal" else 100 if level == "admiral" else 30

        for _ in range(num_particles):
            self.particles.append({
                'x': random.uniform(0, 1),
                'y': -0.1,
                'vx': random.uniform(-0.02, 0.02),
                'vy': random.uniform(0.01, 0.03),
                'color': random.choice(colors),
                'size': random.uniform(4, 12),
                'rotation': random.uniform(0, 360),
            })

        # Start animation
        GLib.timeout_add(16, self._animate)  # ~60 FPS

        # Auto-stop after 3 seconds
        GLib.timeout_add(3000, self._stop_animation)

    def _animate(self):
        """Update particle positions"""
        if not self.animation_active:
            return False

        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.001  # Gravity
            p['rotation'] += 5

        # Remove off-screen particles
        self.particles = [p for p in self.particles if p['y'] < 1.2]

        self.drawing_area.queue_draw()
        return self.animation_active and len(self.particles) > 0

    def _draw_konfetti(self, area, cr, width, height):
        """Draw konfetti particles"""
        try:
            for p in self.particles:
                cr.save()
                x = p['x'] * width
                y = p['y'] * height

                cr.translate(x, y)
                cr.rotate(p['rotation'] * 3.14159 / 180)

                # Set color with alpha
                cr.set_source_rgba(*p['color'], 0.9)

                # Draw square konfetti
                size = p['size']
                cr.rectangle(-size/2, -size/2, size, size)
                cr.fill()

                cr.restore()
        except Exception as e:
            # Cairo drawing failed - disable for future
            self.cairo_available = False
            self.animation_active = False
            self.particles = []

    def _stop_animation(self):
        """Stop the animation"""
        self.animation_active = False
        self.particles = []
        self.drawing_area.queue_draw()
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# ACHIEVEMENT BADGES SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

# Achievement definitions
ACHIEVEMENTS = {
    "first_victory": {
        "name": "First Victory",
        "icon": "🏆",
        "description": "Completegjorde your first victory",
        "color": "wisdom"
    },
    "admiral": {
        "name": "Admiral",
        "icon": "🎖️",
        "description": "Opnåede 30/30 score",
        "color": "divine"
    },
    "grand_admiral": {
        "name": "Grand Admiral",
        "icon": "👑",
        "description": "5+ victorye med Admiral status",
        "color": "sacred"
    },
    "speed_runner": {
        "name": "Speed Runner",
        "icon": "⚡",
        "description": "Completegjorde en victory in under 1 hour",
        "color": "cyan"
    },
    "perfectionist": {
        "name": "Perfectionist",
        "icon": "💯",
        "description": "100% completion på alle 3 passes",
        "color": "heart"
    },
    "streak_3": {
        "name": "On a Streak",
        "icon": "🔥",
        "description": "3 victories in a row without pause",
        "color": "primary"
    },
    "streak_7": {
        "name": "Ustoppelig",
        "icon": "💫",
        "description": "7 victories in a row - you are on fire!",
        "color": "intuition"
    }
}


class AchievementBadge(Gtk.Box):
    """A single achievement badge"""

    def __init__(self, achievement_id: str, unlocked: bool = False):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.achievement_id = achievement_id
        self.unlocked = unlocked

        ach = ACHIEVEMENTS.get(achievement_id, {})

        self.add_css_class("achievement-badge")
        if unlocked:
            self.add_css_class(f"chakra-{ach.get('color', 'primary')}")
            self.add_css_class("unlocked")
        else:
            self.add_css_class("locked")

        # Icon
        icon_label = Gtk.Label(label=ach.get("icon", "❓"))
        icon_label.add_css_class("achievement-icon")
        if not unlocked:
            icon_label.add_css_class("dim-label")
        self.append(icon_label)

        # Name
        name_label = Gtk.Label(label=ach.get("name", "Unknown"))
        name_label.add_css_class("caption")
        if not unlocked:
            name_label.add_css_class("dim-label")
        self.append(name_label)

        # Tooltip with description
        self.set_tooltip_text(ach.get("description", ""))


class AchievementPanel(Gtk.Box):
    """Panel showing all achievements"""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add_css_class("achievement-panel")

        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.set_margin_start(16)
        header.set_margin_end(16)
        header.set_margin_top(12)

        trophy = Gtk.Label(label="🏆")
        trophy.set_markup('<span size="large">🏆</span>')
        header.append(trophy)

        title = Gtk.Label(label="Achievements")
        title.add_css_class("heading")
        header.append(title)

        # Count
        self.count_label = Gtk.Label(label="0/7")
        self.count_label.add_css_class("caption")
        self.count_label.add_css_class("dim-label")
        self.count_label.set_hexpand(True)
        self.count_label.set_halign(Gtk.Align.END)
        header.append(self.count_label)

        self.append(header)

        # Badge grid
        self.badge_grid = Gtk.FlowBox()
        self.badge_grid.set_selection_mode(Gtk.SelectionMode.NONE)
        self.badge_grid.set_max_children_per_line(4)
        self.badge_grid.set_column_spacing(8)
        self.badge_grid.set_row_spacing(8)
        self.badge_grid.set_margin_start(16)
        self.badge_grid.set_margin_end(16)
        self.badge_grid.set_margin_bottom(12)

        self.append(self.badge_grid)

        # Load achievements
        self._load_achievements()

    def _load_achievements(self):
        """Load and display achievements based on system stats"""
        stats = get_system_stats()

        unlocked_count = 0

        for ach_id in ACHIEVEMENTS:
            unlocked = self._check_achievement(ach_id, stats)
            if unlocked:
                unlocked_count += 1

            badge = AchievementBadge(ach_id, unlocked)
            self.badge_grid.append(badge)

        self.count_label.set_text(f"{unlocked_count}/{len(ACHIEVEMENTS)}")

    def _check_achievement(self, ach_id: str, stats: dict) -> bool:
        """Check if achievement is unlocked"""
        if ach_id == "first_victory":
            return stats["archived"] >= 1
        elif ach_id == "admiral":
            return stats["grand_admirals"] >= 1
        elif ach_id == "grand_admiral":
            return stats["grand_admirals"] >= 5
        elif ach_id == "streak_3":
            return stats["archived"] >= 3
        elif ach_id == "streak_7":
            return stats["archived"] >= 7
        elif ach_id == "perfectionist":
            return stats["grand_admirals"] >= 3
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# VF LOGO WIDGET - KV1NT ADMIRAL STANDARD
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# ANIMATED BACKGROUND - LIVING GRADIENT CANVAS
# ═══════════════════════════════════════════════════════════════════════════════

class AnimatedBackground(Gtk.DrawingArea):
    """
    🌊 LEVENDE ANIMERET BAGGRUND

    Premium animated gradient background with:
    - Smoothly shifting chakra colors
    - Floating orbs of light
    - Ambient glow effects
    - 60 FPS smooth animation

    Makes the app feel alive and premium.
    """

    def __init__(self):
        super().__init__()
        self.set_hexpand(True)
        self.set_vexpand(True)

        # Animation state
        self.time = 0.0
        self.orbs = []

        # Initialize floating orbs
        import random
        for _ in range(5):
            self.orbs.append({
                'x': random.random(),
                'y': random.random(),
                'size': random.uniform(0.1, 0.3),
                'speed_x': random.uniform(-0.0005, 0.0005),
                'speed_y': random.uniform(-0.0005, 0.0005),
                'color': random.choice([
                    (0.976, 0.451, 0.086, 0.15),  # Orange
                    (0.659, 0.333, 0.969, 0.12),  # Purple
                    (0.133, 0.827, 1.0, 0.10),    # Cyan
                    (0.384, 0.388, 0.945, 0.12),  # Indigo
                    (0.204, 0.827, 0.506, 0.10),  # Emerald
                ])
            })

        # Connect draw function
        self.set_draw_func(self._on_draw)

        # Start animation loop (30 FPS for efficiency)
        GLib.timeout_add(33, self._animate)

    def _animate(self) -> bool:
        """Update animation state"""
        self.time += 0.02

        # Move orbs
        for orb in self.orbs:
            orb['x'] += orb['speed_x']
            orb['y'] += orb['speed_y']

            # Bounce off edges
            if orb['x'] < 0 or orb['x'] > 1:
                orb['speed_x'] *= -1
            if orb['y'] < 0 or orb['y'] > 1:
                orb['speed_y'] *= -1

        # Request redraw
        self.queue_draw()
        return True  # Continue animation

    def _on_draw(self, area, cr, width, height):
        """Draw the animated background"""
        import math

        # Base gradient - deep space navy
        pattern = cairo.LinearGradient(0, 0, width, height)
        pattern.add_color_stop_rgba(0, 0.039, 0.055, 0.153, 1)  # #0A0E27
        pattern.add_color_stop_rgba(1, 0.059, 0.071, 0.161, 1)  # #0f1229
        cr.set_source(pattern)
        cr.paint()

        # Animated wave gradients
        wave_offset = math.sin(self.time) * 0.1

        # Top glow (orange/amber)
        cr.save()
        pattern = cairo.RadialGradient(
            width * (0.5 + wave_offset), -height * 0.2,
            0,
            width * (0.5 + wave_offset), -height * 0.2,
            width * 0.8
        )
        alpha = 0.08 + math.sin(self.time * 0.5) * 0.04
        pattern.add_color_stop_rgba(0, 0.976, 0.451, 0.086, alpha)
        pattern.add_color_stop_rgba(1, 0, 0, 0, 0)
        cr.set_source(pattern)
        cr.paint()
        cr.restore()

        # Bottom right glow (purple)
        cr.save()
        pattern = cairo.RadialGradient(
            width * (1.1 - wave_offset * 0.5), height * (1.1 + wave_offset * 0.3),
            0,
            width * (1.1 - wave_offset * 0.5), height * (1.1 + wave_offset * 0.3),
            width * 0.6
        )
        alpha = 0.06 + math.sin(self.time * 0.7 + 1) * 0.03
        pattern.add_color_stop_rgba(0, 0.659, 0.333, 0.969, alpha)
        pattern.add_color_stop_rgba(1, 0, 0, 0, 0)
        cr.set_source(pattern)
        cr.paint()
        cr.restore()

        # Left glow (cyan)
        cr.save()
        pattern = cairo.RadialGradient(
            width * (-0.1 + wave_offset * 0.3), height * (0.5 - wave_offset * 0.2),
            0,
            width * (-0.1 + wave_offset * 0.3), height * (0.5 - wave_offset * 0.2),
            width * 0.4
        )
        alpha = 0.05 + math.sin(self.time * 0.6 + 2) * 0.025
        pattern.add_color_stop_rgba(0, 0.133, 0.827, 1.0, alpha)
        pattern.add_color_stop_rgba(1, 0, 0, 0, 0)
        cr.set_source(pattern)
        cr.paint()
        cr.restore()

        # Draw floating orbs
        for orb in self.orbs:
            cr.save()
            x = orb['x'] * width
            y = orb['y'] * height
            size = orb['size'] * min(width, height)
            r, g, b, a = orb['color']

            # Pulsing alpha
            pulse = math.sin(self.time * 2 + orb['x'] * 10) * 0.3 + 0.7
            a *= pulse

            pattern = cairo.RadialGradient(x, y, 0, x, y, size)
            pattern.add_color_stop_rgba(0, r, g, b, a)
            pattern.add_color_stop_rgba(0.5, r, g, b, a * 0.5)
            pattern.add_color_stop_rgba(1, r, g, b, 0)
            cr.set_source(pattern)
            cr.paint()
            cr.restore()

        # Subtle noise/grain overlay for texture
        cr.save()
        cr.set_source_rgba(1, 1, 1, 0.01)
        for i in range(0, width, 4):
            for j in range(0, height, 4):
                if (i + j + int(self.time * 10)) % 7 == 0:
                    cr.rectangle(i, j, 1, 1)
        cr.fill()
        cr.restore()


class VFLogoWidget(Gtk.Box):
    """
    VF Logo - Victory Fleet Admiral Standard

    Animated logo representing Kv1nt's Admiral command.
    Uses Cirkelline Chakra colors with living glow effects.
    """

    def __init__(self, size: int = 64):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_halign(Gtk.Align.CENTER)
        self.add_css_class("vf-logo")

        # Logo container with chakra glow
        logo_frame = Gtk.Frame()
        logo_frame.add_css_class("vf-logo-frame")

        # VF Text as large stylized label
        vf_label = Gtk.Label(label="VF")
        vf_label.add_css_class("vf-logo-text")
        logo_frame.set_child(vf_label)

        self.append(logo_frame)

        # "ADMIRAL" subtitle
        subtitle = Gtk.Label(label="ADMIRAL")
        subtitle.add_css_class("vf-logo-subtitle")
        self.append(subtitle)


# ═══════════════════════════════════════════════════════════════════════════════
# LIVE AKTIVITETS MONITOR - REAL-TIME COMMAND CENTER
# ═══════════════════════════════════════════════════════════════════════════════

class LiveActivityMonitor(Gtk.Box):
    """
    🚀 VERDENSKLASSE LIVE AKTIVITETS MONITOR

    Viser real-time hvad der sker i systemet:
    - Fil ændringer
    - Script kørsler
    - DNA lag aktivering
    - Sejr fremskridt

    Enterprise niveau med animeret status.
    """

    MAX_ENTRIES = 50  # Behold kun de seneste 50 entries

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add_css_class("live-activity-monitor")
        self.activities = []
        self._build_ui()
        self._start_monitoring()

    def _build_ui(self):
        """Byg brugergrænsefladen"""
        # Header med pulserende status
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        header.add_css_class("activity-header")
        header.set_margin_start(16)
        header.set_margin_end(16)
        header.set_margin_top(12)
        header.set_margin_bottom(8)

        # Live puls indikator
        self.pulse_dot = Gtk.Label(label="●")
        self.pulse_dot.add_css_class("pulse-indicator")
        header.append(self.pulse_dot)

        # Titel
        title = Gtk.Label(label="LIVE AKTIVITET")
        title.add_css_class("activity-title")
        title.set_hexpand(True)
        title.set_halign(Gtk.Align.START)
        header.append(title)

        # Status badge
        self.status_badge = Gtk.Label(label="● AKTIV")
        self.status_badge.add_css_class("status-badge-active")
        header.append(self.status_badge)

        # Ryd knap
        clear_btn = Gtk.Button(icon_name="edit-clear-symbolic")
        clear_btn.add_css_class("flat")
        clear_btn.set_tooltip_text("Ryd activityslog")
        clear_btn.connect("clicked", lambda b: self._clear_activities())
        header.append(clear_btn)

        self.append(header)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(sep)

        # Scrollbar activitys liste
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_min_content_height(120)
        scroll.set_max_content_height(200)

        self.activity_list = Gtk.ListBox()
        self.activity_list.add_css_class("activity-list")
        self.activity_list.set_selection_mode(Gtk.SelectionMode.NONE)
        scroll.set_child(self.activity_list)

        self.append(scroll)

        # 5W Status linje i bunden
        self.five_w_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.five_w_bar.add_css_class("five-w-bar")
        self.five_w_bar.set_margin_start(16)
        self.five_w_bar.set_margin_end(16)
        self.five_w_bar.set_margin_top(8)
        self.five_w_bar.set_margin_bottom(12)

        # WHAT
        self.hvad_label = Gtk.Label(label="📋 WHAT: Waiter...")
        self.hvad_label.add_css_class("five-w-item")
        self.five_w_bar.append(self.hvad_label)

        # WHERE
        self.hvor_label = Gtk.Label(label="📍 WHERE: -")
        self.hvor_label.add_css_class("five-w-item")
        self.five_w_bar.append(self.hvor_label)

        # WHEN
        self.hvornaar_label = Gtk.Label(label="⏰ WHEN: Nu")
        self.hvornaar_label.add_css_class("five-w-item")
        self.five_w_bar.append(self.hvornaar_label)

        self.append(self.five_w_bar)

        # Tilføj initial besked
        self._add_activity("system", "Live activitysmonitor startet", "🚀")

    def _start_monitoring(self):
        """Start file monitoring"""
        # Update puls animation hvert sekund
        GLib.timeout_add_seconds(1, self._pulse_animation)

        # Tjek for nye activityer hvert 2. sekund
        GLib.timeout_add_seconds(2, self._check_for_activities)

    def _pulse_animation(self):
        """Animér puls indikatoren"""
        current = self.pulse_dot.get_css_classes()
        if "pulse-on" in current:
            self.pulse_dot.remove_css_class("pulse-on")
        else:
            self.pulse_dot.add_css_class("pulse-on")
        return True  # Fortsæt

    def _check_for_activities(self):
        """Tjek for nye activityer fra AUTO_LOG.jsonl"""
        try:
            # Tjek aktive victorys for nye log entries
            if ACTIVE_DIR.exists():
                for sejr_folder in ACTIVE_DIR.iterdir():
                    if sejr_folder.is_dir():
                        log_file = sejr_folder / "AUTO_LOG.jsonl"
                        if log_file.exists():
                            self._read_new_log_entries(log_file, sejr_folder.name)
        except Exception:
            pass
        return True  # Fortsæt overvågning

    def _read_new_log_entries(self, log_file: Path, sejr_name: str):
        """Read new log entries fra en AUTO_LOG.jsonl fil"""
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()[-5:]  # Kun de seneste 5 linjer

            for line in lines:
                try:
                    entry = json.loads(line.strip())
                    entry_id = f"{log_file}:{entry.get('timestamp', '')}"

                    # Tjek om vi allerede har set denne entry
                    if not hasattr(self, '_seen_entries'):
                        self._seen_entries = set()

                    if entry_id not in self._seen_entries:
                        self._seen_entries.add(entry_id)

                        # Begræns set size
                        if len(self._seen_entries) > 100:
                            self._seen_entries = set(list(self._seen_entries)[-50:])

                        # Tilføj activity
                        action = entry.get('action', 'action')
                        self._add_activity(
                            sejr_name[:20],
                            f"{action}: {entry.get('details', '')[:50]}",
                            self._get_icon_for_action(action)
                        )

                        # Update 5W
                        self._update_five_w(sejr_name, action)
                except json.JSONDecodeError:
                    pass
        except Exception:
            pass

    def _get_icon_for_action(self, action: str) -> str:
        """Get icon based on action"""
        icons = {
            "create": "✨",
            "update": "📝",
            "verify": "✅",
            "archive": "📦",
            "complete": "🏆",
            "error": "❌",
            "start": "🚀",
            "progress": "⏳",
            "git": "🔀",
            "test": "🧪",
        }
        for key, icon in icons.items():
            if key in action.lower():
                return icon
        return "📌"

    def _update_five_w(self, sejr_name: str, action: str):
        """Update 5W statuslinje"""
        now = datetime.now().strftime("%H:%M:%S")
        self.hvad_label.set_text(f"📋 {action[:30]}")
        self.hvor_label.set_text(f"📍 {victory_name[:20]}")
        self.hvornaar_label.set_text(f"⏰ {now}")

    def _add_activity(self, source: str, message: str, icon: str = "📌"):
        """Add a new activity to the list"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        row = Gtk.ListBoxRow()
        row.add_css_class("activity-row")

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(6)
        box.set_margin_bottom(6)

        # Ikon
        icon_label = Gtk.Label(label=icon)
        icon_label.add_css_class("activity-icon")
        box.append(icon_label)

        # Tidsstempel
        time_label = Gtk.Label(label=timestamp)
        time_label.add_css_class("activity-timestamp")
        box.append(time_label)

        # Kilde
        source_label = Gtk.Label(label=f"[{source}]")
        source_label.add_css_class("activity-source")
        box.append(source_label)

        # Besked
        msg_label = Gtk.Label(label=message)
        msg_label.add_css_class("activity-message")
        msg_label.set_hexpand(True)
        msg_label.set_halign(Gtk.Align.START)
        msg_label.set_ellipsize(Pango.EllipsizeMode.END)
        box.append(msg_label)

        row.set_child(box)

        # Tilføj øverst
        self.activity_list.prepend(row)

        # Begræns antal entries
        children = []
        child = self.activity_list.get_first_child()
        while child:
            children.append(child)
            child = child.get_next_sibling()

        while len(children) > self.MAX_ENTRIES:
            old_row = children.pop()
            self.activity_list.remove(old_row)

        self.activities.append({
            "timestamp": timestamp,
            "source": source,
            "message": message,
            "icon": icon
        })

    def _clear_activities(self):
        """Ryd alle activityer"""
        while True:
            row = self.activity_list.get_first_child()
            if row:
                self.activity_list.remove(row)
            else:
                break
        self.activities = []
        self._add_activity("system", "Activityslog ryddet", "🧹")

    def log_event(self, source: str, message: str, icon: str = "📌"):
        """Public metode til at logge events fra andre dele af appen"""
        GLib.idle_add(lambda: self._add_activity(source, message, icon))


# ═══════════════════════════════════════════════════════════════════════════════
# VINDERTAVLE - VICTORY JOURNEY BOARD
# ═══════════════════════════════════════════════════════════════════════════════

class Vindertavle(Gtk.Box):
    """
    Vindertavle - Victory Board showing the entire journey

    Displays all archived victories as a visual timeline,
    showing how each victory led to the current state.
    Cirkelline Chakra colors indicate victory type.
    """

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add_css_class("vindertavle")

        # Header with VF Logo
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        header.add_css_class("vindertavle-header")
        header.set_margin_start(20)
        header.set_margin_end(20)
        header.set_margin_top(16)
        header.set_margin_bottom(8)

        # VF Logo (small version)
        logo = VFLogoWidget(size=48)
        header.append(logo)

        # Title section
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        title_box.set_hexpand(True)

        title = Gtk.Label(label="VINDERTAVLE")
        title.set_halign(Gtk.Align.START)
        title.add_css_class("title-2")
        title.add_css_class("vindertavle-title")
        title_box.append(title)

        subtitle = Gtk.Label(label="Din rejse til Admiral niveau")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("caption")
        subtitle.add_css_class("dim-label")
        title_box.append(subtitle)

        header.append(title_box)

        # Stats badge
        self.stats_label = Gtk.Label(label="0 Victorye")
        self.stats_label.add_css_class("vindertavle-stats")
        header.append(self.stats_label)

        self.append(header)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_start(20)
        sep.set_margin_end(20)
        self.append(sep)

        # Scrollable victory timeline
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_min_content_height(300)

        self.timeline_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.timeline_box.add_css_class("vindertavle-timeline")
        scroll.set_child(self.timeline_box)

        self.append(scroll)

        # Load victories
        self._load_victories()

    def _load_victories(self):
        """Load all archived victories"""
        victories = []

        # Scan archive folder
        if ARCHIVE_DIR.exists():
            for folder in sorted(ARCHIVE_DIR.iterdir(), key=lambda x: x.name):
                if folder.is_dir() and not folder.name.startswith('.'):
                    sejr_liste = folder / "SEJR_LISTE.md"
                    verify_status = folder / "VERIFY_STATUS.yaml"

                    victory_data = {
                        "name": folder.name.split("_2026")[0].replace("_", " "),
                        "path": folder,
                        "date": self._extract_date(folder.name),
                        "score": 0,
                        "pass_level": 0,
                        "chakra": self._determine_chakra(folder.name)
                    }

                    # Try to get score from VERIFY_STATUS.yaml
                    if verify_status.exists():
                        try:
                            import yaml
                            with open(verify_status) as f:
                                data = yaml.safe_load(f) or {}
                                victory_data["score"] = data.get("current_score", 0)
                                victory_data["pass_level"] = data.get("current_pass", 1)
                        except:
                            pass

                    victories.append(victory_data)

        # Update stats
        self.stats_label.set_text(f"{len(victories)} Victorye")

        # Add victory cards
        for i, victory in enumerate(victories):
            card = self._create_victory_card(victory, i, len(victories))
            self.timeline_box.append(card)

        # Add "Now" marker at top
        now_marker = self._create_now_marker()
        self.timeline_box.prepend(now_marker)

    def _extract_date(self, folder_name: str) -> str:
        """Extract date from folder name"""
        import re
        match = re.search(r'(\d{4}-\d{2}-\d{2})', folder_name)
        if match:
            return match.group(1)
        return "Ukendt"

    def _determine_chakra(self, name: str) -> str:
        """Determine chakra color based on victory type"""
        name_lower = name.lower()
        if "admiral" in name_lower or "final" in name_lower:
            return "divine"  # Violet - Crown Chakra
        elif "wisdom" in name_lower or "learn" in name_lower:
            return "wisdom"  # Gold - Solar Plexus
        elif "verify" in name_lower or "test" in name_lower:
            return "heart"  # Emerald - Heart Chakra
        elif "integration" in name_lower or "fase" in name_lower:
            return "intuition"  # Indigo - Third Eye
        elif "fix" in name_lower or "bevis" in name_lower:
            return "sacred"  # Magenta - Divine Feminine
        else:
            return "primary"  # Orange - Brand color

    def _create_victory_card(self, victory: dict, index: int, total: int) -> Gtk.Box:
        """Create a victory card for the timeline"""
        card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        card.add_css_class("victory-card")
        card.add_css_class(f"chakra-{victory['chakra']}")
        card.set_margin_start(20)
        card.set_margin_end(20)
        card.set_margin_top(8)
        card.set_margin_bottom(8)

        # Timeline connector line
        line_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        line_box.set_size_request(24, -1)

        # Victory node (circle)
        node = Gtk.DrawingArea()
        node.set_size_request(16, 16)
        node.add_css_class("victory-node")
        node.add_css_class(f"chakra-{victory['chakra']}")
        line_box.append(node)

        # Connector line (except for last item)
        if index < total - 1:
            line = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
            line.set_vexpand(True)
            line.add_css_class("timeline-line")
            line_box.append(line)

        card.append(line_box)

        # Victory info
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info_box.set_hexpand(True)

        # Name
        name_label = Gtk.Label(label=victory["name"])
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("heading")
        info_box.append(name_label)

        # Date and score
        meta_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        date_label = Gtk.Label(label=victory["date"])
        date_label.add_css_class("caption")
        date_label.add_css_class("dim-label")
        meta_box.append(date_label)

        if victory["score"] > 0:
            score_label = Gtk.Label(label=f"⭐ {victory['score']}/30")
            score_label.add_css_class("caption")
            score_label.add_css_class(f"chakra-{victory['chakra']}-text")
            meta_box.append(score_label)

        info_box.append(meta_box)

        card.append(info_box)

        # Open folder button
        open_btn = Gtk.Button(icon_name="folder-open-symbolic")
        open_btn.add_css_class("flat")
        open_btn.set_valign(Gtk.Align.CENTER)
        open_btn.set_tooltip_text("Open folder")
        open_btn.connect("clicked", lambda b, p=victory["path"]: subprocess.Popen(["nautilus", str(p)]))
        card.append(open_btn)

        return card

    def _create_now_marker(self) -> Gtk.Box:
        """Create the 'NOW' marker at top of timeline"""
        marker = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        marker.add_css_class("now-marker")
        marker.set_margin_start(20)
        marker.set_margin_end(20)
        marker.set_margin_top(16)
        marker.set_margin_bottom(8)

        # Pulsing indicator
        pulse = Gtk.Spinner()
        pulse.start()
        pulse.set_size_request(20, 20)
        marker.append(pulse)

        # NOW label
        now_label = Gtk.Label(label="NU - DU ER HER")
        now_label.add_css_class("title-4")
        now_label.add_css_class("now-marker-text")
        marker.append(now_label)

        return marker


class DNALayerRow(Gtk.Box):
    """A row showing a DNA layer status - interactive and animated"""

    def __init__(self, layer_num, name, description, icon_name, active=False, progress=0.0, running=False):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.layer_num = layer_num
        self.name = name
        self.active = active
        self.running = running

        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_margin_top(8)
        self.set_margin_bottom(8)

        # Make row clickable
        self.add_css_class("dna-layer-row")
        if running:
            self.add_css_class("dna-layer-running")
        elif active:
            self.add_css_class("dna-layer-active")

        # Click gesture for interaction
        click = Gtk.GestureClick.new()
        click.connect("released", self._on_clicked)
        self.add_controller(click)

        # Status indicator with animation support
        if running:
            self.status_icon = Gtk.Spinner()
            self.status_icon.start()
            self.status_icon.set_size_request(16, 16)
        else:
            self.status_icon = Gtk.Image.new_from_icon_name(
                "emblem-ok-symbolic" if active else "radio-symbolic-disabled"
            )
            if active:
                self.status_icon.add_css_class("success")
            else:
                self.status_icon.add_css_class("dim-label")
        self.append(self.status_icon)

        # Layer number badge with glow effect when active
        badge_box = Gtk.Box()
        badge_box.add_css_class("dna-badge")
        if active:
            badge_box.add_css_class("dna-badge-active")
        badge = Gtk.Label(label=layer_num)
        badge.add_css_class("caption")
        badge.add_css_class("accent")
        badge.set_size_request(24, 24)
        badge_box.append(badge)
        self.append(badge_box)

        # Layer icon
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(20)
        self.append(icon)

        # Name and description with progress
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        text_box.set_hexpand(True)

        name_label = Gtk.Label(label=name)
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("heading")
        text_box.append(name_label)

        desc_label = Gtk.Label(label=description)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.add_css_class("caption")
        desc_label.add_css_class("dim-label")
        text_box.append(desc_label)

        # Mini progress bar for this layer
        if progress > 0:
            prog_bar = Gtk.ProgressBar()
            prog_bar.set_fraction(progress)
            prog_bar.add_css_class("dna-progress")
            prog_bar.set_margin_top(4)
            text_box.append(prog_bar)

        self.append(text_box)

        # Action button (trigger script)
        if not active:
            action_btn = Gtk.Button(icon_name="media-playback-start-symbolic")
            action_btn.add_css_class("flat")
            action_btn.add_css_class("circular")
            action_btn.set_tooltip_text(f"Run {name}")
            action_btn.connect("clicked", self._on_action_clicked)
            self.append(action_btn)

    def _on_clicked(self, gesture, n_press, x, y):
        """Handle click - show layer details"""
        # Could expand to show more info or trigger action
        pass

    def _on_action_clicked(self, button):
        """Trigger the DNA layer script"""
        # Map layer to script
        scripts = {
            "1": "auto_track.py",
            "2": "auto_track.py",
            "3": "auto_verify.py",
            "4": "auto_learn.py",
            "5": "auto_archive.py",
            "6": "auto_predict.py",
            "7": None  # Generate is separate
        }
        script = scripts.get(self.layer_num)
        if script:
            script_path = SYSTEM_PATH / "scripts" / script
            if script_path.exists():
                try:
                    subprocess.Popen(["python3", str(script_path)])
                except Exception as e:
                    print(f"Could not run script: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# SEJR FIL MANAGER - HÅNDTER FILER I SEJR MAPPE
# ═══════════════════════════════════════════════════════════════════════════════

class SejrFilManager(Gtk.Box):
    """
    En komplet filhåndtering widget for sejr mapper.

    Features:
    - Vis alle filer og mapper i sejr directory
    - Importér filer/mapper fra eksterne kilder
    - Kopiér filer ind i sejr mappe
    - Visuelle fil type ikoner
    - Størrelse og modificeringstid display
    - Drag & drop support indikation
    - Auto-opdatering ved fil ændringer

    Attributes:
        sejr_path: Sti til sejr mappen
        file_store: Gio.ListStore for fil entries
    """

    def __init__(self, sejr_path: Path):
        """
        Initialiser fil manager.

        Args:
            sejr_path: Sti til sejr mappen
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        self.sejr_path = Path(sejr_path)
        self.file_store = Gio.ListStore()

        self._build_ui()
        self._load_files()

    def _build_ui(self) -> None:
        """Byg fil manager UI."""
        # Action bar
        action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        action_bar.set_margin_start(12)
        action_bar.set_margin_end(12)
        action_bar.set_margin_top(8)

        # Import knap
        import_btn = Gtk.Button()
        import_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        import_box.append(Gtk.Image.new_from_icon_name("document-open-symbolic"))
        import_box.append(Gtk.Label(label="Import"))
        import_btn.set_child(import_box)
        import_btn.add_css_class("suggested-action")
        import_btn.connect("clicked", self._on_import_clicked)
        import_btn.set_tooltip_text("Import files eller folders til denne victory")
        action_bar.append(import_btn)

        # Update knap
        refresh_btn = Gtk.Button(icon_name="view-refresh-symbolic")
        refresh_btn.connect("clicked", lambda b: self._load_files())
        refresh_btn.set_tooltip_text("Update fil liste")
        action_bar.append(refresh_btn)

        # Open folder knap
        open_btn = Gtk.Button(icon_name="folder-open-symbolic")
        open_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", str(self.sejr_path)]))
        open_btn.set_tooltip_text("Open i file manager")
        action_bar.append(open_btn)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        action_bar.append(spacer)

        # Fil tæller label
        self.file_count_label = Gtk.Label()
        self.file_count_label.add_css_class("dim-label")
        self.file_count_label.add_css_class("caption")
        action_bar.append(self.file_count_label)

        self.append(action_bar)

        # Fil liste
        self.file_list = Gtk.ListBox()
        self.file_list.add_css_class("boxed-list")
        self.file_list.set_selection_mode(Gtk.SelectionMode.NONE)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(200)
        scroll.set_max_content_height(400)
        scroll.set_child(self.file_list)

        self.append(scroll)

        # Drop hint
        drop_hint = Gtk.Label(label="📂 Drag files here or use the Import button")
        drop_hint.add_css_class("caption")
        drop_hint.add_css_class("dim-label")
        drop_hint.set_margin_top(4)
        drop_hint.set_margin_bottom(8)
        self.append(drop_hint)

    def _load_files(self) -> None:
        """Indlæs files og folders fra victory directory."""
        # Ryd eksisterende
        while row := self.file_list.get_first_child():
            self.file_list.remove(row)

        if not self.sejr_path.exists():
            return

        # Hent alle items (files og folders)
        items = []
        for item in self.sejr_path.iterdir():
            if item.name.startswith('.'):
                continue  # Spring skjulte filer over

            stat = item.stat()
            items.append({
                "name": item.name,
                "path": item,
                "is_dir": item.is_dir(),
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime),
            })

        # Sortér: folders først, derefter efter navn
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))

        # Update tæller
        folder_count = sum(1 for i in items if i["is_dir"])
        file_count = len(items) - folder_count
        self.file_count_label.set_label(f"{folder_count} folders, {file_count} files")

        # Tilføj items til the list
        for item in items:
            row = self._create_file_row(item)
            self.file_list.append(row)

    def _create_file_row(self, item: Dict[str, Any]) -> Adw.ActionRow:
        """Create a row for a file or folder."""
        row = Adw.ActionRow()
        row.set_title(item["name"])

        # Ikon based on type
        if item["is_dir"]:
            icon_name = "folder-symbolic"
            subtitle = "Folder"
        else:
            ext = item["path"].suffix.lower()
            icon_map = {
                ".md": ("text-x-markdown-symbolic", "Markdown"),
                ".yaml": ("text-x-script-symbolic", "YAML"),
                ".yml": ("text-x-script-symbolic", "YAML"),
                ".json": ("text-x-script-symbolic", "JSON"),
                ".jsonl": ("text-x-log-symbolic", "JSON Lines"),
                ".py": ("text-x-python-symbolic", "Python"),
                ".sh": ("text-x-script-symbolic", "Shell"),
                ".txt": ("text-x-generic-symbolic", "Tekst"),
                ".log": ("text-x-log-symbolic", "Log"),
                ".pdf": ("x-office-document-symbolic", "PDF"),
                ".png": ("image-x-generic-symbolic", "Billede"),
                ".jpg": ("image-x-generic-symbolic", "Billede"),
                ".jpeg": ("image-x-generic-symbolic", "Billede"),
            }
            icon_name, file_type = icon_map.get(ext, ("text-x-generic-symbolic", "Fil"))
            size_str = self._format_size(item["size"])
            subtitle = f"{file_type} • {size_str}"

        row.add_prefix(Gtk.Image.new_from_icon_name(icon_name))
        row.set_subtitle(subtitle)

        # Tidspunkt badge
        time_label = Gtk.Label(label=item["mtime"].strftime("%H:%M"))
        time_label.add_css_class("caption")
        time_label.add_css_class("dim-label")
        row.add_suffix(time_label)

        # Open knap
        open_btn = Gtk.Button(icon_name="document-open-symbolic")
        open_btn.add_css_class("flat")
        open_btn.set_valign(Gtk.Align.CENTER)
        open_btn.connect("clicked", lambda b: subprocess.Popen(["xdg-open", str(item["path"])]))
        open_btn.set_tooltip_text("Open fil")
        row.add_suffix(open_btn)

        # Gør hele rown klikbar
        row.set_activatable(True)
        row.connect("activated", lambda r: subprocess.Popen(["xdg-open", str(item["path"])]))

        return row

    def _format_size(self, size: int) -> str:
        """Format file size in human readable format."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def _on_import_clicked(self, button: Gtk.Button) -> None:
        """Vis fil chooser dialog til import af files."""
        dialog = Gtk.FileChooserDialog(
            title="Import Files til Victory",
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.set_transient_for(button.get_root())
        dialog.set_modal(True)
        dialog.set_select_multiple(True)

        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Import", Gtk.ResponseType.ACCEPT)

        dialog.connect("response", self._on_import_response)
        dialog.present()

    def _on_import_response(self, dialog: Gtk.FileChooserDialog, response: int) -> None:
        """Handle file chooser response."""
        if response == Gtk.ResponseType.ACCEPT:
            files = dialog.get_files()
            imported_count = 0

            for gfile in files:
                source_path = Path(gfile.get_path())
                dest_path = self.sejr_path / source_path.name

                try:
                    if source_path.is_dir():
                        # Kopiér hele foldern
                        shutil.copytree(source_path, dest_path)
                    else:
                        # Kopiér fil
                        shutil.copy2(source_path, dest_path)
                    imported_count += 1
                except Exception as e:
                    print(f"Could not importere {source_path}: {e}")

            # Update fil liste
            self._load_files()

            # Send notifikation
            if imported_count > 0:
                send_notification(
                    "Files Importeret",
                    f"Importerede {imported_count} element(er) til victory folder",
                    "emblem-ok-symbolic"
                )

        dialog.close()


# ═══════════════════════════════════════════════════════════════════════════════
# PRIORITETS OVERBLIK - WHAT HAR BRUG FOR OPMÆRKSOMHED NU
# ═══════════════════════════════════════════════════════════════════════════════

class PrioritetsOverblik(Gtk.Box):
    """
    Et intelligent prioritets dashboard der viser hvad der kræver opmærksomhed NU.

    Features:
    - AKUT: Kritiske ting der kræver øjeblikkelig handling (rød glow)
    - OPMÆRKSOMHED: Ting der bør håndteres snart (amber glow)
    - NÆSTE: AI-forudsagte næste skridt (blå glow)
    - ÉT KLIK: Direkte navigation til problem områder
    - LIVE: Auto-opdaterer hvert 5. sekund

    Dette er det FØRSTE brugeren ser - det guider dem direkte
    til hvor de skal være.
    """

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_start(24)
        self.set_margin_end(24)
        self.set_margin_top(16)
        self.set_margin_bottom(16)

        self._build_ui()
        self._update_priorities()

        # Auto-opdater hvert 5. sekund
        GLib.timeout_add_seconds(5, self._update_priorities)

    def _build_ui(self) -> None:
        """Byg prioritets dashboard UI."""
        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        icon = Gtk.Image.new_from_icon_name("dialog-warning-symbolic")
        icon.set_pixel_size(32)
        icon.add_css_class("warning")
        header.append(icon)

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        title = Gtk.Label(label="⚡ Priority Dashboard")
        title.set_halign(Gtk.Align.START)
        title.add_css_class("title-2")
        title_box.append(title)

        subtitle = Gtk.Label(label="Hvad requires your attention RIGHT NOW")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("dim-label")
        subtitle.add_css_class("caption")
        title_box.append(subtitle)

        header.append(title_box)
        self.append(header)

        # Prioritys sektioner container
        self.sections_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.append(self.sections_box)

    def _update_priorities(self) -> bool:
        """Update prioritets elementer fra nuværende system tilstand."""
        # Ryd eksisterende
        while child := self.sections_box.get_first_child():
            self.sections_box.remove(child)

        priorities = self._analyze_system()

        if not any(priorities.values()):
            # Alt klart!
            clear_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            clear_box.set_halign(Gtk.Align.CENTER)
            clear_box.add_css_class("card")
            clear_box.set_margin_top(16)
            clear_box.set_margin_bottom(16)

            icon = Gtk.Image.new_from_icon_name("emblem-ok-symbolic")
            icon.set_pixel_size(48)
            icon.add_css_class("success")
            clear_box.append(icon)

            label = Gtk.Label(label="✨ Alt Readyt!")
            label.add_css_class("title-3")
            clear_box.append(label)

            desc = Gtk.Label(label="None akutte ting. Du er på rette spor!")
            desc.add_css_class("dim-label")
            clear_box.append(desc)

            self.sections_box.append(clear_box)
        else:
            # Byg prioritets sektioner
            if priorities["akut"]:
                self._add_section("🔴 AKUT", priorities["akut"], "error")
            if priorities["opmaerksomhed"]:
                self._add_section("🟡 OPMÆRKSOMHED", priorities["opmaerksomhed"], "warning")
            if priorities["naeste"]:
                self._add_section("🔵 NÆSTE SKRIDT", priorities["naeste"], "accent")

        return True  # Fortsæt timeout

    def _analyze_system(self) -> Dict[str, List[Dict]]:
        """Analysér system tilstand og returnér prioritets elementer."""
        priorities = {"akut": [], "opmaerksomhed": [], "naeste": []}

        # Tjek for ufærdige aktive victorye
        if ACTIVE_DIR.exists():
            for sejr_dir in ACTIVE_DIR.iterdir():
                if not sejr_dir.is_dir():
                    continue

                sejr_file = sejr_dir / "SEJR_LISTE.md"
                if sejr_file.exists():
                    content = sejr_file.read_text()
                    done, total = count_checkboxes(content)

                    if total > 0:
                        progress = (done / total) * 100

                        if progress < 30:
                            priorities["akut"].append({
                                "title": f"Victory gået i stå: {victory_dir.name}",
                                "subtitle": f"Kun {progress:.0f}% færdig ({done}/{total})",
                                "action": "Open Victory",
                                "path": str(sejr_dir),
                                "icon": "emblem-important-symbolic"
                            })
                        elif progress < 80:
                            priorities["opmaerksomhed"].append({
                                "title": f"Continue: {victory_dir.name}",
                                "subtitle": f"{progress:.0f}% færdig - push til mål!",
                                "action": "Genoptag",
                                "path": str(sejr_dir),
                                "icon": "media-playback-start-symbolic"
                            })

        # Tjek for manglende verifikation
        if ACTIVE_DIR.exists():
            for sejr_dir in ACTIVE_DIR.iterdir():
                if not sejr_dir.is_dir():
                    continue

                verify_file = sejr_dir / "VERIFY_STATUS.yaml"
                if not verify_file.exists():
                    priorities["opmaerksomhed"].append({
                        "title": f"Mangler verifikation: {victory_dir.name}",
                        "subtitle": "Run verifikation for at spore fremskridt",
                        "action": "Verificér Nu",
                        "path": str(sejr_dir),
                        "icon": "emblem-ok-symbolic"
                    })

        # Tjek NEXT.md for forudsigelser
        next_file = SYSTEM_PATH / "_CURRENT" / "NEXT.md"
        if next_file.exists():
            content = next_file.read_text()
            lines = [l.strip() for l in content.split('\n') if l.strip().startswith('- ')]
            for line in lines[:3]:
                priorities["naeste"].append({
                    "title": line[2:50] + "..." if len(line) > 52 else line[2:],
                    "subtitle": "AI forudsagt næste action",
                    "action": "Se Detaljer",
                    "path": str(next_file),
                    "icon": "weather-clear-symbolic"
                })

        # Hvis ingen næste skridt, foreslå at oprette ny victory
        if not priorities["naeste"] and not priorities["akut"]:
            priorities["naeste"].append({
                "title": "Opret en ny victory",
                "subtitle": "Start frisk med et nyt mål",
                "action": "New Victory",
                "path": "new",
                "icon": "list-add-symbolic"
            })

        return priorities

    def _add_section(self, title: str, items: List[Dict], css_class: str) -> None:
        """Tilføj en prioritets sektion med elementer."""
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        # Sektion header
        header = Gtk.Label(label=title)
        header.set_halign(Gtk.Align.START)
        header.add_css_class("heading")
        header.add_css_class(css_class)
        section.append(header)

        # Elementer
        for item in items[:3]:  # Max 3 per sektion
            row = self._create_priority_row(item, css_class)
            section.append(row)

        self.sections_box.append(section)

    def _create_priority_row(self, item: Dict, css_class: str) -> Gtk.Box:
        """Opret en klikbar prioritets row."""
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.add_css_class("card")
        row.set_margin_start(8)
        row.set_margin_end(8)

        # Ikon
        icon = Gtk.Image.new_from_icon_name(item.get("icon", "dialog-information-symbolic"))
        icon.set_pixel_size(24)
        icon.add_css_class(css_class)
        row.append(icon)

        # Tekst
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        text_box.set_hexpand(True)

        title = Gtk.Label(label=item["title"])
        title.set_halign(Gtk.Align.START)
        title.add_css_class("heading")
        title.set_ellipsize(Pango.EllipsizeMode.END)
        text_box.append(title)

        subtitle = Gtk.Label(label=item["subtitle"])
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("caption")
        subtitle.add_css_class("dim-label")
        text_box.append(subtitle)

        row.append(text_box)

        # Handling knap
        btn = Gtk.Button(label=item["action"])
        btn.add_css_class("suggested-action")
        btn.add_css_class("pill")
        btn.set_valign(Gtk.Align.CENTER)

        path = item["path"]
        if path == "new":
            btn.connect("clicked", lambda b: self._create_new_sejr())
        else:
            btn.connect("clicked", lambda b, p=path: subprocess.Popen(["nautilus", p]))

        row.append(btn)

        return row

    def _create_new_sejr(self) -> None:
        """Trigger ny victory oprettelse."""
        script = SCRIPTS_DIR / "generate_victory.py"
        if script.exists():
            subprocess.Popen(["python3", str(script)])
            send_notification("New Victory", "Opretter ny victory...", "list-add-symbolic")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class MasterpieceWindow(Adw.ApplicationWindow):
    """The main application window"""

    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Victory List Masterpiece")
        self.set_default_size(1200, 800)

        self.selected_sejr = None
        self.sejrs = []
        self.search_engine = IntelligentSearch(SYSTEM_PATH)
        self.search_mode = False
        self.zoom_level = 1.0  # For zoom functionality
        self.file_monitors = []  # Real-time file monitoring

        self._build_ui()
        self._load_sejrs()
        self._setup_file_monitoring()
        self._setup_drag_drop()

        # Auto-refresh every 5 seconds (backup to file monitoring)
        GLib.timeout_add_seconds(5, self._auto_refresh)

    def _build_ui(self):
        """Build the user interface"""
        # Confetti overlay for celebrations
        self.konfetti = KonfettiOverlay()

        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Wrap in konfetti overlay
        self.konfetti.set_child(main_box)
        self.set_content(self.konfetti)

        # Header bar
        header = Adw.HeaderBar()

        # Title widget
        title_widget = Adw.WindowTitle()
        title_widget.set_title("Victory List")
        title_widget.set_subtitle("Mesterværk Edition")
        header.set_title_widget(title_widget)

        # Refresh button
        refresh_btn = Gtk.Button(icon_name="view-refresh-symbolic")
        refresh_btn.set_tooltip_text("Reload (Ctrl+R)")
        refresh_btn.connect("clicked", lambda b: self._load_sejrs())
        header.pack_start(refresh_btn)

        # New Victory button
        new_btn = Gtk.Button(icon_name="list-add-symbolic")
        new_btn.set_tooltip_text("New Victory (Ctrl+N)")
        new_btn.add_css_class("suggested-action")
        new_btn.connect("clicked", self._on_new_sejr)
        header.pack_start(new_btn)

        # Universal Converter button
        convert_btn = Gtk.Button(icon_name="document-import-symbolic")
        convert_btn.set_tooltip_text("Konverter til Victory (fra folder/fil/tekst)")
        convert_btn.connect("clicked", self._on_convert_to_sejr)
        header.pack_start(convert_btn)

        # === ZOOM CONTROLS ===
        zoom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        zoom_box.set_valign(Gtk.Align.CENTER)

        zoom_out_btn = Gtk.Button(icon_name="zoom-out-symbolic")
        zoom_out_btn.add_css_class("flat")
        zoom_out_btn.set_tooltip_text("Zoom ud (Ctrl+-)")
        zoom_out_btn.connect("clicked", lambda b: self._zoom_step(-0.1))
        zoom_box.append(zoom_out_btn)

        self.zoom_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.5, 2.0, 0.1)
        self.zoom_scale.set_value(1.0)
        self.zoom_scale.add_css_class("zoom-slider")
        self.zoom_scale.set_draw_value(False)
        self.zoom_scale.connect("value-changed", lambda s: self._on_zoom_changed(s))
        zoom_box.append(self.zoom_scale)

        self.zoom_label = Gtk.Label(label="100%")
        self.zoom_label.add_css_class("zoom-label")
        zoom_box.append(self.zoom_label)

        zoom_in_btn = Gtk.Button(icon_name="zoom-in-symbolic")
        zoom_in_btn.add_css_class("flat")
        zoom_in_btn.set_tooltip_text("Zoom ind (Ctrl++)")
        zoom_in_btn.connect("clicked", lambda b: self._zoom_step(0.1))
        zoom_box.append(zoom_in_btn)

        zoom_reset_btn = Gtk.Button(icon_name="zoom-fit-best-symbolic")
        zoom_reset_btn.add_css_class("flat")
        zoom_reset_btn.set_tooltip_text("Nulstil zoom (Ctrl+0)")
        zoom_reset_btn.connect("clicked", lambda b: self._zoom_reset())
        zoom_box.append(zoom_reset_btn)

        header.pack_end(zoom_box)

        # Search toggle button
        self.search_btn = Gtk.ToggleButton(icon_name="system-search-symbolic")
        self.search_btn.set_tooltip_text("Intelligent Search (Ctrl+F)")
        self.search_btn.connect("toggled", self._on_search_toggled)
        header.pack_end(self.search_btn)

        # Menu button
        menu_btn = Gtk.MenuButton(icon_name="open-menu-symbolic")
        header.pack_end(menu_btn)

        main_box.append(header)

        # Navigation split view (sidebar + content)
        self.split_view = Adw.NavigationSplitView()
        self.split_view.set_vexpand(True)
        main_box.append(self.split_view)

        # === LIVE AKTIVITETS MONITOR (Bund panel) ===
        self.activity_monitor = LiveActivityMonitor()
        main_box.append(self.activity_monitor)

        # === SIDEBAR ===
        sidebar_page = Adw.NavigationPage()
        sidebar_page.set_title("Bibliotek")

        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Sidebar header
        sidebar_header = Adw.HeaderBar()
        sidebar_header.add_css_class("flat")
        sidebar_box.append(sidebar_header)

        # Search bar (hidden by default)
        self.search_bar = Gtk.SearchBar()
        self.search_bar.set_show_close_button(True)

        search_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        search_box.set_margin_start(6)
        search_box.set_margin_end(6)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search i files, kode, detaljer...")
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("search-changed", self._on_search_changed)
        self.search_entry.connect("activate", self._on_search_activate)
        search_box.append(self.search_entry)

        self.search_bar.set_child(search_box)
        self.search_bar.connect_entry(self.search_entry)
        sidebar_box.append(self.search_bar)

        # Search results container (hidden by default)
        self.search_results_scroll = Gtk.ScrolledWindow()
        self.search_results_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.search_results_scroll.set_vexpand(True)
        self.search_results_scroll.set_visible(False)

        self.search_results_list = Gtk.ListBox()
        self.search_results_list.add_css_class("boxed-list")
        self.search_results_list.connect("row-activated", self._on_search_result_activated)
        self.search_results_scroll.set_child(self.search_results_list)
        sidebar_box.append(self.search_results_scroll)

        # === FILTER BAR ===
        self.filter_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.filter_bar.add_css_class("filter-bar")
        self.filter_bar.set_margin_start(8)
        self.filter_bar.set_margin_end(8)

        # Filter chips
        self.filter_all = Gtk.ToggleButton(label="All")
        self.filter_all.add_css_class("filter-chip")
        self.filter_all.set_active(True)
        self.filter_all.connect("toggled", lambda b: self._apply_filter("all"))
        self.filter_bar.append(self.filter_all)

        self.filter_active = Gtk.ToggleButton(label="🔵 Active")
        self.filter_active.add_css_class("filter-chip")
        self.filter_active.connect("toggled", lambda b: self._apply_filter("active"))
        self.filter_bar.append(self.filter_active)

        self.filter_archived = Gtk.ToggleButton(label="✅ Arkiv")
        self.filter_archived.add_css_class("filter-chip")
        self.filter_archived.connect("toggled", lambda b: self._apply_filter("archived"))
        self.filter_bar.append(self.filter_archived)

        # Sort dropdown
        sort_model = Gtk.StringList.new(["📅 Date", "📊 Score", "🔤 Name"])
        self.sort_dropdown = Gtk.DropDown(model=sort_model)
        self.sort_dropdown.add_css_class("sort-dropdown")
        self.sort_dropdown.set_tooltip_text("Sortér efter")
        self.sort_dropdown.connect("notify::selected", lambda d, p: self._apply_sort())
        self.filter_bar.append(self.sort_dropdown)

        sidebar_box.append(self.filter_bar)
        self.current_filter = "all"

        # Scrollable list (regular victory list)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)

        self.sejr_list = Gtk.ListBox()
        self.sejr_list.add_css_class("navigation-sidebar")
        self.sejr_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.sejr_list.connect("row-activated", self._on_sejr_selected)
        scroll.set_child(self.sejr_list)

        sidebar_box.append(scroll)

        # Stats at bottom of sidebar - GENEROUS SPACING
        self.stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.stats_box.set_margin_start(20)
        self.stats_box.set_margin_end(20)
        self.stats_box.set_margin_top(20)
        self.stats_box.set_margin_bottom(20)
        self.stats_box.set_halign(Gtk.Align.CENTER)

        self.active_label = Gtk.Label(label="0 Active")
        self.active_label.add_css_class("caption")
        self.stats_box.append(self.active_label)

        sep = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.stats_box.append(sep)

        self.archived_label = Gtk.Label(label="0 Archived")
        self.archived_label.add_css_class("caption")
        self.stats_box.append(self.archived_label)

        sidebar_box.append(self.stats_box)

        sidebar_page.set_child(sidebar_box)
        self.split_view.set_sidebar(sidebar_page)

        # === CONTENT AREA ===
        content_page = Adw.NavigationPage()
        content_page.set_title("Detaljer")

        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.content_stack.set_transition_duration(350)

        # Welcome page (when no victory selected)
        welcome = self._build_welcome_page()
        self.content_stack.add_named(welcome, "welcome")

        # Detail page (when victory selected) - GENEROUS SPACING
        self.detail_scroll = Gtk.ScrolledWindow()
        self.detail_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.detail_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=32)
        self.detail_box.set_margin_start(40)
        self.detail_box.set_margin_end(40)
        self.detail_box.set_margin_top(32)
        self.detail_box.set_margin_bottom(40)
        self.detail_scroll.set_child(self.detail_box)
        self.content_stack.add_named(self.detail_scroll, "detail")

        content_page.set_child(self.content_stack)
        self.split_view.set_content(content_page)

        self.content_stack.set_visible_child_name("welcome")

    def _build_welcome_page(self):
        """Build the welcome page with VF Logo and Leaderboard"""
        # Main scrollable container
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # === TOP HEADER WITH VF LOGO ===
        header_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        header_area.add_css_class("welcome-header")
        header_area.set_margin_top(32)
        header_area.set_margin_bottom(24)
        header_area.set_halign(Gtk.Align.CENTER)

        # VF Logo (centered, prominent)
        vf_logo = VFLogoWidget(size=80)
        header_area.append(vf_logo)

        # Title
        title = Gtk.Label(label="SEJRLISTE MESTERVÆRK")
        title.add_css_class("title-1")
        title.add_css_class("vindertavle-title")
        header_area.append(title)

        # Subtitle
        subtitle = Gtk.Label(label="Kv1nt Admiral Standard • Cirkelline")
        subtitle.add_css_class("caption")
        subtitle.add_css_class("dim-label")
        header_area.append(subtitle)

        main_box.append(header_area)

        # === QUICK STATS ROW ===
        stats = get_system_stats()
        stats_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        stats_row.set_halign(Gtk.Align.CENTER)
        stats_row.set_margin_bottom(16)

        # Opret chakra-farvede statistik badges
        stat_configs = [
            (str(stats["total_victorys"]), "All", "divine"),
            (str(stats["archived"]), "Archived", "wisdom"),
            (str(stats["grand_admirals"]), "Admiraler", "heart"),
            (f"{stats['completed_checkboxes']}", "✓ Complete", "intuition"),
        ]

        for value, label, chakra in stat_configs:
            stat_badge = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            stat_badge.add_css_class("stat-badge")
            stat_badge.add_css_class(f"chakra-{chakra}")

            val_label = Gtk.Label(label=value)
            val_label.add_css_class("title-2")
            val_label.add_css_class(f"chakra-{chakra}-text")
            stat_badge.append(val_label)

            name_label = Gtk.Label(label=label)
            name_label.add_css_class("caption")
            name_label.add_css_class("dim-label")
            stat_badge.append(name_label)

            stats_row.append(stat_badge)

        main_box.append(stats_row)

        # === ACTION BUTTONS ===
        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        buttons_box.set_halign(Gtk.Align.CENTER)
        buttons_box.set_margin_bottom(24)

        new_btn = Gtk.Button()
        new_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        new_btn_icon = Gtk.Image.new_from_icon_name("list-add-symbolic")
        new_btn_box.append(new_btn_icon)
        new_btn_label = Gtk.Label(label="New Victory")
        new_btn_box.append(new_btn_label)
        new_btn.set_child(new_btn_box)
        new_btn.add_css_class("suggested-action")
        new_btn.add_css_class("pill")
        new_btn.connect("clicked", self._on_new_sejr)
        buttons_box.append(new_btn)

        open_btn = Gtk.Button()
        open_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        open_btn_icon = Gtk.Image.new_from_icon_name("folder-open-symbolic")
        open_btn_box.append(open_btn_icon)
        open_btn_label = Gtk.Label(label="Open System")
        open_btn_box.append(open_btn_label)
        open_btn.set_child(open_btn_box)
        open_btn.add_css_class("pill")
        open_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", str(SYSTEM_PATH)]))
        buttons_box.append(open_btn)

        main_box.append(buttons_box)

        # === ACHIEVEMENT PANEL - GAMIFICATION ===
        self.achievement_panel = AchievementPanel()
        self.achievement_panel.set_margin_start(24)
        self.achievement_panel.set_margin_end(24)
        self.achievement_panel.set_margin_bottom(24)
        main_box.append(self.achievement_panel)

        # === VINDERTAVLE (Victory Board) - THE MAIN ATTRACTION ===
        vindertavle = Vindertavle()
        vindertavle.set_vexpand(True)
        main_box.append(vindertavle)

        scroll.set_child(main_box)
        return scroll

        # Tip
        tip_label = Gtk.Label(label="💡 Tip: Brug Ctrl+N for hurtig ny victory")
        tip_label.add_css_class("caption")
        tip_label.add_css_class("dim-label")
        main_box.append(tip_label)

        return main_box

    def _build_detail_page(self, sejr):
        """Build the detail view for a victory"""
        # Clear existing
        while child := self.detail_box.get_first_child():
            self.detail_box.remove(child)

        # Header with title
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        icon = Gtk.Image.new_from_icon_name(
            "emblem-ok-symbolic" if sejr["is_archived"] else "folder-open-symbolic"
        )
        icon.set_pixel_size(48)
        if sejr["is_archived"]:
            icon.add_css_class("success")
        header_box.append(icon)

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        title_box.set_hexpand(True)

        title = Gtk.Label(label=sejr["display_name"])
        title.set_halign(Gtk.Align.START)
        title.add_css_class("title-1")
        title_box.append(title)

        subtitle = Gtk.Label(label=f"Pass {victory['current_pass']}/3 • {victory['date']}")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("dim-label")
        title_box.append(subtitle)

        header_box.append(title_box)

        # Open folder button
        open_btn = Gtk.Button(icon_name="folder-open-symbolic")
        open_btn.set_tooltip_text("Open i Files")
        open_btn.set_valign(Gtk.Align.CENTER)
        open_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", sejr["path"]]))
        header_box.append(open_btn)

        self.detail_box.append(header_box)

        # ═══════════════════════════════════════════════════════════════════════════
        # 5W KONTROL PANEL - WHAT/WHERE/WHY/HOW/WHEN
        # ═══════════════════════════════════════════════════════════════════════════
        w5_group = Adw.PreferencesGroup()
        w5_group.set_title("📋 5W KONTROL")
        w5_group.set_description("Alt du behøver at vide om denne victory")

        # WHAT - Formål/beskrivelse (Divine violet)
        hvad_row = Adw.ActionRow()
        hvad_row.set_title("❓ WHAT")
        hvad_row.set_subtitle(sejr.get("hvad", sejr["display_name"]))
        hvad_icon = Gtk.Image.new_from_icon_name("help-about-symbolic")
        hvad_icon.set_pixel_size(32)
        hvad_row.add_prefix(hvad_icon)
        hvad_row.add_css_class("w5-hvad")
        w5_group.add(hvad_row)

        # WHERE - Lokation (Wisdom gold)
        hvor_row = Adw.ActionRow()
        hvor_row.set_title("📍 WHERE")
        hvor_row.set_subtitle(sejr["path"])
        hvor_icon = Gtk.Image.new_from_icon_name("folder-symbolic")
        hvor_icon.set_pixel_size(32)
        hvor_row.add_prefix(hvor_icon)
        hvor_row.add_css_class("w5-hvor")
        # Click to åbne
        hvor_row.set_activatable(True)
        hvor_row.connect("activated", lambda r: subprocess.Popen(["nautilus", sejr["path"]]))
        w5_group.add(hvor_row)

        # WHY - Mål/grund (Heart emerald)
        hvorfor_row = Adw.ActionRow()
        hvorfor_row.set_title("🎯 WHY")
        hvorfor_row.set_subtitle(sejr.get("hvorfor", "Nå Admiral niveau med 30/30 score"))
        hvorfor_icon = Gtk.Image.new_from_icon_name("starred-symbolic")
        hvorfor_icon.set_pixel_size(32)
        hvorfor_row.add_prefix(hvorfor_icon)
        hvorfor_row.add_css_class("w5-hvorfor")
        w5_group.add(hvorfor_row)

        # HOW - Metode (Intuition indigo)
        hvordan_row = Adw.ActionRow()
        hvordan_row.set_title("⚙️ HOW")
        pass_status = f"Pass {victory['current_pass']}/3 • {victory['progress']}% færdig"
        hvordan_row.set_subtitle(pass_status)
        hvordan_icon = Gtk.Image.new_from_icon_name("emblem-system-symbolic")
        hvordan_icon.set_pixel_size(32)
        hvordan_row.add_prefix(hvordan_icon)
        hvordan_row.add_css_class("w5-hvordan")
        # Pass indikator badges
        pass_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        for i in range(1, 4):
            pass_badge = Gtk.Label(label=str(i))
            pass_badge.add_css_class("pass-badge")
            if i < sejr["current_pass"]:
                pass_badge.add_css_class("pass-complete")
            elif i == sejr["current_pass"]:
                pass_badge.add_css_class("pass-active")
            pass_box.append(pass_badge)
        hvordan_row.add_suffix(pass_box)
        w5_group.add(hvordan_row)

        # WHEN - Tidslinje (Sacred magenta)
        hvornaar_row = Adw.ActionRow()
        hvornaar_row.set_title("⏰ WHEN")
        hvornaar_row.set_subtitle(f"Oprettet: {victory['date']} → Mål: Complete i dag")
        hvornaar_icon = Gtk.Image.new_from_icon_name("alarm-symbolic")
        hvornaar_icon.set_pixel_size(32)
        hvornaar_row.add_prefix(hvornaar_icon)
        hvornaar_row.add_css_class("w5-hvornaar")
        w5_group.add(hvornaar_row)

        self.detail_box.append(w5_group)

        # Fremgang sektion
        progress_group = Adw.PreferencesGroup()
        progress_group.set_title("📊 Fremgang")

        # Hovedfremgangsbar
        progress_row = Adw.ActionRow()
        progress_row.set_title(f"Samlet fremdrift: {victory['progress']}%")
        progress_row.set_subtitle(f"{victory['done']}/{victory['total']} opgaver afkrydset")

        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(sejr["progress"] / 100)
        progress_bar.set_valign(Gtk.Align.CENTER)
        progress_bar.set_size_request(200, -1)
        if sejr["progress"] >= 80:
            progress_bar.add_css_class("success")
        progress_row.add_suffix(progress_bar)
        progress_group.add(progress_row)

        # 3-Pass status
        passes_row = Adw.ActionRow()
        passes_row.set_title("3-Pass System")

        passes_box = Gtk.Box(spacing=6)
        passes_box.set_valign(Gtk.Align.CENTER)
        for i in range(1, 4):
            badge = Gtk.Label(label=str(i))
            badge.add_css_class("caption")
            if i <= int(sejr["current_pass"]):
                badge.add_css_class("success")
            else:
                badge.add_css_class("dim-label")
            badge.set_size_request(24, 24)
            passes_box.append(badge)

        passes_row.add_suffix(passes_box)
        progress_group.add(passes_row)

        self.detail_box.append(progress_group)

        # DNA Layers section
        dna_group = Adw.PreferencesGroup()
        dna_group.set_title("7 DNA Layers")
        dna_group.set_description("Systemets selvbevidsthed og automatisering")

        dna_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        dna_box.add_css_class("card")

        for i, (num, name, desc, icon) in enumerate(DNA_LAYERS):
            # Random active status for demo (in real version, check from STATUS.yaml)
            active = sejr["progress"] > (i * 12)
            row = DNALayerRow(num, name, desc, icon, active)
            dna_box.append(row)

            if i < len(DNA_LAYERS) - 1:
                sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                dna_box.append(sep)

        dna_group.add(dna_box)
        self.detail_box.append(dna_group)

        # Quick Actions section
        quick_group = Adw.PreferencesGroup()
        quick_group.set_title("Hurtig Navigation")

        quick_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        quick_box.set_halign(Gtk.Align.START)
        quick_box.set_margin_top(8)
        quick_box.set_margin_bottom(8)

        # Open folder button
        folder_btn = Gtk.Button(label="📁 Open Folder")
        folder_btn.add_css_class("pill")
        folder_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", sejr["path"]]))
        quick_box.append(folder_btn)

        # Open SEJR_LISTE.md
        sejr_file = Path(sejr["path"]) / "SEJR_LISTE.md"
        if sejr_file.exists():
            edit_btn = Gtk.Button(label="📝 Rediger Victory")
            edit_btn.add_css_class("pill")
            edit_btn.connect("clicked", lambda b: subprocess.Popen(["xdg-open", str(sejr_file)]))
            quick_box.append(edit_btn)

        # Open terminal in folder
        term_btn = Gtk.Button(label="💻 Terminal")
        term_btn.add_css_class("pill")
        term_btn.connect("clicked", lambda b: subprocess.Popen(
            ["gnome-terminal", f"--working-directory={victory['path']}"]
        ))
        quick_box.append(term_btn)

        quick_group.add(quick_box)
        self.detail_box.append(quick_group)

        # Files section
        files_group = Adw.PreferencesGroup()
        files_group.set_title("Files")
        files_group.set_description(f"{len(victory['files'])} files - klik for at åbne")

        for filename in sejr["files"][:10]:
            icon_name = "text-x-generic-symbolic"
            if filename.endswith(".md"):
                icon_name = "text-x-markdown-symbolic"
            elif filename.endswith(".yaml"):
                icon_name = "text-x-script-symbolic"
            elif filename.endswith(".jsonl"):
                icon_name = "text-x-log-symbolic"

            file_row = Adw.ActionRow()
            file_row.set_title(filename)
            file_row.add_prefix(Gtk.Image.new_from_icon_name(icon_name))
            file_row.set_activatable(True)

            # Store file path for click handler
            file_path = Path(sejr["path"]) / filename
            file_row.connect("activated", lambda r, fp=file_path: subprocess.Popen(["xdg-open", str(fp)]))

            # Add open button
            open_icon = Gtk.Image.new_from_icon_name("document-open-symbolic")
            file_row.add_suffix(open_icon)

            files_group.add(file_row)

        self.detail_box.append(files_group)

        # Actions section
        actions_group = Adw.PreferencesGroup()
        actions_group.set_title("DNA Actions")

        actions = [
            ("Verify", "emblem-ok-symbolic", "auto_verify.py"),
            ("Learn", "view-refresh-symbolic", "auto_learn.py"),
            ("Predict", "weather-clear-symbolic", "auto_predict.py"),
            ("Archive", "folder-symbolic", "auto_archive.py"),
        ]

        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        actions_box.set_halign(Gtk.Align.CENTER)
        actions_box.set_margin_top(12)
        actions_box.set_margin_bottom(12)

        for label, icon, script in actions:
            btn = Gtk.Button()
            btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            btn_box.append(Gtk.Image.new_from_icon_name(icon))
            btn_box.append(Gtk.Label(label=label))
            btn.set_child(btn_box)
            btn.add_css_class("flat")
            btn.connect("clicked", lambda b, s=script: self._run_script(s))
            actions_box.append(btn)

        actions_group.add(actions_box)
        self.detail_box.append(actions_group)

        # Chat Stream sektion - MESSENGER STYLE!
        chat_group = Adw.PreferencesGroup()
        chat_group.set_title("💬 Activity Stream")
        chat_group.set_description("Live samtale om hvad der happens")

        chat_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        chat_card.add_css_class("card")

        self.chat_stream = ChatStream(Path(sejr["path"]))
        chat_card.append(self.chat_stream)

        chat_group.add(chat_card)
        self.detail_box.append(chat_group)

    def _load_sejrs(self):
        """Load all victorys into the sidebar"""
        self.sejrs = get_all_sejrs()

        # Log til activitysmonitor
        if hasattr(self, 'activity_monitor'):
            self.activity_monitor.log_event("system", f"Indlæste {len(self.sejrs)} victorys", "🔄")

        # Clear list
        while row := self.sejr_list.get_first_child():
            self.sejr_list.remove(row)

        active_count = 0
        archived_count = 0

        # Active section header
        active_header = Gtk.Label(label="AKTIVE")
        active_header.add_css_class("caption")
        active_header.add_css_class("dim-label")
        active_header.set_halign(Gtk.Align.START)
        active_header.set_margin_start(12)
        active_header.set_margin_top(12)
        active_header.set_margin_bottom(6)
        self.sejr_list.append(active_header)

        for sejr in self.sejrs:
            if not sejr["is_archived"]:
                row = SejrRow(sejr)
                self.sejr_list.append(row)
                active_count += 1

        if active_count == 0:
            empty = Gtk.Label(label="No active victoriess")
            empty.add_css_class("dim-label")
            empty.set_margin_start(12)
            empty.set_margin_bottom(12)
            self.sejr_list.append(empty)

        # Archived section header
        archive_header = Gtk.Label(label="ARKIVEREDE")
        archive_header.add_css_class("caption")
        archive_header.add_css_class("dim-label")
        archive_header.set_halign(Gtk.Align.START)
        archive_header.set_margin_start(12)
        archive_header.set_margin_top(18)
        archive_header.set_margin_bottom(6)
        self.sejr_list.append(archive_header)

        for sejr in self.sejrs:
            if sejr["is_archived"]:
                row = SejrRow(sejr)
                self.sejr_list.append(row)
                archived_count += 1

        if archived_count == 0:
            empty = Gtk.Label(label="No archived victoriess")
            empty.add_css_class("dim-label")
            empty.set_margin_start(12)
            empty.set_margin_bottom(12)
            self.sejr_list.append(empty)

        # Update stats
        self.active_label.set_label(f"{active_count} Active")
        self.archived_label.set_label(f"{archived_count} Archived")

        return True  # For timeout

    def _apply_filter(self, filter_type: str):
        """Apply filter to victory list"""
        self.current_filter = filter_type

        # Update toggle button states
        self.filter_all.set_active(filter_type == "all")
        self.filter_active.set_active(filter_type == "active")
        self.filter_archived.set_active(filter_type == "archived")

        # Reload with filter
        self._load_sejrs_filtered()

    def _apply_sort(self):
        """Apply sort to victory list"""
        self._load_sejrs_filtered()

    def _load_sejrs_filtered(self):
        """Load victorys with current filter and sort applied"""
        self.sejrs = get_all_sejrs()

        # Apply filter
        if self.current_filter == "active":
            filtered_sejrs = [s for s in self.sejrs if not s["is_archived"]]
        elif self.current_filter == "archived":
            filtered_sejrs = [s for s in self.sejrs if s["is_archived"]]
        else:
            filtered_sejrs = self.sejrs

        # Apply sort
        sort_idx = self.sort_dropdown.get_selected()
        if sort_idx == 0:  # Dato
            filtered_sejrs.sort(key=lambda s: s.get("created", ""), reverse=True)
        elif sort_idx == 1:  # Score
            filtered_sejrs.sort(key=lambda s: s.get("score", 0), reverse=True)
        elif sort_idx == 2:  # Navn
            filtered_sejrs.sort(key=lambda s: s.get("display_name", ""))

        # Clear list
        while row := self.sejr_list.get_first_child():
            self.sejr_list.remove(row)

        active_count = len([s for s in self.sejrs if not s["is_archived"]])
        archived_count = len([s for s in self.sejrs if s["is_archived"]])

        # Show appropriate header based on filter
        if self.current_filter == "all":
            # Active section header
            if any(not s["is_archived"] for s in filtered_sejrs):
                active_header = Gtk.Label(label="🔵 AKTIVE")
                active_header.add_css_class("caption")
                active_header.add_css_class("dim-label")
                active_header.set_halign(Gtk.Align.START)
                active_header.set_margin_start(12)
                active_header.set_margin_top(12)
                active_header.set_margin_bottom(6)
                self.sejr_list.append(active_header)

                for sejr in filtered_sejrs:
                    if not sejr["is_archived"]:
                        row = SejrRow(sejr)
                        self.sejr_list.append(row)

            # Archived section header
            if any(s["is_archived"] for s in filtered_sejrs):
                archive_header = Gtk.Label(label="✅ ARKIVEREDE")
                archive_header.add_css_class("caption")
                archive_header.add_css_class("dim-label")
                archive_header.set_halign(Gtk.Align.START)
                archive_header.set_margin_start(12)
                archive_header.set_margin_top(18)
                archive_header.set_margin_bottom(6)
                self.sejr_list.append(archive_header)

                for sejr in filtered_sejrs:
                    if sejr["is_archived"]:
                        row = SejrRow(sejr)
                        self.sejr_list.append(row)
        else:
            # Single section (filtered view)
            header_text = "🔵 AKTIVE" if self.current_filter == "active" else "✅ ARKIVEREDE"
            header = Gtk.Label(label=header_text)
            header.add_css_class("caption")
            header.add_css_class("dim-label")
            header.set_halign(Gtk.Align.START)
            header.set_margin_start(12)
            header.set_margin_top(12)
            header.set_margin_bottom(6)
            self.sejr_list.append(header)

            for sejr in filtered_sejrs:
                row = SejrRow(sejr)
                self.sejr_list.append(row)

            if not filtered_sejrs:
                empty_text = "No active victoriess" if self.current_filter == "active" else "No archived victoriess"
                empty = Gtk.Label(label=empty_text)
                empty.add_css_class("dim-label")
                empty.set_margin_start(12)
                empty.set_margin_bottom(12)
                self.sejr_list.append(empty)

        # Update stats
        self.active_label.set_label(f"{active_count} Active")
        self.archived_label.set_label(f"{archived_count} Archived")

    def _on_sejr_selected(self, listbox, row):
        """Handle victory selection"""
        if hasattr(row, 'victory_info'):
            self.selected_sejr = row.sejr_info
            self._build_detail_page(row.sejr_info)
            self.content_stack.set_visible_child_name("detail")
            self.split_view.set_show_content(True)

    def _on_new_sejr(self, button):
        """Create a new victory with dialog for name input"""
        # Create dialog
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="Opret New Victory",
            body="Indtast navn på din nye victory:"
        )

        # Add entry
        entry = Gtk.Entry()
        entry.set_placeholder_text("F.eks. MIN_FEATURE")
        entry.set_margin_start(20)
        entry.set_margin_end(20)
        entry.set_margin_bottom(10)
        dialog.set_extra_child(entry)

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("create", "Opret")
        dialog.set_response_appearance("create", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("create")
        dialog.set_close_response("cancel")

        def on_response(dialog, response):
            if response == "create":
                name = entry.get_text().strip()
                if name:
                    # Replace spaces with underscores
                    name = name.replace(" ", "_").upper()
                    self._create_sejr(name)
            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.present()

    def _on_convert_to_sejr(self, button):
        """Open universal converter dialog - 5W KONTROL"""
        dialog = Adw.Window(transient_for=self)
        dialog.set_title("🔄 Universal Victory Converter")
        dialog.set_default_size(600, 700)
        dialog.set_modal(True)

        # Main content
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        dialog.set_content(main_box)

        # Header
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        main_box.append(header)

        # Content scroll
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)

        # Title
        title_label = Gtk.Label(label="Konverter ALT til SEJR Struktur")
        title_label.add_css_class("title-1")
        content_box.append(title_label)

        subtitle_label = Gtk.Label(label="Select input type, kontrol mode, og definer 5W")
        subtitle_label.add_css_class("dim-label")
        content_box.append(subtitle_label)

        # === INPUT TYPE SELECTION ===
        input_group = Adw.PreferencesGroup()
        input_group.set_title("📥 INPUT TYPE")
        input_group.set_description("Hvad vil du konvertere?")

        self.convert_input_type = Gtk.ComboBoxText()
        for key, label in SejrConverter.INPUT_TYPES.items():
            self.convert_input_type.append(key, label)
        self.convert_input_type.set_active_id("folder")

        input_row = Adw.ActionRow()
        input_row.set_title("Type")
        input_row.add_suffix(self.convert_input_type)
        input_group.add(input_row)

        # Input path/text
        self.convert_input_entry = Gtk.Entry()
        self.convert_input_entry.set_placeholder_text("/sti/til/folder/eller/fil")
        self.convert_input_entry.set_hexpand(True)

        path_row = Adw.ActionRow()
        path_row.set_title("Kilde")
        path_row.set_subtitle("Sti til folder/fil, eller indtast tekst")
        path_row.add_suffix(self.convert_input_entry)

        browse_btn = Gtk.Button(icon_name="folder-open-symbolic")
        browse_btn.set_valign(Gtk.Align.CENTER)
        browse_btn.connect("clicked", lambda b: self._browse_for_input())
        path_row.add_suffix(browse_btn)

        input_group.add(path_row)
        content_box.append(input_group)

        # === CONTROL MODE SELECTION ===
        mode_group = Adw.PreferencesGroup()
        mode_group.set_title("🎛️ KONTROL MODE")
        mode_group.set_description("Hvordan vil du styre processen?")

        self.convert_mode = Gtk.ComboBoxText()
        for key, label in SejrConverter.CONTROL_MODES.items():
            self.convert_mode.append(key, label)
        self.convert_mode.set_active_id("manual")

        mode_row = Adw.ActionRow()
        mode_row.set_title("Mode")
        mode_row.add_suffix(self.convert_mode)
        mode_group.add(mode_row)
        content_box.append(mode_group)

        # === 5W KONTROL ===
        w5_group = Adw.PreferencesGroup()
        w5_group.set_title("🎯 5W KONTROL")
        w5_group.set_description("Du har TOTAL KONTROL over alt")

        # WHAT
        self.convert_hvad = Gtk.Entry()
        self.convert_hvad.set_placeholder_text("Hvad skal konverteres/bygges?")
        hvad_row = Adw.ActionRow()
        hvad_row.set_title("WHAT")
        hvad_row.set_subtitle("Beskrivelse af opgaven")
        hvad_row.add_suffix(self.convert_hvad)
        w5_group.add(hvad_row)

        # WHY
        self.convert_hvorfor = Gtk.Entry()
        self.convert_hvorfor.set_placeholder_text("Formål med denne victory")
        hvorfor_row = Adw.ActionRow()
        hvorfor_row.set_title("WHY")
        hvorfor_row.set_subtitle("Formålet/værdien")
        hvorfor_row.add_suffix(self.convert_hvorfor)
        w5_group.add(hvorfor_row)

        # HOW
        self.convert_hvordan = Gtk.Entry()
        self.convert_hvordan.set_placeholder_text("3-pass system")
        hvordan_row = Adw.ActionRow()
        hvordan_row.set_title("HOW")
        hvordan_row.set_subtitle("Tilgangen/metoden")
        hvordan_row.add_suffix(self.convert_hvordan)
        w5_group.add(hvordan_row)

        # WHEN
        self.convert_hvornaar = Gtk.Entry()
        self.convert_hvornaar.set_placeholder_text("Nu → Complete")
        hvornaar_row = Adw.ActionRow()
        hvornaar_row.set_title("WHEN")
        hvornaar_row.set_subtitle("Timeline/deadline")
        hvornaar_row.add_suffix(self.convert_hvornaar)
        w5_group.add(hvornaar_row)

        content_box.append(w5_group)

        # === SEJR NAME ===
        name_group = Adw.PreferencesGroup()
        name_group.set_title("📛 SEJR NAVN")

        self.convert_name = Gtk.Entry()
        self.convert_name.set_placeholder_text("PROJEKT_NAVN")
        name_row = Adw.ActionRow()
        name_row.set_title("Name")
        name_row.set_subtitle("Name på den nye victory (VERSALER)")
        name_row.add_suffix(self.convert_name)
        name_group.add(name_row)
        content_box.append(name_group)

        scroll.set_child(content_box)
        main_box.append(scroll)

        # Bottom action bar
        action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        action_bar.set_margin_start(24)
        action_bar.set_margin_end(24)
        action_bar.set_margin_top(16)
        action_bar.set_margin_bottom(16)
        action_bar.set_halign(Gtk.Align.END)

        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.connect("clicked", lambda b: dialog.close())
        action_bar.append(cancel_btn)

        create_btn = Gtk.Button(label="🚀 Create Victory")
        create_btn.add_css_class("suggested-action")
        create_btn.connect("clicked", lambda b: self._execute_conversion(dialog))
        action_bar.append(create_btn)

        main_box.append(action_bar)

        dialog.present()

    def _browse_for_input(self):
        """Open file chooser for input selection"""
        # Use Nautilus to let user copy path
        subprocess.Popen(["nautilus", str(SYSTEM_PATH)])
        send_notification("📁 File Browser", "Kopiér stien til det du vil konvertere")

    def _execute_conversion(self, dialog):
        """Execute the conversion based on dialog inputs"""
        converter = SejrConverter(SYSTEM_PATH)

        config = {
            "name": self.convert_name.get_text().strip().upper().replace(" ", "_") or "NY_SEJR",
            "input_path": self.convert_input_entry.get_text().strip(),
            "input_type": self.convert_input_type.get_active_id(),
            "mode": self.convert_mode.get_active_id(),
            "hvad": self.convert_hvad.get_text().strip(),
            "hvorfor": self.convert_hvorfor.get_text().strip(),
            "hvordan": self.convert_hvordan.get_text().strip() or "3-pass system",
            "hvornaar": self.convert_hvornaar.get_text().strip() or "Nu → Complete",
            "tasks": [],
        }

        # Analyze input and get suggested tasks
        if config["input_path"]:
            analysis = converter.analyze_input(config["input_path"], config["input_type"])
            config["tasks"] = analysis.get("suggested_tasks", [])

            # Use suggested name if not provided
            if config["name"] == "NY_SEJR" and analysis.get("suggested_name"):
                config["name"] = analysis["suggested_name"]

        # Add default tasks if none detected
        if not config["tasks"]:
            config["tasks"] = [
                "Analysér input",
                "Planlæg struktur",
                "Implementér løsning",
                "Verificér resultat",
                "Dokumentér",
            ]

        # Create the victory
        sejr_path = converter.create_sejr_from_input(config)

        # Close dialog
        dialog.close()

        # Reload and show the new victory
        self._load_sejrs()

        # Find and display the new victory
        for sejr in self.sejrs:
            if config["name"] in sejr["name"]:
                self.selected_sejr = sejr
                self._build_detail_page(sejr)
                self.content_stack.set_visible_child_name("detail")
                self.split_view.set_show_content(True)

                # Open in Nautilus
                subprocess.Popen(["nautilus", str(sejr_path)])

                # Send notification
                send_notification(
                    "✅ Victory Oprettet!",
                    f"{config['name']} er klar med 5W kontrol"
                )

                # Add to chat stream if available
                if hasattr(self, 'chat_stream') and self.chat_stream:
                    self.chat_stream.add_message(
                        sender="System",
                        content=f"Ny victory oprettet: {config['name']}",
                        msg_type="info",
                        file_link=str(sejr_path / "SEJR_LISTE.md")
                    )
                break

    def _create_sejr(self, name):
        """Actually create the victory"""
        script_path = SCRIPTS_DIR / "generate_victory.py"
        if script_path.exists():
            try:
                result = subprocess.run(
                    ["python3", str(script_path), "--name", name],
                    cwd=str(SYSTEM_PATH),
                    capture_output=True,
                    text=True
                )
                self._load_sejrs()

                # Find and select the new victory
                for sejr in self.sejrs:
                    if name in sejr["name"]:
                        self._build_detail_page(sejr)
                        self.content_stack.set_visible_child_name("detail")
                        self.split_view.set_show_content(True)
                        # Open in Nautilus too
                        subprocess.Popen(["nautilus", sejr["path"]])
                        break
            except Exception as e:
                print(f"Error: {e}")

    def _run_script(self, script_name):
        """Run a DNA layer script with notifications and chat updates"""
        script_path = SCRIPTS_DIR / script_name

        # Script metadata for chat
        script_info = {
            "auto_verify.py": {
                "sender": "Verify",
                "start_msg": "Runer verification...",
                "success_msg": "✅ All tests passed!",
                "title": "✅ Verification",
                "body": "Victory verificeret!"
            },
            "auto_learn.py": {
                "sender": "DNA",
                "start_msg": "Analyserer patterns...",
                "success_msg": "🧠 Nye patterns lært og gemt!",
                "title": "🧠 Patterns",
                "body": "Nye patterns lært!"
            },
            "auto_predict.py": {
                "sender": "Kv1nt",
                "start_msg": "Genererer forudsigelser...",
                "success_msg": "🔮 Next skridt beregnet!",
                "title": "🔮 Predictions",
                "body": "Predictelser genereret!"
            },
            "auto_archive.py": {
                "sender": "Admiral",
                "start_msg": "Archiveer victory...",
                "success_msg": "🏆 SEJR ARKIVERET! Du er fantastisk!",
                "title": "🏆 Archived",
                "body": "Victory arkiveret med succes!"
            },
        }

        info = script_info.get(script_name, {
            "sender": "System",
            "start_msg": f"Runer {script_name}...",
            "success_msg": "Script færdig",
            "title": "Script",
            "body": "Complete"
        })

        # Add starting message to chat
        if hasattr(self, 'chat_stream') and self.chat_stream:
            self.chat_stream.add_message(
                sender=info["sender"],
                content=info["start_msg"],
                msg_type="info"
            )

        if script_path.exists():
            try:
                result = subprocess.run(
                    ["python3", str(script_path)],
                    cwd=str(SYSTEM_PATH),
                    capture_output=True,
                    text=True
                )
                self._load_sejrs()

                # Add success message to chat
                if hasattr(self, 'chat_stream') and self.chat_stream:
                    # Check if there was output
                    output = result.stdout.strip() if result.stdout else info["success_msg"]
                    if len(output) > 200:
                        output = output[:200] + "..."

                    self.chat_stream.add_message(
                        sender=info["sender"],
                        content=output if output else info["success_msg"],
                        msg_type="info",
                        verification={"passed": result.returncode == 0, "message": "Verified" if result.returncode == 0 else "Error"}
                    )

                # Send desktop notification
                send_notification(info["title"], info["body"])

                # Special celebration for archive
                if script_name == "auto_archive.py":
                    self._show_celebration()

            except Exception as e:
                # Add error to chat
                if hasattr(self, 'chat_stream') and self.chat_stream:
                    self.chat_stream.add_message(
                        sender="Error",
                        content=f"Script fejlede: {e}",
                        msg_type="error",
                        verification={"passed": False, "message": str(e)}
                    )
                send_notification("❌ Error", f"Script fejlede: {e}")
                print(f"Error: {e}")

    def _show_celebration(self):
        """Show celebration dialog when victory is archived"""
        stats = get_system_stats()

        # Trigger konfetti animation!
        if hasattr(self, 'konfetti'):
            # More konfetti for Grand Admirals!
            if stats['grand_admirals'] > 10:
                self.konfetti.celebrate("epic")
            else:
                self.konfetti.celebrate("normal")

        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="🏆 SEJR ARKIVERET!",
            body=f"""Congratulations! Din victory er nu arkiveret.

📊 System Status:
• Total sejrs: {stats['total_victorys']}
• Aktive: {stats['active']}
• Arkiverede: {stats['archived']}
• Grand Admirals: {stats['grand_admirals']} 🏅

Du er på vej mod Admiral niveau!"""
        )

        dialog.add_response("ok", "Fantastisk! 🎉")
        dialog.set_default_response("ok")
        dialog.present()

        # Update achievements panel
        if hasattr(self, 'achievement_panel'):
            self.achievement_panel._check_achievements()

    def _open_current_folder(self):
        """Open current victory folder in Nautilus"""
        if self.selected_sejr:
            subprocess.Popen(["nautilus", self.selected_sejr["path"]])
        else:
            subprocess.Popen(["nautilus", str(SYSTEM_PATH)])

    def _auto_refresh(self):
        """Auto-refresh every 5 seconds"""
        self._load_sejrs()
        if self.selected_sejr:
            # Refresh current view
            for sejr in self.sejrs:
                if sejr["path"] == self.selected_sejr["path"]:
                    self._build_detail_page(sejr)
                    break
        return True

    # ═══════════════════════════════════════════════════════════════════════════
    # REAL-TIME FILE MONITORING
    # ═══════════════════════════════════════════════════════════════════════════

    def _setup_file_monitoring(self):
        """Setup Gio.FileMonitor for real-time updates"""
        # Monitor active folder
        active_gfile = Gio.File.new_for_path(str(ACTIVE_DIR))
        if active_gfile.query_exists():
            try:
                monitor = active_gfile.monitor_directory(Gio.FileMonitorFlags.WATCH_MOVES, None)
                monitor.connect("changed", self._on_file_changed)
                self.file_monitors.append(monitor)
            except Exception as e:
                print(f"Could not setup file monitoring: {e}")

        # Monitor archive folder
        archive_gfile = Gio.File.new_for_path(str(ARCHIVE_DIR))
        if archive_gfile.query_exists():
            try:
                monitor = archive_gfile.monitor_directory(Gio.FileMonitorFlags.WATCH_MOVES, None)
                monitor.connect("changed", self._on_file_changed)
                self.file_monitors.append(monitor)
            except Exception as e:
                print(f"Could not setup archive monitoring: {e}")

    def _on_file_changed(self, monitor, file, other_file, event_type):
        """Handle file system changes - real-time refresh"""
        if event_type in [Gio.FileMonitorEvent.CREATED, Gio.FileMonitorEvent.DELETED,
                         Gio.FileMonitorEvent.CHANGED, Gio.FileMonitorEvent.MOVED_IN,
                         Gio.FileMonitorEvent.MOVED_OUT]:

            # Log til activitysmonitor
            if hasattr(self, 'activity_monitor'):
                file_path = file.get_path() if file else "ukendt"
                file_name = Path(file_path).name if file_path else "fil"

                event_icons = {
                    Gio.FileMonitorEvent.CREATED: ("✨", "Oprettet"),
                    Gio.FileMonitorEvent.DELETED: ("🗑️", "Deletetet"),
                    Gio.FileMonitorEvent.CHANGED: ("📝", "Ændret"),
                    Gio.FileMonitorEvent.MOVED_IN: ("📥", "Movetet ind"),
                    Gio.FileMonitorEvent.MOVED_OUT: ("📤", "Movetet ud"),
                }
                icon, action = event_icons.get(event_type, ("📌", "Handling"))
                self.activity_monitor.log_event("fil", f"{action}: {file_name[:40]}", icon)

            # Debounce rapid changes - refresh after 500ms
            GLib.timeout_add(500, self._debounced_refresh)

    def _debounced_refresh(self):
        """Debounced refresh to avoid rapid-fire updates"""
        self._load_sejrs()
        return False  # Don't repeat

    # ═══════════════════════════════════════════════════════════════════════════
    # DRAG & DROP SUPPORT
    # ═══════════════════════════════════════════════════════════════════════════

    def _setup_drag_drop(self):
        """Setup drag and drop for importing files/folders to create victorys"""
        # Create drop target for the main window
        drop_target = Gtk.DropTarget.new(Gio.File, Gdk.DragAction.COPY)
        drop_target.connect("drop", self._on_drop)
        drop_target.connect("enter", self._on_drag_enter)
        drop_target.connect("leave", self._on_drag_leave)
        self.add_controller(drop_target)

    def _on_drag_enter(self, drop_target, x, y):
        """Visual feedback when dragging over window"""
        self.add_css_class("drop-active")
        return Gdk.DragAction.COPY

    def _on_drag_leave(self, drop_target):
        """Remove visual feedback"""
        self.remove_css_class("drop-active")

    def _on_drop(self, drop_target, value, x, y):
        """Handle dropped files/folders - create new victory"""
        self.remove_css_class("drop-active")

        if isinstance(value, Gio.File):
            path = value.get_path()
            if path:
                # Log til activitysmonitor
                if hasattr(self, 'activity_monitor'):
                    self.activity_monitor.log_event("drag-drop", f"Fil droppet: {Path(path).name[:40]}", "📂")
                # Show conversion dialog with the dropped path
                self._show_conversion_dialog(Path(path))
                return True
        return False

    def _show_conversion_dialog(self, dropped_path: Path):
        """Show dialog to convert dropped file/folder to Victory"""
        dialog = Adw.AlertDialog()
        dialog.set_heading("Konverter til Victory")
        dialog.set_body(f"Vil du oprette en ny Victory fra:\n{dropped_path.name}?")
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("convert", "Konverter")
        dialog.set_response_appearance("convert", Adw.ResponseAppearance.SUGGESTED)

        def on_response(dlg, response):
            if response == "convert":
                # Use the converter
                self._convert_path_to_sejr(dropped_path)

        dialog.connect("response", on_response)
        dialog.present(self)

    def _convert_path_to_sejr(self, path: Path):
        """Actually convert a path to a new Victory"""
        try:
            converter = SejrConverter()

            if path.is_file():
                sejr_path = converter.from_file(path)
            elif path.is_dir():
                sejr_path = converter.from_folder(path)
            else:
                return

            # Refresh and select the new victory
            self._load_sejrs()

            # Find and select the new victory
            for sejr in self.sejrs:
                if sejr["path"] == sejr_path:
                    self._build_detail_page(sejr)
                    self.content_stack.set_visible_child_name("detail")
                    break

            # Notification
            toast = Adw.Toast(title=f"New Victory oprettet: {path.name}")
            toast.set_timeout(3)
            self.add_toast(toast) if hasattr(self, 'add_toast') else None

        except Exception as e:
            print(f"Konvertering fejlede: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    # ZOOM FUNCTIONALITY
    # ═══════════════════════════════════════════════════════════════════════════

    def _on_zoom_changed(self, scale):
        """Handle zoom level changes using font scaling (GTK4 compatible)"""
        self.zoom_level = scale.get_value()
        # Update zoom label
        self.zoom_label.set_text(f"{int(self.zoom_level * 100)}%")

        # Apply zoom via font scaling (GTK4 doesn't support CSS transform)
        base_sizes = {'title': 28, 'heading': 20, 'body': 14, 'caption': 11}

        css = f"""
        .detail-content label {{
            font-size: {int(base_sizes['body'] * self.zoom_level)}px;
        }}
        .detail-content .title-1 {{
            font-size: {int(base_sizes['title'] * self.zoom_level)}px;
        }}
        .detail-content .title-2 {{
            font-size: {int(base_sizes['heading'] * self.zoom_level)}px;
        }}
        .detail-content .heading {{
            font-size: {int(base_sizes['heading'] * self.zoom_level)}px;
        }}
        .detail-content .caption {{
            font-size: {int(base_sizes['caption'] * self.zoom_level)}px;
        }}
        """
        self._apply_dynamic_css(css)

    def _zoom_step(self, delta):
        """Step zoom in or out"""
        new_value = max(0.5, min(2.0, self.zoom_scale.get_value() + delta))
        self.zoom_scale.set_value(new_value)

    def _zoom_reset(self):
        """Reset zoom to 100%"""
        self.zoom_scale.set_value(1.0)

    def _apply_dynamic_css(self, css_text):
        """Apply dynamic CSS"""
        provider = Gtk.CssProvider()
        provider.load_from_string(css_text)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # DNA SCRIPT RUNNERS (Keyboard Shortcuts)
    # ═══════════════════════════════════════════════════════════════════════════

    def _run_verify_script(self):
        """Run auto_verify.py script (V key)"""
        script_path = SYSTEM_PATH / "scripts" / "auto_verify.py"
        if script_path.exists():
            try:
                subprocess.Popen(["python3", str(script_path)])
                self._show_toast("Runer verifikation...")
            except Exception as e:
                self._show_toast(f"Error: {e}")

    def _run_archive_script(self):
        """Run auto_archive.py script (A key)"""
        if not self.selected_sejr:
            self._show_toast("Select a victory først")
            return

        script_path = SYSTEM_PATH / "scripts" / "auto_archive.py"
        if script_path.exists():
            try:
                subprocess.Popen(["python3", str(script_path), str(self.selected_sejr["path"])])
                self._show_toast("Archiveer victory...")
            except Exception as e:
                self._show_toast(f"Error: {e}")

    def _run_predict_script(self):
        """Run auto_predict.py script (P key)"""
        script_path = SYSTEM_PATH / "scripts" / "auto_predict.py"
        if script_path.exists():
            try:
                subprocess.Popen(["python3", str(script_path)])
                self._show_toast("Genererer forudsigelser...")
            except Exception as e:
                self._show_toast(f"Error: {e}")

    def _show_toast(self, message):
        """Show a toast notification"""
        # Use Adw.Toast overlay if available
        toast = Adw.Toast(title=message)
        toast.set_timeout(2)
        # Try to show via toast overlay
        try:
            overlay = self.get_content()
            if hasattr(overlay, 'add_toast'):
                overlay.add_toast(toast)
        except:
            print(f"Toast: {message}")

    # ═══════════════════════════════════════════════════════════════════════════
    # HELP DIALOG
    # ═══════════════════════════════════════════════════════════════════════════

    def _show_help_dialog(self):
        """Show keyboard shortcuts help dialog (? or F1)"""
        dialog = Adw.AlertDialog()
        dialog.set_heading("Keyboard Genveje")

        help_text = """
<b>Navigation</b>
Ctrl+F    Søg
Escape    Luk søgning
Ctrl+R    Refresh

<b>Handlinger</b>
Ctrl+N    Ny Sejr
Ctrl+O    Åbn mappe
V         Kør verifikation
A         Arkivér sejr
P         Generer forudsigelser

<b>Zoom</b>
Ctrl++    Zoom ind
Ctrl+-    Zoom ud
Ctrl+0    Reset zoom

<b>System</b>
Ctrl+Q    Afslut
?/F1      Denne hjælp
"""

        body_label = Gtk.Label()
        body_label.set_markup(help_text)
        body_label.set_halign(Gtk.Align.START)
        body_label.set_margin_top(12)
        body_label.set_margin_bottom(12)
        body_label.set_margin_start(12)
        body_label.set_margin_end(12)

        dialog.set_extra_child(body_label)
        dialog.add_response("close", "Close")
        dialog.present(self)

    # ═══════════════════════════════════════════════════════════════════════════
    # INTELLIGENT SEARCH HANDLERS
    # ═══════════════════════════════════════════════════════════════════════════

    def _on_search_toggled(self, button):
        """Toggle search mode on/off"""
        self.search_mode = button.get_active()
        self.search_bar.set_search_mode(self.search_mode)

        if self.search_mode:
            # Show search results, hide regular list
            self.search_results_scroll.set_visible(True)
            self.search_entry.grab_focus()
        else:
            # Hide search results, show regular list
            self.search_results_scroll.set_visible(False)
            self._clear_search_results()
            self.search_entry.set_text("")

    def _on_search_changed(self, entry):
        """Handle live search as user types"""
        query = entry.get_text().strip()

        if len(query) < 2:
            self._clear_search_results()
            return

        # Perform search
        results = self.search_engine.search(query, max_results=30)
        self._display_search_results(results, query)

    def _on_search_activate(self, entry):
        """Handle Enter press in search - perform full search"""
        query = entry.get_text().strip()

        if len(query) < 2:
            return

        results = self.search_engine.search(query, max_results=50)
        self._display_search_results(results, query)

    def _clear_search_results(self):
        """Clear all search result rows"""
        while row := self.search_results_list.get_first_child():
            self.search_results_list.remove(row)

    def _display_search_results(self, results, query):
        """Display search results in the list"""
        self._clear_search_results()

        if not results:
            # Show no results message
            empty_row = Adw.ActionRow()
            empty_row.set_title("No results")
            empty_row.set_subtitle(f'None match for "{query}"')
            empty_row.add_prefix(Gtk.Image.new_from_icon_name("dialog-question-symbolic"))
            self.search_results_list.append(empty_row)
            return

        # Add header showing result count
        header = Gtk.Label(label=f"RESULTATER ({len(results)})")
        header.add_css_class("caption")
        header.add_css_class("dim-label")
        header.set_halign(Gtk.Align.START)
        header.set_margin_start(12)
        header.set_margin_top(12)
        header.set_margin_bottom(6)
        self.search_results_list.append(header)

        # Group by victory
        current_sejr = None

        for result in results:
            # Add victory separator if new victory
            if result["victory"] != current_sejr:
                current_sejr = result["victory"]
                sejr_header = Gtk.Label(label=current_sejr.split("_2026")[0].replace("_", " "))
                sejr_header.add_css_class("heading")
                sejr_header.set_halign(Gtk.Align.START)
                sejr_header.set_margin_start(12)
                sejr_header.set_margin_top(8)
                sejr_header.set_margin_bottom(4)
                self.search_results_list.append(sejr_header)

            # Create result row
            row = Adw.ActionRow()
            row.result_data = result  # Store data for click handler

            # Icon based on match type
            icon_name = {
                "folder": "folder-symbolic",
                "filename": "text-x-generic-symbolic",
                "content": "format-text-rich-symbolic",
                "log": "text-x-log-symbolic"
            }.get(result["match_type"], "text-x-generic-symbolic")

            row.add_prefix(Gtk.Image.new_from_icon_name(icon_name))

            # Title with highlighted match
            title = result["context"][:80]
            if len(result["context"]) > 80:
                title += "..."
            row.set_title(title)

            # Subtitle with file info
            if result["line_num"] > 0:
                row.set_subtitle(f'{result["file"]} : linje {result["line_num"]}')
            else:
                row.set_subtitle(result["file"])

            # Type badge
            type_badge = Gtk.Label(label=result["match_type"].upper())
            type_badge.add_css_class("caption")
            type_badge.add_css_class("dim-label")
            row.add_suffix(type_badge)

            row.set_activatable(True)
            self.search_results_list.append(row)

    def _on_search_result_activated(self, listbox, row):
        """Handle click on a search result"""
        if not hasattr(row, 'result_data'):
            return

        result = row.result_data

        # Find the victory folder path
        sejr_path = None

        # Check active
        active_path = ACTIVE_DIR / result["victory"]
        if active_path.exists():
            sejr_path = active_path

        # Check archive
        if not sejr_path:
            archive_path = ARCHIVE_DIR / result["victory"]
            if archive_path.exists():
                sejr_path = archive_path

        if not sejr_path:
            return

        # Get full victory info and display it
        sejr_info = get_sejr_info(sejr_path)
        self.selected_sejr = sejr_info
        self._build_detail_page(sejr_info)
        self.content_stack.set_visible_child_name("detail")
        self.split_view.set_show_content(True)

        # If it's a file match, open the file
        if result["match_type"] in ["content", "filename", "log"]:
            file_path = sejr_path / result["file"]
            if file_path.exists():
                # Open in default text editor
                try:
                    subprocess.Popen(["xdg-open", str(file_path)])
                except Exception as e:
                    print(f"Could not åbne fil: {e}")

        # Close search mode
        self.search_btn.set_active(False)


# ═══════════════════════════════════════════════════════════════════════════════
# APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

class MasterpieceApp(Adw.Application):
    """The main application"""

    def __init__(self):
        super().__init__(
            application_id="dk.cirkelline.victoryliste.masterpiece",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        # Force dark mode for modern look
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def do_activate(self):
        """Activate the application"""
        # Load modern 2026 CSS styling
        load_custom_css()

        win = MasterpieceWindow(self)

        # Add keyboard shortcuts
        self._setup_shortcuts(win)

        win.present()

    def _setup_shortcuts(self, win):
        """Setup keyboard shortcuts"""
        # Ctrl+F for search
        search_action = Gio.SimpleAction.new("search", None)
        search_action.connect("activate", lambda a, p: win.search_btn.set_active(True))
        self.add_action(search_action)
        self.set_accels_for_action("app.search", ["<Control>f"])

        # Escape to close search
        escape_action = Gio.SimpleAction.new("escape", None)
        escape_action.connect("activate", lambda a, p: win.search_btn.set_active(False))
        self.add_action(escape_action)
        self.set_accels_for_action("app.escape", ["Escape"])

        # Ctrl+R for refresh
        refresh_action = Gio.SimpleAction.new("refresh", None)
        refresh_action.connect("activate", lambda a, p: win._load_sejrs())
        self.add_action(refresh_action)
        self.set_accels_for_action("app.refresh", ["<Control>r"])

        # Ctrl+O for open folder
        open_action = Gio.SimpleAction.new("open-folder", None)
        open_action.connect("activate", lambda a, p: win._open_current_folder())
        self.add_action(open_action)
        self.set_accels_for_action("app.open-folder", ["<Control>o"])

        # Ctrl+N for new victory
        new_action = Gio.SimpleAction.new("new-victory", None)
        new_action.connect("activate", lambda a, p: win._on_new_sejr(None))
        self.add_action(new_action)
        self.set_accels_for_action("app.new-victory", ["<Control>n"])

        # Ctrl+Q for quit
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda a, p: self.quit())
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Control>q"])

        # V for verification
        verify_action = Gio.SimpleAction.new("verify", None)
        verify_action.connect("activate", lambda a, p: win._run_verify_script())
        self.add_action(verify_action)
        self.set_accels_for_action("app.verify", ["v"])

        # A for archive
        archive_action = Gio.SimpleAction.new("archive", None)
        archive_action.connect("activate", lambda a, p: win._run_archive_script())
        self.add_action(archive_action)
        self.set_accels_for_action("app.archive", ["a"])

        # P for predictions
        predict_action = Gio.SimpleAction.new("predict", None)
        predict_action.connect("activate", lambda a, p: win._run_predict_script())
        self.add_action(predict_action)
        self.set_accels_for_action("app.predict", ["p"])

        # Zoom shortcuts
        zoom_in_action = Gio.SimpleAction.new("zoom-in", None)
        zoom_in_action.connect("activate", lambda a, p: win._zoom_step(0.1))
        self.add_action(zoom_in_action)
        self.set_accels_for_action("app.zoom-in", ["<Control>plus", "<Control>equal"])

        zoom_out_action = Gio.SimpleAction.new("zoom-out", None)
        zoom_out_action.connect("activate", lambda a, p: win._zoom_step(-0.1))
        self.add_action(zoom_out_action)
        self.set_accels_for_action("app.zoom-out", ["<Control>minus"])

        zoom_reset_action = Gio.SimpleAction.new("zoom-reset", None)
        zoom_reset_action.connect("activate", lambda a, p: win._zoom_reset())
        self.add_action(zoom_reset_action)
        self.set_accels_for_action("app.zoom-reset", ["<Control>0"])

        # ? for help
        help_action = Gio.SimpleAction.new("help", None)
        help_action.connect("activate", lambda a, p: win._show_help_dialog())
        self.add_action(help_action)
        self.set_accels_for_action("app.help", ["question", "F1"])


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = MasterpieceApp()
    app.run(None)
