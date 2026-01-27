# SEJR: Design, Logo & Desktop Folder Branding

**Dato:** 2026-01-27
**Mål:** Giv alle Desktop mapper visuelt udtryk med icons, farver og .directory filer
**Scope:** INTRO FOLDER SYSTEM + sejrliste systemet + MIN ADMIRAL Desktop mapper
**Mapper:** Alle 3 projekt-mapper på Desktop

---

## OVERBLIK: HVAD SKAL DESIGNES?

| Mappe | Icon | .directory | .desktop | Status |
|-------|------|-----------|----------|--------|
| sejrliste systemet | ✅ sejrliste-icon.svg | ✅ BYGGET | ✅ 3 launchers | DELVIST |
| INTRO FOLDER SYSTEM | ✅ intro-system-icon.svg | ✅ BYGGET | ✅ intro-system.desktop | DELVIST |
| MIN ADMIRAL | ✅ admiral-logo.svg | ✅ BYGGET | MANGLER | DELVIST |

**Allerede bygget i denne session:**
- `intro-system-icon.svg` — Indigo/lilla cirkel med folder + LINEN linjer
- `intro-system.desktop` — Desktop launcher
- 3x `.directory` filer — Custom folder icons for GNOME

---

## PASS 1: FUNGERENDE (Få det til at virke)

### FASE 0: ICON DESIGN KOMPLET

- [x] `sejrliste-icon.svg` eksisterer (1.7K) ✅
- [x] `admiral-logo.svg` eksisterer (6.7K) ✅
- [x] `intro-system-icon.svg` oprettet (ny) ✅
- [ ] Verificér at alle 3 icons renderer korrekt i GNOME
- [ ] Verificér at .directory filer virker (mapper viser custom icon)
- [ ] Test: Højreklik på mappe → Properties → viser korrekt icon?

### FASE 1: .DESKTOP FILER KOMPLET

- [x] `victorylist.desktop` eksisterer ✅
- [x] `sejrliste.desktop` eksisterer ✅
- [x] `sejrliste-terminal.desktop` eksisterer ✅
- [x] `intro-system.desktop` oprettet ✅
- [ ] Opret `admiral.desktop` for MIN ADMIRAL:
  - [ ] Exec: xdg-open "/home/rasmus/Desktop/MIN ADMIRAL/"
  - [ ] Icon: admiral-logo.svg
  - [ ] Name: MIN ADMIRAL
- [ ] Verificér alle 5 .desktop filer virker (dobbeltklik)
- [ ] Verificér alle 5 viser korrekte icons

### FASE 2: FOLDER VISUELT DESIGN

- [ ] Verificér .directory filer virker i Nautilus/Files:
  - [ ] INTRO FOLDER SYSTEM viser intro-system-icon
  - [ ] sejrliste systemet viser sejrliste-icon
  - [ ] MIN ADMIRAL viser admiral-logo
- [ ] Hvis .directory ikke virker: brug `gio set` kommando:
  ```bash
  gio set "/home/rasmus/Desktop/INTRO FOLDER SYSTEM" metadata::custom-icon \
    "file:///home/rasmus/Desktop/sejrliste systemet/assets/intro-system-icon.svg"
  ```
- [ ] Test i GNOME Files: Mapper har custom icons

### FASE 3: APP WINDOW BRANDING

- [ ] Victory List app: Verificér window icon er sejrliste-icon.svg
- [ ] Tilføj window icon til masterpiece_en.py hvis mangler:
  ```python
  self.set_icon_name("dk.cirkelline.victorylist")
  ```
- [ ] Verificér .desktop `StartupWMClass` matcher app's WM_CLASS

---

## PASS 1 REVIEW

- [ ] Alle mapper har custom icons i GNOME Files
- [ ] Alle .desktop filer virker med korrekte icons
- [ ] App vinduer har korrekte icons i taskbar
- [ ] Score: ___/10

---

## PASS 2: FORBEDRET (Gør det bedre)

### FASE 0: ICON DESIGN FORBEDRING

- [ ] Redesign intro-system-icon.svg med mere detalje:
  - [ ] LINEN bogstaver synlige
  - [ ] 3-lags arkitektur hint
  - [ ] Cirkelline brand farver
- [ ] Ensret alle 3 icons i stil (same design language)
- [ ] Opret 16x16, 32x32, 48x48, 128x128, 256x256 størrelse varianter

### FASE 1: GNOME DESKTOP INTEGRATION

- [ ] Tilføj apps til GNOME Applications menu (ikke kun Desktop):
  ```bash
  cp *.desktop ~/.local/share/applications/
  ```
- [ ] Verificér: Tryk Super → søg "Victory" → app vises
- [ ] Verificér: Tryk Super → søg "INTRO" → app vises
- [ ] Pin til taskbar/dock

### FASE 2: ABOUT DIALOG I APP

- [ ] Tilføj Adw.AboutWindow til masterpiece_en.py:
  - [ ] App name: Victory List / Sejrliste
  - [ ] Version: 1.0.0
  - [ ] Developer: Rasmus (Cirkelline)
  - [ ] Website: cirkelline.com
  - [ ] Icon: sejrliste-icon.svg
  - [ ] License: Proprietary

---

## PASS 2 REVIEW

- [ ] Icons er professionelle og ensrettede
- [ ] Apps i GNOME menu + søgbare
- [ ] About dialog viser korrekt info
- [ ] Score: ___/10 (SKAL være > Pass 1)

---

## PASS 3: OPTIMERET (Gør det bedst)

### FASE 0: ADAPTIVE ICONS

- [ ] Opret symbolic variants for GNOME dark/light theme
- [ ] Icons tilpasser sig system theme automatisk
- [ ] HiDPI support (retina/4K skærme)

### FASE 1: SPLASH SCREEN

- [ ] Tilføj splash screen ved app start (0.5 sek):
  - [ ] Logo + app navn + loading bar
  - [ ] Fade in animation

---

## PASS 3 REVIEW

- [ ] Adaptive icons virker i dark/light mode
- [ ] Splash screen er elegant
- [ ] Score: ___/10 (SKAL være > Pass 2)

---

## VERIFIKATION

```bash
# Test 1: Folder icons
ls -la "/home/rasmus/Desktop/INTRO FOLDER SYSTEM/.directory"
ls -la "/home/rasmus/Desktop/sejrliste systemet/.directory"
ls -la "/home/rasmus/Desktop/MIN ADMIRAL/.directory"
# Expected: Alle 3 eksisterer

# Test 2: .desktop filer
ls -la /home/rasmus/Desktop/*.desktop
# Expected: 5 .desktop filer (victory, sejrliste, terminal, intro, admiral)

# Test 3: Icons eksisterer
ls -la "/home/rasmus/Desktop/sejrliste systemet/assets/"*.svg
# Expected: 3 SVG filer (sejrliste-icon, admiral-logo, intro-system-icon)

# Test 4: GNOME integration
gio info "/home/rasmus/Desktop/INTRO FOLDER SYSTEM" | grep custom-icon
# Expected: Viser custom icon sti
```
