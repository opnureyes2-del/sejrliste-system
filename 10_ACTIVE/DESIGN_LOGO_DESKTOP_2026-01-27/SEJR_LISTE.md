# SEJR: Design, Logo & Desktop Branding

**Dato:** 2026-01-27
**Mål:** Custom icons, .directory og .desktop filer for alle 3 Desktop mapper
**Scope:** sejrliste systemet + INTRO FOLDER SYSTEM + MIN ADMIRAL

---

## OVERBLIK

| Mappe | Icon | .directory | .desktop | Verificeret |
|-------|------|-----------|----------|-------------|
| sejrliste systemet | ✅ sejrliste-icon.svg (1.7K) | ✅ | ✅ 4 launchers | ❌ IKKE TESTET |
| INTRO FOLDER SYSTEM | ✅ intro-system-icon.svg (1.6K) | ✅ | ✅ intro-system.desktop | ❌ IKKE TESTET |
| MIN ADMIRAL | ✅ admiral-logo.svg (6.7K) | ✅ | ✅ admiral.desktop | ❌ IKKE TESTET |

**Filer oprettet:** 3 SVG + 5 .desktop + 3 .directory = 11 filer total

---

## PASS 1: FUNGERENDE

### A. ICONS (3/3 oprettet, 0/3 verificeret)

- [x] `assets/sejrliste-icon.svg` (1.7K SVG)
- [x] `assets/admiral-logo.svg` (6.7K SVG)
- [x] `assets/intro-system-icon.svg` (1.6K SVG)
- [ ] **TEST:** Alle 3 renderer korrekt i GNOME (åbn Nautilus, se mapper)
- [ ] **TEST:** Højreklik → Properties → viser korrekt icon?

### B. DESKTOP LAUNCHERS (5/5 oprettet, 0/5 verificeret)

| Fil | Exec | Virker? |
|-----|------|---------|
| `victorylist.desktop` | `python3 masterpiece_en.py` | ❌ IKKE TESTET |
| `sejrliste.desktop` | `streamlit run web_app.py` | ❌ IKKE TESTET |
| `sejrliste-terminal.desktop` | `sejr-terminal.sh` | ❌ IKKE TESTET |
| `intro-system.desktop` | `python3 masterpiece_en.py` | ❌ IKKE TESTET |
| `admiral.desktop` | `xdg-open "MIN ADMIRAL/"` | ❌ IKKE TESTET |

- [ ] **TEST:** Dobbeltklik på alle 5 → åbner korrekt?
- [ ] **TEST:** Alle 5 viser korrekte icons?
- [ ] **FIX:** intro-system.desktop Path peger på INTRO mappe men Exec åbner sejrliste app

### C. FOLDER ICONS (3/3 .directory oprettet, 0/3 verificeret)

- [ ] **TEST:** Nautilus viser custom icon for sejrliste systemet?
- [ ] **TEST:** Nautilus viser custom icon for INTRO FOLDER SYSTEM?
- [ ] **TEST:** Nautilus viser custom icon for MIN ADMIRAL?
- [ ] Hvis .directory ikke virker → brug `gio set` metadata

### D. APP WINDOW BRANDING

- [ ] Victory List app window icon = sejrliste-icon.svg?
- [ ] StartupWMClass matcher i .desktop vs. app?

---

## PASS 1 REVIEW

- [ ] Alle 3 mapper viser custom icons i Nautilus
- [ ] Alle 5 .desktop launchers virker ved dobbeltklik
- [ ] App window har korrekt icon i taskbar
- [ ] Score: ___/10

---

## PASS 2: FORBEDRET

### A. ICON ENSRETNING
- [ ] Ensret stil: alle 3 icons i same design language
- [ ] intro-system-icon: tilføj LINEN bogstaver + 3-lags hint
- [ ] Opret størrelsevarianter (16/32/48/128/256px)

### B. GNOME MENU INTEGRATION
- [ ] Kopiér .desktop til `~/.local/share/applications/`
- [ ] **TEST:** Super → søg "Victory" → app vises?
- [ ] Pin til taskbar/dock

### C. ABOUT DIALOG
- [ ] Adw.AboutWindow i masterpiece_en.py (navn, version, developer, website, icon)

---

## PASS 3: OPTIMERET

### A. ADAPTIVE ICONS
- [ ] Symbolic variants for dark/light theme
- [ ] HiDPI support

### B. SPLASH SCREEN
- [ ] Logo + app navn + loading bar ved start (0.5 sek)

---

## VERIFIKATION

```bash
# Filer eksisterer
ls "/home/rasmus/Desktop/sejrliste systemet/assets/"*.svg  # 3 SVG
ls /home/rasmus/Desktop/*.desktop  # 5 launchers
ls "/home/rasmus/Desktop/MIN ADMIRAL/.directory"  # .directory

# GNOME integration
gio info "/home/rasmus/Desktop/INTRO FOLDER SYSTEM" | grep custom-icon
```
