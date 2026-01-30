#!/usr/bin/env python3
"""

             VICTORY LIST MASTERPIECE - GTK4 + LIBADWAITA NATIVE (ENGLISH)                   
                                                                               
   A modern, native GNOME application for the Sejrliste system                 
   Built with GTK4 and Libadwaita for a truly contemporary look                
                                                                               
   Features:                                                                   
   • AdwNavigationSplitView - Modern sidebar navigation                        
   • AdwStatusPage - Beautiful empty/welcome states                            
   • AdwActionRow - Polished list items with progress                          
   • 7 DNA Layers - Visual status indicators                                   
   • Real-time updates - Auto-refresh from filesystem                          
                                                                               
   Author: Kv1nt (Claude Opus 4.5) for Rasmus                                  
   Date: 2026-01-25                                                            

"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Pango, Gdk, GObject
import cairo  # For konfetti drawing
from pathlib import Path
import re
import json
from datetime import datetime
import subprocess
import shutil
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# INTRO Folder System integration (FASE 0 data model)
import intro_integration

# 
# CIRKELLINE KV1NT ADMIRAL DESIGN SYSTEM - VF STANDARD
# 

# VF Logo ASCII Art (for terminal/text display)
VF_LOGO_ASCII = """
   
   
   
 
  
    
  ADMIRAL
"""

MODERN_CSS = """
/* =============================================================================
   SEJRLISTE MESTERVÆRK - CIRKELLINE KV1NT ADMIRAL STANDARD

         VF = VICTORY FLEET
         Admiral Rasmus's Command Center
      
         Cirkelline Chakra-Aligned Color System:
             Divine → Wisdom → Heart → Intuition → Sacred
       

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

/* === DRAG REORDER INDICATORS === */
row.drop-above {
    border-top: 3px solid @primary_500;
    background: rgba(99, 102, 241, 0.12);
}

.drop-zone-active {
    background: rgba(16, 185, 129, 0.1);
    border: 2px dashed #10b981;
}

/* === DRAG VALID/INVALID INDICATORS === */
row.drop-valid {
    border-top: 3px solid #10b981;
    background: rgba(16, 185, 129, 0.12);
}

row.drop-invalid {
    border-top: 3px solid #ef4444;
    background: rgba(239, 68, 68, 0.08);
}

/* === DRAG SUCCESS FLASH === */
@keyframes success-flash {
    0% { background: rgba(16, 185, 129, 0.3); }
    100% { background: transparent; }
}

row.success-flash {
    animation: success-flash 0.6s ease-out;
}

/* === MULTI-SELECT INDICATOR === */
row.selected-multi {
    background: rgba(99, 102, 241, 0.15);
    border-left: 3px solid @primary_500;
}

/* === DRAGGING ROW STYLE === */
row.dragging {
    opacity: 0.4;
    background: rgba(99, 102, 241, 0.05);
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

/* 
   VF LOGO - KV1NT ADMIRAL STANDARD
    */

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

/* 
   VINDERTAVLE - VICTORY JOURNEY BOARD
    */

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

/* 
   5W KONTROL PANEL - HVAD/HVOR/HVORFOR/HVORDAN/HVORNÅR
   Ordblind-venlig: Store ikoner, klar farvekodning, minimal tekst
    */

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

/* 
   ORDBLIND-VENLIG NAVIGATION
   Store ikoner, klar farvekodning, synlige keyboard hints
    */

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

/* 
   ACHIEVEMENT BADGES
    */

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

/* 
   FILTRE & SORTERING
    */

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

/* 
   LIVE AKTIVITETS MONITOR - WORLD CLASS REAL-TIME
    */

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

/* === INTRO SYSTEM SIDEBAR SECTION === */
.intro-section-header {
    font-weight: 800;
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(168, 85, 247, 0.85);
    padding: 12px 16px 4px 16px;
}

.intro-sidebar-btn {
    border-radius: 10px;
    padding: 8px 12px;
    background: rgba(168, 85, 247, 0.04);
    border: 1px solid rgba(168, 85, 247, 0.06);
    transition: all 200ms ease;
}

.intro-sidebar-btn:hover {
    background: rgba(168, 85, 247, 0.10);
    border-color: rgba(168, 85, 247, 0.18);
    box-shadow: 0 2px 12px -3px rgba(168, 85, 247, 0.20);
}

.intro-sidebar-icon {
    font-size: 14px;
    min-width: 22px;
    color: rgba(168, 85, 247, 0.80);
}

.intro-sidebar-label {
    font-weight: 600;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.85);
}

.intro-sidebar-count {
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 6px;
    background: rgba(168, 85, 247, 0.12);
    color: rgba(168, 85, 247, 0.90);
}

.intro-sidebar-date {
    font-size: 9px;
    color: rgba(255, 255, 255, 0.35);
}

/* INTRO category color accents */
.intro-cat-I .intro-sidebar-icon { color: #a855f7; }
.intro-cat-I .intro-sidebar-count { background: rgba(168, 85, 247, 0.12); color: #c084fc; }

.intro-cat-B .intro-sidebar-icon { color: #00D9FF; }
.intro-cat-B .intro-sidebar-count { background: rgba(0, 217, 255, 0.12); color: #22d3ee; }

.intro-cat-C .intro-sidebar-icon { color: #f59e0b; }
.intro-cat-C .intro-sidebar-count { background: rgba(245, 158, 11, 0.12); color: #fcd34d; }

.intro-cat-D .intro-sidebar-icon { color: #6366f1; }
.intro-cat-D .intro-sidebar-count { background: rgba(99, 102, 241, 0.12); color: #818cf8; }

.intro-cat-structure .intro-sidebar-icon { color: #10b981; }
.intro-cat-structure .intro-sidebar-count { background: rgba(16, 185, 129, 0.12); color: #34d399; }

.intro-cat-health .intro-sidebar-icon { color: #00FF88; }
.intro-cat-health .intro-sidebar-count { background: rgba(0, 255, 136, 0.12); color: #4ade80; }

/* === INTRO SYSTEM CONTENT VIEW === */
.intro-view-header {
    font-weight: 800;
    font-size: 22px;
    letter-spacing: -0.02em;
    color: rgba(255, 255, 255, 0.95);
}

.intro-view-subtitle {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.50);
}

.intro-category-card {
    background: linear-gradient(135deg,
        rgba(25, 25, 45, 0.8) 0%,
        rgba(30, 30, 55, 0.6) 100%);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 20px;
    transition: all 200ms ease;
}

.intro-category-card:hover {
    border-color: rgba(168, 85, 247, 0.20);
    box-shadow: 0 4px 20px -6px rgba(168, 85, 247, 0.15);
}

.intro-file-row {
    padding: 10px 16px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    transition: all 150ms ease;
}

.intro-file-row:hover {
    background: rgba(168, 85, 247, 0.06);
    border-color: rgba(168, 85, 247, 0.12);
}

.intro-file-number {
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-weight: 800;
    font-size: 14px;
    min-width: 32px;
}

.intro-file-title {
    font-weight: 600;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.90);
}

.intro-file-meta {
    font-size: 10px;
    color: rgba(255, 255, 255, 0.40);
    font-family: "JetBrains Mono", "Fira Code", monospace;
}

.intro-status-badge {
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 6px;
}

.intro-status-complete {
    background: rgba(0, 255, 136, 0.12);
    color: #4ade80;
}

.intro-status-active {
    background: rgba(0, 217, 255, 0.12);
    color: #22d3ee;
}

.intro-status-unknown {
    background: rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.40);
}

.intro-health-score {
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-weight: 800;
    font-size: 36px;
}

.intro-health-pass {
    color: #4ade80;
}

.intro-health-warn {
    color: #fbbf24;
}

.intro-health-fail {
    color: #f87171;
}

.intro-check-row {
    padding: 8px 12px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
}

.intro-check-pass {
    border-left: 3px solid #4ade80;
}

.intro-check-fail {
    border-left: 3px solid #f87171;
}

/* === INTRO STRUCTURE VIEW RULE CARDS (FASE 3) === */
.intro-rule-card {
    border-left: 3px solid rgba(251, 191, 36, 0.40);
    margin-top: 2px;
    margin-bottom: 2px;
}

.intro-rule-card:hover {
    border-left-color: rgba(251, 191, 36, 0.70);
    box-shadow: 0 4px 20px -6px rgba(251, 191, 36, 0.15);
}

.intro-open-btn {
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 8px;
    background: rgba(168, 85, 247, 0.10);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.15);
}

.intro-open-btn:hover {
    background: rgba(168, 85, 247, 0.20);
    border-color: rgba(168, 85, 247, 0.30);
}

/* === INTRO I-FILE CATEGORY COLOR ROWS (FASE 2) === */
.intro-i-row-vision {
    border-left: 3px solid #a855f7;
}
.intro-i-row-vision:hover {
    background: rgba(168, 85, 247, 0.08);
    border-color: rgba(168, 85, 247, 0.15);
    border-left: 3px solid #a855f7;
}

.intro-i-row-orders {
    border-left: 3px solid #ef4444;
}
.intro-i-row-orders:hover {
    background: rgba(239, 68, 68, 0.08);
    border-color: rgba(239, 68, 68, 0.15);
    border-left: 3px solid #ef4444;
}

.intro-i-row-hybrids {
    border-left: 3px solid #10b981;
}
.intro-i-row-hybrids:hover {
    background: rgba(16, 185, 129, 0.08);
    border-color: rgba(16, 185, 129, 0.15);
    border-left: 3px solid #10b981;
}

.intro-i-row-operations {
    border-left: 3px solid #f59e0b;
}
.intro-i-row-operations:hover {
    background: rgba(245, 158, 11, 0.08);
    border-color: rgba(245, 158, 11, 0.15);
    border-left: 3px solid #f59e0b;
}

.intro-i-row-technical {
    border-left: 3px solid #6366f1;
}
.intro-i-row-technical:hover {
    background: rgba(99, 102, 241, 0.08);
    border-color: rgba(99, 102, 241, 0.15);
    border-left: 3px solid #6366f1;
}

.intro-i-row-ecosystem {
    border-left: 3px solid #00FF88;
}
.intro-i-row-ecosystem:hover {
    background: rgba(0, 255, 136, 0.08);
    border-color: rgba(0, 255, 136, 0.15);
    border-left: 3px solid #00FF88;
}

.intro-i-row-prevention {
    border-left: 3px solid #f97316;
}
.intro-i-row-prevention:hover {
    background: rgba(249, 115, 22, 0.08);
    border-color: rgba(249, 115, 22, 0.15);
    border-left: 3px solid #f97316;
}

.intro-i-row-sejrliste {
    border-left: 3px solid #ff9f43;
}
.intro-i-row-sejrliste:hover {
    background: rgba(255, 159, 67, 0.08);
    border-color: rgba(255, 159, 67, 0.15);
    border-left: 3px solid #ff9f43;
}

.intro-i-status-ok {
    background: rgba(0, 255, 136, 0.12);
    color: #4ade80;
}

.intro-i-status-pending {
    background: rgba(245, 158, 11, 0.12);
    color: #fcd34d;
}

.intro-i-open-files-btn {
    font-size: 10px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-left: 4px;
}

.intro-i-open-files-btn:hover {
    background: rgba(255, 255, 255, 0.10);
    color: rgba(255, 255, 255, 0.80);
    border-color: rgba(255, 255, 255, 0.18);
}

/* === INTRO SYSTEM FUNCTIONS VIEW (FASE 4) === */
.intro-sysfunc-card {
    padding: 12px 16px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-left: 3px solid rgba(0, 217, 255, 0.40);
}

.intro-sysfunc-card:hover {
    border-left-color: rgba(0, 217, 255, 0.70);
    box-shadow: 0 4px 20px -6px rgba(0, 217, 255, 0.15);
}

.intro-sysfunc-title {
    font-weight: 700;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.90);
}

.intro-sysfunc-desc {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.55);
}

.intro-sysfunc-status-active {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
    background: rgba(0, 255, 136, 0.12);
    color: #4ade80;
}

.intro-sysfunc-status-inactive {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
    background: rgba(248, 113, 113, 0.12);
    color: #f87171;
}

.intro-sysfunc-detail {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.45);
}

.intro-sysfunc-run-btn {
    font-size: 11px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 8px;
    background: rgba(0, 217, 255, 0.12);
    color: #67e8f9;
    border: 1px solid rgba(0, 217, 255, 0.20);
}

.intro-sysfunc-run-btn:hover {
    background: rgba(0, 217, 255, 0.22);
    border-color: rgba(0, 217, 255, 0.35);
}

.intro-sysfunc-runall-btn {
    font-weight: 700;
    padding: 8px 24px;
    border-radius: 10px;
    background: rgba(0, 217, 255, 0.15);
    color: #67e8f9;
    border: 1px solid rgba(0, 217, 255, 0.25);
}

.intro-sysfunc-runall-btn:hover {
    background: rgba(0, 217, 255, 0.28);
    border-color: rgba(0, 217, 255, 0.45);
}

.intro-sysfunc-log-panel {
    font-family: monospace;
    font-size: 11px;
    padding: 12px;
    border-radius: 8px;
    background: rgba(0, 0, 0, 0.30);
    border: 1px solid rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.70);
}

.intro-sysfunc-level-card {
    padding: 6px 10px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
}

.intro-sysfunc-phase-card {
    padding: 6px 10px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
}

/* === INTRO DNA LAYER CARDS (FASE 5) === */

.intro-dna-card {
    padding: 16px 20px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-left: 4px solid rgba(99, 102, 241, 0.40);
    transition: all 200ms ease;
}

.intro-dna-card:hover {
    background: rgba(255, 255, 255, 0.045);
    border-left-color: rgba(99, 102, 241, 0.70);
    box-shadow: 0 4px 20px -6px rgba(99, 102, 241, 0.15);
}

.intro-dna-card-active {
    border-left-color: rgba(74, 222, 128, 0.60);
}

.intro-dna-card-active:hover {
    border-left-color: rgba(74, 222, 128, 0.85);
    box-shadow: 0 4px 20px -6px rgba(74, 222, 128, 0.15);
}

.intro-dna-card-missing {
    border-left-color: rgba(248, 113, 113, 0.40);
}

.intro-dna-card-missing:hover {
    border-left-color: rgba(248, 113, 113, 0.70);
    box-shadow: 0 4px 20px -6px rgba(248, 113, 113, 0.12);
}

.intro-dna-layer-num {
    font-size: 20px;
    font-weight: 800;
    min-width: 36px;
    min-height: 36px;
    border-radius: 50%;
    background: rgba(99, 102, 241, 0.15);
    color: #a5b4fc;
}

.intro-dna-layer-num-active {
    background: rgba(74, 222, 128, 0.15);
    color: #4ade80;
    box-shadow: 0 0 12px rgba(74, 222, 128, 0.25);
}

.intro-dna-layer-name {
    font-weight: 700;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.90);
}

.intro-dna-layer-detail {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.50);
    font-family: monospace;
}

.intro-dna-layer-status {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
}

.intro-dna-status-found {
    background: rgba(0, 255, 136, 0.12);
    color: #4ade80;
}

.intro-dna-status-missing {
    background: rgba(248, 113, 113, 0.12);
    color: #f87171;
}

.intro-dna-status-partial {
    background: rgba(250, 204, 21, 0.12);
    color: #fbbf24;
}

.intro-dna-progress {
    min-height: 6px;
    border-radius: 3px;
}

.intro-dna-progress trough {
    background: rgba(255, 255, 255, 0.08);
    min-height: 6px;
    border-radius: 3px;
}

.intro-dna-progress progress {
    background: linear-gradient(90deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8));
    border-radius: 3px;
}

.intro-dna-progress-active progress {
    background: linear-gradient(90deg, rgba(74, 222, 128, 0.8), rgba(34, 197, 94, 0.8));
}

.intro-dna-overall-score {
    font-size: 42px;
    font-weight: 900;
    color: #a5b4fc;
}

.intro-dna-overall-pass {
    color: #4ade80;
}

.intro-dna-overall-warn {
    color: #fbbf24;
}

.intro-dna-overall-low {
    color: #f87171;
}

/* FASE 6: Quick Actions Panel */
.intro-qa-section-header {
    font-size: 18px;
    font-weight: 800;
    color: #e2e8f0;
}

.intro-qa-system-label {
    font-size: 14px;
    font-weight: 700;
    font-family: "JetBrains Mono", monospace;
}

.intro-qa-cmd-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 4px;
}

.intro-qa-cmd-card:hover {
    background: rgba(30, 41, 59, 0.7);
    border-color: rgba(255, 255, 255, 0.12);
}

.intro-qa-cmd-text {
    font-size: 12px;
    font-family: "JetBrains Mono", monospace;
    color: #22d3ee;
}

.intro-qa-cmd-desc {
    font-size: 11px;
    color: #94a3b8;
}

.intro-qa-copy-btn {
    min-height: 28px;
    min-width: 28px;
    padding: 2px 8px;
    font-size: 11px;
}

.intro-qa-run-btn {
    min-height: 28px;
    min-width: 28px;
    padding: 2px 8px;
    font-size: 11px;
    background: rgba(74, 222, 128, 0.15);
    color: #4ade80;
}

.intro-qa-env-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 12px 16px;
}

.intro-qa-env-card:hover {
    background: rgba(30, 41, 59, 0.7);
    border-color: rgba(255, 255, 255, 0.12);
}

.intro-qa-env-name {
    font-size: 14px;
    font-weight: 700;
    color: #e2e8f0;
}

.intro-qa-env-detail {
    font-size: 12px;
    color: #94a3b8;
    font-family: "JetBrains Mono", monospace;
}

.intro-qa-status-running {
    color: #4ade80;
    font-weight: 700;
    font-size: 12px;
}

.intro-qa-status-stopped {
    color: #f87171;
    font-weight: 700;
    font-size: 12px;
}

.intro-qa-status-unknown {
    color: #fbbf24;
    font-weight: 700;
    font-size: 12px;
}

.intro-qa-status-configured {
    color: #a78bfa;
    font-weight: 700;
    font-size: 12px;
}

.intro-qa-check-btn {
    min-height: 28px;
    padding: 2px 10px;
    font-size: 11px;
}

