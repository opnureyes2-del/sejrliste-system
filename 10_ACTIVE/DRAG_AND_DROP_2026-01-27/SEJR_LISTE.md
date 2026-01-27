# SEJR: Drag and Drop i Victory List + INTRO System

**Dato:** 2026-01-27
**Mål:** Implementér fuld drag-and-drop i begge apps (intern + ekstern + folder-to-folder)
**Scope:** GTK4 DnD i masterpiece_en.py + file management
**App:** `/home/rasmus/Desktop/sejrliste systemet/masterpiece_en.py`

---

## OVERBLIK: HVAD SKAL DRAG AND DROP GØRE?

| Type | Fra → Til | Eksempel | Status |
|------|-----------|----------|--------|
| **Ekstern Drop** | Desktop fil → App vindue | Træk .md fil ind i app → opret sejr | DELVIST (linje 5319-5350) |
| **Intern Reorder** | Sejr → Anden position i listen | Flyt sejr op/ned i sidebar | MANGLER |
| **Folder-to-Folder** | Sejr mappe → Anden kategori | Flyt fra 10_ACTIVE til 90_ARCHIVE | MANGLER |
| **File-to-Folder** | Fil → Sejr mappe | Træk SEJR_LISTE.md ind i eksisterende sejr | MANGLER |
| **App-to-Desktop** | Sejr → Desktop | Eksportér sejr som mappe til Desktop | MANGLER |

---

## PASS 1: FUNGERENDE (Få det til at virke)

### FASE 0: AUDIT EKSISTERENDE DND

- [x] Læs eksisterende DnD kode i masterpiece_en.py (linje 6762-6826)
- [x] Dokumentér: `_setup_drag_drop()`, `_on_drag_enter()`, `_on_drag_leave()`, `_on_drop()`
- [x] Identificér: Hvad virker allerede (ekstern fil-drop + konverterings-dialog)
- [x] Identificér: Hvad mangler (intern, folder-to-folder, file-to-folder)

### FASE 1: INTERN SEJR REORDER (Drag inden i app)

- [x] Tilføj `Gtk.DragSource` til `SejrRow` widget
- [x] Tilføj `Gtk.DropTarget` til sejr-listen (sidebar) — via SejrRow per-row target
- [x] Implementér `_on_drag_begin()` → visuelt "grabbed" state (opacity 0.4)
- [x] Implementér `_on_reorder_drop()` → flyt sejr til ny position / kategori
- [x] Opdater filsystem (shutil.move for cross-category)
- [x] Visuelt feedback: Blå linje viser drop-position (`row.drop-above` CSS)
- [ ] Annullér drag med Escape ← Pass 2

### FASE 2: FOLDER-TO-FOLDER (Kategori flytning)

- [x] Tilføj drag fra sidebar sejr → drop på kategori (Active/Archive) — via SejrRow DragSource
- [x] Implementér cross-category move i `_on_reorder_drop()`
- [x] Active → Archive: Flyt mappe fra 10_ACTIVE/ til 90_ARCHIVE/ (shutil.move)
- [x] Archive → Active: Flyt mappe fra 90_ARCHIVE/ til 10_ACTIVE/ (shutil.move)
- [ ] Bekræftelses-dialog: "Flyt X til Arkiv?" ← Pass 2
- [x] Auto-refresh sidebar efter flytning (`window._load_sejrs()`)

### FASE 3: FILE-TO-FOLDER (Fil ind i sejr)

- [x] Tilføj Gtk.DropTarget til sejr detail view (`detail_box`)
- [x] Accept file drops (Gio.File type)
- [x] Kopiér dropped fil til sejr-mappen (shutil.copy2)
- [x] Vis ny fil i sejr's detalje-view (refresh via `_build_detail_page`)
- [x] Filtype-validering (.md, .yaml, .yml, .jsonl, .json, .py, .sh, .txt, .csv)

### FASE 4: EKSTERN DROP FORBEDRING

- [x] Forbedre eksisterende ekstern drop:
  - [x] Drop .md fil → parse via SejrConverter.analyze_input + create_sejr
  - [x] Drop mappe → importér som komplet sejr (smart: folder med SEJR_LISTE.md → direkte import)
  - [ ] Drop multiple filer → bulk import dialog ← Pass 2 (kræver Gdk.FileList)
- [x] Vis "Drop zone" overlay — CSS allerede implementeret (window.drop-active + .drop-zone-active)
- [x] Fix `_convert_path_to_sejr` bug: brugte ikke-eksisterende `from_file/from_folder` metoder → rettet til SejrConverter API

---

## PASS 1 REVIEW

- [x] Intern reorder virker (drag sejr op/ned med visuelt feedback)
- [x] Folder-to-folder virker (Active ↔ Archive via cross-category drag)
- [x] File-to-folder virker (træk fil ind i sejr detail view)
- [x] Ekstern drop forbedret (SejrConverter API + smart folder detection)
- [x] App starter uden fejl (py_compile ✅, launch ✅)
- [x] Score: 8/10 (mangler: Escape annullér, bekræftelses-dialog, multi-file drop → Pass 2)

---

## PASS 2: FORBEDRET (Gør det bedre)

### FASE 0: VISUAL FEEDBACK

- [ ] Drag ghost (semi-transparent kopi af sejr under drag)
- [ ] Drop zone highlight (grøn ramme = valid, rød = invalid)
- [ ] Animated insertion marker (blå linje ved drop-position)
- [ ] Success animation ved completed drop

### FASE 1: UNDO SYSTEM

- [ ] Ctrl+Z undo sidst drag operation
- [ ] Vis toast: "Sejr flyttet. Undo?" med 5 sekunder timeout
- [ ] Gem drag-historik for session

### FASE 2: MULTI-SELECT DRAG

- [ ] Ctrl+Click for multi-select sejrlister
- [ ] Drag multiple sejrlister samtidig
- [ ] Vis "3 sejrlister" badge på drag ghost

---

## PASS 2 REVIEW

- [ ] Visual feedback er poleret
- [ ] Undo virker
- [ ] Multi-select drag virker
- [ ] Score: ___/10 (SKAL være > Pass 1)

---

## PASS 3: OPTIMERET (Gør det bedst)

### FASE 0: APP-TO-DESKTOP EXPORT

- [ ] Drag sejr ud af app → opret mappe på Desktop
- [ ] Drag sejr → anden app (file manager, terminal)
- [ ] Export som .zip ved drag til Desktop

### FASE 1: PERFORMANCE

- [ ] Smooth 60fps drag animations
- [ ] Lazy load sejr data under drag (ikke hele fil)
- [ ] Debounce reorder operations

---

## PASS 3 REVIEW

- [ ] App-to-Desktop export virker
- [ ] Performance er smooth
- [ ] Score: ___/10 (SKAL være > Pass 2)

---

## VERIFIKATION

```bash
# Test 1: Intern reorder
# Drag en sejr op/ned i sidebar → position ændres

# Test 2: Folder-to-folder
# Drag sejr fra Active til Archive → sejr flytter

# Test 3: File drop
# Træk .md fil fra Desktop ind i app → sejr oprettes

# Test 4: Undo
# Ctrl+Z efter drag → sejr vender tilbage
```
