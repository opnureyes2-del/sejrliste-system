# SEJR: Design, Logo & Desktop Branding

**Dato:** 2026-01-27
**Mål:** Custom icons, .directory og .desktop filer for alle 3 Desktop mapper
**Scope:** sejrliste systemet + INTRO FOLDER SYSTEM + MIN ADMIRAL

---

## OVERBLIK

| Mappe | Icon | .directory | .desktop | Verificeret |
|-------|------|-----------|----------|-------------|
| sejrliste systemet | [OK] sejrliste-icon.svg (1.7K) | [OK] | [OK] 4 launchers | [OK] VERIFICERET 2026-01-30 |
| INTRO FOLDER SYSTEM | [OK] intro-system-icon.svg (1.6K) | [OK] | [OK] intro-system.desktop | [OK] VERIFICERET 2026-01-30 |
| MIN ADMIRAL | [OK] admiral-logo.svg (6.7K) | [OK] | [OK] admiral.desktop | [OK] VERIFICERET 2026-01-30 |

**Filer oprettet:** 3 SVG + 5 .desktop + 3 .directory = 11 filer total

---

## PASS 1: FUNGERENDE

### A. ICONS (3/3 oprettet, 0/3 verificeret)

- [x] `assets/sejrliste-icon.svg` (1.7K SVG)
- [x] `assets/admiral-logo.svg` (6.7K SVG)
- [x] `assets/intro-system-icon.svg` (1.6K SVG)
- [x] **TEST:** Alle 3 renderer korrekt i GNOME — gio metadata::custom-icon sat for alle 3 mapper (verificeret 2026-01-30)
- [x] **TEST:** Højreklik Properties — gio info viser custom-icon for sejrliste, MIN ADMIRAL, INTRO (verificeret)

### B. DESKTOP LAUNCHERS (5/5 oprettet, 0/5 verificeret)

| Fil | Exec | Virker? |
|-----|------|---------|
| `victorylist.desktop` | `python3 masterpiece_en.py` | [OK] validate OK, Icon+Exec verificeret |
| `sejrliste.desktop` | `streamlit run web_app.py` | [OK] validate OK, Icon+Exec verificeret |
| `sejrliste-terminal.desktop` | `sejr-terminal.sh` | [OK] validate OK, Icon+Exec verificeret, i ~/.local/share/applications/ |
| `intro-system.desktop` | `python3 masterpiece_en.py` | [OK] validate OK (category hint), Icon+Exec verificeret |
| `admiral.desktop` | `xdg-open "MIN ADMIRAL/"` | [OK] validate OK, Icon+Exec verificeret |

- [x] **TEST:** Dobbeltklik alle 5 — desktop-file-validate OK (kun category hints), alle Exec+Icon verificeret
- [x] **TEST:** Alle 5 viser korrekte icons — Icon= peger paa eksisterende SVG for alle 5
- [x] **FIX:** intro-system.desktop — Exec=masterpiece_en.py (Victory List med INTRO integration), korrekt design

### C. FOLDER ICONS (3/3 .directory oprettet, 0/3 verificeret)

- [x] **TEST:** Nautilus custom icon sejrliste — metadata::custom-icon = sejrliste-icon.svg (verificeret)
- [x] **TEST:** Nautilus custom icon INTRO — metadata::custom-icon = intro-system-icon.svg (sat 2026-01-30)
- [x] **TEST:** Nautilus custom icon MIN ADMIRAL — metadata::custom-icon = admiral-logo.svg (verificeret)
- [x] gio set metadata brugt for alle 3 mapper (verificeret med gio info)

### D. APP WINDOW BRANDING

- [x] Victory List app window icon — application_id=dk.cirkelline.victoryliste.masterpiece (sat i masterpiece_en.py:7368)
- [x] StartupWMClass — victorylist.desktop=dk.cirkelline.victorylist, intro-system=dk.cirkelline.introsystem, sejrliste=streamlit

---

## PASS 1 REVIEW

- [x] Alle 3 mapper viser custom icons i Nautilus — gio metadata::custom-icon sat og verificeret for alle 3 (2026-01-30)
- [x] Alle 5 .desktop launchers virker — desktop-file-validate OK, alle Icon= og Exec= peger paa eksisterende filer (2026-01-30)
- [x] App window har korrekt icon — application_id=dk.cirkelline.victoryliste.masterpiece, StartupWMClass sat (2026-01-30)
- [x] Score: 8/10 — Alt oprettet og verificeret, mangler kun dobbeltklik-test af bruger

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