.intro-qa-system-cirkelline { color: #f97316; }
.intro-qa-system-cosmic { color: #a855f7; }
.intro-qa-system-ckc { color: #22d3ee; }
.intro-qa-system-kommandor { color: #6366f1; }
.intro-qa-system-docker { color: #3b82f6; }
.intro-qa-system-db { color: #f59e0b; }
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

# 
# INTELLIGENT SEARCH ENGINE
# 

# 
# UNIVERSAL SEJR CONVERTER - FRA ALT TIL SEJR STRUKTUR
# 

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
        "folder": " Folder",
        "file": " Fil",
        "pdf": " PDF",
        "text": " Tekst",
        "command": " Kommando",
    }

    CONTROL_MODES = {
        "manual": " Manuel - Du styrer ALT",
        "kv1nt": " Kv1nt - AI-assisteret med forslag",
        "admiral": " Admiral - Fuld automatisk",
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
**Status:**  PASS 1 - IN PROGRESS
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

##  3-PASS KONKURRENCE SYSTEM (OBLIGATORISK)

```
PASS 1: FUNGERENDE     → "Get it working"      → REVIEW REQUIRED
PASS 2: FORBEDRET      → "Make it better"      → REVIEW REQUIRED
PASS 3: OPTIMERET      → "Make it best"        → FINAL VERIFICATION
                                                        ↓
                                                KAN ARKIVERES
```

---

#  PASS 1: FUNGERENDE ("Get It Working")

## Tasks

"""
        # Add tasks
        for task in config.get('tasks', []):
            if not task.startswith("- [ ]"):
                task = f"- [ ] {task}"
            victory_content += f"{task}\n"

        victory_content += """
---

## Verification

- [ ] Alle tasks completeret
- [ ] Output verificeret
- [ ] Ready for Pass 2

---

#  PASS 2: FORBEDRET ("Make It Better")

*Udfyldes efter Pass 1 er færdig*

---

#  PASS 3: OPTIMERET ("Make It Best")

*Udfyldes efter Pass 2 er færdig*
"""

        # Write SEJR_LISTE.md
        (sejr_path / "SEJR_LISTE.md").write_text(victory_content)

        # Create CLAUDE.md focus lock
        claude_content = f"""# CLAUDE FOKUS LOCK - LÆS DETTE FØRST

> **DU ER I EN SEJR LISTE MAPPE. DU HAR ÉN OPGAVE. FOKUSÉR.**

---

##  CURRENT STATE

**Sejr:** {config['name']}
**Current Pass:** 1/3
**Status:** Pass 1 - Fungerende
**Input:** {config.get('input_type', 'unknown')}

---

##  DIN ENESTE OPGAVE RIGHT NOW

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

# 
# CONFIGURATION
# 

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

# LINEN Framework — 5 pillars of INTRO folder organization
INTRO_PATH = Path.home() / "Desktop" / "MASTER FOLDERS(INTRO)"

LINEN_COMPONENTS = [
    ("L", "LOGGING", "ÆNDRINGSLOG i alle filer", "document-edit-symbolic"),
    ("I", "INDEKSERING", "Numerisk hierarki 00-99", "view-list-ordered-symbolic"),
    ("N", "NESTING", "_TODO_VERIFIKATION i mapper", "folder-symbolic"),
    ("E", "EFTERPRØVNING", "STATUS.md metrics", "emblem-ok-symbolic"),
    ("N2", "NAVIGATION", "INDEX filer i sektioner", "compass-symbolic"),
]

# LINEN color scheme (chakra-inspired, used in Pass 3 polish)
LINEN_COLORS = {
    "L": "#00D9FF",   # Cyan — Logging
    "I": "#f59e0b",   # Gold — Indeksering
    "N": "#6366f1",   # Indigo — Nesting
    "E": "#00FF88",   # Green — Efterprøvning
    "N2": "#10b981",  # Emerald — Navigation
}


@dataclass
class LinenScore:
    """Score for a single LINEN component"""
    component: str       # L, I, N, E, N2
    name: str            # Full name (LOGGING, INDEKSERING, etc.)
    total_items: int     # Total files/folders checked
    passing_items: int   # Items that pass validation
    percentage: float    # 0.0 - 100.0
    details: list = field(default_factory=list)  # List of (path, passed: bool) tuples
    last_checked: str = ""


# 3-Lags Arkitektur — INTRO system architecture model
ARCHITECTURE_LAYERS = [
    ("1", "PRESENTATIONS LAG", "Markdown filer — human readable, git versionable", "text-x-generic-symbolic"),
    ("2", "STRUKTURELT LAG", "Numerisk hierarki, mappestruktur, navngivning", "view-grid-symbolic"),
    ("3", "VERIFIKATIONS LAG", "LINEN system, STATUS.md, validation scripts", "emblem-ok-symbolic"),
]

ARCHITECTURE_PRINCIPLES = [
    ("Flat File Structure", "Markdown i mapper, ingen database"),
    ("Self-Contained", "Hver sektion er standalone"),
    ("Hierarchical", "Numerisk 00-99 sortering"),
    ("Versioned", "Semantic versioning i filer"),
    ("Validated", "LINEN + validation scripts"),
    ("Redundant", "Vigtig info flere steder"),
]

DESIGN_PATTERNS = [
    ("Sektion Container", "XX_SEKTION/ med hovedfil + undermapper + _TODO_VERIFIKATION/",
     "Self-contained, Konsistent, Verificerbar"),
    ("Document Sandwich", "Header (metadata) → Content (##) → Footer (ÆNDRINGSLOG)",
     "Metadata same sted, flexible content, historik i bunden"),
    ("Meta-Data Nesting", "_TODO_VERIFIKATION/STATUS.md i alle content mapper",
     "Separation of concerns, underscore prefix, consistent naming"),
]

NUMERISK_HIERARKI = [
    ("00-05", "Root dokumenter", "#9ca3af"),
    ("06-09", "Templates/system", "#60a5fa"),
    ("10-19", "Arkitektur og infrastruktur", "#6366f1"),
    ("20-29", "Projekter", "#10b981"),
    ("30-39", "TODOs og opgaver", "#f59e0b"),
    ("40-49", "Baselines", "#14b8a6"),
    ("50-59", "Roadmaps og planer", "#a855f7"),
    ("60-69", "CLAUDE.md og instruktioner", "#00D9FF"),
    ("70-79", "Guides og tutorials", "#eab308"),
    ("80-89", "Kritisk dokumentation", "#ef4444"),
    ("90-99", "Analyser og rapporter", "#ec4899"),
]

LAYER_COLORS = {
    "1": "#a855f7",  # Violet — Presentation
    "2": "#f59e0b",  # Gold — Structure
    "3": "#00FF88",  # Green — Verification
}

# --- 3-LAGS PASS 2: Design Decisions ---
DESIGN_DECISIONS = [
    ("Markdown Over Database",
     "Valgt: Markdown filer i mapper",
     ["Human-readable uden specialvaerktoj", "Git versionable linje-for-linje",
      "Kopi/pasta til enhver platform", "Ingen server eller runtime kraevet"],
     ["Ingen SQL queries eller relationer", "Manuel cross-referencing",
      "Ingen real-time collaboration"]),
    ("Flat Files Over Nested DB",
     "Valgt: Flad mappestruktur med numerisk prefix",
     ["Synlig i enhver filbrowser", "Naturlig sortering med 00-99",
      "Ingen broken foreign keys", "cp/mv/rsync fungerer direkte"],
     ["Begroenset til 100 top-level", "Ingen automatisk referentiel integritet",
      "Manuel navigation i store systemer"]),
    ("Numerisk Hierarki",
     "Valgt: 00-99 prefix system",
     ["Garanteret sorteringsorden", "Visuelt klart hierarki",
      "Reserverede ranges for kategorier", "Nemt at inserere nye filer"],
     ["Alle ranges skal planlaegges forud", "Omnavngivning = mange filaendringer",
      "Maksimalt 100 per niveau"]),
    ("LINEN Overhead",
     "Valgt: Obligatorisk LINEN verification",
     ["Konsistent kvalitet over tid", "Automatiserbar validering",
      "Self-documenting system", "Fejl opdages proaktivt"],
     ["Ekstra overhead per fil/mappe", "Laeringsbarriere for nye bidragydere",
      "Kraever disciplin at vedligeholde"]),
]

SCALING_MILESTONES = [
    ("Nu", "~400 filer, ~50 mapper", 400),
    ("Aar 1", "400 -> 600 filer", 600),
    ("Aar 2", "600 -> 1000 filer", 1000),
    ("Aar 3", "1000 -> 2000 filer", 2000),
]

SCALING_STRATEGIES = [
    "Split store sektioner i undersektioner (XX -> XXA/XXB/XXC)",
    "Arkiver afsluttede projekter til 90_ARCHIVE",
    "Brug INDEX filer som navigation hubs",
    "Auto-genereret search index for hurtig opslag",
]

FOLDER_ANATOMY = [
    ("XX_SEKTION.md", "Hovedfil", "Primaer content for sektionen", "#a855f7"),
    ("XX_INDEX.md", "Navigation", "Links til alle filer i sektionen", "#60a5fa"),
    ("XXA_UNDERSEKTION/", "Undermapper", "Dybere indhold organiseret", "#10b981"),
    ("_TODO_VERIFIKATION/STATUS.md", "Meta-data", "LINEN verifikationsdata", "#f59e0b"),
    ("_SKRALDESPAND/", "Arkiv", "Soft-delete for gammel content", "#9ca3af"),
]

SYSTEM_FOLDERS = [
    ("_TODO_VERIFIKATION/", "Verifikationsdata per mappe"),
    ("_SKRALDESPAND/", "Soft-delete arkiv"),
    ("_MANUAL/", "Instruktioner og guides"),
    ("_ARCHIVE/", "Historiske versioner"),
]

# --- LINEN PASS 2: Validation Layers ---
VALIDATION_LAYERS = [
    ("1", "Syntax Validation", "Markdown valid, ingen parse errors", "#60a5fa"),
    ("2", "Structure Validation", "VERSION + AENDRINGSLOG i alle filer", "#6366f1"),
    ("3", "Content Validation", "STATUS.md konsistent med virkelighed", "#10b981"),
    ("4", "Cross-Reference Validation", "Alle links virker, ingen orphans", "#f59e0b"),
]

VALIDATION_SCHEDULE = [
    ("Dagligt", "validate_single.sh", "Filer under aktiv redigering"),
    ("Ugentligt", "validate_all.sh", "Hele INTRO systemet"),
    ("Maanedligt", "Fuld manuel audit", "Komplet gennemgang af alt"),
]


@dataclass
class ArchitectureStats:
    """Stats for a single architecture layer"""
    layer: int
    name: str
    total_items: int
    description: str


# Sync Functions — DEL 21 sync components
SYNC_COMPONENTS = [
    ("SYNC-1", "Git Pull/Push", "Automatisk sync med GitHub", "network-transmit-symbolic", "P1"),
    ("SYNC-2", "Ændringslog Tracking", "Log alle ændringer med dato/tid", "document-edit-symbolic", "P1"),
    ("SYNC-3", "VERSION.md", "Versionering i alle mapper", "emblem-default-symbolic", "P2"),
    ("SYNC-4", "Cross-Reference", "Opdater alle krydsreferencer", "emblem-shared-symbolic", "P2"),
    ("SYNC-5", "STATUS.md Auto", "Automatisk statusopdatering", "view-refresh-symbolic", "P2"),
    ("SYNC-6", "Notifikation", "Advarsler ved remote ændringer", "dialog-warning-symbolic", "P3"),
]

SYNC_PRIORITY_COLORS = {
    "P1": "#ef4444",  # Red — critical
    "P2": "#f59e0b",  # Orange — important
    "P3": "#9ca3af",  # Grey — nice to have
}

# Component-specific colors for sync cards (Pass 3 visual polish)
SYNC_COMPONENT_COLORS = {
    "SYNC-1": "#00D9FF",  # Git: Cyan
    "SYNC-2": "#f59e0b",  # Log: Wisdom gold
    "SYNC-3": "#6366f1",  # Version: Intuition indigo
    "SYNC-4": "#10b981",  # Links: Heart emerald
    "SYNC-5": "#00FF88",  # Status: Success green
    "SYNC-6": "#f97316",  # Notify: Warning orange
}


@dataclass
class SyncStatus:
    """Status for a single sync component"""
    component_id: str   # SYNC-1 through SYNC-6
    name: str
    priority: str       # P1, P2, P3
    status: str         # "ok", "warning", "error", "unknown"
    detail: str         # Human-readable detail string
    count_ok: int = 0
    count_total: int = 0


# 
# HELPERS
# 

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


# 
# LINEN SCANNING FUNCTIONS
# 

def _scan_logging(intro_path: Path) -> LinenScore:
    """L — Check which .md files contain ÆNDRINGSLOG section"""
    details = []
    if not intro_path.exists():
        return LinenScore("L", "LOGGING", 0, 0, 0.0, details,
                          datetime.now().strftime("%H:%M:%S"))

    md_files = list(intro_path.rglob("*.md"))
    for f in md_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            has_log = "ÆNDRINGSLOG" in content or "ÆNDRINGS LOG" in content
            details.append((str(f.relative_to(intro_path)), has_log))
        except (PermissionError, OSError):
            details.append((str(f.relative_to(intro_path)), False))

    passing = sum(1 for _, ok in details if ok)
    total = len(details)
    pct = (passing / total * 100) if total > 0 else 0.0
    return LinenScore("L", "LOGGING", total, passing, pct, details,
                      datetime.now().strftime("%H:%M:%S"))


def _scan_indeksering(intro_path: Path) -> LinenScore:
    """I — Check which files/folders use numeric prefix (00-99)"""
    details = []
    if not intro_path.exists():
        return LinenScore("I", "INDEKSERING", 0, 0, 0.0, details,
                          datetime.now().strftime("%H:%M:%S"))

    # Check top-level items (folders and files directly in INTRO)
    items = [p for p in intro_path.iterdir() if not p.name.startswith(".")]
    for item in items:
        has_prefix = bool(re.match(r'^\d{2}_', item.name))
        details.append((item.name, has_prefix))

    passing = sum(1 for _, ok in details if ok)
    total = len(details)
    pct = (passing / total * 100) if total > 0 else 0.0
    return LinenScore("I", "INDEKSERING", total, passing, pct, details,
                      datetime.now().strftime("%H:%M:%S"))


def _scan_nesting(intro_path: Path) -> LinenScore:
    """N — Check which directories have _TODO_VERIFIKATION subfolder"""
    details = []
    if not intro_path.exists():
        return LinenScore("N", "NESTING", 0, 0, 0.0, details,
                          datetime.now().strftime("%H:%M:%S"))

    # Check all directories (top-level and one level deep)
    dirs = [d for d in intro_path.iterdir()
            if d.is_dir() and not d.name.startswith(".")]
    for d in dirs:
        has_todo = (d / "_TODO_VERIFIKATION").is_dir()
        details.append((d.name, has_todo))

    passing = sum(1 for _, ok in details if ok)
    total = len(details)
    pct = (passing / total * 100) if total > 0 else 0.0
    return LinenScore("N", "NESTING", total, passing, pct, details,
                      datetime.now().strftime("%H:%M:%S"))


def _scan_efterproevning(intro_path: Path) -> LinenScore:
    """E — Check which directories have STATUS.md files"""
    details = []
    if not intro_path.exists():
        return LinenScore("E", "EFTERPRØVNING", 0, 0, 0.0, details,
                          datetime.now().strftime("%H:%M:%S"))

    dirs = [d for d in intro_path.iterdir()
            if d.is_dir() and not d.name.startswith(".")]
    for d in dirs:
        status_files = list(d.glob("*STATUS*")) + list(d.glob("*status*"))
        has_status = len(status_files) > 0
        details.append((d.name, has_status))

    passing = sum(1 for _, ok in details if ok)
    total = len(details)
    pct = (passing / total * 100) if total > 0 else 0.0
    return LinenScore("E", "EFTERPRØVNING", total, passing, pct, details,
                      datetime.now().strftime("%H:%M:%S"))


def _scan_navigation(intro_path: Path) -> LinenScore:
    """N2 — Check which sections have INDEX files"""
    details = []
    if not intro_path.exists():
        return LinenScore("N2", "NAVIGATION", 0, 0, 0.0, details,
                          datetime.now().strftime("%H:%M:%S"))

    dirs = [d for d in intro_path.iterdir()
            if d.is_dir() and not d.name.startswith(".")]
    for d in dirs:
        index_files = list(d.glob("*INDEX*")) + list(d.glob("*index*"))
        has_index = len(index_files) > 0
        details.append((d.name, has_index))

    passing = sum(1 for _, ok in details if ok)
    total = len(details)
    pct = (passing / total * 100) if total > 0 else 0.0
    return LinenScore("N2", "NAVIGATION", total, passing, pct, details,
                      datetime.now().strftime("%H:%M:%S"))


def get_linen_status(intro_path: Path = None) -> List[LinenScore]:
    """Scan INTRO folder and return scores for all 5 LINEN components"""
    if intro_path is None:
        intro_path = INTRO_PATH

    return [
        _scan_logging(intro_path),
        _scan_indeksering(intro_path),
        _scan_nesting(intro_path),
        _scan_efterproevning(intro_path),
        _scan_navigation(intro_path),
    ]


def get_linen_health(intro_path: Path = None) -> float:
    """Return overall LINEN health as 0-100% (average of 5 components)"""
    scores = get_linen_status(intro_path)
    if not scores:
        return 0.0
    return sum(s.percentage for s in scores) / len(scores)


# 
# 3-LAGS ARKITEKTUR SCANNING
# 

def get_layer_stats(intro_path: Path = None) -> List[ArchitectureStats]:
    """Get statistics for each of the 3 architecture layers"""
    if intro_path is None:
        intro_path = INTRO_PATH

    stats = []

    if not intro_path.exists():
        for i, (num, name, desc, _icon) in enumerate(ARCHITECTURE_LAYERS, 1):
            stats.append(ArchitectureStats(i, name, 0, desc))
        return stats

    # Layer 1: Presentation — count .md files
    md_count = len(list(intro_path.rglob("*.md")))
    stats.append(ArchitectureStats(1, "PRESENTATIONS LAG", md_count,
                                   f"{md_count} Markdown filer"))

    # Layer 2: Structure — count items with numeric prefix
    all_items = [p for p in intro_path.iterdir() if not p.name.startswith(".")]
    numeric_items = [p for p in all_items if re.match(r'^\d{2}_', p.name)]
    stats.append(ArchitectureStats(2, "STRUKTURELT LAG", len(numeric_items),
                                   f"{len(numeric_items)}/{len(all_items)} numerisk"))

    # Layer 3: Verification — count _TODO_VERIFIKATION + STATUS.md
    dirs = [d for d in intro_path.iterdir() if d.is_dir() and not d.name.startswith(".")]
    todo_dirs = sum(1 for d in dirs if (d / "_TODO_VERIFIKATION").is_dir())
    status_files = sum(1 for d in dirs if list(d.glob("*STATUS*")))
    stats.append(ArchitectureStats(3, "VERIFIKATIONS LAG", todo_dirs + status_files,
                                   f"{todo_dirs} _TODO + {status_files} STATUS"))

    return stats


def get_numerisk_distribution(intro_path: Path = None) -> Dict[str, int]:
    """Count files per numeric range (00-09, 10-19, etc.)"""
    if intro_path is None:
        intro_path = INTRO_PATH

    distribution = {}
    for range_str, label, _color in NUMERISK_HIERARKI:
        distribution[range_str] = 0

    if not intro_path.exists():
        return distribution

    for item in intro_path.iterdir():
        if item.name.startswith("."):
            continue
        match = re.match(r'^(\d{2})', item.name)
        if match:
            num = int(match.group(1))
            for range_str, _label, _color in NUMERISK_HIERARKI:
                low, high = range_str.split("-")
                if int(low) <= num <= int(high):
                    distribution[range_str] += 1
                    break

    return distribution


# 
# SYNC SCANNING FUNCTIONS (DEL 21)
# 

def _sync_git_status(intro_path: Path) -> SyncStatus:
    """SYNC-1: Check git ahead/behind status"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "-b"],
            cwd=str(intro_path), capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            return SyncStatus("SYNC-1", "Git Pull/Push", "P1", "error",
                              "Git not available", 0, 1)

        # Check ahead/behind from branch line
        ahead = 0
        behind = 0
        for line in output.split("\n"):
            if line.startswith("##"):
                import re as _re
                m_ahead = _re.search(r'ahead (\d+)', line)
                m_behind = _re.search(r'behind (\d+)', line)
                if m_ahead:
                    ahead = int(m_ahead.group(1))
                if m_behind:
                    behind = int(m_behind.group(1))
                break

        # Count dirty files
        dirty = len([l for l in output.split("\n") if l and not l.startswith("##")])

        if behind > 0:
            return SyncStatus("SYNC-1", "Git Pull/Push", "P1", "warning",
                              f"{behind} behind, {ahead} ahead, {dirty} dirty", 0, 1)
        elif dirty > 0:
            return SyncStatus("SYNC-1", "Git Pull/Push", "P1", "warning",
                              f"Synced but {dirty} uncommitted changes", 0, 1)
        elif ahead > 0:
            return SyncStatus("SYNC-1", "Git Pull/Push", "P1", "warning",
                              f"{ahead} unpushed commits", 0, 1)
        else:
            return SyncStatus("SYNC-1", "Git Pull/Push", "P1", "ok",
                              "Fully synced", 1, 1)
    except Exception as e:
        return SyncStatus("SYNC-1", "Git Pull/Push", "P1", "error",
                          f"Git error: {str(e)[:60]}", 0, 1)


def _sync_aendringslog(intro_path: Path) -> SyncStatus:
    """SYNC-2: Count files with ÆNDRINGSLOG section"""
    md_files = list(intro_path.rglob("*.md"))
    has_log = 0
    for f in md_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "ÆNDRINGSLOG" in content or "CHANGELOG" in content:
                has_log += 1
        except Exception:
            pass
    total = len(md_files) if md_files else 1
    pct = (has_log / total * 100) if total > 0 else 0
    status = "ok" if pct >= 80 else ("warning" if pct >= 50 else "error")
    return SyncStatus("SYNC-2", "Ændringslog Tracking", "P1", status,
                      f"{has_log}/{total} filer ({pct:.0f}%)", has_log, total)


def _sync_version_md(intro_path: Path) -> SyncStatus:
    """SYNC-3: Count directories with VERSION.md"""
    dirs = [d for d in intro_path.iterdir()
            if d.is_dir() and not d.name.startswith(".") and not d.name.startswith("_")]
    has_version = 0
    for d in dirs:
        if list(d.glob("*VERSION*")) or list(d.glob("*version*")):
            has_version += 1
    total = len(dirs) if dirs else 1
    pct = (has_version / total * 100) if total > 0 else 0
    status = "ok" if pct >= 60 else ("warning" if pct >= 30 else "error")
    return SyncStatus("SYNC-3", "VERSION.md", "P2", status,
                      f"{has_version}/{total} mapper ({pct:.0f}%)", has_version, total)


def _sync_cross_references(intro_path: Path) -> SyncStatus:
    """SYNC-4: Check for broken markdown links"""
    md_files = list(intro_path.rglob("*.md"))
    total_links = 0
    broken_links = 0
    for f in md_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # Find [text](path) links — only local, not http
            links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
            for _text, href in links:
                if href.startswith("http") or href.startswith("#") or href.startswith("mailto"):
                    continue
                total_links += 1
                # Resolve relative path
                target = f.parent / href
                if not target.exists():
                    broken_links += 1
        except Exception:
            pass

    ok_links = total_links - broken_links
    if total_links == 0:
        return SyncStatus("SYNC-4", "Cross-Reference", "P2", "ok",
                          "Ingen lokale links fundet", 0, 0)
    status = "ok" if broken_links == 0 else ("warning" if broken_links <= 3 else "error")
    return SyncStatus("SYNC-4", "Cross-Reference", "P2", status,
                      f"{ok_links} OK / {broken_links} broken", ok_links, total_links)


def _get_broken_links_detail(intro_path: Path):
    """Return list of (source_file, link_text, target_path) for broken links"""
    broken = []
    md_files = list(intro_path.rglob("*.md"))
    for f in md_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
            for text, href in links:
                if href.startswith("http") or href.startswith("#") or href.startswith("mailto"):
                    continue
                target = f.parent / href
                if not target.exists():
                    # Try to find a close match for auto-suggest
                    suggested = _suggest_link_fix(f.parent, href)
                    broken.append((str(f.relative_to(intro_path)), text, href, suggested))
        except Exception:
            pass
    return broken


def _suggest_link_fix(base_dir: Path, broken_href: str):
    """Try to find a close match for a broken link"""
    target_name = Path(broken_href).name
    # Search in base_dir and parent
    search_dirs = [base_dir, base_dir.parent]
    for d in search_dirs:
        if not d.exists():
            continue
        for entry in d.iterdir():
            if entry.name.lower() == target_name.lower():
                try:
                    return str(entry.relative_to(base_dir))
                except ValueError:
                    return str(entry)
    # Try fuzzy: same prefix
    prefix = target_name[:5].lower() if len(target_name) > 5 else target_name.lower()
    for d in search_dirs:
        if not d.exists():
            continue
        for entry in d.iterdir():
            if entry.name.lower().startswith(prefix):
                try:
                    return str(entry.relative_to(base_dir))
                except ValueError:
                    return str(entry)
    return None


def _sync_status_md(intro_path: Path) -> SyncStatus:
    """SYNC-5: Count STATUS.md files that are up-to-date"""
    dirs = [d for d in intro_path.iterdir()
            if d.is_dir() and not d.name.startswith(".") and not d.name.startswith("_")]
    has_status = 0
    for d in dirs:
        if list(d.glob("*STATUS*")):
            has_status += 1
    total = len(dirs) if dirs else 1
    pct = (has_status / total * 100) if total > 0 else 0
    status = "ok" if pct >= 60 else ("warning" if pct >= 30 else "error")
    return SyncStatus("SYNC-5", "STATUS.md Auto", "P2", status,
                      f"{has_status}/{total} mapper ({pct:.0f}%)", has_status, total)


def _sync_remote_check(intro_path: Path) -> SyncStatus:
    """SYNC-6: Check if remote has new commits (without fetching)"""
    try:
        # Use git log to compare local vs remote tracking branch
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD..@{upstream}"],
            cwd=str(intro_path), capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return SyncStatus("SYNC-6", "Notifikation", "P3", "unknown",
                              "Kan ikke tjekke remote (kør git fetch)", 0, 1)
        count = int(result.stdout.strip()) if result.stdout.strip() else 0
        if count > 0:
            return SyncStatus("SYNC-6", "Notifikation", "P3", "warning",
                              f"{count} nye commits på remote", 0, 1)
        else:
            return SyncStatus("SYNC-6", "Notifikation", "P3", "ok",
                              "Remote op to date", 1, 1)
    except Exception:
        return SyncStatus("SYNC-6", "Notifikation", "P3", "unknown",
                          "Remote check fejlede", 0, 1)


def get_sync_status(intro_path: Path = None) -> list:
    """Get status for all 6 sync components"""
    if intro_path is None:
        intro_path = INTRO_PATH
    if not intro_path.exists():
        return [SyncStatus(cid, name, pri, "error", "INTRO path not found", 0, 1)
                for cid, name, _desc, _icon, pri in SYNC_COMPONENTS]

    return [
        _sync_git_status(intro_path),
        _sync_aendringslog(intro_path),
        _sync_version_md(intro_path),
        _sync_cross_references(intro_path),
        _sync_status_md(intro_path),
        _sync_remote_check(intro_path),
    ]


def get_sync_health(intro_path: Path = None) -> float:
    """Get overall sync health as 0-100%"""
    statuses = get_sync_status(intro_path)
    if not statuses:
        return 0.0
    ok_count = sum(1 for s in statuses if s.status == "ok")
    return (ok_count / len(statuses)) * 100


# 
# CUSTOM WIDGETS
# 

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

        # === MULTI-SELECT (Ctrl+Click) ===
        click_ctrl = Gtk.GestureClick()
        click_ctrl.set_button(1)  # Left mouse button
        click_ctrl.connect("pressed", self._on_multi_click)
        self.add_controller(click_ctrl)

        # === DRAG SOURCE (for reorder + folder-to-folder) ===
        drag_source = Gtk.DragSource()
        drag_source.set_actions(Gdk.DragAction.MOVE | Gdk.DragAction.COPY)
        drag_source.connect("prepare", self._on_drag_prepare)
        drag_source.connect("drag-begin", self._on_drag_begin)
        drag_source.connect("drag-end", self._on_drag_end)
        drag_source.connect("drag-cancel", self._on_drag_cancel)
        self.add_controller(drag_source)

        # === DROP TARGET (for reorder — accept drops on this row) ===
        drop_target = Gtk.DropTarget.new(GObject.TYPE_STRING, Gdk.DragAction.MOVE)
        drop_target.connect("drop", self._on_reorder_drop)
        drop_target.connect("enter", self._on_reorder_enter)
        drop_target.connect("leave", self._on_reorder_leave)
        self.add_controller(drop_target)

    def _on_multi_click(self, gesture, n_press, x, y):
        """Handle Ctrl+Click for multi-select"""
        state = gesture.get_current_event_state()
        ctrl_held = bool(state & Gdk.ModifierType.CONTROL_MASK)
        window = self.get_root()

        if ctrl_held and window and hasattr(window, '_selected_rows'):
            path_str = str(self.sejr_info.get("path", ""))
            if path_str in window._selected_rows:
                window._selected_rows.discard(path_str)
                self.remove_css_class("selected-multi")
            else:
                window._selected_rows.add(path_str)
                self.add_css_class("selected-multi")
            # Show multi-select count
            count = len(window._selected_rows)
            if count > 0 and hasattr(window, '_toast_overlay'):
                toast = Adw.Toast.new(f"{count} sejrliste{'r' if count > 1 else ''} valgt")
                toast.set_timeout(1)
                window._toast_overlay.add_toast(toast)
        else:
            # Normal click: clear multi-selection
            if window and hasattr(window, '_selected_rows'):
                for row_widget in self._get_all_rows(window):
                    row_widget.remove_css_class("selected-multi")
                window._selected_rows.clear()

    @staticmethod
    def _get_all_rows(window):
        """Get all SejrRow widgets from the sidebar list"""
        rows = []
        if hasattr(window, 'sejr_list'):
            child = window.sejr_list.get_first_child()
            while child:
                if isinstance(child, SejrRow):
                    rows.append(child)
                child = child.get_next_sibling()
        return rows

    def _on_drag_prepare(self, source, x, y):
        """Provide the sejr path(s) as drag data — supports multi-select + external app export"""
        window = self.get_root()
        # If multi-selected, include all selected paths
        if window and hasattr(window, '_selected_rows') and len(window._selected_rows) > 1:
            path_str = str(self.sejr_info.get("path", ""))
            if path_str in window._selected_rows:
                # Internal: pipe-separated paths for reorder
                all_paths = "|".join(sorted(window._selected_rows))
                string_value = GObject.Value(GObject.TYPE_STRING, all_paths)
                string_provider = Gdk.ContentProvider.new_for_value(string_value)
                # External: text/uri-list for file manager / desktop / other apps
                try:
                    uris = [Path(p).as_uri() for p in sorted(window._selected_rows)]
                    uri_data = "\r\n".join(uris) + "\r\n"
                    uri_bytes = GLib.Bytes.new(uri_data.encode("utf-8"))
                    uri_provider = Gdk.ContentProvider.new_for_bytes("text/uri-list", uri_bytes)
                    return Gdk.ContentProvider.new_union([string_provider, uri_provider])
                except Exception:
                    return string_provider
        # Single drag
        path_str = str(self.sejr_info.get("path", ""))
        if not path_str:
            return None
        string_value = GObject.Value(GObject.TYPE_STRING, path_str)
        string_provider = Gdk.ContentProvider.new_for_value(string_value)
        # External: text/uri-list for file manager / desktop / other apps
        try:
            uri = Path(path_str).as_uri()
            uri_bytes = GLib.Bytes.new((uri + "\r\n").encode("utf-8"))
            uri_provider = Gdk.ContentProvider.new_for_bytes("text/uri-list", uri_bytes)
            return Gdk.ContentProvider.new_union([string_provider, uri_provider])
        except Exception:
            return string_provider

    def _on_drag_begin(self, source, drag):
        """Visual feedback: dim the row being dragged + show drag ghost"""
        self.set_opacity(0.4)
        self.add_css_class("dragging")
        window = self.get_root()
        multi_count = 0
        if window and hasattr(window, '_selected_rows') and len(window._selected_rows) > 1:
            multi_count = len(window._selected_rows)
            # Dim all selected rows
            for row in SejrRow._get_all_rows(window):
                path_str = str(row.sejr_info.get("path", ""))
                if path_str in window._selected_rows:
                    row.set_opacity(0.4)
                    row.add_css_class("dragging")
        # Create drag ghost (semi-transparent snapshot of the row)
        try:
            if multi_count > 1:
                # Multi-select: show count badge
                badge_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
                badge_box.set_opacity(0.85)
                label = Gtk.Label(label=f"{multi_count} sejrlister")
                label.add_css_class("heading")
                badge_box.append(label)
                icon_widget = Gtk.DragIcon.get_for_drag(drag)
                icon_widget.set_child(badge_box)
            else:
                # Single: show row snapshot
                snapshot = Gtk.Snapshot()
                self.snapshot(snapshot)
                paintable = snapshot.to_paintable(None)
                if paintable:
                    icon_widget = Gtk.DragIcon.get_for_drag(drag)
                    picture = Gtk.Picture.new_for_paintable(paintable)
                    picture.set_size_request(250, 48)
                    picture.set_opacity(0.8)
                    icon_widget.set_child(picture)
        except Exception:
            pass  # Fallback: no ghost, still functional
        # Track active drag for Escape cancellation
        if window:
            window._active_drag_row = self

    def _on_drag_end(self, source, drag, delete_data):
        """Restore opacity after drag"""
        self.set_opacity(1.0)
        self.remove_css_class("drop-above")
        self.remove_css_class("dragging")
        # Clear active drag tracking
        window = self.get_root()
        if window and hasattr(window, '_active_drag_row'):
            window._active_drag_row = None

    def _on_drag_cancel(self, source, drag, reason):
        """Handle drag cancellation (e.g. Escape key)"""
        self.set_opacity(1.0)
        self.remove_css_class("drop-above")
        self.remove_css_class("dragging")
        window = self.get_root()
        if window and hasattr(window, '_active_drag_row'):
            window._active_drag_row = None
        # Show toast for user feedback
        if window and hasattr(window, '_toast_overlay'):
            toast = Adw.Toast.new("Drag annulleret")
            toast.set_timeout(2)
            window._toast_overlay.add_toast(toast)
        return True

    def _on_reorder_enter(self, target, x, y):
        """Show drop indicator with valid/invalid coloring"""
        self.add_css_class("drop-above")
        # Determine if this is a valid drop target
        window = self.get_root()
        if window and hasattr(window, '_active_drag_row'):
            drag_row = window._active_drag_row
            if drag_row and drag_row != self:
                self.add_css_class("drop-valid")
            else:
                self.add_css_class("drop-invalid")
        return Gdk.DragAction.MOVE

    def _on_reorder_leave(self, target):
        """Remove all drop indicator classes"""
        self.remove_css_class("drop-above")
        self.remove_css_class("drop-valid")
        self.remove_css_class("drop-invalid")

    def _on_reorder_drop(self, target, value, x, y):
        """Handle a sejr being dropped onto this row (reorder or move)"""
        self.remove_css_class("drop-above")
        self.remove_css_class("drop-valid")
        self.remove_css_class("drop-invalid")
        source_path = str(value)
        dest_info = self.sejr_info

        if not source_path or source_path == str(dest_info.get("path", "")):
            return False  # Dropped on itself

        source = Path(source_path)
        dest = Path(str(dest_info.get("path", "")))

        if not source.exists() or not dest.exists():
            return False

        # Determine if this is a category move (Active ↔ Archive)
        source_parent = source.parent.name  # e.g. "10_ACTIVE" or "90_ARCHIVE"
        dest_parent = dest.parent.name

        if source_parent != dest_parent:
            # Cross-category move: show confirmation dialog first
            target_dir = dest.parent / source.name
            direction = "Arkiv" if "ARCHIVE" in dest_parent else "Aktiv"
            window = self.get_root()
            if not window:
                return False

            dialog = Adw.AlertDialog()
            dialog.set_heading(f"Flyt til {direction}?")
            dialog.set_body(
                f"Vil du flytte:\n{source.name}\n\nFra: {source_parent}\nTil: {dest_parent}"
            )
            dialog.add_response("cancel", "Annuller")
            dialog.add_response("move", f"Flyt til {direction}")
            dialog.set_response_appearance("move", Adw.ResponseAppearance.DESTRUCTIVE)

            drop_row = self  # Capture for closure

            def on_move_response(dlg, response):
                if response == "move":
                    try:
                        import shutil
                        shutil.move(str(source), str(target_dir))
                        # Track for undo
                        if hasattr(window, '_drag_history'):
                            window._drag_history.append({
                                'from': str(source),
                                'to': str(target_dir),
                                'name': source.name,
                                'direction': direction
                            })
                        if hasattr(window, '_load_sejrs'):
                            window._load_sejrs()
                        # Success animation
                        drop_row.add_css_class("success-flash")
                        GLib.timeout_add(700, lambda: drop_row.remove_css_class("success-flash") or False)
                        # Undo toast with 5 second timeout
                        toast = Adw.Toast.new(f"Flyttet til {direction}: {source.name}")
                        toast.set_timeout(5)
                        toast.set_button_label("Fortryd")
                        toast.connect("button-clicked", lambda t: window._undo_last_drag() if hasattr(window, '_undo_last_drag') else None)
                        if hasattr(window, '_toast_overlay'):
                            window._toast_overlay.add_toast(toast)
                    except Exception as e:
                        toast = Adw.Toast.new(f"Fejl: {str(e)[:50]}")
                        toast.set_timeout(3)
                        if hasattr(window, '_toast_overlay'):
                            window._toast_overlay.add_toast(toast)

            dialog.connect("response", on_move_response)
            dialog.present(window)
            return True
        else:
            # Same category: this is a reorder (just visual feedback)
            self.add_css_class("success-flash")
            GLib.timeout_add(700, lambda: self.remove_css_class("success-flash") or False)
            return True


# 
# CHAT STREAM WIDGET - MESSENGER-STYLE INTERFACE
# 

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
                "system": "",
                "kv1nt": "",
                "admiral": "",
                "dna": "",
                "verify": "",
                "error": "",
                "info": "",
            }
            emoji = avatar_emojis.get(sender.lower(), "")

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
            avatar_label.set_markup('<span size="large"></span>')
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
                content=f"Welcome to {sejr_path.name.split('_2026')[0].replace('_', ' ')}! I am watching everything that happens here.",
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


# 
# KONFETTI ANIMATION - CELEBRATION WIDGET
# 

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
            print(f" Celebration! (konfetti fejlede: {e})")
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


# 
# ACHIEVEMENT BADGES SYSTEM
# 

# Achievement definitions
ACHIEVEMENTS = {
    "first_victory": {
        "name": "First Victory",
        "icon": "",
        "description": "Completegjorde your first victory",
        "color": "wisdom"
    },
    "admiral": {
        "name": "Admiral",
        "icon": "",
        "description": "Opnåede 30/30 score",
        "color": "divine"
    },
    "grand_admiral": {
        "name": "Grand Admiral",
        "icon": "",
        "description": "5+ victorye med Admiral status",
        "color": "sacred"
    },
    "speed_runner": {
        "name": "Speed Runner",
        "icon": "",
        "description": "Completegjorde en victory in under 1 hour",
        "color": "cyan"
    },
    "perfectionist": {
        "name": "Perfectionist",
        "icon": "",
        "description": "100% completion på alle 3 passes",
        "color": "heart"
    },
    "streak_3": {
        "name": "On a Streak",
        "icon": "",
        "description": "3 victories in a row without pause",
        "color": "primary"
    },
    "streak_7": {
        "name": "Ustoppelig",
        "icon": "",
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
        icon_label = Gtk.Label(label=ach.get("icon", ""))
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

        trophy = Gtk.Label(label="")
        trophy.set_markup('<span size="large"></span>')
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


# 
# VF LOGO WIDGET - KV1NT ADMIRAL STANDARD
# 

# 
# ANIMATED BACKGROUND - LIVING GRADIENT CANVAS
# 

class AnimatedBackground(Gtk.DrawingArea):
    """
     LEVENDE ANIMERET BAGGRUND

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


# 
# LIVE AKTIVITETS MONITOR - REAL-TIME COMMAND CENTER
# 

class LiveActivityMonitor(Gtk.Box):
    """
     VERDENSKLASSE LIVE AKTIVITETS MONITOR

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
        self.pulse_dot = Gtk.Label(label="")
        self.pulse_dot.add_css_class("pulse-indicator")
        header.append(self.pulse_dot)

        # Titel
        title = Gtk.Label(label="LIVE AKTIVITET")
        title.add_css_class("activity-title")
        title.set_hexpand(True)
        title.set_halign(Gtk.Align.START)
        header.append(title)

        # Status badge
        self.status_badge = Gtk.Label(label=" AKTIV")
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
        self.hvad_label = Gtk.Label(label=" WHAT: Waiter...")
        self.hvad_label.add_css_class("five-w-item")
        self.five_w_bar.append(self.hvad_label)

        # WHERE
        self.hvor_label = Gtk.Label(label=" WHERE: -")
        self.hvor_label.add_css_class("five-w-item")
        self.five_w_bar.append(self.hvor_label)

        # WHEN
        self.hvornaar_label = Gtk.Label(label=" WHEN: Nu")
        self.hvornaar_label.add_css_class("five-w-item")
        self.five_w_bar.append(self.hvornaar_label)

        self.append(self.five_w_bar)

        # Tilføj initial besked
        self._add_activity("system", "Live activitysmonitor startet", "")

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
            "create": "",
            "update": "",
            "verify": "",
            "archive": "",
            "complete": "",
            "error": "",
            "start": "",
            "progress": "",
            "git": "",
            "test": "",
        }
        for key, icon in icons.items():
            if key in action.lower():
                return icon
        return ""

    def _update_five_w(self, sejr_name: str, action: str):
        """Update 5W statuslinje"""
        now = datetime.now().strftime("%H:%M:%S")
        self.hvad_label.set_text(f" {action[:30]}")
        self.hvor_label.set_text(f" {sejr_name[:20]}")
        self.hvornaar_label.set_text(f" {now}")

    def _add_activity(self, source: str, message: str, icon: str = ""):
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
        self._add_activity("system", "Activityslog ryddet", "")

    def log_event(self, source: str, message: str, icon: str = ""):
        """Public metode til at logge events fra andre dele af appen"""
        GLib.idle_add(lambda: self._add_activity(source, message, icon))


# 
# VINDERTAVLE - VICTORY JOURNEY BOARD
# 

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
            score_label = Gtk.Label(label=f" {victory['score']}/30")
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


# 
# SEJR FIL MANAGER - HÅNDTER FILER I SEJR MAPPE
# 

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
        drop_hint = Gtk.Label(label=" Drag files here or use the Import button")
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


# 
# PRIORITETS OVERBLIK - WHAT HAR BRUG FOR OPMÆRKSOMHED NU
# 

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

        title = Gtk.Label(label=" Priority Dashboard")
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

            label = Gtk.Label(label=" Alt Readyt!")
            label.add_css_class("title-3")
            clear_box.append(label)

            desc = Gtk.Label(label="None akutte ting. Du er på rette spor!")
            desc.add_css_class("dim-label")
            clear_box.append(desc)

            self.sections_box.append(clear_box)
        else:
            # Byg prioritets sektioner
            if priorities["akut"]:
                self._add_section(" AKUT", priorities["akut"], "error")
            if priorities["opmaerksomhed"]:
                self._add_section(" OPMÆRKSOMHED", priorities["opmaerksomhed"], "warning")
            if priorities["naeste"]:
                self._add_section(" NÆSTE SKRIDT", priorities["naeste"], "accent")

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
                                "title": f"Victory gået i stå: {sejr_dir.name}",
                                "subtitle": f"Kun {progress:.0f}% færdig ({done}/{total})",
                                "action": "Open Victory",
                                "path": str(sejr_dir),
                                "icon": "emblem-important-symbolic"
                            })
                        elif progress < 80:
                            priorities["opmaerksomhed"].append({
                                "title": f"Continue: {sejr_dir.name}",
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
                        "title": f"Mangler verifikation: {sejr_dir.name}",
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
        script = SCRIPTS_DIR / "generate_sejr.py"
        if script.exists():
            subprocess.Popen(["python3", str(script)])
            send_notification("New Victory", "Opretter ny victory...", "list-add-symbolic")


# 
# LINEN HEALTH VIEW
# 

LINEN_CHAKRA_COLORS = {
    "L": "#00D9FF",   # Cyan — Logging
    "I": "#f59e0b",   # Wisdom gold — Indeksering
    "N": "#6366f1",   # Intuition indigo — Nesting
    "E": "#00FF88",   # Success green — Efterproevning
    "N2": "#10b981",  # Heart emerald — Navigation
}


class LinenComponentRow(Gtk.Box):
    """A single row showing one LINEN component with progress bar and chakra colors (Pass 3)"""

    def __init__(self, score: LinenScore):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.score = score
        self.add_css_class("card")
        self.set_margin_start(4)
        self.set_margin_end(4)
        self.set_margin_top(4)
        self.set_margin_bottom(4)

        # Chakra color indicator bar (left side)
        outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        chakra_color = LINEN_CHAKRA_COLORS.get(score.component, "#9ca3af")
        color_bar = Gtk.Box()
        color_bar.set_size_request(4, -1)
        css_bar = Gtk.CssProvider()
        css_bar.load_from_string(f"box {{ background-color: {chakra_color}; border-radius: 2px; }}")
        color_bar.get_style_context().add_provider(css_bar, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        outer.append(color_bar)

        inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        inner.set_margin_start(16)
        inner.set_margin_end(16)
        inner.set_margin_top(12)
        inner.set_margin_bottom(12)
        inner.set_hexpand(True)

        # Top row: Letter + Name + Percentage
        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        # Letter badge with chakra color
        letter_label = Gtk.Label(label=score.component[0])  # Just first char (L, I, N, E, N)
        letter_label.add_css_class("title-1")
        letter_label.set_size_request(40, 40)
        letter_label.set_valign(Gtk.Align.CENTER)
        letter_css = Gtk.CssProvider()
        letter_css.load_from_string(f"label {{ color: {chakra_color}; }}")
        letter_label.get_style_context().add_provider(letter_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        top_row.append(letter_label)

        # Name + description
        name_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        name_box.set_hexpand(True)

        name_label = Gtk.Label(label=score.name)
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("heading")
        name_box.append(name_label)

        # Find description from LINEN_COMPONENTS
        desc = ""
        for comp in LINEN_COMPONENTS:
            if comp[0] == score.component:
                desc = comp[2]
                break
        desc_label = Gtk.Label(label=desc)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.add_css_class("caption")
        desc_label.add_css_class("dim-label")
        name_box.append(desc_label)

        top_row.append(name_box)

        # Percentage
        pct_label = Gtk.Label(label=f"{score.percentage:.0f}%")
        pct_label.add_css_class("title-2")
        if score.percentage >= 80:
            pct_label.add_css_class("success")
        elif score.percentage >= 50:
            pct_label.add_css_class("warning")
        else:
            pct_label.add_css_class("error")
        pct_label.set_valign(Gtk.Align.CENTER)
        top_row.append(pct_label)

        inner.append(top_row)

        # Progress bar
        progress = Gtk.ProgressBar()
        progress.set_fraction(score.percentage / 100.0)
        progress.set_size_request(-1, 8)
        if score.percentage >= 80:
            progress.add_css_class("success")
        elif score.percentage >= 50:
            progress.add_css_class("warning")
        inner.append(progress)

        # Stats line: "32/40 files passing • Last check: 23:50"
        stats_label = Gtk.Label(
            label=f"{score.passing_items}/{score.total_items} items passing"
            + (f" • Checked: {score.last_checked}" if score.last_checked else "")
        )
        stats_label.set_halign(Gtk.Align.START)
        stats_label.add_css_class("caption")
        stats_label.add_css_class("dim-label")
        inner.append(stats_label)

        outer.append(inner)
        self.append(outer)

        # === EXPANDABLE DETAIL SECTION ===
        self.detail_revealer = Gtk.Revealer()
        self.detail_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        self.detail_revealer.set_transition_duration(250)

        detail_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        detail_box.set_margin_start(16)
        detail_box.set_margin_end(16)
        detail_box.set_margin_bottom(12)

        # Show max 20 items (avoid gigantic lists)
        shown = 0
        max_show = 20
        # Show failing first, then passing
        failing = [(p, ok) for p, ok in score.details if not ok]
        passing = [(p, ok) for p, ok in score.details if ok]
        sorted_details = failing + passing

        for path_str, passed in sorted_details:
            if shown >= max_show:
                remaining = len(sorted_details) - max_show
                more_label = Gtk.Label(label=f"... og {remaining} mere")
                more_label.add_css_class("caption")
                more_label.add_css_class("dim-label")
                more_label.set_halign(Gtk.Align.START)
                detail_box.append(more_label)
                break

            item_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            status_icon = Gtk.Label(label="PASS" if passed else "FAIL")
            status_icon.add_css_class("caption")
            if passed:
                status_icon.add_css_class("success")
            else:
                status_icon.add_css_class("error")
            status_icon.set_size_request(36, -1)
            item_row.append(status_icon)

            path_label = Gtk.Label(label=path_str)
            path_label.set_halign(Gtk.Align.START)
            path_label.add_css_class("caption")
            path_label.add_css_class("monospace")
            path_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
            path_label.set_hexpand(True)
            item_row.append(path_label)

            detail_box.append(item_row)
            shown += 1

        self.detail_revealer.set_child(detail_box)
        self.append(self.detail_revealer)

        # Make clickable to expand/collapse
        click = Gtk.GestureClick()
        click.connect("released", self._on_clicked)
        self.add_controller(click)
        self.set_cursor_from_name("pointer")

    def _on_clicked(self, gesture, n_press, x, y):
        """Toggle detail view"""
        revealed = self.detail_revealer.get_child_revealed()
        self.detail_revealer.set_reveal_child(not revealed)


class LinenHealthView(Gtk.Box):
    """
    LINEN System Health Dashboard.

    Shows the 5 LINEN pillars (Logging, Indeksering, Nesting,
    Efterprøvning, Navigation) with real-time progress bars
    from scanning the MASTER FOLDERS(INTRO) directory.
    """

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_start(32)
        self.set_margin_end(32)
        self.set_margin_top(24)
        self.set_margin_bottom(24)

        self.scores = []
        self._build_ui()
        self._refresh_scores()

    def _build_ui(self):
        """Build the LINEN health dashboard"""
        # === HEADER ===
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        icon = Gtk.Image.new_from_icon_name("applications-science-symbolic")
        icon.set_pixel_size(32)
        header.append(icon)

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # LINEN badge (Pass 3)
        badge_label = Gtk.Label(label="LINEN")
        badge_label.add_css_class("heading")
        badge_css = Gtk.CssProvider()
        badge_css.load_from_string(
            "label { color: #00D9FF; letter-spacing: 3px; font-weight: bold; }"
        )
        badge_label.get_style_context().add_provider(badge_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        title_box.append(badge_label)

        title = Gtk.Label(label="System Health")
        title.set_halign(Gtk.Align.START)
        title.add_css_class("title-1")
        title_box.append(title)

        subtitle = Gtk.Label(label="Logging | Indeksering | Nesting | Efterproevning | Navigation")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("caption")
        subtitle.add_css_class("dim-label")
        title_box.append(subtitle)

        title_box.set_hexpand(True)
        header.append(title_box)

        # Overall score badge
        self.overall_label = Gtk.Label(label="...")
        self.overall_label.add_css_class("title-1")
        header.append(self.overall_label)

        self.append(header)

        # Separator
        self.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        # === OVERALL PROGRESS ===
        self.overall_bar = Gtk.ProgressBar()
        self.overall_bar.set_size_request(-1, 12)
        self.overall_bar.add_css_class("linen-overall")
        self.append(self.overall_bar)

        # === COMPONENT ROWS ===
        self.components_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.append(self.components_box)

        # === ACTIONS ===
        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        action_box.set_margin_top(16)
        action_box.set_halign(Gtk.Align.CENTER)

        refresh_btn = Gtk.Button(label="Scan Again")
        refresh_btn.set_icon_name("view-refresh-symbolic")
        refresh_btn.add_css_class("suggested-action")
        refresh_btn.add_css_class("pill")
        refresh_btn.connect("clicked", lambda b: self._refresh_scores())
        action_box.append(refresh_btn)

        # Info about scan path
        path_label = Gtk.Label(label=f"Scanning: {INTRO_PATH}")
        path_label.add_css_class("caption")
        path_label.add_css_class("dim-label")
        action_box.append(path_label)

        self.append(action_box)

        # === PASS 2 SECTIONS ===
        self.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        # 4-layer validation diagram
        self._build_validation_layers()

        # Continuous validation schedule
        self._build_validation_schedule()

        # Live monitoring
        self._setup_live_monitoring()

        # Monitoring status indicator
        monitor_label = Gtk.Label(
            label="Live monitoring: Aktiv" if getattr(self, '_monitoring_active', False)
            else "Live monitoring: INTRO mappe ikke fundet"
        )
        monitor_label.set_halign(Gtk.Align.START)
        monitor_label.add_css_class("caption")
        monitor_label.add_css_class("dim-label")
        monitor_label.set_margin_top(8)
        self.append(monitor_label)

    def _refresh_scores(self):
        """Scan INTRO folder and update all components"""
        self.scores = get_linen_status()
        overall = sum(s.percentage for s in self.scores) / len(self.scores) if self.scores else 0

        # Update overall
        self.overall_label.set_label(f"{overall:.0f}%")
        self.overall_bar.set_fraction(overall / 100.0)

        # Color the overall score
        for cls in ["success", "warning", "error"]:
            self.overall_label.remove_css_class(cls)
        if overall >= 80:
            self.overall_label.add_css_class("success")
        elif overall >= 50:
            self.overall_label.add_css_class("warning")
        else:
            self.overall_label.add_css_class("error")

        # Rebuild component rows
        while True:
            child = self.components_box.get_first_child()
            if child is None:
                break
            self.components_box.remove(child)

        for score in self.scores:
            row = LinenComponentRow(score)
            self.components_box.append(row)

    def get_scores(self) -> List[LinenScore]:
        """Return current scores for use by other widgets"""
        return self.scores

    def _build_validation_layers(self):
        """Build the 4-layer validation diagram (Pass 2)"""
        section_label = Gtk.Label(label="4-Lags Validering")
        section_label.set_halign(Gtk.Align.START)
        section_label.add_css_class("title-3")
        section_label.set_margin_top(16)
        self.append(section_label)

        desc = Gtk.Label(
            label="Validering sker i 4 lag — fra syntaks til cross-referencer"
        )
        desc.set_halign(Gtk.Align.START)
        desc.add_css_class("caption")
        desc.add_css_class("dim-label")
        desc.set_wrap(True)
        desc.set_wrap_mode(Pango.WrapMode.WORD)
        self.append(desc)

        layers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        layers_box.set_margin_top(8)

        for i, (num, name, description, _color) in enumerate(VALIDATION_LAYERS):
            card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            card.add_css_class("card")
            card.set_margin_start(4)
            card.set_margin_end(4)

            inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            inner.set_margin_start(16)
            inner.set_margin_end(16)
            inner.set_margin_top(10)
            inner.set_margin_bottom(10)
            inner.set_hexpand(True)

            # Layer number badge
            num_label = Gtk.Label(label=f"L{num}")
            num_label.add_css_class("title-2")
            num_label.set_size_request(40, -1)
            inner.append(num_label)

            # Name + description
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            info_box.set_hexpand(True)

            n_label = Gtk.Label(label=name)
            n_label.set_halign(Gtk.Align.START)
            n_label.add_css_class("heading")
            info_box.append(n_label)

            d_label = Gtk.Label(label=description)
            d_label.set_halign(Gtk.Align.START)
            d_label.add_css_class("caption")
            d_label.add_css_class("dim-label")
            d_label.set_wrap(True)
            d_label.set_wrap_mode(Pango.WrapMode.WORD)
            info_box.append(d_label)

            inner.append(info_box)
            card.append(inner)
            layers_box.append(card)

            # Arrow between layers (except after last)
            if i < len(VALIDATION_LAYERS) - 1:
                arrow = Gtk.Label(label="v")
                arrow.add_css_class("dim-label")
                arrow.set_halign(Gtk.Align.CENTER)
                arrow.set_margin_top(2)
                arrow.set_margin_bottom(2)
                layers_box.append(arrow)

        self.append(layers_box)

    def _build_validation_schedule(self):
        """Build the validation schedule view with action buttons (Pass 2)"""
        section_label = Gtk.Label(label="Validerings Tidsplan")
        section_label.set_halign(Gtk.Align.START)
        section_label.add_css_class("title-3")
        section_label.set_margin_top(16)
        self.append(section_label)

        schedule_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        schedule_box.set_margin_top(8)

        for freq, script, description in VALIDATION_SCHEDULE:
            card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            card.add_css_class("card")
            card.set_margin_start(4)
            card.set_margin_end(4)

            inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            inner.set_margin_start(16)
            inner.set_margin_end(16)
            inner.set_margin_top(10)
            inner.set_margin_bottom(10)
            inner.set_hexpand(True)

            # Frequency badge
            f_label = Gtk.Label(label=freq)
            f_label.add_css_class("heading")
            f_label.set_size_request(90, -1)
            f_label.set_halign(Gtk.Align.START)
            inner.append(f_label)

            # Script + description
            info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            info.set_hexpand(True)

            s_label = Gtk.Label(label=script)
            s_label.set_halign(Gtk.Align.START)
            s_label.add_css_class("monospace")
            s_label.add_css_class("caption")
            info.append(s_label)

            d_label = Gtk.Label(label=description)
            d_label.set_halign(Gtk.Align.START)
            d_label.add_css_class("caption")
            d_label.add_css_class("dim-label")
            info.append(d_label)

            inner.append(info)

            # Timestamp placeholder
            self._schedule_timestamps = getattr(self, '_schedule_timestamps', {})
            ts = self._schedule_timestamps.get(freq, "Aldrig koert")
            ts_label = Gtk.Label(label=ts)
            ts_label.add_css_class("caption")
            ts_label.add_css_class("dim-label")
            inner.append(ts_label)

            card.append(inner)
            schedule_box.append(card)

        self.append(schedule_box)

        # Action buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_margin_top(8)
        btn_box.set_halign(Gtk.Align.CENTER)

        daily_btn = Gtk.Button(label="Koer Daglig Check")
        daily_btn.set_icon_name("emblem-ok-symbolic")
        daily_btn.add_css_class("suggested-action")
        daily_btn.add_css_class("pill")
        daily_btn.connect("clicked", lambda b: self._run_validation("Dagligt"))
        btn_box.append(daily_btn)

        weekly_btn = Gtk.Button(label="Koer Ugentlig Check")
        weekly_btn.set_icon_name("view-refresh-symbolic")
        weekly_btn.add_css_class("pill")
        weekly_btn.connect("clicked", lambda b: self._run_validation("Ugentligt"))
        btn_box.append(weekly_btn)

        self.append(btn_box)

    def _run_validation(self, freq: str):
        """Run a validation check and update timestamp"""
        from datetime import datetime
        self._schedule_timestamps = getattr(self, '_schedule_timestamps', {})
        self._schedule_timestamps[freq] = datetime.now().strftime("%Y-%m-%d %H:%M")
        # Refresh the LINEN scan
        self._refresh_scores()

    def _setup_live_monitoring(self):
        """Set up FileMonitor for auto-refresh when INTRO files change (Pass 2)"""
        intro_path = str(INTRO_PATH)
        if not os.path.isdir(intro_path):
            return

        monitor_file = Gio.File.new_for_path(intro_path)
        try:
            self._file_monitor = monitor_file.monitor_directory(
                Gio.FileMonitorFlags.NONE, None
            )
            self._file_monitor.set_rate_limit(5000)  # 5 sec debounce
            self._file_monitor.connect("changed", self._on_intro_changed)
            self._monitoring_active = True
        except Exception:
            self._monitoring_active = False

    def _on_intro_changed(self, monitor, file, other_file, event_type):
        """Auto-refresh LINEN scores when INTRO files change"""
        if event_type in (
            Gio.FileMonitorEvent.CHANGED,
            Gio.FileMonitorEvent.CREATED,
            Gio.FileMonitorEvent.DELETED,
        ):
            # Use GLib.idle_add for thread safety
            GLib.idle_add(self._refresh_scores)


#
# ARCHITECTURE OVERVIEW VIEW
#

class ArchitectureOverviewView(Gtk.Box):
    """
    3-Lags Arkitektur Dashboard.

    Shows the INTRO system's three architectural layers (Presentation,
    Structure, Verification), the 6 design principles, 3 design patterns,
    and the 00-99 numeric hierarchy allocation.
    """

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.set_margin_start(32)
        self.set_margin_end(32)
        self.set_margin_top(24)
        self.set_margin_bottom(24)

        self._build_ui()

    def _build_ui(self):
        """Build the complete architecture overview"""
        # === HEADER ===
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        icon = Gtk.Image.new_from_icon_name("view-grid-symbolic")
        icon.set_pixel_size(32)
        header.append(icon)

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        title = Gtk.Label(label="3-Lags Arkitektur")
        title.set_halign(Gtk.Align.START)
        title.add_css_class("title-1")
        title_box.append(title)

        subtitle = Gtk.Label(label="Presentation → Struktur → Verifikation")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.add_css_class("caption")
        subtitle.add_css_class("dim-label")
        title_box.append(subtitle)

        header.append(title_box)
        self.append(header)

        self.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        # === SECTION 1: THREE LAYERS FLOW DIAGRAM ===
        self._build_layers_section()

        # === SECTION 2: 6 PRINCIPLES ===
        self._build_principles_section()

        # === SECTION 3: DESIGN PATTERNS ===
        self._build_patterns_section()

        # === SECTION 4: NUMERIC HIERARCHY ===
        self._build_hierarchy_section()

        # === SECTION 5: DESIGN DECISIONS (Pass 2) ===
        self._build_decisions_section()

        # === SECTION 6: SCALING OVERVIEW (Pass 2) ===
        self._build_scaling_section()

        # === SECTION 7: FOLDER ANATOMY (Pass 2) ===
        self._build_anatomy_section()

    def _build_layers_section(self):
        """Build the 3-layer flow diagram with real stats, colors, and click detail (Pass 3)"""
        section_label = Gtk.Label(label="Systemets 3 Lag")
        section_label.set_halign(Gtk.Align.START)
        section_label.add_css_class("title-3")
        section_label.set_margin_top(8)
        self.append(section_label)

        hint = Gtk.Label(label="Klik paa et lag for detaljeret statistik")
        hint.set_halign(Gtk.Align.START)
        hint.add_css_class("caption")
        hint.add_css_class("dim-label")
        self.append(hint)

        stats = get_layer_stats()
        flow_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        for i, stat in enumerate(stats):
            layer_color = LAYER_COLORS.get(str(stat.layer), "#9ca3af")

            # Layer card
            card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            card.add_css_class("card")
            card.set_margin_start(4)
            card.set_margin_end(4)
            card.set_cursor(Gdk.Cursor.new_from_name("pointer"))

            # Color indicator bar (left side)
            color_bar = Gtk.Box()
            color_bar.set_size_request(6, -1)
            css_prov = Gtk.CssProvider()
            css_prov.load_from_string(f"box {{ background-color: {layer_color}; border-radius: 3px 0 0 3px; }}")
            color_bar.get_style_context().add_provider(css_prov, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            card.append(color_bar)

            inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            inner.set_margin_start(16)
            inner.set_margin_end(16)
            inner.set_margin_top(12)
            inner.set_margin_bottom(12)
            inner.set_hexpand(True)

            # Layer number with color
            num_label = Gtk.Label(label=str(stat.layer))
            num_label.add_css_class("title-1")
            num_label.set_size_request(40, 40)
            num_label.set_valign(Gtk.Align.CENTER)
            num_css = Gtk.CssProvider()
            num_css.load_from_string(f"label {{ color: {layer_color}; }}")
            num_label.get_style_context().add_provider(num_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            inner.append(num_label)

            # Layer info
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            info_box.set_hexpand(True)

            name_label = Gtk.Label(label=stat.name)
            name_label.set_halign(Gtk.Align.START)
            name_label.add_css_class("heading")
            info_box.append(name_label)

            desc_label = Gtk.Label(label=stat.description)
            desc_label.set_halign(Gtk.Align.START)
            desc_label.add_css_class("caption")
            desc_label.add_css_class("dim-label")
            info_box.append(desc_label)

            inner.append(info_box)

            # Item count badge
            count_label = Gtk.Label(label=str(stat.total_items))
            count_label.add_css_class("title-2")
            count_label.set_valign(Gtk.Align.CENTER)
            inner.append(count_label)

            # Click indicator
            arrow = Gtk.Label(label=">")
            arrow.add_css_class("dim-label")
            arrow.set_valign(Gtk.Align.CENTER)
            inner.append(arrow)

            card.append(inner)
            flow_box.append(card)

            # Detail revealer for layer stats
            detail_revealer = Gtk.Revealer()
            detail_revealer.set_reveal_child(False)
            detail_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
            detail_revealer.set_transition_duration(200)
            flow_box.append(detail_revealer)

            # Click gesture
            gesture = Gtk.GestureClick.new()
            gesture.connect("released", self._on_layer_clicked, stat, detail_revealer)
            card.add_controller(gesture)

            # Arrow between layers (except after last)
            if i < len(stats) - 1:
                flow_arrow = Gtk.Label(label="v")
                flow_arrow.add_css_class("title-3")
                flow_arrow.add_css_class("dim-label")
                flow_arrow.set_halign(Gtk.Align.CENTER)
                flow_arrow.set_margin_top(4)
                flow_arrow.set_margin_bottom(4)
                flow_box.append(flow_arrow)

        self.append(flow_box)

    def _on_layer_clicked(self, gesture, n_press, x, y, stat, revealer):
        """Show detailed stats for a layer"""
        if revealer.get_reveal_child():
            revealer.set_reveal_child(False)
            return

        detail = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        detail.set_margin_start(24)
        detail.set_margin_end(8)
        detail.set_margin_top(4)
        detail.set_margin_bottom(8)

        # Summary
        summary = Gtk.Label(label=f"Lag {stat.layer}: {stat.name}")
        summary.set_halign(Gtk.Align.START)
        summary.add_css_class("heading")
        detail.append(summary)

        info_lines = [
            f"Beskrivelse: {stat.description}",
            f"Total items: {stat.total_items}",
        ]
        if hasattr(stat, 'details') and stat.details:
            info_lines.append(f"Detaljer: {stat.details}")

        for line in info_lines:
            l = Gtk.Label(label=line)
            l.set_halign(Gtk.Align.START)
            l.add_css_class("caption")
            l.set_wrap(True)
            l.set_wrap_mode(Pango.WrapMode.WORD)
            detail.append(l)

        revealer.set_child(detail)
        revealer.set_reveal_child(True)

    def _build_principles_section(self):
        """Build the 6 architecture principles as a grid"""
        section_label = Gtk.Label(label="6 Arkitektur Principper")
        section_label.set_halign(Gtk.Align.START)
        section_label.add_css_class("title-3")
        section_label.set_margin_top(16)
        self.append(section_label)

        grid = Gtk.FlowBox()
        grid.set_max_children_per_line(3)
        grid.set_min_children_per_line(2)
        grid.set_selection_mode(Gtk.SelectionMode.NONE)
        grid.set_row_spacing(8)
        grid.set_column_spacing(8)

        for name, impl in ARCHITECTURE_PRINCIPLES:
            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            card.add_css_class("card")
            card.set_size_request(180, -1)

            inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            inner.set_margin_start(12)
            inner.set_margin_end(12)
            inner.set_margin_top(10)
            inner.set_margin_bottom(10)

            n_label = Gtk.Label(label=name)
            n_label.set_halign(Gtk.Align.START)
            n_label.add_css_class("heading")
            inner.append(n_label)

            i_label = Gtk.Label(label=impl)
            i_label.set_halign(Gtk.Align.START)
            i_label.add_css_class("caption")
            i_label.add_css_class("dim-label")
            i_label.set_wrap(True)
            i_label.set_wrap_mode(Pango.WrapMode.WORD)
            inner.append(i_label)

            card.append(inner)
            grid.insert(card, -1)

        self.append(grid)

    def _build_patterns_section(self):
        """Build the 3 design patterns as clickable expandable cards (Pass 3)"""
        section_label = Gtk.Label(label="3 Design Patterns")
        section_label.set_halign(Gtk.Align.START)
        section_label.add_css_class("title-3")
        section_label.set_margin_top(16)
        self.append(section_label)

        hint = Gtk.Label(label="Klik paa et pattern for at se eksempler fra INTRO")
        hint.set_halign(Gtk.Align.START)
        hint.add_css_class("caption")
        hint.add_css_class("dim-label")
        self.append(hint)

        patterns_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        for name, description, rationale in DESIGN_PATTERNS:
            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            card.add_css_class("card")
            card.set_margin_start(4)
            card.set_margin_end(4)
            card.set_cursor(Gdk.Cursor.new_from_name("pointer"))

            inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            inner.set_margin_start(16)
            inner.set_margin_end(16)
            inner.set_margin_top(12)
            inner.set_margin_bottom(12)

            # Pattern name with click hint
            name_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            n_label = Gtk.Label(label=name)
            n_label.set_halign(Gtk.Align.START)
            n_label.add_css_class("heading")
            n_label.set_hexpand(True)
            name_row.append(n_label)

            arrow = Gtk.Label(label=">")
            arrow.add_css_class("dim-label")
            name_row.append(arrow)
            inner.append(name_row)

            # Description (monospace for structure)
            d_label = Gtk.Label(label=description)
            d_label.set_halign(Gtk.Align.START)
            d_label.add_css_class("caption")
            d_label.add_css_class("monospace")
            d_label.set_wrap(True)
            d_label.set_wrap_mode(Pango.WrapMode.WORD)
            inner.append(d_label)

            # Rationale
            r_label = Gtk.Label(label=f"Rationale: {rationale}")
            r_label.set_halign(Gtk.Align.START)
            r_label.add_css_class("caption")
            r_label.add_css_class("dim-label")
            r_label.set_wrap(True)
            r_label.set_wrap_mode(Pango.WrapMode.WORD)
            inner.append(r_label)

            card.append(inner)
            patterns_box.append(card)

            # Detail revealer for pattern examples
            detail_revealer = Gtk.Revealer()
            detail_revealer.set_reveal_child(False)
            detail_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
            detail_revealer.set_transition_duration(200)
            patterns_box.append(detail_revealer)

            # Click gesture
            gesture = Gtk.GestureClick.new()
            gesture.connect("released", self._on_pattern_clicked, name, detail_revealer)
            card.add_controller(gesture)

        self.append(patterns_box)

    def _on_pattern_clicked(self, gesture, n_press, x, y, pattern_name, revealer):
        """Show real INTRO examples for a design pattern"""
        if revealer.get_reveal_child():
            revealer.set_reveal_child(False)
            return

        examples = self._get_pattern_examples(pattern_name)
        detail = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        detail.set_margin_start(24)
        detail.set_margin_end(8)
        detail.set_margin_top(4)
        detail.set_margin_bottom(8)

        header = Gtk.Label(label=f"Eksempler fra INTRO ({pattern_name}):")
        header.set_halign(Gtk.Align.START)
        header.add_css_class("heading")
        detail.append(header)

        if examples:
            for ex in examples[:10]:
                e_label = Gtk.Label(label=ex)
                e_label.set_halign(Gtk.Align.START)
                e_label.add_css_class("monospace")
                e_label.add_css_class("caption")
                detail.append(e_label)
            if len(examples) > 10:
                more = Gtk.Label(label=f"... og {len(examples) - 10} mere")
                more.add_css_class("caption")
                more.add_css_class("dim-label")
                more.set_halign(Gtk.Align.START)
                detail.append(more)
        else:
            empty = Gtk.Label(label="Ingen eksempler fundet")
            empty.add_css_class("caption")
            empty.add_css_class("dim-label")
            empty.set_halign(Gtk.Align.START)
            detail.append(empty)

        revealer.set_child(detail)
        revealer.set_reveal_child(True)

    def _get_pattern_examples(self, pattern_name):
        """Find real INTRO files matching a design pattern"""
        intro_path = str(INTRO_PATH)
        if not os.path.isdir(intro_path):
            return []
        results = []
        if "Sektion Container" in pattern_name:
            # Look for XX_SEKTION folders with content + _TODO_VERIFIKATION
            for entry in sorted(os.listdir(intro_path)):
                full = os.path.join(intro_path, entry)
                if os.path.isdir(full) and re.match(r'^\d{2}_', entry):
                    has_todo = os.path.isdir(os.path.join(full, "_TODO_VERIFIKATION"))
                    tag = " [+VERIFIKATION]" if has_todo else ""
                    results.append(f"{entry}/{tag}")
        elif "Document Sandwich" in pattern_name:
            # Look for .md files that have AENDRINGSLOG
            for entry in sorted(os.listdir(intro_path)):
                if entry.endswith(".md"):
                    try:
                        full = os.path.join(intro_path, entry)
                        with open(full, "r", errors="ignore") as f:
                            content = f.read(4096)
                        has_log = "NDRINGSLOG" in content or "CHANGELOG" in content
                        tag = " [+AENDRINGSLOG]" if has_log else ""
                        results.append(f"{entry}{tag}")
                    except Exception:
                        results.append(entry)
        elif "Meta-Data Nesting" in pattern_name:
            # Look for _TODO_VERIFIKATION/STATUS.md
            for entry in sorted(os.listdir(intro_path)):
                full = os.path.join(intro_path, entry)
                if os.path.isdir(full):
                    status = os.path.join(full, "_TODO_VERIFIKATION", "STATUS.md")
                    if os.path.exists(status):
                        results.append(f"{entry}/_TODO_VERIFIKATION/STATUS.md")
        return results

    def _build_hierarchy_section(self):
        """Build the 00-99 numeric hierarchy table with clickable rows (Pass 3)"""
        section_label = Gtk.Label(label="Numerisk Hierarki (00-99)")
        section_label.set_halign(Gtk.Align.START)
        section_label.add_css_class("title-3")
        section_label.set_margin_top(16)
        self.append(section_label)

        hint = Gtk.Label(label="Klik paa en range for at se filer")
        hint.set_halign(Gtk.Align.START)
        hint.add_css_class("caption")
        hint.add_css_class("dim-label")
        self.append(hint)

        distribution = get_numerisk_distribution()

        hierarchy_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        for range_str, label, _color in NUMERISK_HIERARKI:
            count = distribution.get(range_str, 0)

            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            row.add_css_class("card")
            row.set_margin_start(4)
            row.set_margin_end(4)
            row.set_cursor(Gdk.Cursor.new_from_name("pointer"))

            inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            inner.set_margin_start(12)
            inner.set_margin_end(12)
            inner.set_margin_top(8)
            inner.set_margin_bottom(8)
            inner.set_hexpand(True)

            # Range badge
            range_label = Gtk.Label(label=range_str)
            range_label.add_css_class("heading")
            range_label.add_css_class("monospace")
            range_label.set_size_request(60, -1)
            inner.append(range_label)

            # Label
            label_widget = Gtk.Label(label=label)
            label_widget.set_halign(Gtk.Align.START)
            label_widget.set_hexpand(True)
            inner.append(label_widget)

            # Count
            count_label = Gtk.Label(label=str(count) if count > 0 else "---")
            count_label.add_css_class("caption")
            if count > 0:
                count_label.add_css_class("success")
            else:
                count_label.add_css_class("dim-label")
            inner.append(count_label)

            # Click indicator
            arrow_label = Gtk.Label(label=">")
            arrow_label.add_css_class("dim-label")
            inner.append(arrow_label)

            row.append(inner)
            hierarchy_box.append(row)

            # Detail revealer (hidden by default)
            detail_revealer = Gtk.Revealer()
            detail_revealer.set_reveal_child(False)
            detail_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
            detail_revealer.set_transition_duration(200)
            hierarchy_box.append(detail_revealer)

            # Click gesture
            gesture = Gtk.GestureClick.new()
            gesture.connect("released", self._on_range_clicked, range_str, detail_revealer)
            row.add_controller(gesture)

        self.append(hierarchy_box)

    def _on_range_clicked(self, gesture, n_press, x, y, range_str, revealer):
        """Toggle file list for a numeric range"""
        if revealer.get_reveal_child():
            revealer.set_reveal_child(False)
            return

        files = self._get_files_for_range(range_str)
        detail_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        detail_box.set_margin_start(24)
        detail_box.set_margin_end(8)
        detail_box.set_margin_top(4)
        detail_box.set_margin_bottom(8)

        if files:
            for f in files[:20]:  # Limit to 20
                f_label = Gtk.Label(label=f)
                f_label.set_halign(Gtk.Align.START)
                f_label.add_css_class("monospace")
                f_label.add_css_class("caption")
                detail_box.append(f_label)
            if len(files) > 20:
                more = Gtk.Label(label=f"... og {len(files) - 20} mere")
                more.set_halign(Gtk.Align.START)
                more.add_css_class("caption")
                more.add_css_class("dim-label")
                detail_box.append(more)
        else:
            empty = Gtk.Label(label="Ingen filer i denne range")
            empty.set_halign(Gtk.Align.START)
            empty.add_css_class("caption")
            empty.add_css_class("dim-label")
            detail_box.append(empty)

        revealer.set_child(detail_box)
        revealer.set_reveal_child(True)

    def _get_files_for_range(self, range_str):
        """Scan INTRO for files/folders matching a numeric range"""
        parts = range_str.split("-")
        min_num = int(parts[0])
        max_num = int(parts[1])
        intro_path = str(INTRO_PATH)
        if not os.path.isdir(intro_path):
            return []
        files = []
        for entry in os.listdir(intro_path):
            match = re.match(r'^(\d{2})_', entry)
            if match:
                num = int(match.group(1))
                if min_num <= num <= max_num:
                    files.append(entry)
        return sorted(files)

    def _build_decisions_section(self):
        """Build the 4 design decisions with pros/cons cards (Pass 2)"""
        section_label = Gtk.Label(label="4 Design Beslutninger")
        section_label.set_halign(Gtk.Align.START)
        section_label.add_css_class("title-3")
        section_label.set_margin_top(24)
        self.append(section_label)

        desc = Gtk.Label(
            label="Bevidste valg der former systemets arkitektur — med afvejning af fordele og ulemper"
        )
        desc.set_halign(Gtk.Align.START)
        desc.add_css_class("caption")
        desc.add_css_class("dim-label")
        desc.set_wrap(True)
        desc.set_wrap_mode(Pango.WrapMode.WORD)
        self.append(desc)

        decisions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        decisions_box.set_margin_top(8)

        for title, chosen, pros, cons in DESIGN_DECISIONS:
            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            card.add_css_class("card")
            card.set_margin_start(4)
            card.set_margin_end(4)

            inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            inner.set_margin_start(16)
            inner.set_margin_end(16)
            inner.set_margin_top(12)
            inner.set_margin_bottom(12)

            # Title row with "Valgt" badge
            title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            t_label = Gtk.Label(label=title)
            t_label.set_halign(Gtk.Align.START)
            t_label.add_css_class("heading")
            t_label.set_hexpand(True)
            title_row.append(t_label)

            badge = Gtk.Label(label="Valgt")
            badge.add_css_class("success")
            badge.add_css_class("caption")
            title_row.append(badge)
            inner.append(title_row)

            # Chosen approach
            c_label = Gtk.Label(label=chosen)
            c_label.set_halign(Gtk.Align.START)
            c_label.add_css_class("caption")
            c_label.add_css_class("dim-label")
            inner.append(c_label)

            # Pros and cons in two columns
            columns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
            columns.set_margin_top(4)

            # Pros column
            pros_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            pros_box.set_hexpand(True)
            pros_header = Gtk.Label(label="Fordele")
            pros_header.set_halign(Gtk.Align.START)
            pros_header.add_css_class("caption")
            pros_header.add_css_class("success")
            pros_box.append(pros_header)
            for pro in pros:
                p = Gtk.Label(label=f"+ {pro}")
                p.set_halign(Gtk.Align.START)
                p.add_css_class("caption")
                p.set_wrap(True)
                p.set_wrap_mode(Pango.WrapMode.WORD)
                pros_box.append(p)
            columns.append(pros_box)

            # Cons column
            cons_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            cons_box.set_hexpand(True)
            cons_header = Gtk.Label(label="Ulemper")
            cons_header.set_halign(Gtk.Align.START)
            cons_header.add_css_class("caption")
            cons_header.add_css_class("error")
            cons_box.append(cons_header)
            for con in cons:
                c = Gtk.Label(label=f"- {con}")
                c.set_halign(Gtk.Align.START)
                c.add_css_class("caption")
                c.add_css_class("dim-label")
                c.set_wrap(True)
                c.set_wrap_mode(Pango.WrapMode.WORD)
                cons_box.append(c)
            columns.append(cons_box)

            inner.append(columns)
            card.append(inner)
            decisions_box.append(card)

        self.append(decisions_box)

    def _build_scaling_section(self):
        """Build the scaling overview with horizontal + vertical + strategies (Pass 2)"""
        section_label = Gtk.Label(label="Skalerings Oversigt")
        section_label.set_halign(Gtk.Align.START)
        section_label.add_css_class("title-3")
        section_label.set_margin_top(24)
        self.append(section_label)

        # --- Horizontal scaling: timeline ---
        h_label = Gtk.Label(label="Horisontal Skalering (mere content)")
        h_label.set_halign(Gtk.Align.START)
        h_label.add_css_class("heading")
        h_label.set_margin_top(8)
        self.append(h_label)

        timeline = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        timeline.set_halign(Gtk.Align.FILL)
        timeline.set_margin_start(4)
        timeline.set_margin_end(4)

        max_files = SCALING_MILESTONES[-1][2]
        for i, (period, desc, count) in enumerate(SCALING_MILESTONES):
            milestone = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            milestone.set_hexpand(True)

            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            card.add_css_class("card")

            card_inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            card_inner.set_margin_start(8)
            card_inner.set_margin_end(8)
            card_inner.set_margin_top(8)
            card_inner.set_margin_bottom(8)

            p_label = Gtk.Label(label=period)
            p_label.add_css_class("heading")
            p_label.set_halign(Gtk.Align.CENTER)
            card_inner.append(p_label)

            # Progress bar
            bar = Gtk.ProgressBar()
            bar.set_fraction(count / max_files)
            card_inner.append(bar)

            d_label = Gtk.Label(label=desc)
            d_label.add_css_class("caption")
            d_label.add_css_class("dim-label")
            d_label.set_halign(Gtk.Align.CENTER)
            d_label.set_wrap(True)
            d_label.set_wrap_mode(Pango.WrapMode.WORD)
            card_inner.append(d_label)

            card.append(card_inner)
            milestone.append(card)

            # Arrow between milestones
            if i < len(SCALING_MILESTONES) - 1:
                arrow = Gtk.Label(label="->")
                arrow.add_css_class("dim-label")
                arrow.set_halign(Gtk.Align.CENTER)
                arrow.set_valign(Gtk.Align.CENTER)
                milestone.append(arrow)

            timeline.append(milestone)

        self.append(timeline)

        # --- Vertical scaling: depth ---
        v_label = Gtk.Label(label="Vertikal Skalering (dybere hierarki)")
        v_label.set_halign(Gtk.Align.START)
        v_label.add_css_class("heading")
        v_label.set_margin_top(16)
        self.append(v_label)

        depth_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        depth_card.add_css_class("card")
        depth_card.set_margin_start(4)
        depth_card.set_margin_end(4)

        depth_inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        depth_inner.set_margin_start(16)
        depth_inner.set_margin_end(16)
        depth_inner.set_margin_top(12)
        depth_inner.set_margin_bottom(12)

        max_label = Gtk.Label(label="Max dybde: 3 niveauer")
        max_label.set_halign(Gtk.Align.START)
        max_label.add_css_class("heading")
        depth_inner.append(max_label)

        levels = [
            ("Niveau 1", "XX_SEKTION/", "#a855f7", 0),
            ("Niveau 2", "XXA_UNDERSEKTION/", "#f59e0b", 24),
            ("Niveau 3", "XXA1_DYB_FIL.md", "#00FF88", 48),
        ]
        for level_name, example, _color, indent in levels:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            row.set_margin_start(indent)
            n = Gtk.Label(label=level_name)
            n.add_css_class("caption")
            n.set_size_request(80, -1)
            row.append(n)
            e = Gtk.Label(label=example)
            e.add_css_class("monospace")
            e.add_css_class("caption")
            row.append(e)
            depth_inner.append(row)

        depth_card.append(depth_inner)
        self.append(depth_card)

        # --- Strategies for 1000+ files ---
        s_label = Gtk.Label(label="Optimerings-strategier for 1000+ filer")
        s_label.set_halign(Gtk.Align.START)
        s_label.add_css_class("heading")
        s_label.set_margin_top(16)
        self.append(s_label)

        strat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        strat_box.set_margin_start(4)
        strat_box.set_margin_end(4)

        for strategy in SCALING_STRATEGIES:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            row.add_css_class("card")

            row_inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            row_inner.set_margin_start(12)
            row_inner.set_margin_end(12)
            row_inner.set_margin_top(8)
            row_inner.set_margin_bottom(8)

            bullet = Gtk.Label(label="*")
            bullet.add_css_class("success")
            row_inner.append(bullet)

            text = Gtk.Label(label=strategy)
            text.set_halign(Gtk.Align.START)
            text.set_hexpand(True)
            text.set_wrap(True)
            text.set_wrap_mode(Pango.WrapMode.WORD)
            row_inner.append(text)

            row.append(row_inner)
            strat_box.append(row)

        self.append(strat_box)

    def _build_anatomy_section(self):
        """Build the folder structure anatomy view (Pass 2)"""
        section_label = Gtk.Label(label="Mappestruktur Anatomi")
        section_label.set_halign(Gtk.Align.START)
        section_label.add_css_class("title-3")
        section_label.set_margin_top(24)
        self.append(section_label)

        # --- Content folder anatomy ---
        content_label = Gtk.Label(label="Content Mappe (fuld anatomi)")
        content_label.set_halign(Gtk.Align.START)
        content_label.add_css_class("heading")
        content_label.set_margin_top(8)
        self.append(content_label)

        anatomy_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        anatomy_box.set_margin_start(4)
        anatomy_box.set_margin_end(4)

        for filename, role, description, _color in FOLDER_ANATOMY:
            card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            card.add_css_class("card")

            inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            inner.set_margin_start(12)
            inner.set_margin_end(12)
            inner.set_margin_top(8)
            inner.set_margin_bottom(8)
            inner.set_hexpand(True)

            # Filename (monospace)
            f_label = Gtk.Label(label=filename)
            f_label.add_css_class("monospace")
            f_label.add_css_class("caption")
            f_label.set_size_request(260, -1)
            f_label.set_halign(Gtk.Align.START)
            inner.append(f_label)

            # Role
            r_label = Gtk.Label(label=role)
            r_label.add_css_class("heading")
            r_label.set_size_request(100, -1)
            r_label.set_halign(Gtk.Align.START)
            inner.append(r_label)

            # Description
            d_label = Gtk.Label(label=description)
            d_label.add_css_class("caption")
            d_label.add_css_class("dim-label")
            d_label.set_hexpand(True)
            d_label.set_halign(Gtk.Align.START)
            d_label.set_wrap(True)
            d_label.set_wrap_mode(Pango.WrapMode.WORD)
            inner.append(d_label)

            card.append(inner)
            anatomy_box.append(card)

        self.append(anatomy_box)

        # --- System folders with underscore convention ---
        sys_label = Gtk.Label(label="System Mapper (underscore convention)")
        sys_label.set_halign(Gtk.Align.START)
        sys_label.add_css_class("heading")
        sys_label.set_margin_top(16)
        self.append(sys_label)

        sys_desc = Gtk.Label(
            label="Mapper med underscore prefix (_) er system/meta-data — aldrig primaer content"
        )
        sys_desc.set_halign(Gtk.Align.START)
        sys_desc.add_css_class("caption")
        sys_desc.add_css_class("dim-label")
        sys_desc.set_wrap(True)
        sys_desc.set_wrap_mode(Pango.WrapMode.WORD)
        self.append(sys_desc)

        sys_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        sys_box.set_margin_start(4)
        sys_box.set_margin_end(4)
        sys_box.set_margin_top(4)

        for folder, purpose in SYSTEM_FOLDERS:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            row.add_css_class("card")

            row_inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            row_inner.set_margin_start(12)
            row_inner.set_margin_end(12)
            row_inner.set_margin_top(8)
            row_inner.set_margin_bottom(8)

            f = Gtk.Label(label=folder)
            f.add_css_class("monospace")
            f.add_css_class("caption")
            f.set_size_request(200, -1)
            f.set_halign(Gtk.Align.START)
            row_inner.append(f)

            p = Gtk.Label(label=purpose)
            p.set_halign(Gtk.Align.START)
            p.set_hexpand(True)
            p.add_css_class("dim-label")
            row_inner.append(p)

            row.append(row_inner)
            sys_box.append(row)

        self.append(sys_box)


#
# SYNC DASHBOARD VIEW (DEL 21)
#

class SyncComponentCard(Gtk.Box):
    """A card showing status for one sync component"""

    def __init__(self, sync_status: SyncStatus):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_margin_top(8)
        self.set_margin_bottom(8)
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.sync_status = sync_status

        # Component-specific color (Pass 3)
        comp_color = SYNC_COMPONENT_COLORS.get(sync_status.component_id, "#9ca3af")

        # Card frame with color bar
        frame = Gtk.Frame()
        outer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # Color bar (left side — component identity)
        color_bar = Gtk.Box()
        color_bar.set_size_request(5, -1)
        css_bar = Gtk.CssProvider()
        css_bar.load_from_string(f"box {{ background-color: {comp_color}; border-radius: 3px 0 0 3px; }}")
        color_bar.get_style_context().add_provider(css_bar, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        outer_box.append(color_bar)

        frame_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        frame_box.set_margin_top(12)
        frame_box.set_margin_bottom(12)
        frame_box.set_margin_start(12)
        frame_box.set_margin_end(12)

        # Header row: icon + name + status badge
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        # Find icon from SYNC_COMPONENTS
        icon_name = "emblem-system-symbolic"
        for cid, _name, _desc, ico, _pri in SYNC_COMPONENTS:
            if cid == sync_status.component_id:
                icon_name = ico
                break
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(24)
        icon_css = Gtk.CssProvider()
        icon_css.load_from_string(f"image {{ color: {comp_color}; }}")
        icon.get_style_context().add_provider(icon_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        header.append(icon)

        # Component name
        name_label = Gtk.Label(label=f"{sync_status.component_id}: {sync_status.name}")
        name_label.set_xalign(0)
        name_label.set_hexpand(True)
        name_label.add_css_class("heading")
        header.append(name_label)

        # Status badge
        status_map = {
            "ok": ("", "#10b981"),
            "warning": ("", "#f59e0b"),
            "error": ("", "#ef4444"),
            "unknown": ("", "#9ca3af"),
        }
        badge_text, badge_color = status_map.get(sync_status.status, ("?", "#9ca3af"))
        badge = Gtk.Label(label=badge_text)
        header.append(badge)

        frame_box.append(header)

        # Priority tag
        pri_label = Gtk.Label(label=f"Priority: {sync_status.priority}")
        pri_label.set_xalign(0)
        pri_label.add_css_class("dim-label")
        frame_box.append(pri_label)

        # Detail text
        detail_label = Gtk.Label(label=sync_status.detail)
        detail_label.set_xalign(0)
        detail_label.set_wrap(True)
        frame_box.append(detail_label)

        # Progress bar (if counts available)
        if sync_status.count_total > 0:
            bar = Gtk.ProgressBar()
            fraction = sync_status.count_ok / sync_status.count_total
            bar.set_fraction(fraction)
            bar.set_text(f"{sync_status.count_ok}/{sync_status.count_total}")
            bar.set_show_text(True)
            bar.set_margin_top(4)
            frame_box.append(bar)

        frame_box.set_hexpand(True)
        outer_box.append(frame_box)
        frame.set_child(outer_box)
        self.append(frame)


class SyncDashboardView(Gtk.Box):
    """Dashboard showing all 6 sync components from DEL 21"""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self._build_ui()

    def _build_ui(self):
        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        header_box.set_margin_bottom(8)

        title = Gtk.Label(label="Sync Functions (DEL 21)")
        title.add_css_class("title-1")
        title.set_xalign(0)
        title.set_hexpand(True)
        header_box.append(title)

        # Overall health
        health = get_sync_health()
        self.health_label = Gtk.Label(label=f"Sync Health: {health:.0f}%")
        self.health_label.add_css_class("title-2")
        if health >= 60:
            pass  # Green implied
        elif health >= 30:
            self.health_label.add_css_class("warning")
        header_box.append(self.health_label)

        self.append(header_box)

        # Overall progress bar
        self.health_bar = Gtk.ProgressBar()
        self.health_bar.set_fraction(health / 100)
        self.health_bar.set_text(f"{health:.0f}%")
        self.health_bar.set_show_text(True)
        self.health_bar.set_margin_bottom(12)
        self.append(self.health_bar)

        # Sync component cards in a FlowBox (2 per row)
        self.cards_box = Gtk.FlowBox()
        self.cards_box.set_max_children_per_line(2)
        self.cards_box.set_min_children_per_line(1)
        self.cards_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.cards_box.set_homogeneous(True)

        self._populate_cards()
        self.append(self.cards_box)

        # Action buttons section
        actions_label = Gtk.Label(label="Quick Actions")
        actions_label.add_css_class("title-3")
        actions_label.set_xalign(0)
        actions_label.set_margin_top(16)
        self.append(actions_label)

        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        actions_box.set_margin_top(8)

        # Git Pull button
        pull_btn = Gtk.Button(label="Git Pull")
        pull_btn.set_icon_name("network-receive-symbolic")
        pull_btn.connect("clicked", self._on_git_pull)
        pull_btn.add_css_class("suggested-action")
        actions_box.append(pull_btn)

        # Check Links button
        links_btn = Gtk.Button(label="Check Links")
        links_btn.set_icon_name("emblem-shared-symbolic")
        links_btn.connect("clicked", self._on_check_links)
        actions_box.append(links_btn)

        # Refresh button with animated indicator
        self._refresh_btn = Gtk.Button(label="Scan Again")
        self._refresh_btn.set_icon_name("view-refresh-symbolic")
        self._refresh_btn.connect("clicked", self._on_refresh_animated)
        actions_box.append(self._refresh_btn)

        # --- Pass 1 deferred: Git Push + Full Sync ---
        push_btn = Gtk.Button(label="Git Push")
        push_btn.set_icon_name("network-transmit-symbolic")
        push_btn.connect("clicked", self._on_git_push)
        actions_box.append(push_btn)

        full_sync_btn = Gtk.Button(label="Full Sync")
        full_sync_btn.set_icon_name("emblem-synchronizing-symbolic")
        full_sync_btn.add_css_class("suggested-action")
        full_sync_btn.connect("clicked", self._on_full_sync)
        actions_box.append(full_sync_btn)

        self.append(actions_box)

        # --- Pass 2: Last synced timestamp ---
        self._last_synced = None
        self.timestamp_label = Gtk.Label(label="Last synced: aldrig")
        self.timestamp_label.set_xalign(0)
        self.timestamp_label.add_css_class("caption")
        self.timestamp_label.add_css_class("dim-label")
        self.timestamp_label.set_margin_top(4)
        self.append(self.timestamp_label)

        # Output log area
        self.log_label = Gtk.Label(label="")
        self.log_label.set_xalign(0)
        self.log_label.set_wrap(True)
        self.log_label.set_margin_top(8)
        self.log_label.set_selectable(True)
        self.append(self.log_label)

        # --- Pass 1 deferred: Session Checkliste (DEL 21) ---
        self._build_session_checkliste()

        # --- Pass 2: Sync Historik ---
        self._build_sync_history()

        # --- Pass 2: Broken Link Fixer ---
        self._build_broken_links()

        # --- Pass 3: Background sync timer (every 5 minutes) ---
        self._prev_health = None  # Track for change-only notifications
        GLib.timeout_add_seconds(300, self._background_sync)

        # --- Pass 2: Auto-sync on start ---
        GLib.idle_add(self._auto_sync_start)

    def _build_session_checkliste(self):
        """Build DEL 21 session checkliste (Pass 1 deferred)"""
        check_label = Gtk.Label(label="Session Sync Checkliste (DEL 21)")
        check_label.add_css_class("title-3")
        check_label.set_xalign(0)
        check_label.set_margin_top(16)
        self.append(check_label)

        checklist_items = [
            "Git pull ved session start",
            "Check AENDRINGSLOG coverage",
            "Verificer VERSION.md",
            "Scan krydsreferencer",
            "Opdater STATUS.md",
            "Git push ved session slut",
        ]
        checklist_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        checklist_box.set_margin_top(4)

        for item in checklist_items:
            row = Gtk.CheckButton(label=item)
            row.add_css_class("caption")
            checklist_box.append(row)

        self.append(checklist_box)

    def _build_sync_history(self):
        """Build sync history log section (Pass 2)"""
        hist_label = Gtk.Label(label="Sync Historik")
        hist_label.add_css_class("title-3")
        hist_label.set_xalign(0)
        hist_label.set_margin_top(16)
        self.append(hist_label)

        self.history_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.history_box.set_margin_top(4)
        self._sync_history = []

        empty = Gtk.Label(label="Ingen sync-operationer endnu")
        empty.add_css_class("caption")
        empty.add_css_class("dim-label")
        empty.set_xalign(0)
        self.history_box.append(empty)
        self.append(self.history_box)

        # View Git Log button
        log_btn = Gtk.Button(label="View Git Log")
        log_btn.set_icon_name("document-open-recent-symbolic")
        log_btn.add_css_class("pill")
        log_btn.add_css_class("caption")
        log_btn.set_margin_top(4)
        log_btn.set_halign(Gtk.Align.START)
        log_btn.connect("clicked", self._on_view_git_log)
        self.append(log_btn)

    def _build_broken_links(self):
        """Build broken link fixer section (Pass 2 FASE 2)"""
        bl_header = Gtk.Label(label="Broken Link Fixer")
        bl_header.add_css_class("title-3")
        bl_header.set_xalign(0)
        bl_header.set_margin_top(16)
        self.append(bl_header)

        self.broken_links_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.broken_links_box.set_margin_top(4)

        # Scan button
        scan_btn = Gtk.Button(label="Scan Broken Links")
        scan_btn.set_icon_name("edit-find-symbolic")
        scan_btn.add_css_class("pill")
        scan_btn.add_css_class("caption")
        scan_btn.set_halign(Gtk.Align.START)
        scan_btn.connect("clicked", self._on_scan_broken_links)
        self.append(scan_btn)

        empty = Gtk.Label(label="Klik 'Scan Broken Links' for at finde problemer")
        empty.add_css_class("caption")
        empty.add_css_class("dim-label")
        empty.set_xalign(0)
        self.broken_links_box.append(empty)
        self.append(self.broken_links_box)

    def _on_scan_broken_links(self, button):
        """Scan and display broken links with fix suggestions"""
        # Clear existing
        child = self.broken_links_box.get_first_child()
        while child:
            next_c = child.get_next_sibling()
            self.broken_links_box.remove(child)
            child = next_c

        broken = _get_broken_links_detail(INTRO_PATH)
        if not broken:
            ok_label = Gtk.Label(label="Ingen broken links fundet!")
            ok_label.add_css_class("caption")
            ok_label.set_xalign(0)
            ok_css = Gtk.CssProvider()
            ok_css.load_from_string("label { color: #10b981; }")
            ok_label.get_style_context().add_provider(ok_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            self.broken_links_box.append(ok_label)
            self._add_history_entry("Link Scan", "0 broken")
            return

        count_label = Gtk.Label(label=f"{len(broken)} broken links fundet:")
        count_label.add_css_class("caption")
        count_label.set_xalign(0)
        err_css = Gtk.CssProvider()
        err_css.load_from_string("label { color: #ef4444; }")
        count_label.get_style_context().add_provider(err_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.broken_links_box.append(count_label)

        for source, text, href, suggestion in broken[:15]:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            row.set_margin_start(8)

            # Source and broken path
            info = Gtk.Label(label=f"{source}: [{text}]({href})")
            info.set_xalign(0)
            info.set_hexpand(True)
            info.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
            info.add_css_class("caption")
            row.append(info)

            # Suggestion badge
            if suggestion:
                fix_label = Gtk.Label(label=f"-> {suggestion}")
                fix_label.add_css_class("caption")
                fix_css = Gtk.CssProvider()
                fix_css.load_from_string("label { color: #f59e0b; font-style: italic; }")
                fix_label.get_style_context().add_provider(fix_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
                row.append(fix_label)
            else:
                no_fix = Gtk.Label(label="[ingen forslag]")
                no_fix.add_css_class("caption")
                no_fix.add_css_class("dim-label")
                row.append(no_fix)

            self.broken_links_box.append(row)

        if len(broken) > 15:
            more = Gtk.Label(label=f"... og {len(broken) - 15} mere")
            more.add_css_class("caption")
            more.add_css_class("dim-label")
            more.set_xalign(0)
            self.broken_links_box.append(more)

        self._add_history_entry("Link Scan", f"{len(broken)} broken")

    def _add_history_entry(self, action, result):
        """Add an entry to sync history"""
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] {action}: {result}"
        self._sync_history.insert(0, entry)
        if len(self._sync_history) > 20:
            self._sync_history = self._sync_history[:20]

        # Rebuild history box
        child = self.history_box.get_first_child()
        while child:
            next_c = child.get_next_sibling()
            self.history_box.remove(child)
            child = next_c

        for e in self._sync_history[:10]:
            lbl = Gtk.Label(label=e)
            lbl.set_xalign(0)
            lbl.add_css_class("monospace")
            lbl.add_css_class("caption")
            lbl.set_ellipsize(Pango.EllipsizeMode.END)
            self.history_box.append(lbl)

    def _on_git_push(self, button):
        """Git push with commit message (Pass 1 deferred)"""
        try:
            # Check if there are changes to commit
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(INTRO_PATH), capture_output=True, text=True, timeout=10
            )
            if status.stdout.strip():
                # Auto-commit with timestamp
                from datetime import datetime
                msg = f"Auto-sync {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                subprocess.run(
                    ["git", "add", "-A"],
                    cwd=str(INTRO_PATH), capture_output=True, timeout=10
                )
                subprocess.run(
                    ["git", "commit", "-m", msg],
                    cwd=str(INTRO_PATH), capture_output=True, timeout=10
                )

            result = subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=str(INTRO_PATH), capture_output=True, text=True, timeout=30
            )
            output = result.stdout.strip() or result.stderr.strip() or "Push complete"
            self.log_label.set_label(f"Git Push:\n{output}")
            self._add_history_entry("Git Push", output[:80])
            self._update_timestamp()
            self._on_refresh(button)
        except Exception as e:
            self.log_label.set_label(f"Git Push Error: {str(e)}")
            self._add_history_entry("Git Push", f"ERROR: {str(e)[:60]}")

    def _on_full_sync(self, button):
        """Run complete sync sequence (Pass 1 deferred)"""
        self.log_label.set_label("Running full sync...")
        steps = []

        # Step 1: Git Pull
        try:
            r = subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=str(INTRO_PATH), capture_output=True, text=True, timeout=30
            )
            steps.append(f"Pull: {r.stdout.strip() or 'OK'}")
        except Exception as e:
            steps.append(f"Pull: ERROR {e}")

        # Step 2: Check links
        link_status = _sync_cross_references(INTRO_PATH)
        steps.append(f"Links: {link_status.detail}")

        # Step 3: Refresh status
        self._populate_cards()
        health = get_sync_health()
        self.health_label.set_label(f"Sync Health: {health:.0f}%")
        self.health_bar.set_fraction(health / 100)
        steps.append(f"Health: {health:.0f}%")

        output = "\n".join(steps)
        self.log_label.set_label(f"Full Sync Complete:\n{output}")
        self._add_history_entry("Full Sync", f"Health {health:.0f}%")
        self._update_timestamp()

    def _auto_sync_start(self):
        """Auto-sync at app start (Pass 2)"""
        try:
            result = subprocess.run(
                ["git", "pull", "--rebase", "origin", "main"],
                cwd=str(INTRO_PATH), capture_output=True, text=True, timeout=15
            )
            output = result.stdout.strip() if result.stdout else "OK"
            if "Already up to date" not in output:
                # Remote had changes — pulse animation (Pass 3)
                self._pulse_health_label()
                self._add_history_entry("Auto Pull (start)", f"Nye aendringer: {output[:60]}")
            else:
                self._add_history_entry("Auto Pull (start)", "Already up to date")
            self._update_timestamp()
            self._on_refresh(None)
        except Exception:
            pass
        return False  # Run once

    def _pulse_health_label(self):
        """Pulse animation on health label when remote changes detected (Pass 3)"""
        pulse_css = Gtk.CssProvider()
        pulse_css.load_from_string(
            "label { color: #00D9FF; font-weight: bold; }"
        )
        self.health_label.get_style_context().add_provider(
            pulse_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        # Remove pulse after 3 seconds
        GLib.timeout_add_seconds(3, self._remove_pulse, pulse_css)

    def _remove_pulse(self, pulse_css):
        """Remove pulse animation"""
        self.health_label.get_style_context().remove_provider(pulse_css)
        return False

    def _background_sync(self):
        """Background sync every 5 minutes (Pass 3) — only notify on changes"""
        try:
            self._populate_cards()
            health = get_sync_health()
            self.health_label.set_label(f"Sync Health: {health:.0f}%")
            self.health_bar.set_fraction(health / 100)
            self._update_timestamp()
            # Only log if health changed (not spam)
            if self._prev_health is not None and abs(health - self._prev_health) >= 1:
                self._add_history_entry("Background Sync",
                    f"Health {self._prev_health:.0f}% -> {health:.0f}%")
            self._prev_health = health
        except Exception:
            pass
        return True  # Keep running

    def _update_timestamp(self):
        """Update the last synced timestamp"""
        from datetime import datetime
        self._last_synced = datetime.now()
        self.timestamp_label.set_label(
            f"Last synced: {self._last_synced.strftime('%H:%M:%S')}"
        )

    def _on_view_git_log(self, button):
        """Show recent git commits (Pass 2)"""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                cwd=str(INTRO_PATH), capture_output=True, text=True, timeout=10
            )
            self.log_label.set_label(f"Git Log (last 10):\n{result.stdout.strip()}")
        except Exception as e:
            self.log_label.set_label(f"Git Log Error: {str(e)}")

    def _populate_cards(self):
        # Clear existing
        child = self.cards_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.cards_box.remove(child)
            child = next_child

        statuses = get_sync_status()
        for s in statuses:
            card = SyncComponentCard(s)
            self.cards_box.append(card)

    def _on_git_pull(self, button):
        """Run git pull in MASTER FOLDERS"""
        try:
            result = subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=str(INTRO_PATH), capture_output=True, text=True, timeout=30
            )
            output = result.stdout.strip() or result.stderr.strip()
            self.log_label.set_label(f"Git Pull:\n{output}")
            self._on_refresh(button)
        except Exception as e:
            self.log_label.set_label(f"Git Pull Error: {str(e)}")

    def _on_check_links(self, button):
        """Scan for broken cross-references"""
        status = _sync_cross_references(INTRO_PATH)
        self.log_label.set_label(f"Link Check: {status.detail}")
        self._on_refresh(button)

    def _on_refresh_animated(self, button):
        """Refresh with spinning indicator animation (Pass 3)"""
        # Add spinning CSS to button
        spin_css = Gtk.CssProvider()
        spin_css.load_from_string("button { opacity: 0.6; }")
        button.get_style_context().add_provider(spin_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        button.set_label("Scanning...")
        button.set_sensitive(False)
        # Defer actual work so UI updates
        GLib.idle_add(self._do_refresh_animated, button, spin_css)

    def _do_refresh_animated(self, button, spin_css):
        """Perform refresh and restore button"""
        self._on_refresh(button)
        button.get_style_context().remove_provider(spin_css)
        button.set_label("Scan Again")
        button.set_sensitive(True)
        return False

    def _on_refresh(self, button):
        """Refresh all sync status"""
        self._populate_cards()
        health = get_sync_health()
        self.health_label.set_label(f"Sync Health: {health:.0f}%")
        self.health_bar.set_fraction(health / 100)
        self.health_bar.set_text(f"{health:.0f}%")


#
# INTRO SYSTEM VIEW — FASE 1 SIDEBAR INTEGRATION
#

# I-file color mapping (chakra-aligned, FASE 2 spec)
INTRO_I_FILE_COLORS = {
    1: "#a855f7",   # I1 Vision — Divine violet
    2: "#ef4444",   # I2 Orders — Error red
    3: "#10b981",   # I3 Hybrids — Heart emerald
    4: "#f59e0b",   # I4 Operations — Wisdom gold
    5: "#f59e0b",   # I5 Operations — Wisdom gold
    6: "#6366f1",   # I6 Technical — Intuition indigo
    7: "#6366f1",   # I7 Technical — Intuition indigo
    8: "#6366f1",   # I8 Technical — Intuition indigo
    9: "#6366f1",   # I9 Technical — Intuition indigo
    10: "#00FF88",  # I10 Ecosystem — Success green
    11: "#f97316",  # I11 Prevention — Warning orange
    12: "#ff9f43",  # I12 Sejrliste — Primary orange
}

# I-file category name mapping for CSS classes
INTRO_I_FILE_CATEGORY_NAMES = {
    1: "vision",       # I1 — Divine violet
    2: "orders",       # I2 — Error red
    3: "hybrids",      # I3 — Heart emerald
    4: "operations",   # I4 — Wisdom gold
    5: "operations",   # I5 — Wisdom gold
    6: "technical",    # I6 — Intuition indigo
    7: "technical",    # I7 — Intuition indigo
    8: "technical",    # I8 — Intuition indigo
    9: "technical",    # I9 — Intuition indigo
    10: "ecosystem",   # I10 — Success green
    11: "prevention",  # I11 — Warning orange
    12: "sejrliste",   # I12 — Primary orange
}

# Sidebar item definitions for INTRO categories
INTRO_SIDEBAR_ITEMS = [
    ("I", "I-Files (System Intelligence)", "I1-I12", "accessories-text-editor-symbolic"),
    ("B", "Terminal Commands", "B1-B10", "utilities-terminal-symbolic"),
    ("C", "Environment Config", "C2-C10", "preferences-system-symbolic"),
    ("D", "Architecture", "D1-D10", "view-grid-symbolic"),
    ("structure", "Folder Structure", "Governance + Rules", "folder-symbolic"),
    ("system_functions", "System Functions", "Scripts + Automation", "system-run-symbolic"),
    ("dna_layers", "7-DNA Layers", "INTRO DNA Analysis", "applications-science-symbolic"),
    ("quick_actions", "Quick Actions", "Commands + Environment", "utilities-terminal-symbolic"),
    ("health", "System Health", "Live verification", "emblem-ok-symbolic"),
]


class IntroIFilesView(Gtk.Box):
    """FASE 2: Full detail view for I1-I12 System Intelligence files.

    Displays all I-files with:
    - I-number + title (from file header via intro_integration)
    - Status badge ([OK] or [PENDING])
    - Size + line count
    - Last modified date
    - Click to open file in editor
    - Category colors per I-file (vision, orders, hybrids, etc.)
    - "Open in Files" button for each file
    """

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # Main scrollable area
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)

        self._container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        self._container.set_margin_start(40)
        self._container.set_margin_end(40)
        self._container.set_margin_top(32)
        self._container.set_margin_bottom(40)

        scroll.set_child(self._container)
        self.append(scroll)

        self._build()

    def _build(self):
        """Build the complete I-files detail view."""
        # Header: "System Intelligence -- I1-I12"
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        title = Gtk.Label(label="System Intelligence \u2014 I1-I12")
        title.add_css_class("intro-view-header")
        title.set_xalign(0)
        header_box.append(title)

        subtitle = Gtk.Label(
            label="Core system intelligence files: vision, orders, briefings, environments, compliance, and more"
        )
        subtitle.add_css_class("intro-view-subtitle")
        subtitle.set_xalign(0)
        subtitle.set_wrap(True)
        header_box.append(subtitle)
        self._container.append(header_box)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(4)
        sep.set_margin_bottom(4)
        self._container.append(sep)

        # Load I-files from real filesystem
        i_files = intro_integration.get_intro_i_files()

        if not i_files:
            empty = Adw.StatusPage()
            empty.set_title("No I-Files Found")
            empty.set_description(f"Could not find I-files in {intro_integration.INTRO_PATH}")
            empty.set_icon_name("dialog-warning-symbolic")
            self._container.append(empty)
            return

        # Summary bar
        total_lines = sum(f.lines for f in i_files)
        total_size = sum(f.size for f in i_files)
        size_kb = total_size / 1024
        complete_count = sum(
            1 for f in i_files
            if f.status in ("COMPLETE", "VERIFIED", "ALL_WORKING", "OPERATIONAL", "ESTABLISHED", "STABLE")
        )
        summary_text = (
            f"{len(i_files)} files  |  {total_lines:,} lines  |  {size_kb:.0f} KB total  |  "
            f"{complete_count} OK / {len(i_files) - complete_count} pending"
        )
        summary = Gtk.Label(label=summary_text)
        summary.add_css_class("caption")
        summary.add_css_class("dim-label")
        summary.set_xalign(0)
        self._container.append(summary)

        # File rows
        files_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        for ifile in i_files:
            row = self._build_i_file_row(ifile)
            files_box.append(row)

        self._container.append(files_box)

    def _build_i_file_row(self, ifile):
        """Build a single I-file row with category color, status badge, meta, and buttons."""
        num = ifile.category_number or 0
        color = INTRO_I_FILE_COLORS.get(num, "#a855f7")
        cat_name = INTRO_I_FILE_CATEGORY_NAMES.get(num, "vision")
        i_title = intro_integration.get_i_file_title(num)
        i_desc = intro_integration.get_i_file_description(num)

        # Row container with category color CSS class
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.add_css_class("intro-file-row")
        row.add_css_class(f"intro-i-row-{cat_name}")

        # I-number with color (Pango markup for foreground)
        number_label = Gtk.Label(label=f"I{num}")
        number_label.add_css_class("intro-file-number")
        number_label.set_markup(f'<span foreground="{color}" weight="ultrabold">I{num}</span>')
        number_label.set_valign(Gtk.Align.CENTER)
        row.append(number_label)

        # Title, description, and meta info
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_box.set_hexpand(True)

        title = Gtk.Label(label=i_title)
        title.add_css_class("intro-file-title")
        title.set_xalign(0)
        title.set_ellipsize(Pango.EllipsizeMode.END)
        info_box.append(title)

        # Description line
        if i_desc:
            desc = Gtk.Label(label=i_desc)
            desc.add_css_class("intro-file-meta")
            desc.set_xalign(0)
            desc.set_ellipsize(Pango.EllipsizeMode.END)
            info_box.append(desc)

        # Meta: size + lines + date
        mod_date = ifile.last_modified[:10] if ifile.last_modified else "?"
        meta_text = f"{ifile.size_human}  |  {ifile.lines:,} lines  |  {mod_date}"
        meta = Gtk.Label(label=meta_text)
        meta.add_css_class("intro-file-meta")
        meta.set_xalign(0)
        info_box.append(meta)

        row.append(info_box)

        # Status badge: [OK] or [PENDING]
        is_ok = ifile.status in ("COMPLETE", "VERIFIED", "ALL_WORKING", "OPERATIONAL", "ESTABLISHED", "STABLE")
        badge_text = "[OK]" if is_ok else "[PENDING]"
        status_label = Gtk.Label(label=badge_text)
        status_label.add_css_class("intro-status-badge")
        if is_ok:
            status_label.add_css_class("intro-i-status-ok")
        else:
            status_label.add_css_class("intro-i-status-pending")
        status_label.set_valign(Gtk.Align.CENTER)
        status_label.set_tooltip_text(f"Status: {ifile.status}")
        row.append(status_label)

        # Buttons box
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        btn_box.set_valign(Gtk.Align.CENTER)

        # "Open" button (opens in default text editor)
        open_btn = Gtk.Button(label="Open")
        open_btn.add_css_class("intro-open-btn")
        file_path = str(ifile.path)
        open_btn.connect("clicked", lambda b, p=file_path: self._open_file(p))
        open_btn.set_tooltip_text("Open in default text editor")
        btn_box.append(open_btn)

        # "Open in Files" button (opens containing folder in file manager)
        files_btn = Gtk.Button(label="Files")
        files_btn.add_css_class("intro-i-open-files-btn")
        folder_path = str(ifile.path.parent)
        files_btn.connect("clicked", lambda b, p=folder_path: self._open_folder(p))
        files_btn.set_tooltip_text("Open in Files (file manager)")
        btn_box.append(files_btn)

        row.append(btn_box)

        return row

    def _open_file(self, path: str):
        """Open a file in the default system editor."""
        try:
            subprocess.Popen(["xdg-open", path])
        except Exception as e:
            print(f"Could not open file: {e}")

    def _open_folder(self, path: str):
        """Open a folder in the system file manager."""
        try:
            subprocess.Popen(["xdg-open", path])
        except Exception as e:
            print(f"Could not open folder: {e}")


class IntroStructureView(Gtk.Box):
    """FASE 3: Full detail view for INTRO folder structure.

    Displays:
    - Tree-like view of MASTER FOLDERS(INTRO)/ directory layout
    - File counts per directory (live from filesystem)
    - Naming conventions reference (I/B/C/D/E/F/G/H categories)
    - BOGFORINGSMAPPE A-F category overview from 00_HOVEDINDEKS.md
    - 5 governance rules from FOLDER_STRUCTURE_AND_RULES.md as styled cards
    """

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # Main scrollable area
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)

        self._container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        self._container.set_margin_start(40)
        self._container.set_margin_end(40)
        self._container.set_margin_top(32)
        self._container.set_margin_bottom(40)

        scroll.set_child(self._container)
        self.append(scroll)

        self._build()

    def _build(self):
        """Build the complete folder structure view."""
        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        title = Gtk.Label(label="Folder Structure & Governance")
        title.add_css_class("intro-view-header")
        title.set_xalign(0)
        header_box.append(title)

        subtitle = Gtk.Label(
            label="MASTER FOLDERS(INTRO) directory layout, naming conventions, BOGFORINGSMAPPE categories, and governance rules"
        )
        subtitle.add_css_class("intro-view-subtitle")
        subtitle.set_xalign(0)
        subtitle.set_wrap(True)
        header_box.append(subtitle)
        self._container.append(header_box)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(4)
        sep.set_margin_bottom(4)
        self._container.append(sep)

        # --- SECTION 1: TREE VIEW OF FOLDER STRUCTURE ---
        self._build_tree_view()

        # --- SECTION 2: NAMING CONVENTIONS ---
        self._build_naming_conventions()

        # --- SECTION 3: BOGFORINGSMAPPE INTEGRATION ---
        self._build_bogforingsmappe()

        # --- SECTION 4: GOVERNANCE RULES ---
        self._build_governance_rules()

    # -----------------------------------------------------------------
    # SECTION 1: TREE VIEW
    # -----------------------------------------------------------------

    def _build_tree_view(self):
        """Build the tree-like folder structure view with file counts."""
        import pathlib
        intro_path = pathlib.Path("/home/rasmus/Desktop/MASTER FOLDERS(INTRO)")

        tree_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        tree_card.add_css_class("intro-category-card")

        # Section title
        section_title = Gtk.Label()
        section_title.set_markup(
            '<span weight="bold" font_size="large">Directory Tree</span>'
        )
        section_title.set_xalign(0)
        tree_card.append(section_title)

        section_desc = Gtk.Label(
            label="Live filesystem scan of MASTER FOLDERS(INTRO)/"
        )
        section_desc.add_css_class("intro-file-meta")
        section_desc.set_xalign(0)
        section_desc.set_margin_bottom(8)
        tree_card.append(section_desc)

        # Build tree rows
        tree_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)

        # Root level
        root_file_count = 0
        root_dir_count = 0
        subdirs = []
        if intro_path.exists():
            for item in sorted(intro_path.iterdir()):
                if item.name.startswith("."):
                    continue
                if item.is_dir():
                    root_dir_count += 1
                    # Count files in subdirectory
                    sub_count = sum(
                        1 for f in item.iterdir()
                        if f.is_file() and not f.name.startswith(".")
                    )
                    subdirs.append((item.name, sub_count))
                elif item.is_file():
                    root_file_count += 1

        # Root entry
        root_row = self._make_tree_row(
            "MASTER FOLDERS(INTRO)/",
            0,
            f"{root_file_count} root files, {root_dir_count} subdirectories",
            "#a855f7",
            is_root=True,
        )
        tree_box.append(root_row)

        # Subdirectories with indent
        for dirname, file_count in subdirs:
            color = self._get_dir_color(dirname)
            count_text = f"{file_count} files" if file_count != 1 else "1 file"
            if file_count == 0:
                count_text = "empty"
            dir_row = self._make_tree_row(
                f"{dirname}/", 1, count_text, color
            )
            tree_box.append(dir_row)

        tree_card.append(tree_box)

        # Total summary at bottom
        total_files = root_file_count + sum(c for _, c in subdirs)
        total_label = Gtk.Label()
        total_label.set_markup(
            f'<span font_family="JetBrains Mono" foreground="rgba(255,255,255,0.5)" '
            f'font_size="small">Total: {total_files} files across {root_dir_count} subdirectories + root</span>'
        )
        total_label.set_xalign(0)
        total_label.set_margin_top(8)
        tree_card.append(total_label)

        self._container.append(tree_card)

    def _make_tree_row(self, name, indent_level, meta_text, color, is_root=False):
        """Create a single tree row with indent, icon, name, and file count."""
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.set_margin_start(indent_level * 28)
        row.set_margin_top(2)
        row.set_margin_bottom(2)

        # Tree connector character
        if indent_level > 0:
            connector = Gtk.Label()
            connector.set_markup(
                '<span font_family="JetBrains Mono" foreground="rgba(255,255,255,0.20)">+--</span>'
            )
            connector.set_valign(Gtk.Align.CENTER)
            row.append(connector)

        # Folder icon
        icon = Gtk.Image.new_from_icon_name(
            "folder-open-symbolic" if is_root else "folder-symbolic"
        )
        if is_root:
            icon.add_css_class("accent")
        else:
            icon.add_css_class("dim-label")
        icon.set_valign(Gtk.Align.CENTER)
        row.append(icon)

        # Directory name with color
        name_label = Gtk.Label()
        weight = "ultrabold" if is_root else "bold"
        size = "medium" if is_root else "small"
        name_label.set_markup(
            f'<span foreground="{color}" weight="{weight}" '
            f'font_family="JetBrains Mono" font_size="{size}">{GLib.markup_escape_text(name)}</span>'
        )
        name_label.set_xalign(0)
        name_label.set_hexpand(True)
        name_label.set_valign(Gtk.Align.CENTER)
        row.append(name_label)

        # File count badge
        count_label = Gtk.Label(label=meta_text)
        count_label.add_css_class("intro-file-meta")
        count_label.set_valign(Gtk.Align.CENTER)
        row.append(count_label)

        return row

    def _get_dir_color(self, dirname):
        """Return a color for a directory name based on its purpose."""
        color_map = {
            "01_PRODUCTION": "#4ade80",
            "96_ADMIRAL_HYBRID_ORGANIC": "#f59e0b",
            "ADMIRAL FLEET COLLABORATION": "#06b6d4",
            "ARCHIVE": "#6b7280",
            "BOGFØRINGSMAPPE (MED INDHOLDSFORTEGNELSERNE)": "#f472b6",
            "HISTORICAL ARCHIVE": "#9ca3af",
            "LAPTOP KATALOG": "#8b5cf6",
            "OLD PROJEKTS ORIGINAL": "#a78bfa",
            "PROJEKTS ARKITEKTUR(TEMPLATES)": "#3b82f6",
            "PROJEKTS LOKAL ENV": "#22d3ee",
            "PROJEKTS TERMINALS": "#ef4444",
            "STATUS PROJEKTS": "#fbbf24",
        }
        return color_map.get(dirname, "#a855f7")

    # -----------------------------------------------------------------
    # SECTION 2: NAMING CONVENTIONS
    # -----------------------------------------------------------------

    def _build_naming_conventions(self):
        """Build the naming conventions reference card."""
        conv_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        conv_card.add_css_class("intro-category-card")

        section_title = Gtk.Label()
        section_title.set_markup(
            '<span weight="bold" font_size="large">Naming Conventions</span>'
        )
        section_title.set_xalign(0)
        conv_card.append(section_title)

        section_desc = Gtk.Label(
            label="File prefix categories and their number ranges"
        )
        section_desc.add_css_class("intro-file-meta")
        section_desc.set_xalign(0)
        section_desc.set_margin_bottom(8)
        conv_card.append(section_desc)

        # Naming convention entries
        conventions = [
            ("I", "System Intelligence", "I1-I12", "#a855f7",
             "Core system intelligence files: vision, orders, briefings, environments, compliance"),
            ("B", "Terminal Commands", "B1-B10", "#ef4444",
             "Operational terminal commands for all platforms and services"),
            ("C", "Environment Config", "C2-C10", "#22d3ee",
             "Configuration files, .env setups, and environment variables"),
            ("D", "Architecture", "D1-D10", "#3b82f6",
             "System architecture documentation and design patterns"),
            ("E", "Templates", "E1-E4", "#f59e0b",
             "Agent templates and patterns (structure only, NOT agent content)"),
            ("F", "Old Projects", "F1-F10", "#a78bfa",
             "Historical project references and original plans"),
            ("G", "Laptop Catalog", "G0-G4", "#8b5cf6",
             "Desktop organization catalog and complete file index"),
            ("H", "Fleet Collaboration", "H1-H3", "#06b6d4",
             "Multi-Admiral development workflow and collaboration guides"),
        ]

        conv_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        for letter, name, file_range, color, description in conventions:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            row.add_css_class("intro-file-row")

            # Letter prefix with color
            letter_label = Gtk.Label()
            letter_label.set_markup(
                f'<span foreground="{color}" weight="ultrabold" '
                f'font_family="JetBrains Mono" font_size="large">{letter}</span>'
            )
            letter_label.set_valign(Gtk.Align.CENTER)
            letter_label.set_size_request(28, -1)
            row.append(letter_label)

            # Name + description + range
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            info_box.set_hexpand(True)

            name_label = Gtk.Label(label=name)
            name_label.add_css_class("intro-file-title")
            name_label.set_xalign(0)
            info_box.append(name_label)

            desc_label = Gtk.Label(label=description)
            desc_label.add_css_class("intro-file-meta")
            desc_label.set_xalign(0)
            desc_label.set_wrap(True)
            info_box.append(desc_label)

            row.append(info_box)

            # Range badge
            range_label = Gtk.Label(label=file_range)
            range_label.add_css_class("intro-status-badge")
            range_label.add_css_class("intro-status-active")
            range_label.set_valign(Gtk.Align.CENTER)
            row.append(range_label)

            conv_box.append(row)

        conv_card.append(conv_box)
        self._container.append(conv_card)

    # -----------------------------------------------------------------
    # SECTION 3: BOGFORINGSMAPPE INTEGRATION
    # -----------------------------------------------------------------

    def _build_bogforingsmappe(self):
        """Build the BOGFORINGSMAPPE A-F category overview from 00_HOVEDINDEKS.md."""
        bog_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        bog_card.add_css_class("intro-category-card")

        section_title = Gtk.Label()
        section_title.set_markup(
            '<span weight="bold" font_size="large">BOGFORINGSMAPPE Categories</span>'
        )
        section_title.set_xalign(0)
        bog_card.append(section_title)

        section_desc = Gtk.Label(
            label="Category overview from 00_HOVEDINDEKS.md -- the central catalog"
        )
        section_desc.add_css_class("intro-file-meta")
        section_desc.set_xalign(0)
        section_desc.set_margin_bottom(8)
        bog_card.append(section_desc)

        # A-F categories from HOVEDINDEKS
        categories = [
            ("A", "STATUS", "Current State", "10 files", "#4ade80",
             "STATUS PROJEKTS/",
             "System overview, platform status, agents, Docker, databases, integration, monitoring, ports, processes, code metrics"),
            ("B", "COMMANDS", "Operational", "10 files", "#ef4444",
             "PROJEKTS TERMINALS/",
             "Terminal commands for Cirkelline, Cosmic, CKC, Kommandor, Docker, databases, monitoring, backup, deployment, troubleshooting"),
            ("C", "ARCHITECTURE", "Configuration", "10 files", "#22d3ee",
             "PROJEKTS LOKAL ENV/",
             "Environment configs for all platforms, Redis, RabbitMQ, Docker, PostgreSQL, AWS LocalStack, monitoring"),
            ("D", "TEMPLATES", "Design", "10 files", "#3b82f6",
             "PROJEKTS ARKITEKTUR(TEMPLATES)/",
             "System architecture, platform architectures, integration, DB schemas, API patterns, security, deployment"),
            ("E", "INTEGRATION", "Agents", "4 files", "#f59e0b",
             "PROJEKTS ARKITEKTUR(TEMPLATES)/",
             "Agent templates: Kommandor (21), ELLE (26), CKC (5), Cosmic (9) -- 60+ agents documented"),
            ("F", "HISTORY", "Original Plans", "10 files", "#a78bfa",
             "OLD PROJEKTS ORIGINAL/",
             "Historical documentation: original visions, development history, planning, evolution, lessons learned"),
        ]

        cat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        for letter, name, purpose, file_count, color, location, description in categories:
            row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            row.add_css_class("intro-file-row")

            # Top line: Letter + Name + Purpose + File count
            top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

            letter_label = Gtk.Label()
            letter_label.set_markup(
                f'<span foreground="{color}" weight="ultrabold" '
                f'font_family="JetBrains Mono" font_size="large">{letter}</span>'
            )
            letter_label.set_valign(Gtk.Align.CENTER)
            letter_label.set_size_request(24, -1)
            top_row.append(letter_label)

            name_label = Gtk.Label()
            name_label.set_markup(
                f'<span weight="bold" foreground="{color}">{GLib.markup_escape_text(name)}</span>'
                f'  <span foreground="rgba(255,255,255,0.50)" font_size="small">({purpose})</span>'
            )
            name_label.set_xalign(0)
            name_label.set_hexpand(True)
            top_row.append(name_label)

            count_badge = Gtk.Label(label=file_count)
            count_badge.add_css_class("intro-status-badge")
            count_badge.add_css_class("intro-status-complete")
            count_badge.set_valign(Gtk.Align.CENTER)
            top_row.append(count_badge)

            row.append(top_row)

            # Location line
            loc_label = Gtk.Label()
            loc_label.set_markup(
                f'<span font_family="JetBrains Mono" font_size="small" '
                f'foreground="rgba(255,255,255,0.35)">Location: {GLib.markup_escape_text(location)}</span>'
            )
            loc_label.set_xalign(0)
            loc_label.set_margin_start(36)
            row.append(loc_label)

            # Description line
            desc_label = Gtk.Label(label=description)
            desc_label.add_css_class("intro-file-meta")
            desc_label.set_xalign(0)
            desc_label.set_margin_start(36)
            desc_label.set_wrap(True)
            row.append(desc_label)

            cat_box.append(row)

        bog_card.append(cat_box)
        self._container.append(bog_card)

    # -----------------------------------------------------------------
    # SECTION 4: GOVERNANCE RULES
    # -----------------------------------------------------------------

    def _build_governance_rules(self):
        """Build the 5 governance rules from FOLDER_STRUCTURE_AND_RULES.md as styled cards."""
        rules_header = Gtk.Label()
        rules_header.set_markup(
            '<span weight="bold" font_size="large" foreground="#fbbf24">Governance Rules</span>'
        )
        rules_header.set_xalign(0)
        rules_header.set_margin_top(8)
        self._container.append(rules_header)

        rules_desc = Gtk.Label(
            label="From FOLDER_STRUCTURE_AND_RULES.md -- the 5 core rules that keep the system reliable"
        )
        rules_desc.add_css_class("intro-file-meta")
        rules_desc.set_xalign(0)
        rules_desc.set_margin_bottom(8)
        self._container.append(rules_desc)

        # 5 governance rules
        rules = [
            (
                "Regel 1",
                "Filnavne og indhold SKAL stemme overens",
                "File names must match their content headers. "
                "Example: I7_ADMIRAL_BUG_FIXES.md must have header '# I7. ADMIRAL BUG FIXES'. "
                "Mismatch between filename number and header number is blocked by pre-commit hook.",
                "#a855f7",
            ),
            (
                "Regel 2",
                "Status headers SKAL svare til indhold",
                "A file marked 'COMPLETE (100%)' must not contain TODOs or unfinished sections. "
                "A file marked 'IN PROGRESS (73%)' must not actually be 100% done. "
                "Pre-commit hook scans headers vs. content.",
                "#ef4444",
            ),
            (
                "Regel 3",
                "Alle filer 0% eller 100%",
                "PRODUCTION files must be 100% complete and fully verified. "
                "INVESTIGATION files can be 0-100% while work is in progress. "
                "ARCHIVE files are historical, read-only references.",
                "#22d3ee",
            ),
            (
                "Regel 4",
                "Dato-headers SKAL vaere aktuelle",
                "Every file must have an updated date header matching its last modification. "
                "Files older than 2 days are flagged as potentially stale. "
                "Daily sync script synchronizes date headers with file timestamps.",
                "#4ade80",
            ),
            (
                "Regel 5",
                "Interne referencer SKAL virke",
                "All cross-references like '[See also I7](I7_ADMIRAL_BUG_FIXES.md)' must point to existing files. "
                "Broken references are detected by daily sync and pre-commit hooks. "
                "Renaming or deleting files requires updating all references.",
                "#fbbf24",
            ),
        ]

        for regel_num, regel_title, regel_desc, regel_color in rules:
            rule_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            rule_card.add_css_class("intro-category-card")
            rule_card.add_css_class("intro-rule-card")

            # Rule header row
            rule_header_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

            rule_num_label = Gtk.Label()
            rule_num_label.set_markup(
                f'<span foreground="{regel_color}" weight="ultrabold" '
                f'font_family="JetBrains Mono">{regel_num}</span>'
            )
            rule_num_label.set_valign(Gtk.Align.CENTER)
            rule_header_row.append(rule_num_label)

            rule_title_label = Gtk.Label()
            rule_title_label.set_markup(
                f'<span weight="bold" foreground="{regel_color}">'
                f'{GLib.markup_escape_text(regel_title)}</span>'
            )
            rule_title_label.set_xalign(0)
            rule_title_label.set_hexpand(True)
            rule_header_row.append(rule_title_label)

            rule_card.append(rule_header_row)

            # Rule description
            rule_desc_label = Gtk.Label(label=regel_desc)
            rule_desc_label.set_xalign(0)
            rule_desc_label.set_wrap(True)
            rule_desc_label.add_css_class("caption")
            rule_desc_label.set_margin_start(4)
            rule_card.append(rule_desc_label)

            self._container.append(rule_card)


class IntroSystemView(Gtk.Box):
    """Content view for INTRO System sidebar items.

    Shows different sub-views depending on which INTRO sidebar category
    was clicked: I-files, B-files, C-files, D-files, structure, or health.
    """

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self._current_view = None

        # Main scrollable area
        self._scroll = Gtk.ScrolledWindow()
        self._scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._scroll.set_vexpand(True)

        self._container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        self._container.set_margin_start(40)
        self._container.set_margin_end(40)
        self._container.set_margin_top(32)
        self._container.set_margin_bottom(40)

        self._scroll.set_child(self._container)
        self.append(self._scroll)

    def _clear(self):
        """Remove all children from the container."""
        while child := self._container.get_first_child():
            self._container.remove(child)

    def show_category(self, category_key: str):
        """Display the specified INTRO category view.

        Args:
            category_key: One of 'I', 'B', 'C', 'D', 'structure', 'system_functions', 'dna_layers', 'health'
        """
        self._current_view = category_key
        self._clear()

        if category_key == "health":
            self._build_health_view()
        elif category_key == "structure":
            self._build_structure_view()
        elif category_key == "system_functions":
            self._build_system_functions_view()
        elif category_key == "dna_layers":
            self._build_dna_layers_view()
        elif category_key == "quick_actions":
            self._build_quick_actions_view()
        elif category_key == "I":
            self._build_i_files_view()
        elif category_key in ("B", "C", "D"):
            self._build_category_view(category_key)
        else:
            self._build_category_view(category_key)

    # -----------------------------------------------------------------
    # I-FILES VIEW (System Intelligence I1-I12)
    # -----------------------------------------------------------------

    def _build_i_files_view(self):
        """Build the I1-I12 System Intelligence file listing.

        Delegates to IntroIFilesView (FASE 2 widget) and embeds it
        directly inside the IntroSystemView container.
        """
        i_view = IntroIFilesView()
        # Extract the inner container content from IntroIFilesView and
        # add each child to our own container for consistent scrolling.
        # IntroIFilesView builds into its own _container, so we read
        # children from there.
        source = i_view._container
        children = []
        child = source.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            children.append(child)
            child = next_child
        for ch in children:
            source.remove(ch)
            self._container.append(ch)

    # -----------------------------------------------------------------
    # CATEGORY VIEW (B, C, D files)
    # -----------------------------------------------------------------

    def _build_category_view(self, letter: str):
        """Build a view for a file category (B, C, D, etc.)."""
        categories = intro_integration.get_intro_categories()
        target_cat = None
        for cat in categories:
            if cat.letter == letter:
                target_cat = cat
                break

        if not target_cat:
            empty = Adw.StatusPage()
            empty.set_title(f"Category {letter} Not Found")
            empty.set_icon_name("dialog-warning-symbolic")
            self._container.append(empty)
            return

        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        title = Gtk.Label(label=f"{target_cat.name} -- {letter}-Files")
        title.add_css_class("intro-view-header")
        title.set_xalign(0)
        header_box.append(title)

        subtitle = Gtk.Label(label=target_cat.description)
        subtitle.add_css_class("intro-view-subtitle")
        subtitle.set_xalign(0)
        subtitle.set_wrap(True)
        header_box.append(subtitle)
        self._container.append(header_box)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(4)
        sep.set_margin_bottom(4)
        self._container.append(sep)

        if not target_cat.files:
            empty = Adw.StatusPage()
            empty.set_title(f"No {letter}-Files Found")
            empty.set_description(f"Could not find {letter}-files in MASTER FOLDERS(INTRO)")
            empty.set_icon_name("folder-symbolic")
            self._container.append(empty)
            return

        # Summary
        summary = Gtk.Label(
            label=f"{target_cat.file_count} files  |  {target_cat.total_lines:,} lines  |  Last modified: {target_cat.latest_modified[:10] if target_cat.latest_modified else '?'}"
        )
        summary.add_css_class("caption")
        summary.add_css_class("dim-label")
        summary.set_xalign(0)
        self._container.append(summary)

        # File rows
        files_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        for f in target_cat.files:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            row.add_css_class("intro-file-row")

            # File number
            num = f.category_number
            num_str = f"{letter}{num}" if num is not None else f.name[:3]
            number_label = Gtk.Label(label=num_str)
            number_label.add_css_class("intro-file-number")
            number_label.set_valign(Gtk.Align.CENTER)
            row.append(number_label)

            # Info
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            info_box.set_hexpand(True)

            name_label = Gtk.Label(label=f.name)
            name_label.add_css_class("intro-file-title")
            name_label.set_xalign(0)
            name_label.set_ellipsize(Pango.EllipsizeMode.END)
            info_box.append(name_label)

            mod_date = f.last_modified[:10] if f.last_modified else "?"
            meta = Gtk.Label(label=f"{f.size_human}  |  {f.lines:,} lines  |  {mod_date}")
            meta.add_css_class("intro-file-meta")
            meta.set_xalign(0)
            info_box.append(meta)

            row.append(info_box)

            # Status badge
            status = Gtk.Label(label=f.status)
            status.add_css_class("intro-status-badge")
            if f.status in ("COMPLETE", "VERIFIED", "ALL_WORKING", "OPERATIONAL", "ESTABLISHED", "STABLE"):
                status.add_css_class("intro-status-complete")
            elif f.status in ("ACTIVE", "IN_PROGRESS"):
                status.add_css_class("intro-status-active")
            else:
                status.add_css_class("intro-status-unknown")
            status.set_valign(Gtk.Align.CENTER)
            row.append(status)

            # Open button
            open_btn = Gtk.Button(label="Open")
            open_btn.add_css_class("intro-open-btn")
            open_btn.set_valign(Gtk.Align.CENTER)
            fpath = str(f.path)
            open_btn.connect("clicked", lambda b, p=fpath: self._open_file(p))
            row.append(open_btn)

            files_box.append(row)

        self._container.append(files_box)

    # -----------------------------------------------------------------
    # STRUCTURE VIEW (Folder governance + rules)
    # -----------------------------------------------------------------

    def _build_structure_view(self):
        """Build the folder structure and governance rules view.

        Delegates to IntroStructureView (FASE 3 widget) and embeds it
        directly inside the IntroSystemView container.
        """
        struct_view = IntroStructureView()
        # Extract the inner container content from IntroStructureView and
        # add each child to our own container for consistent scrolling.
        source = struct_view._container
        children = []
        child = source.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            children.append(child)
            child = next_child
        for ch in children:
            source.remove(ch)
            self._container.append(ch)

    # -----------------------------------------------------------------
    # SYSTEM FUNCTIONS VIEW (FASE 4: Automated scripts + run buttons)
    # -----------------------------------------------------------------

    def _build_system_functions_view(self):
        """Build the System Functions view showing all automated INTRO scripts.

        Displays:
        - Pre-commit hook status and 7 verification levels
        - Daily Sync Script with 5 phases
        - Verification Script with 6 checks and Run Now button
        - Navigation Index Generator stats
        - Health Check with Run Now button
        - Run All Checks button
        - Real-time log panel
        """
        intro_path = INTRO_PATH

        # --- Header ---
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        title = Gtk.Label(label="INTRO System Functions")
        title.add_css_class("intro-view-header")
        title.set_xalign(0)
        header_box.append(title)

        subtitle = Gtk.Label(label="Automated scripts, verification hooks, and system maintenance tools")
        subtitle.add_css_class("intro-view-subtitle")
        subtitle.set_xalign(0)
        subtitle.set_wrap(True)
        header_box.append(subtitle)
        self._container.append(header_box)

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(4)
        sep.set_margin_bottom(8)
        self._container.append(sep)

        # =============================================================
        # 1. PRE-COMMIT HOOK
        # =============================================================
        self._build_precommit_card(intro_path)

        # =============================================================
        # 2. DAILY SYNC SCRIPT
        # =============================================================
        self._build_sync_script_card(intro_path)

        # =============================================================
        # 3. VERIFICATION SCRIPT
        # =============================================================
        self._build_verification_script_card(intro_path)

        # =============================================================
        # 4. NAVIGATION INDEX GENERATOR
        # =============================================================
        self._build_nav_index_card(intro_path)

        # =============================================================
        # 5. HEALTH CHECK SCRIPT
        # =============================================================
        self._build_health_check_card(intro_path)

        # =============================================================
        # 6. RUN ALL CHECKS BUTTON
        # =============================================================
        run_all_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        run_all_sep.set_margin_top(8)
        run_all_sep.set_margin_bottom(4)
        self._container.append(run_all_sep)

        run_all_btn = Gtk.Button(label="Run All Checks")
        run_all_btn.add_css_class("intro-sysfunc-runall-btn")
        run_all_btn.set_halign(Gtk.Align.CENTER)
        run_all_btn.set_tooltip_text("Runs verify_master_folders.py, check_folder_health.sh, and generate_navigation_index.py sequentially")
        run_all_btn.connect("clicked", self._on_run_all_checks)
        self._container.append(run_all_btn)

        # =============================================================
        # 7. REAL-TIME LOG PANEL
        # =============================================================
        log_label = Gtk.Label(label="Execution Log")
        log_label.add_css_class("intro-view-subtitle")
        log_label.set_xalign(0)
        log_label.set_margin_top(12)
        self._container.append(log_label)

        log_scroll = Gtk.ScrolledWindow()
        log_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        log_scroll.set_min_content_height(200)
        log_scroll.set_max_content_height(300)

        self._log_textview = Gtk.TextView()
        self._log_textview.set_editable(False)
        self._log_textview.set_cursor_visible(False)
        self._log_textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self._log_textview.add_css_class("intro-sysfunc-log-panel")
        self._log_buffer = self._log_textview.get_buffer()
        self._log_buffer.set_text("No script output yet. Click a 'Run Now' button or 'Run All Checks' to begin.\n")

        log_scroll.set_child(self._log_textview)
        self._container.append(log_scroll)

    # -- Pre-commit hook card --

    def _build_precommit_card(self, intro_path):
        """Build the pre-commit hook information card."""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("intro-sysfunc-card")

        # Title row
        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        icon = Gtk.Image.new_from_icon_name("security-high-symbolic")
        icon.set_pixel_size(20)
        title_row.append(icon)

        title = Gtk.Label(label="Pre-commit Hook")
        title.add_css_class("intro-sysfunc-title")
        title.set_xalign(0)
        title.set_hexpand(True)
        title_row.append(title)

        # Status badge: check if hook file exists and is executable
        hook_path = intro_path / ".git" / "hooks" / "pre-commit"
        hook_exists = hook_path.exists()
        hook_executable = False
        hook_mtime = ""
        if hook_exists:
            import os as _os
            import stat as _stat
            st = hook_path.stat()
            hook_executable = bool(st.st_mode & _stat.S_IXUSR)
            hook_mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        is_active = hook_exists and hook_executable
        status_badge = Gtk.Label(label="Active" if is_active else "Inactive")
        status_badge.add_css_class("intro-sysfunc-status-active" if is_active else "intro-sysfunc-status-inactive")
        title_row.append(status_badge)

        card.append(title_row)

        # Description
        desc = Gtk.Label(label="Runs verify_master_folders.py before every commit to MASTER FOLDERS")
        desc.add_css_class("intro-sysfunc-desc")
        desc.set_xalign(0)
        desc.set_wrap(True)
        card.append(desc)

        # File path
        path_label = Gtk.Label(label=f"Path: {hook_path}")
        path_label.add_css_class("intro-sysfunc-detail")
        path_label.set_xalign(0)
        path_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        card.append(path_label)

        # Last run timestamp
        if hook_mtime:
            ts_label = Gtk.Label(label=f"Last modified: {hook_mtime}")
            ts_label.add_css_class("intro-sysfunc-detail")
            ts_label.set_xalign(0)
            card.append(ts_label)

        # 7 verification levels
        levels_label = Gtk.Label(label="7 Verification Levels:")
        levels_label.add_css_class("caption")
        levels_label.set_xalign(0)
        levels_label.set_margin_top(6)
        card.append(levels_label)

        verification_levels = [
            ("1. Git Status", "Checks for uncommitted changes in the repository"),
            ("2. HOVEDINDEKS Accuracy", "Verifies master index matches physical files"),
            ("3. I-File Numbering", "Confirms I1-I12 files are correctly numbered"),
            ("4. Cross-References", "Validates all internal file references resolve"),
            ("5. Subdirectory Structure", "Ensures all expected directories exist"),
            ("6. TODO Analysis", "Distinguishes intentional vs forgotten TODOs"),
            ("7. Report Generation", "Produces verification report with PASS/FAIL status"),
        ]

        for level_name, level_desc in verification_levels:
            level_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            level_box.add_css_class("intro-sysfunc-level-card")

            name_lbl = Gtk.Label(label=level_name)
            name_lbl.add_css_class("caption")
            name_lbl.set_xalign(0)
            name_lbl.set_hexpand(False)
            level_box.append(name_lbl)

            desc_lbl = Gtk.Label(label=level_desc)
            desc_lbl.add_css_class("intro-sysfunc-detail")
            desc_lbl.set_xalign(0)
            desc_lbl.set_hexpand(True)
            desc_lbl.set_ellipsize(Pango.EllipsizeMode.END)
            level_box.append(desc_lbl)

            card.append(level_box)

        self._container.append(card)

    # -- Daily Sync Script card --

    def _build_sync_script_card(self, intro_path):
        """Build the daily sync script information card."""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("intro-sysfunc-card")

        # Title row
        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        icon = Gtk.Image.new_from_icon_name("emblem-synchronizing-symbolic")
        icon.set_pixel_size(20)
        title_row.append(icon)

        title = Gtk.Label(label="Daily Sync Script")
        title.add_css_class("intro-sysfunc-title")
        title.set_xalign(0)
        title.set_hexpand(True)
        title_row.append(title)

        # Status: check if script exists
        script_path = intro_path / "sync_indexes.sh"
        script_exists = script_path.exists()
        status_badge = Gtk.Label(label="Available" if script_exists else "Missing")
        status_badge.add_css_class("intro-sysfunc-status-active" if script_exists else "intro-sysfunc-status-inactive")
        title_row.append(status_badge)

        card.append(title_row)

        # Description
        desc = Gtk.Label(label="Runs daily at 04:00 to auto-fix metadata mismatches and verify indexes")
        desc.add_css_class("intro-sysfunc-desc")
        desc.set_xalign(0)
        desc.set_wrap(True)
        card.append(desc)

        # Schedule + log info
        schedule_label = Gtk.Label(label="Schedule: Daily at 04:00 CET")
        schedule_label.add_css_class("intro-sysfunc-detail")
        schedule_label.set_xalign(0)
        card.append(schedule_label)

        log_label = Gtk.Label(label="Log location: /tmp/MASTER_FOLDERS_SYNC_*.log")
        log_label.add_css_class("intro-sysfunc-detail")
        log_label.set_xalign(0)
        card.append(log_label)

        # 5 sync phases
        phases_label = Gtk.Label(label="5 Sync Phases:")
        phases_label.add_css_class("caption")
        phases_label.set_xalign(0)
        phases_label.set_margin_top(6)
        card.append(phases_label)

        sync_phases = [
            ("Phase 1: Verify State", "Runs verification check on current state"),
            ("Phase 2: Update Timestamps", "Updates documentation date headers for modified files"),
            ("Phase 3: Verify Links", "Checks all internal markdown references are valid"),
            ("Phase 4: Uncommitted Check", "Reports files with uncommitted changes (no auto-commit)"),
            ("Phase 5: Generate Report", "Creates verification report in /tmp/"),
        ]

        for phase_name, phase_desc in sync_phases:
            phase_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            phase_box.add_css_class("intro-sysfunc-phase-card")

            name_lbl = Gtk.Label(label=phase_name)
            name_lbl.add_css_class("caption")
            name_lbl.set_xalign(0)
            name_lbl.set_hexpand(False)
            phase_box.append(name_lbl)

            desc_lbl = Gtk.Label(label=phase_desc)
            desc_lbl.add_css_class("intro-sysfunc-detail")
            desc_lbl.set_xalign(0)
            desc_lbl.set_hexpand(True)
            desc_lbl.set_ellipsize(Pango.EllipsizeMode.END)
            phase_box.append(desc_lbl)

            card.append(phase_box)

        self._container.append(card)

    # -- Verification Script card --

    def _build_verification_script_card(self, intro_path):
        """Build the verification script card with Run Now button."""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("intro-sysfunc-card")

        # Title row
        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        icon = Gtk.Image.new_from_icon_name("emblem-default-symbolic")
        icon.set_pixel_size(20)
        title_row.append(icon)

        title = Gtk.Label(label="Verification Script")
        title.add_css_class("intro-sysfunc-title")
        title.set_xalign(0)
        title.set_hexpand(True)
        title_row.append(title)

        # Run Now button
        run_btn = Gtk.Button(label="Run Now")
        run_btn.add_css_class("intro-sysfunc-run-btn")
        run_btn.set_tooltip_text("Run verify_master_folders.py")
        run_btn.connect("clicked", lambda b: self._run_script_async(
            "python3", str(intro_path / "verify_master_folders.py"),
            cwd=str(intro_path), label="verify_master_folders.py"
        ))
        title_row.append(run_btn)

        card.append(title_row)

        # Description
        desc = Gtk.Label(label="Admiral-level automatic verification of the entire documentation system")
        desc.add_css_class("intro-sysfunc-desc")
        desc.set_xalign(0)
        desc.set_wrap(True)
        card.append(desc)

        # Path
        script_path = intro_path / "verify_master_folders.py"
        path_label = Gtk.Label(label=f"Path: {script_path}")
        path_label.add_css_class("intro-sysfunc-detail")
        path_label.set_xalign(0)
        path_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        card.append(path_label)

        # 6 checks explained
        checks_label = Gtk.Label(label="6 Verification Checks:")
        checks_label.add_css_class("caption")
        checks_label.set_xalign(0)
        checks_label.set_margin_top(6)
        card.append(checks_label)

        verify_checks = [
            ("1. Git Status", "Verifies repository is clean with no uncommitted changes"),
            ("2. HOVEDINDEKS Accuracy", "Checks master index file listings match physical files"),
            ("3. I-File Numbering", "Confirms I1-I12 numbering is correct and complete"),
            ("4. Cross-References", "Scans all markdown files for broken internal references"),
            ("5. Subdirectory Structure", "Ensures all 8 expected directories exist"),
            ("6. TODO Markers", "Analyzes TODO markers -- intentional vs forgotten"),
        ]

        for check_name, check_desc in verify_checks:
            check_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            check_box.add_css_class("intro-sysfunc-level-card")

            name_lbl = Gtk.Label(label=check_name)
            name_lbl.add_css_class("caption")
            name_lbl.set_xalign(0)
            name_lbl.set_hexpand(False)
            check_box.append(name_lbl)

            desc_lbl = Gtk.Label(label=check_desc)
            desc_lbl.add_css_class("intro-sysfunc-detail")
            desc_lbl.set_xalign(0)
            desc_lbl.set_hexpand(True)
            desc_lbl.set_ellipsize(Pango.EllipsizeMode.END)
            check_box.append(desc_lbl)

            card.append(check_box)

        self._container.append(card)

    # -- Navigation Index Generator card --

    def _build_nav_index_card(self, intro_path):
        """Build the navigation index generator information card."""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("intro-sysfunc-card")

        # Title row
        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        icon = Gtk.Image.new_from_icon_name("system-search-symbolic")
        icon.set_pixel_size(20)
        title_row.append(icon)

        title = Gtk.Label(label="Navigation Index Generator")
        title.add_css_class("intro-sysfunc-title")
        title.set_xalign(0)
        title.set_hexpand(True)
        title_row.append(title)

        # Status: check if script exists
        script_path = intro_path / "generate_navigation_index.py"
        script_exists = script_path.exists()
        status_badge = Gtk.Label(label="Available" if script_exists else "Missing")
        status_badge.add_css_class("intro-sysfunc-status-active" if script_exists else "intro-sysfunc-status-inactive")
        title_row.append(status_badge)

        card.append(title_row)

        # Description
        desc = Gtk.Label(label="Creates automated, searchable index of all documents across MASTER FOLDERS and MANUAL")
        desc.add_css_class("intro-sysfunc-desc")
        desc.set_xalign(0)
        desc.set_wrap(True)
        card.append(desc)

        # Path
        path_label = Gtk.Label(label=f"Path: {script_path}")
        path_label.add_css_class("intro-sysfunc-detail")
        path_label.set_xalign(0)
        path_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        card.append(path_label)

        # Stats: try to read NAVIGATION_INDEX.json for live stats
        stats_text = "113 documents, 68,506 lines, 2,650+ keywords"
        nav_json = intro_path / "NAVIGATION_INDEX.json"
        if nav_json.exists():
            try:
                with open(nav_json, "r") as f:
                    nav_data = json.load(f)
                summary = nav_data.get("summary", {})
                total_docs = summary.get("total_documents", 113)
                total_lines = summary.get("total_lines", 68506)
                total_kw = summary.get("unique_keywords", 2650)
                stats_text = f"{total_docs} documents, {total_lines:,} lines, {total_kw:,}+ keywords"
            except Exception:
                pass

        stats_label = Gtk.Label(label=f"Index scope: {stats_text}")
        stats_label.add_css_class("intro-sysfunc-detail")
        stats_label.set_xalign(0)
        card.append(stats_label)

        # Features
        features_label = Gtk.Label(label="Features:")
        features_label.add_css_class("caption")
        features_label.set_xalign(0)
        features_label.set_margin_top(6)
        card.append(features_label)

        features = [
            ("Markdown scanning", "Scans all .md files in both MASTER FOLDERS and MANUAL"),
            ("Header extraction", "Extracts all headers and document structure automatically"),
            ("Keyword indexing", "Builds searchable keyword index across all documents"),
            ("Cross-references", "Generates organized index by category and topic"),
            ("JSON + Markdown", "Outputs both NAVIGATION_INDEX.md and NAVIGATION_INDEX.json"),
        ]

        for feat_name, feat_desc in features:
            feat_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            feat_box.add_css_class("intro-sysfunc-level-card")

            name_lbl = Gtk.Label(label=feat_name)
            name_lbl.add_css_class("caption")
            name_lbl.set_xalign(0)
            name_lbl.set_hexpand(False)
            feat_box.append(name_lbl)

            desc_lbl = Gtk.Label(label=feat_desc)
            desc_lbl.add_css_class("intro-sysfunc-detail")
            desc_lbl.set_xalign(0)
            desc_lbl.set_hexpand(True)
            desc_lbl.set_ellipsize(Pango.EllipsizeMode.END)
            feat_box.append(desc_lbl)

            card.append(feat_box)

        self._container.append(card)

    # -- Health Check Script card --

    def _build_health_check_card(self, intro_path):
        """Build the health check script card with Run Now button."""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("intro-sysfunc-card")

        # Title row
        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        icon = Gtk.Image.new_from_icon_name("dialog-information-symbolic")
        icon.set_pixel_size(20)
        title_row.append(icon)

        title = Gtk.Label(label="Folder Health Check")
        title.add_css_class("intro-sysfunc-title")
        title.set_xalign(0)
        title.set_hexpand(True)
        title_row.append(title)

        # Run Now button
        run_btn = Gtk.Button(label="Run Now")
        run_btn.add_css_class("intro-sysfunc-run-btn")
        run_btn.set_tooltip_text("Run check_folder_health.sh --summary")
        run_btn.connect("clicked", lambda b: self._run_script_async(
            "bash", str(intro_path / "check_folder_health.sh"), "--summary",
            cwd=str(intro_path), label="check_folder_health.sh"
        ))
        title_row.append(run_btn)

        card.append(title_row)

        # Description
        desc = Gtk.Label(label="Real-time status dashboard for MASTER FOLDERS and MANUAL folders")
        desc.add_css_class("intro-sysfunc-desc")
        desc.set_xalign(0)
        desc.set_wrap(True)
        card.append(desc)

        # Path
        script_path = intro_path / "check_folder_health.sh"
        path_label = Gtk.Label(label=f"Path: {script_path}")
        path_label.add_css_class("intro-sysfunc-detail")
        path_label.set_xalign(0)
        path_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        card.append(path_label)

        # Capabilities
        caps_label = Gtk.Label(label="Capabilities:")
        caps_label.add_css_class("caption")
        caps_label.set_xalign(0)
        caps_label.set_margin_top(6)
        card.append(caps_label)

        capabilities = [
            ("File statistics", "Counts markdown files and total lines per folder"),
            ("TODO analysis", "Reports TODO/PENDING/TBD marker counts"),
            ("Link verification", "Checks for broken reference indicators"),
            ("Git status", "Reports pushed/unpushed commits status"),
            ("Critical files", "Verifies critical I-files and STATUS files exist"),
            ("Completeness", "Calculates overall completeness percentage"),
        ]

        for cap_name, cap_desc in capabilities:
            cap_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            cap_box.add_css_class("intro-sysfunc-level-card")

            name_lbl = Gtk.Label(label=cap_name)
            name_lbl.add_css_class("caption")
            name_lbl.set_xalign(0)
            name_lbl.set_hexpand(False)
            cap_box.append(name_lbl)

            desc_lbl = Gtk.Label(label=cap_desc)
            desc_lbl.add_css_class("intro-sysfunc-detail")
            desc_lbl.set_xalign(0)
            desc_lbl.set_hexpand(True)
            desc_lbl.set_ellipsize(Pango.EllipsizeMode.END)
            cap_box.append(desc_lbl)

            card.append(cap_box)

        self._container.append(card)

    # -- Script execution helpers --

    def _run_script_async(self, *cmd_args, cwd=None, label="script"):
        """Run a script in a background thread and stream output to the log panel.

        Uses GLib.idle_add() to safely update the UI from the worker thread.
        """
        import threading

        def _append_log(text):
            """Thread-safe log append via GLib.idle_add."""
            def _do():
                end_iter = self._log_buffer.get_end_iter()
                self._log_buffer.insert(end_iter, text)
                # Auto-scroll to bottom
                mark = self._log_buffer.get_insert()
                self._log_textview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)
                return False
            GLib.idle_add(_do)

        def _worker():
            _append_log(f"\n--- Running {label} ---\n")
            try:
                result = subprocess.run(
                    list(cmd_args),
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.stdout:
                    _append_log(result.stdout)
                if result.stderr:
                    _append_log(f"[stderr] {result.stderr}")
                exit_label = "OK" if result.returncode == 0 else f"EXIT {result.returncode}"
                _append_log(f"--- {label} finished ({exit_label}) ---\n")
            except subprocess.TimeoutExpired:
                _append_log(f"--- {label} TIMED OUT (120s) ---\n")
            except Exception as e:
                _append_log(f"--- {label} ERROR: {e} ---\n")

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()

    def _on_run_all_checks(self, button):
        """Run all INTRO system scripts sequentially in a background thread."""
        import threading
        intro_path = INTRO_PATH

        def _append_log(text):
            def _do():
                end_iter = self._log_buffer.get_end_iter()
                self._log_buffer.insert(end_iter, text)
                mark = self._log_buffer.get_insert()
                self._log_textview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)
                return False
            GLib.idle_add(_do)

        def _run_one(cmd_list, cwd_path, script_label):
            _append_log(f"\n=== Running {script_label} ===\n")
            try:
                result = subprocess.run(
                    cmd_list,
                    cwd=str(cwd_path),
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.stdout:
                    _append_log(result.stdout)
                if result.stderr:
                    _append_log(f"[stderr] {result.stderr}")
                exit_label = "OK" if result.returncode == 0 else f"EXIT {result.returncode}"
                _append_log(f"=== {script_label} finished ({exit_label}) ===\n")
            except subprocess.TimeoutExpired:
                _append_log(f"=== {script_label} TIMED OUT ===\n")
            except Exception as e:
                _append_log(f"=== {script_label} ERROR: {e} ===\n")

        def _worker():
            _append_log("\n" + "=" * 60 + "\n")
            _append_log("  RUN ALL CHECKS -- Starting sequential execution\n")
            _append_log("=" * 60 + "\n")

            scripts = [
                (["python3", str(intro_path / "verify_master_folders.py")], intro_path, "verify_master_folders.py"),
                (["bash", str(intro_path / "check_folder_health.sh"), "--summary"], intro_path, "check_folder_health.sh"),
                (["python3", str(intro_path / "generate_navigation_index.py")], intro_path, "generate_navigation_index.py"),
            ]

            for cmd, cwd_path, label in scripts:
                script_file = Path(cmd[-1]) if len(cmd) > 1 else None
                if script_file and not script_file.exists():
                    _append_log(f"\n=== SKIPPING {label} (file not found) ===\n")
                    continue
                _run_one(cmd, cwd_path, label)

            _append_log("\n" + "=" * 60 + "\n")
            _append_log("  RUN ALL CHECKS -- Complete\n")
            _append_log("=" * 60 + "\n")

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()

    # -----------------------------------------------------------------
    # DNA LAYERS VIEW (FASE 5: 7-DNA with real INTRO data)
    # -----------------------------------------------------------------

    def _build_dna_layers_view(self):
        """Build the 7-DNA Layers view with REAL data from INTRO files.

        Reads actual files from MASTER FOLDERS(INTRO) to determine the
        status and completion percentage of each of the 7 DNA layers:
          Lag 1 SELF-AWARE       -- DNA.yaml + system identity
          Lag 2 SELF-DOCUMENTING -- AUTO_LOG.jsonl status
          Lag 3 SELF-VERIFYING   -- verify_master_folders.py result
          Lag 4 SELF-IMPROVING   -- PATTERNS.yaml + learned patterns
          Lag 5 SELF-ARCHIVING   -- ARCHIVE/ count + last archived
          Lag 6 PREDICTIVE       -- _CURRENT/NEXT.md content
          Lag 7 SELF-OPTIMIZING  -- 3-pass status from sejrliste data
        """
        intro_path = INTRO_PATH

        # --- Header ---
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        title = Gtk.Label(label="INTRO 7-DNA Layers")
        title.add_css_class("intro-view-header")
        title.set_xalign(0)
        header_box.append(title)

        subtitle = Gtk.Label(
            label="Real-time analysis of the 7 DNA layers from MASTER FOLDERS(INTRO) -- based on actual files, not dummy data"
        )
        subtitle.add_css_class("intro-view-subtitle")
        subtitle.set_xalign(0)
        subtitle.set_wrap(True)
        header_box.append(subtitle)
        self._container.append(header_box)

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(4)
        sep.set_margin_bottom(8)
        self._container.append(sep)

        # --- Gather real data for each layer ---
        layer_data = self._gather_dna_layer_data(intro_path)

        # --- Overall score ---
        total_pct = sum(ld["completion"] for ld in layer_data) / len(layer_data) if layer_data else 0.0

        score_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        score_box.set_halign(Gtk.Align.CENTER)
        score_box.set_margin_top(12)
        score_box.set_margin_bottom(16)

        score_label = Gtk.Label(label=f"{total_pct:.0f}%")
        score_label.add_css_class("intro-dna-overall-score")
        if total_pct >= 70:
            score_label.add_css_class("intro-dna-overall-pass")
        elif total_pct >= 40:
            score_label.add_css_class("intro-dna-overall-warn")
        else:
            score_label.add_css_class("intro-dna-overall-low")
        score_box.append(score_label)

        score_meta = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        score_meta.set_valign(Gtk.Align.CENTER)

        active_count = sum(1 for ld in layer_data if ld["completion"] > 0)
        meta_label = Gtk.Label(label=f"{active_count}/7 layers active")
        meta_label.add_css_class("caption")
        score_meta.append(meta_label)

        from datetime import datetime as _dt
        ts_label = Gtk.Label(label=f"Scanned: {_dt.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ts_label.add_css_class("caption")
        ts_label.add_css_class("dim-label")
        score_meta.append(ts_label)

        score_box.append(score_meta)
        self._container.append(score_box)

        # --- Refresh button ---
        refresh_btn = Gtk.Button(label="Re-scan DNA Layers")
        refresh_btn.add_css_class("suggested-action")
        refresh_btn.add_css_class("pill")
        refresh_btn.set_halign(Gtk.Align.CENTER)
        refresh_btn.connect("clicked", lambda b: self.show_category("dna_layers"))
        self._container.append(refresh_btn)

        refresh_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        refresh_sep.set_margin_top(12)
        refresh_sep.set_margin_bottom(4)
        self._container.append(refresh_sep)

        # --- Layer cards ---
        layers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        layers_box.set_margin_top(8)

        for ld in layer_data:
            card = self._build_dna_layer_card(ld)
            layers_box.append(card)

        self._container.append(layers_box)

    def _gather_dna_layer_data(self, intro_path: Path) -> list:
        """Gather real data for each of the 7 DNA layers.

        Returns a list of dicts with keys:
            layer_num, name, icon, status, status_class,
            detail_lines, completion
        """
        import json as _json
        from datetime import datetime as _dt

        layers = []

        # ---------------------------------------------------------------
        # LAG 1: SELF-AWARE -- DNA.yaml + system identity
        # ---------------------------------------------------------------
        dna_yaml_path = intro_path / "DNA.yaml"
        dna_found = dna_yaml_path.exists()
        dna_detail = []
        dna_completion = 0.0

        if dna_found:
            try:
                content = dna_yaml_path.read_text(encoding="utf-8", errors="replace")
                line_count = len(content.splitlines())
                dna_detail.append(f"DNA.yaml: {line_count} lines")
                # Try to extract system identity from YAML
                for line in content.splitlines()[:20]:
                    if "name:" in line.lower() or "identity:" in line.lower() or "system:" in line.lower():
                        dna_detail.append(line.strip()[:80])
                        break
                dna_completion = 100.0
            except Exception:
                dna_detail.append("DNA.yaml: exists but unreadable")
                dna_completion = 50.0
        else:
            # Check for alternative identity files
            alt_files = [
                intro_path / "00_SYSTEM_GENESIS.md",
                intro_path / "I1_ADMIRAL_PLUS_VISION.md",
                intro_path / "I8_ADMIRAL_CENTRAL.md",
            ]
            found_alts = [f for f in alt_files if f.exists()]
            if found_alts:
                dna_detail.append(f"DNA.yaml: missing -- {len(found_alts)} identity alt(s) found")
                for af in found_alts[:2]:
                    dna_detail.append(f"  -> {af.name}")
                dna_completion = 60.0
            else:
                dna_detail.append("DNA.yaml: missing -- no identity files found")
                dna_completion = 0.0

        layers.append({
            "layer_num": "1",
            "name": "SELF-AWARE",
            "icon": "user-info-symbolic",
            "status": "Found" if dna_found else ("Partial" if dna_completion > 0 else "Missing"),
            "status_class": "intro-dna-status-found" if dna_found else ("intro-dna-status-partial" if dna_completion > 0 else "intro-dna-status-missing"),
            "detail_lines": dna_detail,
            "completion": dna_completion,
        })

        # ---------------------------------------------------------------
        # LAG 2: SELF-DOCUMENTING -- AUTO_LOG.jsonl status
        # ---------------------------------------------------------------
        log_path = intro_path / "AUTO_LOG.jsonl"
        log_found = log_path.exists()
        log_detail = []
        log_completion = 0.0

        if log_found:
            try:
                content = log_path.read_text(encoding="utf-8", errors="replace")
                lines = [l.strip() for l in content.splitlines() if l.strip()]
                log_detail.append(f"AUTO_LOG.jsonl: {len(lines)} entries")
                if lines:
                    # Try to parse last entry for timestamp
                    try:
                        last_entry = _json.loads(lines[-1])
                        ts = last_entry.get("timestamp", last_entry.get("ts", last_entry.get("date", "?")))
                        log_detail.append(f"Last entry: {str(ts)[:25]}")
                    except (_json.JSONDecodeError, KeyError):
                        log_detail.append(f"Last line: {lines[-1][:60]}")
                log_completion = 100.0 if len(lines) >= 5 else 50.0
            except Exception:
                log_detail.append("AUTO_LOG.jsonl: exists but unreadable")
                log_completion = 25.0
        else:
            # Check for git log as alternative documentation
            git_dir = intro_path / ".git"
            if git_dir.exists():
                try:
                    result = subprocess.run(
                        ["git", "log", "--oneline", "-5"],
                        cwd=str(intro_path),
                        capture_output=True, text=True, timeout=10,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        commit_count = len(result.stdout.strip().splitlines())
                        log_detail.append(f"AUTO_LOG.jsonl: missing -- git has {commit_count}+ commits")
                        log_detail.append(f"Last commit: {result.stdout.strip().splitlines()[0][:60]}")
                        log_completion = 40.0
                    else:
                        log_detail.append("AUTO_LOG.jsonl: missing -- git log empty")
                        log_completion = 10.0
                except Exception:
                    log_detail.append("AUTO_LOG.jsonl: missing -- git check failed")
                    log_completion = 5.0
            else:
                log_detail.append("AUTO_LOG.jsonl: missing -- no git repo either")
                log_completion = 0.0

        layers.append({
            "layer_num": "2",
            "name": "SELF-DOCUMENTING",
            "icon": "document-edit-symbolic",
            "status": "Found" if log_found else ("Partial" if log_completion > 0 else "Missing"),
            "status_class": "intro-dna-status-found" if log_found else ("intro-dna-status-partial" if log_completion > 0 else "intro-dna-status-missing"),
            "detail_lines": log_detail,
            "completion": log_completion,
        })

        # ---------------------------------------------------------------
        # LAG 3: SELF-VERIFYING -- verify_master_folders.py
        # ---------------------------------------------------------------
        verify_path = intro_path / "verify_master_folders.py"
        verify_found = verify_path.exists()
        verify_detail = []
        verify_completion = 0.0

        if verify_found:
            try:
                st = verify_path.stat()
                size_kb = st.st_size / 1024
                mtime = _dt.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
                verify_detail.append(f"verify_master_folders.py: {size_kb:.1f} KB")
                verify_detail.append(f"Last modified: {mtime}")
                # Check if executable
                import stat as _stat
                is_exec = bool(st.st_mode & _stat.S_IXUSR)
                verify_detail.append(f"Executable: {'Yes' if is_exec else 'No'}")
                # Check for pre-commit hook integration
                hook_path = intro_path / ".git" / "hooks" / "pre-commit"
                if hook_path.exists():
                    verify_detail.append("Pre-commit hook: Active")
                    verify_completion = 100.0
                else:
                    verify_detail.append("Pre-commit hook: Not found")
                    verify_completion = 75.0
            except Exception:
                verify_detail.append("verify_master_folders.py: exists but stat failed")
                verify_completion = 50.0
        else:
            # Check for alternative verification scripts
            alt_scripts = [
                intro_path / "check_folder_health.sh",
                intro_path / "auto_verify_hook.sh",
            ]
            found_alts = [s for s in alt_scripts if s.exists()]
            if found_alts:
                verify_detail.append(f"verify_master_folders.py: missing -- {len(found_alts)} alt script(s)")
                for s in found_alts:
                    verify_detail.append(f"  -> {s.name}")
                verify_completion = 30.0
            else:
                verify_detail.append("verify_master_folders.py: missing")
                verify_completion = 0.0

        layers.append({
            "layer_num": "3",
            "name": "SELF-VERIFYING",
            "icon": "emblem-ok-symbolic",
            "status": "Found" if verify_found else ("Partial" if verify_completion > 0 else "Missing"),
            "status_class": "intro-dna-status-found" if verify_found else ("intro-dna-status-partial" if verify_completion > 0 else "intro-dna-status-missing"),
            "detail_lines": verify_detail,
            "completion": verify_completion,
        })

        # ---------------------------------------------------------------
        # LAG 4: SELF-IMPROVING -- PATTERNS.yaml + learned patterns
        # ---------------------------------------------------------------
        patterns_path = intro_path / "PATTERNS.yaml"
        patterns_found = patterns_path.exists()
        patterns_detail = []
        patterns_completion = 0.0

        if patterns_found:
            try:
                content = patterns_path.read_text(encoding="utf-8", errors="replace")
                lines = content.splitlines()
                # Count pattern entries (lines starting with '- ' or containing 'pattern')
                pattern_count = sum(1 for l in lines if l.strip().startswith("- ") or "pattern" in l.lower())
                patterns_detail.append(f"PATTERNS.yaml: {len(lines)} lines, ~{pattern_count} patterns")
                patterns_completion = 100.0 if pattern_count >= 5 else 50.0
            except Exception:
                patterns_detail.append("PATTERNS.yaml: exists but unreadable")
                patterns_completion = 25.0
        else:
            # Check for learning evidence in other files
            learning_files = list(intro_path.glob("*PATTERN*")) + list(intro_path.glob("*LEARN*"))
            if learning_files:
                patterns_detail.append(f"PATTERNS.yaml: missing -- {len(learning_files)} learning file(s)")
                for lf in learning_files[:2]:
                    patterns_detail.append(f"  -> {lf.name}")
                patterns_completion = 20.0
            else:
                # Check for I-files that document patterns
                i4_path = intro_path / "I4_ADMIRAL_MORNING_BRIEFING.md"
                if i4_path.exists():
                    patterns_detail.append("PATTERNS.yaml: missing -- I4 briefing exists as learning proxy")
                    patterns_completion = 15.0
                else:
                    patterns_detail.append("PATTERNS.yaml: missing -- no learning evidence")
                    patterns_completion = 0.0

        layers.append({
            "layer_num": "4",
            "name": "SELF-IMPROVING",
            "icon": "emblem-synchronizing-symbolic",
            "status": "Found" if patterns_found else ("Partial" if patterns_completion > 0 else "Missing"),
            "status_class": "intro-dna-status-found" if patterns_found else ("intro-dna-status-partial" if patterns_completion > 0 else "intro-dna-status-missing"),
            "detail_lines": patterns_detail,
            "completion": patterns_completion,
        })

        # ---------------------------------------------------------------
        # LAG 5: SELF-ARCHIVING -- ARCHIVE/ count + last archived
        # ---------------------------------------------------------------
        archive_paths = [
            intro_path / "90_ARCHIVE",
            intro_path / "ARCHIVE",
            intro_path / "HISTORICAL ARCHIVE",
        ]
        archive_detail = []
        archive_completion = 0.0
        total_archive_items = 0
        latest_archive_date = ""

        for ap in archive_paths:
            if ap.exists() and ap.is_dir():
                try:
                    items = list(ap.iterdir())
                    item_count = len(items)
                    total_archive_items += item_count
                    archive_detail.append(f"{ap.name}/: {item_count} items")
                    # Find latest modification
                    if items:
                        latest_item = max(items, key=lambda p: p.stat().st_mtime)
                        item_date = _dt.fromtimestamp(latest_item.stat().st_mtime).strftime("%Y-%m-%d")
                        if not latest_archive_date or item_date > latest_archive_date:
                            latest_archive_date = item_date
                except Exception:
                    archive_detail.append(f"{ap.name}/: exists but scan failed")

        if total_archive_items > 0:
            archive_detail.insert(0, f"Total archived: {total_archive_items} items")
            if latest_archive_date:
                archive_detail.append(f"Last archived: {latest_archive_date}")
            archive_completion = min(100.0, 40.0 + total_archive_items * 6.0)
        else:
            found_dirs = [ap for ap in archive_paths if ap.exists()]
            if found_dirs:
                archive_detail.append(f"{len(found_dirs)} archive dir(s) exist but empty")
                archive_completion = 10.0
            else:
                archive_detail.append("No archive directories found (90_ARCHIVE/, ARCHIVE/, HISTORICAL ARCHIVE/)")
                archive_completion = 0.0

        layers.append({
            "layer_num": "5",
            "name": "SELF-ARCHIVING",
            "icon": "folder-visiting-symbolic",
            "status": "Found" if total_archive_items > 0 else ("Partial" if archive_completion > 0 else "Missing"),
            "status_class": "intro-dna-status-found" if total_archive_items > 0 else ("intro-dna-status-partial" if archive_completion > 0 else "intro-dna-status-missing"),
            "detail_lines": archive_detail,
            "completion": archive_completion,
        })

        # ---------------------------------------------------------------
        # LAG 6: PREDICTIVE -- _CURRENT/NEXT.md content
        # ---------------------------------------------------------------
        next_paths = [
            intro_path / "_CURRENT" / "NEXT.md",
            intro_path / "NEXT.md",
            intro_path / "OBLIGATORISK_OPGAVER.md",
            intro_path / "OBLIGATORISKE_ORDRER.md",
        ]
        predict_detail = []
        predict_completion = 0.0

        for np_path in next_paths:
            if np_path.exists():
                try:
                    content = np_path.read_text(encoding="utf-8", errors="replace")
                    lines = content.splitlines()
                    predict_detail.append(f"{np_path.name}: {len(lines)} lines")
                    # Show first 3 non-empty content lines
                    content_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]
                    for cl in content_lines[:3]:
                        predict_detail.append(f"  {cl[:70]}")
                    if np_path.name in ("NEXT.md",):
                        predict_completion = max(predict_completion, 100.0)
                    else:
                        predict_completion = max(predict_completion, 60.0)
                except Exception:
                    predict_detail.append(f"{np_path.name}: exists but unreadable")
                    predict_completion = max(predict_completion, 20.0)

        if not predict_detail:
            predict_detail.append("No predictive files found (_CURRENT/NEXT.md, OBLIGATORISK_OPGAVER.md)")
            predict_completion = 0.0

        layers.append({
            "layer_num": "6",
            "name": "PREDICTIVE",
            "icon": "weather-few-clouds-symbolic",
            "status": "Found" if predict_completion >= 60 else ("Partial" if predict_completion > 0 else "Missing"),
            "status_class": "intro-dna-status-found" if predict_completion >= 60 else ("intro-dna-status-partial" if predict_completion > 0 else "intro-dna-status-missing"),
            "detail_lines": predict_detail,
            "completion": predict_completion,
        })

        # ---------------------------------------------------------------
        # LAG 7: SELF-OPTIMIZING -- 3-pass status from sejrliste data
        # ---------------------------------------------------------------
        opt_detail = []
        opt_completion = 0.0

        # Check for 3-pass system evidence in sejrliste data
        sejr_path = SYSTEM_PATH
        active_dir = sejr_path / "10_ACTIVE"
        three_pass_count = 0
        total_active = 0

        if active_dir.exists():
            for item in active_dir.iterdir():
                if item.is_dir():
                    total_active += 1
                    status_yaml = item / "STATUS.yaml"
                    sejr_liste = item / "SEJR_LISTE.md"
                    claude_md = item / "CLAUDE.md"
                    if status_yaml.exists() or claude_md.exists():
                        three_pass_count += 1

            opt_detail.append(f"Active sejrlister: {total_active}")
            opt_detail.append(f"With 3-pass tracking: {three_pass_count}")

            if total_active > 0:
                # Check for alternatives/optimization tracking
                alt_count = 0
                for item in active_dir.iterdir():
                    if item.is_dir():
                        alt_dir = item / "ALTERNATIVES"
                        if alt_dir.exists():
                            alt_count += len(list(alt_dir.iterdir()))
                if alt_count > 0:
                    opt_detail.append(f"Alternative evaluations: {alt_count}")

                opt_completion = min(100.0, (three_pass_count / max(total_active, 1)) * 100.0)
            else:
                opt_detail.append("No active sejrlister for 3-pass analysis")
                opt_completion = 0.0
        else:
            opt_detail.append("10_ACTIVE/ directory not found")
            opt_completion = 0.0

        # Also check for navigation index (optimization artifact)
        nav_index = intro_path / "NAVIGATION_INDEX.md"
        if nav_index.exists():
            try:
                content = nav_index.read_text(encoding="utf-8", errors="replace")
                nav_lines = len(content.splitlines())
                opt_detail.append(f"NAVIGATION_INDEX.md: {nav_lines} lines (optimization index)")
                opt_completion = min(100.0, opt_completion + 15.0)
            except Exception:
                pass

        layers.append({
            "layer_num": "7",
            "name": "SELF-OPTIMIZING",
            "icon": "preferences-other-symbolic",
            "status": "Found" if opt_completion >= 60 else ("Partial" if opt_completion > 0 else "Missing"),
            "status_class": "intro-dna-status-found" if opt_completion >= 60 else ("intro-dna-status-partial" if opt_completion > 0 else "intro-dna-status-missing"),
            "detail_lines": opt_detail,
            "completion": opt_completion,
        })

        return layers

    def _build_dna_layer_card(self, ld: dict) -> Gtk.Box:
        """Build a single DNA layer card widget.

        Args:
            ld: Dict with layer_num, name, icon, status, status_class,
                detail_lines, completion
        """
        is_active = ld["completion"] >= 60.0
        is_missing = ld["completion"] == 0.0

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("intro-dna-card")
        if is_active:
            card.add_css_class("intro-dna-card-active")
        elif is_missing:
            card.add_css_class("intro-dna-card-missing")

        # --- Top row: number, name, status badge ---
        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        # Layer number circle
        num_label = Gtk.Label(label=ld["layer_num"])
        num_label.add_css_class("intro-dna-layer-num")
        if is_active:
            num_label.add_css_class("intro-dna-layer-num-active")
        num_label.set_size_request(36, 36)
        num_label.set_valign(Gtk.Align.CENTER)
        top_row.append(num_label)

        # Icon
        icon = Gtk.Image.new_from_icon_name(ld["icon"])
        icon.set_pixel_size(20)
        icon.set_valign(Gtk.Align.CENTER)
        top_row.append(icon)

        # Name
        name_label = Gtk.Label(label=f"Lag {ld['layer_num']}: {ld['name']}")
        name_label.add_css_class("intro-dna-layer-name")
        name_label.set_xalign(0)
        name_label.set_hexpand(True)
        name_label.set_valign(Gtk.Align.CENTER)
        top_row.append(name_label)

        # Completion percentage
        pct_label = Gtk.Label(label=f"{ld['completion']:.0f}%")
        pct_label.add_css_class("caption")
        pct_label.add_css_class("accent")
        pct_label.set_valign(Gtk.Align.CENTER)
        top_row.append(pct_label)

        # Status badge
        status_badge = Gtk.Label(label=ld["status"])
        status_badge.add_css_class("intro-dna-layer-status")
        status_badge.add_css_class(ld["status_class"])
        status_badge.set_valign(Gtk.Align.CENTER)
        top_row.append(status_badge)

        card.append(top_row)

        # --- Progress bar ---
        prog_bar = Gtk.ProgressBar()
        prog_bar.set_fraction(ld["completion"] / 100.0)
        prog_bar.add_css_class("intro-dna-progress")
        if is_active:
            prog_bar.add_css_class("intro-dna-progress-active")
        card.append(prog_bar)

        # --- Detail lines ---
        if ld["detail_lines"]:
            details_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            details_box.set_margin_top(4)

            for detail_text in ld["detail_lines"]:
                detail_label = Gtk.Label(label=detail_text)
                detail_label.add_css_class("intro-dna-layer-detail")
                detail_label.set_xalign(0)
                detail_label.set_ellipsize(Pango.EllipsizeMode.END)
                details_box.append(detail_label)

            card.append(details_box)

        return card

    # -----------------------------------------------------------------
    # HEALTH VIEW (Live verification status)
    # -----------------------------------------------------------------

    def _build_health_view(self):
        """Build the system health verification dashboard."""
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        title = Gtk.Label(label="INTRO System Health")
        title.add_css_class("intro-view-header")
        title.set_xalign(0)
        header_box.append(title)

        subtitle = Gtk.Label(label="Live verification status for the MASTER FOLDERS(INTRO) system")
        subtitle.add_css_class("intro-view-subtitle")
        subtitle.set_xalign(0)
        subtitle.set_wrap(True)
        header_box.append(subtitle)
        self._container.append(header_box)

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(4)
        sep.set_margin_bottom(4)
        self._container.append(sep)

        # Run health checks
        report = intro_integration.get_intro_health()

        # Score display
        score_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        score_box.set_halign(Gtk.Align.CENTER)
        score_box.set_margin_top(16)
        score_box.set_margin_bottom(16)

        score_label = Gtk.Label(label=f"{report.overall_score:.0f}%")
        score_label.add_css_class("intro-health-score")
        if report.overall_score >= 80:
            score_label.add_css_class("intro-health-pass")
        elif report.overall_score >= 50:
            score_label.add_css_class("intro-health-warn")
        else:
            score_label.add_css_class("intro-health-fail")
        score_box.append(score_label)

        score_meta_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        score_meta_box.set_valign(Gtk.Align.CENTER)

        passed_count = sum(1 for c in report.checks if c.passed)
        total_count = len(report.checks)
        passed_label = Gtk.Label(label=f"{passed_count}/{total_count} checks passed")
        passed_label.add_css_class("caption")
        score_meta_box.append(passed_label)

        ts_label = Gtk.Label(label=f"Checked: {report.timestamp[:19]}")
        ts_label.add_css_class("caption")
        ts_label.add_css_class("dim-label")
        score_meta_box.append(ts_label)

        score_box.append(score_meta_box)
        self._container.append(score_box)

        # Refresh button
        refresh_btn = Gtk.Button(label="Re-run Health Checks")
        refresh_btn.add_css_class("suggested-action")
        refresh_btn.add_css_class("pill")
        refresh_btn.set_halign(Gtk.Align.CENTER)
        refresh_btn.connect("clicked", lambda b: self.show_category("health"))
        self._container.append(refresh_btn)

        # Individual checks
        checks_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        checks_box.set_margin_top(12)

        for check in report.checks:
            check_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            check_row.add_css_class("intro-check-row")
            if check.passed:
                check_row.add_css_class("intro-check-pass")
            else:
                check_row.add_css_class("intro-check-fail")

            # Status icon
            icon_name = "emblem-ok-symbolic" if check.passed else "dialog-error-symbolic"
            icon = Gtk.Image.new_from_icon_name(icon_name)
            if check.passed:
                icon.add_css_class("success")
            else:
                icon.add_css_class("error")
            icon.set_valign(Gtk.Align.CENTER)
            check_row.append(icon)

            # Check info
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
            info_box.set_hexpand(True)

            name = Gtk.Label(label=check.check_name)
            name.set_xalign(0)
            name.add_css_class("intro-file-title")
            info_box.append(name)

            msg = Gtk.Label(label=check.message)
            msg.set_xalign(0)
            msg.add_css_class("intro-file-meta")
            msg.set_ellipsize(Pango.EllipsizeMode.END)
            info_box.append(msg)

            # Show details if any
            if check.details:
                details_text = ", ".join(check.details[:5])
                if len(check.details) > 5:
                    details_text += f" (+{len(check.details) - 5} more)"
                details = Gtk.Label(label=details_text)
                details.set_xalign(0)
                details.add_css_class("caption")
                details.add_css_class("dim-label")
                details.set_wrap(True)
                info_box.append(details)

            check_row.append(info_box)

            # Pass/Fail badge
            badge = Gtk.Label(label="PASS" if check.passed else "FAIL")
            badge.add_css_class("intro-status-badge")
            badge.add_css_class("intro-status-complete" if check.passed else "error")
            badge.set_valign(Gtk.Align.CENTER)
            check_row.append(badge)

            checks_box.append(check_row)

        self._container.append(checks_box)

    # -----------------------------------------------------------------
    # FASE 6: QUICK ACTIONS PANEL
    # -----------------------------------------------------------------

    def _build_quick_actions_view(self):
        """Build the Quick Actions panel with Terminal Commands and Environment Config.

        Terminal Commands section:
          - Groups commands by system: Cirkelline, Cosmic, CKC, Kommandor, Docker, DB
          - Shows command text + Copy button + Run in Terminal button
          - Only the top 3-5 most important per category
          - Sourced from B-files in MASTER FOLDERS(INTRO)/PROJEKTS TERMINALS/

        Environment Config section:
          - Shows environment overview: Redis, RabbitMQ, Docker, PostgreSQL, AWS
          - Status indicator per service (checks if service is running)
          - "Check Status" button per service
          - Sourced from C-files in MASTER FOLDERS(INTRO)/PROJEKTS LOKAL ENV/
        """

        # --- Header ---
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        title = Gtk.Label(label="Quick Actions")
        title.add_css_class("intro-view-header")
        title.set_xalign(0)
        header_box.append(title)

        subtitle = Gtk.Label(
            label="Terminal commands and environment status -- sourced from B-files and C-files in MASTER FOLDERS(INTRO)"
        )
        subtitle.add_css_class("intro-view-subtitle")
        subtitle.set_xalign(0)
        subtitle.set_wrap(True)
        header_box.append(subtitle)
        self._container.append(header_box)

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(4)
        sep.set_margin_bottom(8)
        self._container.append(sep)

        # ============================================================
        # SECTION 1: TERMINAL COMMANDS (from B-files)
        # ============================================================
        term_header = Gtk.Label(label="Terminal Commands")
        term_header.add_css_class("intro-qa-section-header")
        term_header.set_xalign(0)
        term_header.set_margin_top(8)
        self._container.append(term_header)

        term_desc = Gtk.Label(
            label="Top 3-5 essential commands per system -- Copy to clipboard or run directly in terminal"
        )
        term_desc.add_css_class("intro-file-meta")
        term_desc.set_xalign(0)
        term_desc.set_margin_bottom(8)
        self._container.append(term_desc)

        # Define command groups sourced from B1-B6 files
        command_groups = self._get_terminal_command_groups()

        for group in command_groups:
            group_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            group_box.set_margin_top(8)
            group_box.set_margin_bottom(4)

            # System name header with color
            sys_label = Gtk.Label()
            sys_label.set_markup(
                f'<span weight="bold" font_family="JetBrains Mono">{GLib.markup_escape_text(group["name"])}</span>'
                f'  <span size="small" foreground="#64748b">({group["source"]})</span>'
            )
            sys_label.add_css_class("intro-qa-system-label")
            sys_label.add_css_class(f'intro-qa-system-{group["css_class"]}')
            sys_label.set_xalign(0)
            group_box.append(sys_label)

            # Command cards
            for cmd in group["commands"]:
                cmd_card = self._build_command_card(cmd["description"], cmd["command"])
                group_box.append(cmd_card)

            self._container.append(group_box)

        # Separator between sections
        mid_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        mid_sep.set_margin_top(16)
        mid_sep.set_margin_bottom(8)
        self._container.append(mid_sep)

        # ============================================================
        # SECTION 2: ENVIRONMENT CONFIG (from C-files)
        # ============================================================
        env_header = Gtk.Label(label="Environment Status")
        env_header.add_css_class("intro-qa-section-header")
        env_header.set_xalign(0)
        env_header.set_margin_top(8)
        self._container.append(env_header)

        env_desc = Gtk.Label(
            label="Service status overview -- Redis, RabbitMQ, Docker, PostgreSQL, AWS (from C-files)"
        )
        env_desc.add_css_class("intro-file-meta")
        env_desc.set_xalign(0)
        env_desc.set_margin_bottom(8)
        self._container.append(env_desc)

        # Check All button
        check_all_btn = Gtk.Button(label="Check All Services")
        check_all_btn.add_css_class("suggested-action")
        check_all_btn.add_css_class("pill")
        check_all_btn.set_halign(Gtk.Align.START)
        check_all_btn.set_margin_bottom(12)
        self._container.append(check_all_btn)

        # Environment service cards
        env_services = self._get_environment_services()

        self._env_status_labels = {}
        env_grid = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        for svc in env_services:
            svc_card = self._build_env_service_card(svc)
            env_grid.append(svc_card)

        self._container.append(env_grid)

        # Connect Check All button
        check_all_btn.connect("clicked", lambda b: self._check_all_services(env_services))

    def _get_terminal_command_groups(self) -> list:
        """Return the top 3-5 essential commands per system, sourced from B-files."""
        return [
            {
                "name": "Cirkelline System",
                "source": "B1",
                "css_class": "cirkelline",
                "commands": [
                    {
                        "description": "Start backend (Port 7777)",
                        "command": "cd /home/rasmus/Desktop/projekts/projects/cirkelline-kv1ntos && source .venv/bin/activate && python my_os.py",
                    },
                    {
                        "description": "Start frontend (Port 3000)",
                        "command": "cd /home/rasmus/Desktop/projekts/projects/cirkelline-kv1ntos/cirkelline-ui && pnpm dev",
                    },
                    {
                        "description": "Health check",
                        "command": "curl http://localhost:7777/health",
                    },
                    {
                        "description": "Check port usage",
                        "command": "lsof -i :7777",
                    },
                ],
            },
            {
                "name": "Cosmic Library",
                "source": "B2",
                "css_class": "cosmic",
                "commands": [
                    {
                        "description": "Start backend (Port 7778)",
                        "command": "cd /home/rasmus/Desktop/projekts/projects/cosmic-library/backend && source venv/bin/activate && python main.py",
                    },
                    {
                        "description": "Start frontend (Port 3001)",
                        "command": "cd /home/rasmus/Desktop/projekts/projects/cosmic-library/frontend && pnpm dev",
                    },
                    {
                        "description": "Health check",
                        "command": "curl http://localhost:7778/health",
                    },
                    {
                        "description": "List training rooms",
                        "command": "curl http://localhost:7778/api/training/rooms",
                    },
                ],
            },
            {
                "name": "CKC Gateway",
                "source": "B3",
                "css_class": "ckc",
                "commands": [
                    {
                        "description": "Start backend (Port 7779)",
                        "command": "cd /home/rasmus/Desktop/projekts/projects/lib-admin/backend && source venv/bin/activate && python main.py",
                    },
                    {
                        "description": "Health check",
                        "command": "curl http://localhost:7779/health",
                    },
                    {
                        "description": "Agent Registry stats",
                        "command": "curl http://localhost:7779/api/agents/registry/stats/summary",
                    },
                    {
                        "description": "Event Bus health",
                        "command": "curl http://localhost:7779/api/events/health",
                    },
                ],
            },
            {
                "name": "Kommandor Gateway",
                "source": "B4",
                "css_class": "kommandor",
                "commands": [
                    {
                        "description": "Start main gateway (Port 7800)",
                        "command": "cd /home/rasmus/Desktop/projekts/projects/kommandor-og-agenter/backend && uvicorn api_gateway.main:app --host 0.0.0.0 --port 7800",
                    },
                    {
                        "description": "Health check",
                        "command": "curl http://localhost:7800/health",
                    },
                    {
                        "description": "List all agents (21)",
                        "command": "curl http://localhost:7800/api/agents/list",
                    },
                    {
                        "description": "Check specialist services (8001-8009)",
                        "command": "for port in $(seq 8001 8009); do echo -n \"Port $port: \"; lsof -i :$port > /dev/null 2>&1 && echo 'Running' || echo 'Stopped'; done",
                    },
                ],
            },
            {
                "name": "Docker Infrastructure",
                "source": "B5",
                "css_class": "docker",
                "commands": [
                    {
                        "description": "List all containers with status",
                        "command": "docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'",
                    },
                    {
                        "description": "Start all containers",
                        "command": "docker start $(docker ps -aq)",
                    },
                    {
                        "description": "Check resource usage",
                        "command": "docker stats --no-stream --format 'table {{.Name}}\\t{{.CPUPerc}}\\t{{.MemUsage}}'",
                    },
                    {
                        "description": "Count running containers",
                        "command": "docker ps -q | wc -l",
                    },
                ],
            },
            {
                "name": "Database Operations",
                "source": "B6",
                "css_class": "db",
                "commands": [
                    {
                        "description": "Check all PostgreSQL databases",
                        "command": "for db in cirkelline-postgres cosmic-library-postgres kommandor-postgres; do echo -n \"$db: \"; docker exec $db pg_isready 2>/dev/null && echo 'Ready' || echo 'Not ready'; done",
                    },
                    {
                        "description": "Check all Redis instances",
                        "command": "for r in cirkelline-redis cosmic-library-redis cc-redis; do echo -n \"$r: \"; docker exec $r redis-cli ping 2>/dev/null || echo 'No response'; done",
                    },
                    {
                        "description": "Connect to Cirkelline DB",
                        "command": "docker exec -it cirkelline-postgres psql -U cirkelline -d cirkelline",
                    },
                    {
                        "description": "Backup all PostgreSQL databases",
                        "command": "for db in cirkelline-postgres cosmic-library-postgres kommandor-postgres; do docker exec $db pg_dump -U $(docker exec $db psql -U postgres -tAc \"SELECT usename FROM pg_user LIMIT 1;\") > backup_${db}_$(date +%Y%m%d).sql; done",
                    },
                ],
            },
        ]

    def _build_command_card(self, description: str, command: str) -> Gtk.Box:
        """Build a single command card with description, command text, Copy, and Run buttons."""
        card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        card.add_css_class("intro-qa-cmd-card")

        # Left side: description + command text
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_box.set_hexpand(True)

        desc_label = Gtk.Label(label=description)
        desc_label.add_css_class("intro-qa-cmd-desc")
        desc_label.set_xalign(0)
        info_box.append(desc_label)

        cmd_label = Gtk.Label(label=command)
        cmd_label.add_css_class("intro-qa-cmd-text")
        cmd_label.set_xalign(0)
        cmd_label.set_ellipsize(Pango.EllipsizeMode.END)
        cmd_label.set_max_width_chars(80)
        cmd_label.set_selectable(True)
        info_box.append(cmd_label)

        card.append(info_box)

        # Right side: buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        btn_box.set_valign(Gtk.Align.CENTER)

        # Copy button
        copy_btn = Gtk.Button()
        copy_btn.set_icon_name("edit-copy-symbolic")
        copy_btn.set_tooltip_text("Copy command to clipboard")
        copy_btn.add_css_class("intro-qa-copy-btn")
        copy_btn.add_css_class("flat")
        copy_btn.connect("clicked", lambda b, c=command: self._copy_to_clipboard(c, b))
        btn_box.append(copy_btn)

        # Run in Terminal button
        run_btn = Gtk.Button()
        run_btn.set_icon_name("media-playback-start-symbolic")
        run_btn.set_tooltip_text("Run in terminal")
        run_btn.add_css_class("intro-qa-run-btn")
        run_btn.add_css_class("flat")
        run_btn.connect("clicked", lambda b, c=command: self._run_in_terminal(c))
        btn_box.append(run_btn)

        card.append(btn_box)

        return card

    def _copy_to_clipboard(self, text: str, button: Gtk.Button):
        """Copy text to clipboard using Wayland-compatible method."""
        try:
            display = Gdk.Display.get_default()
            clipboard = display.get_clipboard()
            clipboard.set(text)
            # Visual feedback -- temporarily change icon
            button.set_icon_name("emblem-ok-symbolic")
            GLib.timeout_add(1500, lambda: button.set_icon_name("edit-copy-symbolic") or False)
        except Exception as e:
            print(f"Clipboard error: {e}")

    def _run_in_terminal(self, command: str):
        """Open a terminal and run the command."""
        try:
            # Try various terminal emulators
            terminals = [
                ["gnome-terminal", "--", "bash", "-c", f"{command}; echo ''; echo 'Press Enter to close...'; read"],
                ["kgx", "-e", f"bash -c \"{command}; echo ''; echo 'Press Enter to close...'; read\""],
                ["xterm", "-e", f"bash -c \"{command}; echo ''; echo 'Press Enter to close...'; read\""],
            ]
            for term_cmd in terminals:
                try:
                    subprocess.Popen(term_cmd)
                    return
                except FileNotFoundError:
                    continue
            # Fallback: try xdg-open with a shell script
            print(f"No terminal emulator found to run: {command}")
        except Exception as e:
            print(f"Terminal launch error: {e}")

    def _get_environment_services(self) -> list:
        """Return environment service definitions sourced from C-files."""
        return [
            {
                "name": "Redis (Cirkelline)",
                "source": "C5",
                "port": 6379,
                "container": "cirkelline-redis",
                "check_cmd": ["docker", "exec", "cirkelline-redis", "redis-cli", "ping"],
                "check_expect": "PONG",
                "detail": "Port 6379 -- Cirkelline Cache + Event Bus",
                "icon": "network-server-symbolic",
            },
            {
                "name": "Redis (Cosmic Library)",
                "source": "C5",
                "port": 6381,
                "container": "cosmic-library-redis",
                "check_cmd": ["docker", "exec", "cosmic-library-redis", "redis-cli", "ping"],
                "check_expect": "PONG",
                "detail": "Port 6381 -- Cosmic Cache + Job Queue",
                "icon": "network-server-symbolic",
            },
            {
                "name": "Redis (Kommandor/CC)",
                "source": "C5",
                "port": 6380,
                "container": "cc-redis",
                "check_cmd": ["docker", "exec", "cc-redis", "redis-cli", "ping"],
                "check_expect": "PONG",
                "detail": "Port 6380 -- Commando Center Cache",
                "icon": "network-server-symbolic",
            },
            {
                "name": "RabbitMQ",
                "source": "C6",
                "port": 5672,
                "container": "rabbitmq",
                "check_cmd": ["docker", "ps", "--filter", "name=rabbit", "--format", "{{.Names}}"],
                "check_expect": "rabbit",
                "detail": "Port 5672 -- AMQP Message Queue (PLANNED, not deployed)",
                "icon": "mail-send-symbolic",
                "note": "Configured in .env but container not yet deployed",
            },
            {
                "name": "Docker Engine",
                "source": "C7",
                "port": None,
                "container": None,
                "check_cmd": ["docker", "info", "--format", "{{.ContainersRunning}}"],
                "check_expect": None,
                "detail": "18 containers expected -- 7 PostgreSQL, 3 Redis, 3 Monitoring, 5 CC",
                "icon": "application-x-executable-symbolic",
            },
            {
                "name": "PostgreSQL (Cirkelline)",
                "source": "C8",
                "port": 5533,
                "container": "cirkelline-postgres",
                "check_cmd": ["docker", "exec", "cirkelline-postgres", "pg_isready", "-U", "cirkelline"],
                "check_expect": "accepting connections",
                "detail": "Port 5533 -- pgvector PG15 -- cirkelline_db",
                "icon": "drive-harddisk-symbolic",
            },
            {
                "name": "PostgreSQL (Cosmic Library)",
                "source": "C8",
                "port": 5534,
                "container": "cosmic-library-postgres",
                "check_cmd": ["docker", "exec", "cosmic-library-postgres", "pg_isready", "-U", "cosmic_library"],
                "check_expect": "accepting connections",
                "detail": "Port 5534 -- PG17 -- 53 tables",
                "icon": "drive-harddisk-symbolic",
            },
            {
                "name": "PostgreSQL (Kommandor)",
                "source": "C8",
                "port": 5535,
                "container": "kommandor-postgres",
                "check_cmd": ["docker", "exec", "kommandor-postgres", "pg_isready", "-U", "kommandor"],
                "check_expect": "accepting connections",
                "detail": "Port 5535 -- PG15 -- 127.0.0.1 only",
                "icon": "drive-harddisk-symbolic",
            },
            {
                "name": "AWS / LocalStack",
                "source": "C9",
                "port": 4566,
                "container": "localstack",
                "check_cmd": ["docker", "ps", "--filter", "name=localstack", "--format", "{{.Names}}"],
                "check_expect": "localstack",
                "detail": "Port 4566 -- Local AWS simulation (PLANNED, not deployed)",
                "icon": "weather-overcast-symbolic",
                "note": "Configured in .env but container not yet deployed",
            },
            {
                "name": "Grafana (Monitoring)",
                "source": "C7",
                "port": 3030,
                "container": "cirkelline-grafana",
                "check_cmd": ["docker", "ps", "--filter", "name=cirkelline-grafana", "--format", "{{.Status}}"],
                "check_expect": "Up",
                "detail": "Port 3030 -- Metrics visualization",
                "icon": "utilities-system-monitor-symbolic",
            },
            {
                "name": "Loki (Log Aggregation)",
                "source": "C7",
                "port": 3100,
                "container": "cirkelline-loki",
                "check_cmd": ["docker", "ps", "--filter", "name=cirkelline-loki", "--format", "{{.Status}}"],
                "check_expect": "Up",
                "detail": "Port 3100 -- Log aggregation for all platforms",
                "icon": "utilities-system-monitor-symbolic",
            },
        ]

    def _build_env_service_card(self, svc: dict) -> Gtk.Box:
        """Build an environment service card with status indicator and Check button."""
        card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        card.add_css_class("intro-qa-env-card")

        # Icon
        icon = Gtk.Image.new_from_icon_name(svc.get("icon", "network-server-symbolic"))
        icon.set_pixel_size(24)
        icon.set_valign(Gtk.Align.CENTER)
        card.append(icon)

        # Info column
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_box.set_hexpand(True)

        name_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        name_label = Gtk.Label(label=svc["name"])
        name_label.add_css_class("intro-qa-env-name")
        name_label.set_xalign(0)
        name_row.append(name_label)

        source_label = Gtk.Label(label=f"({svc['source']})")
        source_label.add_css_class("dim-label")
        source_label.add_css_class("caption")
        source_label.set_valign(Gtk.Align.CENTER)
        name_row.append(source_label)

        info_box.append(name_row)

        detail_label = Gtk.Label(label=svc["detail"])
        detail_label.add_css_class("intro-qa-env-detail")
        detail_label.set_xalign(0)
        detail_label.set_ellipsize(Pango.EllipsizeMode.END)
        info_box.append(detail_label)

        if svc.get("note"):
            note_label = Gtk.Label(label=svc["note"])
            note_label.add_css_class("caption")
            note_label.add_css_class("dim-label")
            note_label.set_xalign(0)
            info_box.append(note_label)

        card.append(info_box)

        # Status indicator
        status_label = Gtk.Label(label="--")
        status_label.add_css_class("intro-qa-status-unknown")
        status_label.set_valign(Gtk.Align.CENTER)
        status_label.set_width_chars(12)
        card.append(status_label)

        # Store reference for updating
        svc_key = svc["name"].replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        self._env_status_labels[svc_key] = status_label

        # Check Status button
        check_btn = Gtk.Button(label="Check")
        check_btn.add_css_class("intro-qa-check-btn")
        check_btn.add_css_class("flat")
        check_btn.set_valign(Gtk.Align.CENTER)
        check_btn.connect("clicked", lambda b, s=svc, lbl=status_label: self._check_service_status(s, lbl, b))
        card.append(check_btn)

        return card

    def _check_service_status(self, svc: dict, status_label: Gtk.Label, button: Gtk.Button):
        """Check the status of a single service and update the label."""
        button.set_sensitive(False)
        status_label.set_label("Checking...")

        # Run check in a thread to avoid blocking UI
        import threading

        def _do_check():
            result_text = "Unknown"
            result_class = "intro-qa-status-unknown"

            try:
                result = subprocess.run(
                    svc["check_cmd"],
                    capture_output=True, text=True, timeout=10,
                )
                output = result.stdout.strip()

                if svc.get("check_expect") is None:
                    # Docker Engine special case -- just check if it returned a number
                    if output and output.isdigit():
                        count = int(output)
                        result_text = f"Running ({count})"
                        result_class = "intro-qa-status-running" if count > 0 else "intro-qa-status-stopped"
                    elif result.returncode == 0:
                        result_text = "Running"
                        result_class = "intro-qa-status-running"
                    else:
                        result_text = "Stopped"
                        result_class = "intro-qa-status-stopped"
                elif svc["check_expect"] in output:
                    result_text = "Running"
                    result_class = "intro-qa-status-running"
                elif result.returncode == 0 and output:
                    result_text = "Partial"
                    result_class = "intro-qa-status-configured"
                else:
                    result_text = "Stopped"
                    result_class = "intro-qa-status-stopped"

            except subprocess.TimeoutExpired:
                result_text = "Timeout"
                result_class = "intro-qa-status-unknown"
            except FileNotFoundError:
                result_text = "N/A"
                result_class = "intro-qa-status-unknown"
            except Exception:
                result_text = "Error"
                result_class = "intro-qa-status-stopped"

            # Update UI on main thread
            GLib.idle_add(lambda: self._update_status_label(status_label, button, result_text, result_class) or False)

        thread = threading.Thread(target=_do_check, daemon=True)
        thread.start()

    def _update_status_label(self, label: Gtk.Label, button: Gtk.Button, text: str, css_class: str):
        """Update a status label on the main thread."""
        # Remove old status classes
        for old_cls in ("intro-qa-status-running", "intro-qa-status-stopped",
                        "intro-qa-status-unknown", "intro-qa-status-configured"):
            label.remove_css_class(old_cls)
        label.add_css_class(css_class)
        label.set_label(text)
        button.set_sensitive(True)

    def _check_all_services(self, services: list):
        """Check all services sequentially."""
        for svc in services:
            svc_key = svc["name"].replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
            if svc_key in self._env_status_labels:
                status_label = self._env_status_labels[svc_key]
                # Create a dummy button for the callback
                dummy_btn = Gtk.Button()
                self._check_service_status(svc, status_label, dummy_btn)

    # -----------------------------------------------------------------
    # UTILITY
    # -----------------------------------------------------------------

    def _open_file(self, path: str):
        """Open a file in the default system editor."""
        try:
            subprocess.Popen(["xdg-open", path])
        except Exception as e:
            print(f"Could not open file: {e}")


#
# MAIN WINDOW
#

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
        self._drag_history = []  # Undo stack for drag operations
        self._selected_rows = set()  # Multi-select tracking
        self._active_drag_row = None  # Currently dragged row

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

        # Wrap in toast overlay (REQUIRED for toasts to work) then konfetti
        self._toast_overlay = Adw.ToastOverlay()
        self.konfetti.set_child(main_box)
        self._toast_overlay.set_child(self.konfetti)
        self.set_content(self._toast_overlay)

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

        self.filter_active = Gtk.ToggleButton(label=" Active")
        self.filter_active.add_css_class("filter-chip")
        self.filter_active.connect("toggled", lambda b: self._apply_filter("active"))
        self.filter_bar.append(self.filter_active)

        self.filter_archived = Gtk.ToggleButton(label=" Arkiv")
        self.filter_archived.add_css_class("filter-chip")
        self.filter_archived.connect("toggled", lambda b: self._apply_filter("archived"))
        self.filter_bar.append(self.filter_archived)

        # Sort dropdown
        sort_model = Gtk.StringList.new([" Date", " Score", " Name"])
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

        # === INTRO SYSTEM SIDEBAR SECTION ===
        intro_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        intro_sep.set_margin_top(8)
        sidebar_box.append(intro_sep)

        # Section header
        intro_header = Gtk.Label(label="INTRO SYSTEM")
        intro_header.add_css_class("intro-section-header")
        intro_header.set_xalign(0)
        sidebar_box.append(intro_header)

        # Build INTRO sidebar items from INTRO_SIDEBAR_ITEMS
        # Each item: (key, label, range_text, icon_name)
        self._intro_sidebar_btns = {}

        # Pre-fetch category data for file counts and dates
        try:
            intro_summary = intro_integration.get_intro_summary()
            intro_cats = intro_integration.get_intro_categories()
            intro_cat_dict = {cat.letter: cat for cat in intro_cats}
        except Exception:
            intro_summary = {"available": False}
            intro_cat_dict = {}

        for cat_key, cat_label, cat_range, cat_icon in INTRO_SIDEBAR_ITEMS:
            btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            btn_box.set_margin_start(12)
            btn_box.set_margin_end(12)
            btn_box.set_margin_top(2)
            btn_box.set_margin_bottom(2)

            btn = Gtk.Button()
            btn.set_hexpand(True)
            btn.add_css_class("flat")
            btn.add_css_class("intro-sidebar-btn")
            btn.add_css_class(f"intro-cat-{cat_key}")

            btn_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

            icon = Gtk.Image.new_from_icon_name(cat_icon)
            icon.add_css_class("intro-sidebar-icon")
            btn_content.append(icon)

            # Label + date column
            label_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
            label_box.set_hexpand(True)

            name_label = Gtk.Label(label=cat_label)
            name_label.add_css_class("intro-sidebar-label")
            name_label.set_xalign(0)
            name_label.set_ellipsize(Pango.EllipsizeMode.END)
            label_box.append(name_label)

            # Last updated date
            date_text = ""
            if cat_key in intro_cat_dict:
                lm = intro_cat_dict[cat_key].latest_modified
                if lm:
                    date_text = f"Updated: {lm[:10]}"
            elif cat_key == "structure":
                date_text = f"{cat_range}"
            elif cat_key == "system_functions":
                date_text = f"{cat_range}"
            elif cat_key == "health":
                date_text = f"{cat_range}"
            elif cat_key == "dna_layers":
                date_text = f"{cat_range}"

            if date_text:
                date_label = Gtk.Label(label=date_text)
                date_label.add_css_class("intro-sidebar-date")
                date_label.set_xalign(0)
                label_box.append(date_label)

            btn_content.append(label_box)

            # File count badge
            count_text = ""
            if cat_key in intro_cat_dict:
                count_text = str(intro_cat_dict[cat_key].file_count)
            elif cat_key == "structure":
                if intro_summary.get("available"):
                    count_text = str(len(intro_integration.get_intro_structure().get("subdirectories", [])))
            elif cat_key == "system_functions":
                count_text = "5"
            elif cat_key == "health":
                count_text = "..."
            elif cat_key == "dna_layers":
                count_text = "7"

            if count_text:
                count_label = Gtk.Label(label=count_text)
                count_label.add_css_class("intro-sidebar-count")
                btn_content.append(count_label)

            btn.set_child(btn_content)
            btn.connect("clicked", self._on_intro_sidebar_clicked, cat_key)
            btn_box.append(btn)

            self._intro_sidebar_btns[cat_key] = btn
            sidebar_box.append(btn_box)

        # === LINEN HEALTH BUTTON (INTRO System) ===
        linen_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        linen_sep.set_margin_top(8)
        sidebar_box.append(linen_sep)

        linen_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        linen_btn_box.set_margin_start(12)
        linen_btn_box.set_margin_end(12)
        linen_btn_box.set_margin_top(8)
        linen_btn_box.set_margin_bottom(8)

        linen_btn = Gtk.Button()
        linen_btn.set_hexpand(True)
        linen_btn.add_css_class("flat")

        linen_btn_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        linen_icon = Gtk.Image.new_from_icon_name("applications-science-symbolic")
        linen_btn_content.append(linen_icon)

        linen_text = Gtk.Label(label="LINEN Health")
        linen_text.set_hexpand(True)
        linen_text.set_halign(Gtk.Align.START)
        linen_btn_content.append(linen_text)

        self.linen_score_label = Gtk.Label(label="...")
        self.linen_score_label.add_css_class("caption")
        linen_btn_content.append(self.linen_score_label)

        linen_btn.set_child(linen_btn_content)
        linen_btn.connect("clicked", self._on_linen_clicked)
        linen_btn_box.append(linen_btn)

        sidebar_box.append(linen_btn_box)

        # === ARCHITECTURE BUTTON (INTRO System) ===
        arch_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        arch_btn_box.set_margin_start(12)
        arch_btn_box.set_margin_end(12)
        arch_btn_box.set_margin_bottom(8)

        arch_btn = Gtk.Button()
        arch_btn.set_hexpand(True)
        arch_btn.add_css_class("flat")

        arch_btn_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        arch_icon = Gtk.Image.new_from_icon_name("view-grid-symbolic")
        arch_btn_content.append(arch_icon)

        arch_text = Gtk.Label(label="3-Lags Arkitektur")
        arch_text.set_hexpand(True)
        arch_text.set_halign(Gtk.Align.START)
        arch_btn_content.append(arch_text)

        arch_btn.set_child(arch_btn_content)
        arch_btn.connect("clicked", self._on_architecture_clicked)
        arch_btn_box.append(arch_btn)

        sidebar_box.append(arch_btn_box)

        # Sync Functions button
        sync_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        sync_btn_box.set_margin_start(12)
        sync_btn_box.set_margin_end(12)
        sync_btn_box.set_margin_bottom(8)

        sync_btn = Gtk.Button()
        sync_btn.set_hexpand(True)
        sync_btn.add_css_class("flat")

        sync_btn_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        sync_icon = Gtk.Image.new_from_icon_name("network-transmit-symbolic")
        sync_btn_content.append(sync_icon)

        sync_text = Gtk.Label(label="Sync Functions")
        sync_text.set_xalign(0)
        sync_text.set_hexpand(True)
        sync_btn_content.append(sync_text)

        self.sync_score_label = Gtk.Label(label="...")
        self.sync_score_label.add_css_class("caption")
        sync_btn_content.append(self.sync_score_label)

        sync_btn.set_child(sync_btn_content)
        sync_btn.connect("clicked", self._on_sync_clicked)
        sync_btn_box.append(sync_btn)

        sidebar_box.append(sync_btn_box)

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

        # LINEN Health page (system health dashboard)
        linen_scroll = Gtk.ScrolledWindow()
        linen_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.linen_view = LinenHealthView()
        linen_scroll.set_child(self.linen_view)
        self.content_stack.add_named(linen_scroll, "linen")

        # Architecture Overview page (3-layer architecture dashboard)
        arch_scroll = Gtk.ScrolledWindow()
        arch_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.architecture_view = ArchitectureOverviewView()
        arch_scroll.set_child(self.architecture_view)
        self.content_stack.add_named(arch_scroll, "architecture")

        # Sync Functions page (DEL 21 sync dashboard)
        sync_scroll = Gtk.ScrolledWindow()
        sync_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.sync_view = SyncDashboardView()
        sync_scroll.set_child(self.sync_view)
        self.content_stack.add_named(sync_scroll, "sync")

        # INTRO System page (FASE 1 sidebar integration)
        self.intro_view = IntroSystemView()
        self.content_stack.add_named(self.intro_view, "intro")

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
            (f"{stats['completed_checkboxes']}", " Complete", "intuition"),
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
        tip_label = Gtk.Label(label=" Tip: Brug Ctrl+N for hurtig ny victory")
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

        subtitle = Gtk.Label(label=f"Pass {sejr['current_pass']}/3 • {sejr['date']}")
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

        # 
        # 5W KONTROL PANEL - WHAT/WHERE/WHY/HOW/WHEN
        # 
        w5_group = Adw.PreferencesGroup()
        w5_group.set_title(" 5W KONTROL")
        w5_group.set_description("Alt du behøver at vide om denne victory")

        # WHAT - Formål/beskrivelse (Divine violet)
        hvad_row = Adw.ActionRow()
        hvad_row.set_title(" WHAT")
        hvad_row.set_subtitle(sejr.get("hvad", sejr["display_name"]))
        hvad_icon = Gtk.Image.new_from_icon_name("help-about-symbolic")
        hvad_icon.set_pixel_size(32)
        hvad_row.add_prefix(hvad_icon)
        hvad_row.add_css_class("w5-hvad")
        w5_group.add(hvad_row)

        # WHERE - Lokation (Wisdom gold)
        hvor_row = Adw.ActionRow()
        hvor_row.set_title(" WHERE")
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
        hvorfor_row.set_title(" WHY")
        hvorfor_row.set_subtitle(sejr.get("hvorfor", "Nå Admiral niveau med 30/30 score"))
        hvorfor_icon = Gtk.Image.new_from_icon_name("starred-symbolic")
        hvorfor_icon.set_pixel_size(32)
        hvorfor_row.add_prefix(hvorfor_icon)
        hvorfor_row.add_css_class("w5-hvorfor")
        w5_group.add(hvorfor_row)

        # HOW - Metode (Intuition indigo)
        hvordan_row = Adw.ActionRow()
        hvordan_row.set_title(" HOW")
        pass_status = f"Pass {sejr['current_pass']}/3 • {sejr['progress']}% færdig"
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
        hvornaar_row.set_title(" WHEN")
        hvornaar_row.set_subtitle(f"Oprettet: {sejr['date']} → Mål: Complete i dag")
        hvornaar_icon = Gtk.Image.new_from_icon_name("alarm-symbolic")
        hvornaar_icon.set_pixel_size(32)
        hvornaar_row.add_prefix(hvornaar_icon)
        hvornaar_row.add_css_class("w5-hvornaar")
        w5_group.add(hvornaar_row)

        self.detail_box.append(w5_group)

        # Fremgang sektion
        progress_group = Adw.PreferencesGroup()
        progress_group.set_title(" Fremgang")

        # Hovedfremgangsbar
        progress_row = Adw.ActionRow()
        progress_row.set_title(f"Samlet fremdrift: {sejr['progress']}%")
        progress_row.set_subtitle(f"{sejr['done']}/{sejr['total']} opgaver afkrydset")

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
        folder_btn = Gtk.Button(label=" Open Folder")
        folder_btn.add_css_class("pill")
        folder_btn.connect("clicked", lambda b: subprocess.Popen(["nautilus", sejr["path"]]))
        quick_box.append(folder_btn)

        # Open SEJR_LISTE.md
        sejr_file = Path(sejr["path"]) / "SEJR_LISTE.md"
        if sejr_file.exists():
            edit_btn = Gtk.Button(label=" Rediger Victory")
            edit_btn.add_css_class("pill")
            edit_btn.connect("clicked", lambda b: subprocess.Popen(["xdg-open", str(sejr_file)]))
            quick_box.append(edit_btn)

        # Open terminal in folder
        term_btn = Gtk.Button(label=" Terminal")
        term_btn.add_css_class("pill")
        term_btn.connect("clicked", lambda b: subprocess.Popen(
            ["gnome-terminal", f"--working-directory={sejr['path']}"]
        ))
        quick_box.append(term_btn)

        quick_group.add(quick_box)
        self.detail_box.append(quick_group)

        # Files section
        files_group = Adw.PreferencesGroup()
        files_group.set_title("Files")
        files_group.set_description(f"{len(sejr['files'])} files - klik for at åbne")

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
        chat_group.set_title(" Activity Stream")
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
            self.activity_monitor.log_event("system", f"Indlæste {len(self.sejrs)} victorys", "")

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

        # Update LINEN sidebar score
        if hasattr(self, 'linen_score_label'):
            self._update_linen_sidebar_label()

        # Update Sync sidebar score
        if hasattr(self, 'sync_score_label'):
            self._update_sync_sidebar_label()

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
                active_header = Gtk.Label(label=" AKTIVE")
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
                archive_header = Gtk.Label(label=" ARKIVEREDE")
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
            header_text = " AKTIVE" if self.current_filter == "active" else " ARKIVEREDE"
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

    def _on_linen_clicked(self, button):
        """Navigate to LINEN Health view"""
        # Deselect any selected victory in sidebar
        self.sejr_list.unselect_all()
        # Refresh scores and show LINEN view
        self.linen_view._refresh_scores()
        self.content_stack.set_visible_child_name("linen")
        self.split_view.set_show_content(True)
        # Update sidebar label
        self._update_linen_sidebar_label()

    def _update_linen_sidebar_label(self):
        """Update the LINEN score shown in the sidebar"""
        try:
            overall = get_linen_health()
            self.linen_score_label.set_label(f"{overall:.0f}%")
            for cls in ["success", "warning", "error"]:
                self.linen_score_label.remove_css_class(cls)
            if overall >= 80:
                self.linen_score_label.add_css_class("success")
            elif overall >= 50:
                self.linen_score_label.add_css_class("warning")
            else:
                self.linen_score_label.add_css_class("error")
        except Exception:
            self.linen_score_label.set_label("?")

    def _on_architecture_clicked(self, button):
        """Navigate to Architecture Overview view"""
        self.sejr_list.unselect_all()
        self.content_stack.set_visible_child_name("architecture")
        self.split_view.set_show_content(True)

    def _on_sync_clicked(self, button):
        """Navigate to Sync Functions dashboard"""
        self.sejr_list.unselect_all()
        self.sync_view._on_refresh(button)
        self.content_stack.set_visible_child_name("sync")
        self.split_view.set_show_content(True)
        self._update_sync_sidebar_label()

    def _update_sync_sidebar_label(self):
        """Update the Sync score shown in the sidebar"""
        try:
            health = get_sync_health()
            self.sync_score_label.set_label(f"{health:.0f}%")
            for cls in ["success", "warning", "error"]:
                self.sync_score_label.remove_css_class(cls)
            if health >= 60:
                self.sync_score_label.add_css_class("success")
            elif health >= 30:
                self.sync_score_label.add_css_class("warning")
            else:
                self.sync_score_label.add_css_class("error")
        except Exception:
            self.sync_score_label.set_label("?")

    def _on_intro_sidebar_clicked(self, button, category_key):
        """Navigate to an INTRO system view for the given category."""
        # Deselect any selected victory in sidebar
        self.sejr_list.unselect_all()
        # Show the INTRO view for this category
        self.intro_view.show_category(category_key)
        self.content_stack.set_visible_child_name("intro")
        self.split_view.set_show_content(True)

        # Update health score in sidebar if health category exists
        if category_key == "health" and "health" in self._intro_sidebar_btns:
            try:
                report = intro_integration.get_intro_health()
                # Find the count label in the health button
                btn = self._intro_sidebar_btns["health"]
                # The btn's child is btn_content, find the count label (last child)
                content_box = btn.get_child()
                if content_box:
                    child = content_box.get_last_child()
                    if child and isinstance(child, Gtk.Label):
                        child.set_label(f"{report.overall_score:.0f}%")
            except Exception:
                pass

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
        dialog.set_title(" Universal Victory Converter")
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
        input_group.set_title(" INPUT TYPE")
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
        mode_group.set_title(" KONTROL MODE")
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
        w5_group.set_title(" 5W KONTROL")
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
        name_group.set_title(" SEJR NAVN")

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

        create_btn = Gtk.Button(label=" Create Victory")
        create_btn.add_css_class("suggested-action")
        create_btn.connect("clicked", lambda b: self._execute_conversion(dialog))
        action_bar.append(create_btn)

        main_box.append(action_bar)

        dialog.present()

    def _browse_for_input(self):
        """Open file chooser for input selection"""
        # Use Nautilus to let user copy path
        subprocess.Popen(["nautilus", str(SYSTEM_PATH)])
        send_notification(" File Browser", "Kopiér stien til det du vil konvertere")

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
                    " Victory Oprettet!",
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
        script_path = SCRIPTS_DIR / "generate_sejr.py"
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
                "success_msg": " All tests passed!",
                "title": " Verification",
                "body": "Victory verificeret!"
            },
            "auto_learn.py": {
                "sender": "DNA",
                "start_msg": "Analyserer patterns...",
                "success_msg": " Nye patterns lært og gemt!",
                "title": " Patterns",
                "body": "Nye patterns lært!"
            },
            "auto_predict.py": {
                "sender": "Kv1nt",
                "start_msg": "Genererer forudsigelser...",
                "success_msg": " Next skridt beregnet!",
                "title": " Predictions",
                "body": "Predictelser genereret!"
            },
            "auto_archive.py": {
                "sender": "Admiral",
                "start_msg": "Archiveer victory...",
                "success_msg": " SEJR ARKIVERET! Du er fantastisk!",
                "title": " Archived",
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
                send_notification(" Error", f"Script fejlede: {e}")
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
            heading=" SEJR ARKIVERET!",
            body=f"""Congratulations! Din victory er nu arkiveret.

 System Status:
• Total sejrs: {stats['total_victorys']}
• Aktive: {stats['active']}
• Arkiverede: {stats['archived']}
• Grand Admirals: {stats['grand_admirals']} 

Du er på vej mod Admiral niveau!"""
        )

        dialog.add_response("ok", "Fantastisk! ")
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

    #
    # DRAG UNDO SYSTEM
    #

    def _undo_last_drag(self):
        """Undo the last drag-and-drop move operation (Ctrl+Z)"""
        if not self._drag_history:
            toast = Adw.Toast.new("Ingen drag-operationer at fortryde")
            toast.set_timeout(2)
            if hasattr(self, '_toast_overlay'):
                self._toast_overlay.add_toast(toast)
            return

        last = self._drag_history.pop()
        moved_to = Path(last['to'])
        original_from = Path(last['from'])

        if moved_to.exists() and not original_from.exists():
            try:
                import shutil
                shutil.move(str(moved_to), str(original_from))
                self._load_sejrs()
                toast = Adw.Toast.new(f"Fortrudt: {last['name']} flyttet tilbage")
                toast.set_timeout(3)
                if hasattr(self, '_toast_overlay'):
                    self._toast_overlay.add_toast(toast)
            except Exception as e:
                toast = Adw.Toast.new(f"Fortryd fejl: {str(e)[:50]}")
                toast.set_timeout(3)
                if hasattr(self, '_toast_overlay'):
                    self._toast_overlay.add_toast(toast)
                # Put it back in history since undo failed
                self._drag_history.append(last)
        else:
            toast = Adw.Toast.new("Kan ikke fortryde: filer er aendret")
            toast.set_timeout(3)
            if hasattr(self, '_toast_overlay'):
                self._toast_overlay.add_toast(toast)

    #
    # EXPORT SEJR AS ZIP
    #

    def _export_sejr_zip(self):
        """Export current or selected sejrliste(r) as .zip to Desktop (Ctrl+Shift+E)"""
        desktop = Path.home() / "Desktop"
        paths = []

        # Multi-select: export all selected
        if hasattr(self, '_selected_rows') and self._selected_rows:
            paths = [Path(p) for p in self._selected_rows if Path(p).is_dir()]
        # Single: export currently viewed sejr
        elif hasattr(self, 'selected_sejr') and self.selected_sejr:
            sp = Path(self.selected_sejr.get("path", ""))
            if sp.is_dir():
                paths = [sp]

        if not paths:
            if hasattr(self, '_toast_overlay'):
                toast = Adw.Toast.new("Ingen sejrliste valgt til eksport")
                toast.set_timeout(2)
                self._toast_overlay.add_toast(toast)
            return

        exported = 0
        for sejr_path in paths:
            try:
                zip_path = shutil.make_archive(
                    str(desktop / sejr_path.name),
                    'zip',
                    str(sejr_path.parent),
                    sejr_path.name
                )
                exported += 1
            except Exception as e:
                if hasattr(self, '_toast_overlay'):
                    toast = Adw.Toast.new(f"Eksport fejl: {str(e)[:50]}")
                    toast.set_timeout(3)
                    self._toast_overlay.add_toast(toast)

        if exported > 0 and hasattr(self, '_toast_overlay'):
            msg = f"{exported} sejrliste{'r' if exported > 1 else ''} eksporteret som .zip til Desktop"
            toast = Adw.Toast.new(msg)
            toast.set_timeout(3)
            self._toast_overlay.add_toast(toast)

    #
    # REAL-TIME FILE MONITORING
    #

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
                    Gio.FileMonitorEvent.CREATED: ("", "Oprettet"),
                    Gio.FileMonitorEvent.DELETED: ("", "Deletetet"),
                    Gio.FileMonitorEvent.CHANGED: ("", "Ændret"),
                    Gio.FileMonitorEvent.MOVED_IN: ("", "Movetet ind"),
                    Gio.FileMonitorEvent.MOVED_OUT: ("", "Movetet ud"),
                }
                icon, action = event_icons.get(event_type, ("", "Handling"))
                self.activity_monitor.log_event("fil", f"{action}: {file_name[:40]}", icon)

            # Debounce rapid changes - refresh after 500ms
            GLib.timeout_add(500, self._debounced_refresh)

    def _debounced_refresh(self):
        """Debounced refresh to avoid rapid-fire updates"""
        self._load_sejrs()
        return False  # Don't repeat

    # 
    # DRAG & DROP SUPPORT
    # 

    def _setup_drag_drop(self):
        """Setup drag and drop for importing files/folders to create victorys"""
        # === External file drop on main window (create new victory) ===
        drop_target = Gtk.DropTarget.new(Gio.File, Gdk.DragAction.COPY)
        drop_target.connect("drop", self._on_drop)
        drop_target.connect("enter", self._on_drag_enter)
        drop_target.connect("leave", self._on_drag_leave)
        self.add_controller(drop_target)

        # === File drop on detail view (add file to current victory) ===
        # Accept single files
        detail_drop = Gtk.DropTarget.new(Gio.File, Gdk.DragAction.COPY)
        detail_drop.connect("drop", self._on_detail_file_drop)
        detail_drop.connect("enter", self._on_detail_drop_enter)
        detail_drop.connect("leave", self._on_detail_drop_leave)
        self.detail_box.add_controller(detail_drop)

        # === Multi-file drop on detail view (bulk import) ===
        try:
            multi_drop = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
            multi_drop.connect("drop", self._on_detail_multi_file_drop)
            multi_drop.connect("enter", self._on_detail_drop_enter)
            multi_drop.connect("leave", self._on_detail_drop_leave)
            self.detail_box.add_controller(multi_drop)
        except Exception:
            pass  # Gdk.FileList not available in older GTK4

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
                    self.activity_monitor.log_event("drag-drop", f"Fil droppet: {Path(path).name[:40]}", "")
                # Show conversion dialog with the dropped path
                self._show_conversion_dialog(Path(path))
                return True
        return False

    # === FILE-TO-FOLDER DROP (add file to current victory) ===

    def _on_detail_drop_enter(self, target, x, y):
        """Visual feedback when dragging file over detail view"""
        self.detail_box.add_css_class("drop-zone-active")
        return Gdk.DragAction.COPY

    def _on_detail_drop_leave(self, target):
        """Remove visual feedback"""
        self.detail_box.remove_css_class("drop-zone-active")

    def _on_detail_file_drop(self, target, value, x, y):
        """Handle file dropped onto detail view — copy to current victory folder"""
        self.detail_box.remove_css_class("drop-zone-active")

        if not isinstance(value, Gio.File):
            return False

        source_path = value.get_path()
        if not source_path:
            return False

        source = Path(source_path)

        # Get current victory path
        if not hasattr(self, 'selected_sejr') or not self.selected_sejr:
            return False

        sejr_path = Path(self.selected_sejr.get("path", ""))
        if not sejr_path.exists() or not sejr_path.is_dir():
            return False

        # Validate file type
        allowed_ext = {".md", ".yaml", ".yml", ".jsonl", ".json", ".py", ".sh", ".txt", ".csv"}
        if source.suffix.lower() not in allowed_ext:
            # Show error toast
            toast = Adw.Toast.new(f"Filtype {source.suffix} ikke tilladt")
            toast.set_timeout(3)
            if hasattr(self, '_toast_overlay'):
                self._toast_overlay.add_toast(toast)
            return False

        # Copy file to victory folder
        import shutil
        dest = sejr_path / source.name
        try:
            if source.is_file():
                shutil.copy2(str(source), str(dest))
            elif source.is_dir():
                shutil.copytree(str(source), str(dest))

            # Show success toast
            toast = Adw.Toast.new(f"Fil tilføjet: {source.name}")
            toast.set_timeout(3)
            if hasattr(self, '_toast_overlay'):
                self._toast_overlay.add_toast(toast)

            # Refresh detail view
            self._build_detail_page(self.selected_sejr)
            return True
        except Exception as e:
            toast = Adw.Toast.new(f"Fejl: {str(e)[:50]}")
            toast.set_timeout(3)
            if hasattr(self, '_toast_overlay'):
                self._toast_overlay.add_toast(toast)
            return False

    def _on_detail_multi_file_drop(self, target, value, x, y):
        """Handle MULTIPLE files dropped onto detail view — bulk import dialog"""
        self.detail_box.remove_css_class("drop-zone-active")

        try:
            files = value.get_files()
        except Exception:
            return False

        if not files:
            return False

        # Get current victory path
        if not hasattr(self, 'selected_sejr') or not self.selected_sejr:
            return False
        sejr_path = Path(self.selected_sejr.get("path", ""))
        if not sejr_path.exists():
            return False

        # Filter valid files
        allowed_ext = {".md", ".yaml", ".yml", ".jsonl", ".json", ".py", ".sh", ".txt", ".csv"}
        valid_files = []
        skipped = 0
        for f in files:
            path = f.get_path()
            if path:
                p = Path(path)
                if p.suffix.lower() in allowed_ext or p.is_dir():
                    valid_files.append(p)
                else:
                    skipped += 1

        if not valid_files:
            toast = Adw.Toast.new(f"{skipped} filer afvist (forkert type)")
            toast.set_timeout(3)
            if hasattr(self, '_toast_overlay'):
                self._toast_overlay.add_toast(toast)
            return False

        # Show bulk import confirmation dialog
        dialog = Adw.AlertDialog()
        dialog.set_heading(f"Import {len(valid_files)} filer?")
        file_list = "\n".join(f"  {f.name}" for f in valid_files[:10])
        if len(valid_files) > 10:
            file_list += f"\n  ... +{len(valid_files) - 10} mere"
        body = f"Tilfoej til: {sejr_path.name}\n\n{file_list}"
        if skipped > 0:
            body += f"\n\n({skipped} filer afvist — forkert filtype)"
        dialog.set_body(body)
        dialog.add_response("cancel", "Annuller")
        dialog.add_response("import", f"Import {len(valid_files)} filer")
        dialog.set_response_appearance("import", Adw.ResponseAppearance.SUGGESTED)

        def on_bulk_response(dlg, response):
            if response == "import":
                import shutil
                imported = 0
                for src in valid_files:
                    try:
                        dest = sejr_path / src.name
                        if src.is_file():
                            shutil.copy2(str(src), str(dest))
                            imported += 1
                        elif src.is_dir():
                            shutil.copytree(str(src), str(dest))
                            imported += 1
                    except Exception:
                        pass
                toast = Adw.Toast.new(f"{imported}/{len(valid_files)} filer importeret")
                toast.set_timeout(3)
                if hasattr(self, '_toast_overlay'):
                    self._toast_overlay.add_toast(toast)
                # Refresh detail view
                self._build_detail_page(self.selected_sejr)

        dialog.connect("response", on_bulk_response)
        dialog.present(self)
        return True

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
        """Actually convert a path to a new Victory using SejrConverter API"""
        try:
            import shutil
            system_path = SYSTEM_PATH
            converter = SejrConverter(system_path)

            # Determine input type
            if path.is_file():
                input_type = "file"
            elif path.is_dir():
                input_type = "folder"
            else:
                return

            # Analyze input
            analysis = converter.analyze_input(str(path), input_type)
            name = analysis.get("suggested_name", path.stem.upper().replace(" ", "_"))

            # Check if dropped folder already IS a victory (has SEJR_LISTE.md)
            if path.is_dir() and (path / "SEJR_LISTE.md").exists():
                # Direct import — copy entire folder to 10_ACTIVE
                dest = system_path / "10_ACTIVE" / path.name
                if not dest.exists():
                    shutil.copytree(str(path), str(dest))
                sejr_path = dest
            else:
                # Create new victory via converter
                config = {
                    "name": name,
                    "input_path": str(path),
                    "input_type": input_type,
                    "mode": "kv1nt",
                    "hvad": f"Konvertering af {path.name}",
                    "tasks": analysis.get("suggested_tasks", []),
                }
                sejr_path = converter.create_sejr_from_input(config)

                # Copy source files into the new victory folder
                if path.is_file():
                    shutil.copy2(str(path), str(sejr_path / path.name))
                elif path.is_dir():
                    for item in path.iterdir():
                        dest_item = sejr_path / item.name
                        if not dest_item.exists():
                            if item.is_file():
                                shutil.copy2(str(item), str(dest_item))
                            elif item.is_dir():
                                shutil.copytree(str(item), str(dest_item))

            # Refresh and select the new victory
            self._load_sejrs()

            # Find and select the new victory
            for sejr in self.sejrs:
                if str(sejr.get("path", "")) == str(sejr_path):
                    self._build_detail_page(sejr)
                    self.content_stack.set_visible_child_name("detail")
                    break

            # Notification
            toast = Adw.Toast.new(f"Victory oprettet: {name}")
            toast.set_timeout(3)
            if hasattr(self, '_toast_overlay'):
                self._toast_overlay.add_toast(toast)

        except Exception as e:
            print(f"Konvertering fejlede: {e}")
            toast = Adw.Toast.new(f"Fejl ved konvertering: {str(e)[:50]}")
            toast.set_timeout(3)
            if hasattr(self, '_toast_overlay'):
                self._toast_overlay.add_toast(toast)

    # 
    # ZOOM FUNCTIONALITY
    # 

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

    # 
    # DNA SCRIPT RUNNERS (Keyboard Shortcuts)
    # 

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

    # 
    # HELP DIALOG
    # 

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

    # 
    # INTELLIGENT SEARCH HANDLERS
    # 

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


# 
# APPLICATION
# 

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

        # Set window icon from SVG
        icon_path = SYSTEM_PATH / "assets" / "sejrliste-icon.svg"
        if icon_path.exists():
            try:
                icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
                icon_theme.add_search_path(str(icon_path.parent))
            except Exception:
                pass

        # Show splash screen (0.5 sec) then main window
        self._show_splash()

    def _show_splash(self):
        """Show splash screen with logo, app name, and loading bar."""
        splash = Adw.Window(application=self)
        splash.set_default_size(400, 300)
        splash.set_resizable(False)
        splash.set_decorated(False)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        box.set_margin_top(40)
        box.set_margin_bottom(40)
        box.set_margin_start(40)
        box.set_margin_end(40)
        box.set_valign(Gtk.Align.CENTER)
        box.set_halign(Gtk.Align.CENTER)

        # Logo icon
        splash_icon = SYSTEM_PATH / "assets" / "icons" / "sejrliste-icon" / "128.png"
        if splash_icon.exists():
            try:
                texture = Gdk.Texture.new_from_filename(str(splash_icon))
                image = Gtk.Image.new_from_paintable(texture)
                image.set_pixel_size(96)
                box.append(image)
            except Exception:
                pass

        # App name
        title = Gtk.Label(label="Victory List")
        title.add_css_class("title-1")
        box.append(title)

        # Subtitle
        subtitle = Gtk.Label(label="Sejrliste Systemet")
        subtitle.add_css_class("dim-label")
        box.append(subtitle)

        # Loading bar
        progress = Gtk.ProgressBar()
        progress.set_fraction(0.0)
        progress.set_margin_top(16)
        box.append(progress)

        # Version
        version_label = Gtk.Label(label="v1.0.0 -- Cirkelline")
        version_label.add_css_class("dim-label")
        version_label.add_css_class("caption")
        box.append(version_label)

        splash.set_content(box)
        splash.present()

        # Animate progress bar + transition to main window
        self._splash_ref = splash
        self._splash_progress = progress
        self._splash_step = 0
        GLib.timeout_add(50, self._splash_tick)

    def _splash_tick(self):
        """Animate splash screen progress bar."""
        self._splash_step += 1
        fraction = min(self._splash_step / 10.0, 1.0)
        self._splash_progress.set_fraction(fraction)

        if self._splash_step >= 10:  # 10 x 50ms = 0.5 sec
            self._splash_ref.close()
            self._open_main_window()
            return False  # Stop timer
        return True  # Continue

    def _open_main_window(self):
        """Open the main application window after splash."""
        win = MasterpieceWindow(self)

        # Add keyboard shortcuts
        self._setup_shortcuts(win)

        # Add About action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", lambda a, p: self._show_about(win))
        self.add_action(about_action)

        win.present()

    def _show_about(self, win):
        """Show About dialog with app branding"""
        about = Adw.AboutDialog()
        about.set_application_name("Victory List")
        about.set_version("1.0.0")
        about.set_developer_name("Rasmus — Cirkelline")
        about.set_application_icon("dk.cirkelline.victoryliste.masterpiece")
        about.set_website("https://cirkelline.com")
        about.set_issue_url("")
        about.set_copyright("© 2026 Cirkelline")
        about.set_license_type(Gtk.License.CUSTOM)
        about.set_license("Proprietary — All rights reserved")
        about.set_developers(["Rasmus (CEO/Founder)", "Kv1nt (AI Admiral)"])
        about.set_comments(
            "Sejrliste Systemet — En GTK4/Libadwaita desktop app til systematisk "
            "eksekvering af opgaver via 3-Pass Victory Lists.\n\n"
            "Bygget med: Python, GTK4, Libadwaita, Ollama, ChromaDB"
        )
        about.present(win)

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

        # Ctrl+Z for undo last drag
        undo_action = Gio.SimpleAction.new("undo-drag", None)
        undo_action.connect("activate", lambda a, p: win._undo_last_drag())
        self.add_action(undo_action)
        self.set_accels_for_action("app.undo-drag", ["<Control>z"])

        # Ctrl+Shift+E for export sejr as .zip to Desktop
        export_action = Gio.SimpleAction.new("export-zip", None)
        export_action.connect("activate", lambda a, p: win._export_sejr_zip())
        self.add_action(export_action)
        self.set_accels_for_action("app.export-zip", ["<Control><Shift>e"])

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


# 
# MAIN
# 

if __name__ == "__main__":
    app = MasterpieceApp()
    app.run(None)
