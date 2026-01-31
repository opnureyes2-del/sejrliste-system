#!/usr/bin/env python3
"""
Generate Icon Sizes — Opretter PNG varianter af SVG icons
==========================================================
Bruger rsvg-convert (librsvg) til at generere PNG i standardstoerrelser.

Brug:
    python3 scripts/generate_icon_sizes.py

Output:
    assets/icons/{name}/{size}.png for hver SVG fil

Fra: DESIGN_LOGO_DESKTOP SEJR LISTE, Pass 2 Fase A
"""

import subprocess
import os
import sys

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
SIZES = [16, 32, 48, 128, 256]

SVG_FILES = [
    "sejrliste-icon.svg",
    "admiral-logo.svg",
    "intro-system-icon.svg",
]


def generate_sizes():
    """Generér PNG varianter for alle SVG icons."""
    os.makedirs(ICONS_DIR, exist_ok=True)

    # Find conversion tool (rsvg-convert > cairosvg > imagemagick)
    converter = None
    for cmd in ["rsvg-convert", "convert"]:
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=False)
            converter = cmd
            break
        except FileNotFoundError:
            continue

    # Also try cairosvg Python module
    has_cairosvg = False
    if not converter:
        try:
            import cairosvg  # noqa: F401
            has_cairosvg = True
            converter = "cairosvg"
        except ImportError:
            pass

    if not converter:
        print("[FAIL] Ingen SVG converter fundet.")
        print("       Installer en af: librsvg2-bin, imagemagick, cairosvg")
        return False

    print(f"[TOOL] Bruger: {converter}")

    total = 0
    errors = 0

    for svg_file in SVG_FILES:
        svg_path = os.path.join(ASSETS_DIR, svg_file)
        if not os.path.isfile(svg_path):
            print(f"[WARN] SVG ikke fundet: {svg_path}")
            continue

        name = svg_file.replace(".svg", "")
        icon_dir = os.path.join(ICONS_DIR, name)
        os.makedirs(icon_dir, exist_ok=True)

        print(f"\n[SVG] {svg_file}")
        for size in SIZES:
            output = os.path.join(icon_dir, f"{size}.png")
            try:
                if converter == "rsvg-convert":
                    subprocess.run([
                        "rsvg-convert",
                        "-w", str(size), "-h", str(size),
                        "-o", output, svg_path
                    ], check=True, capture_output=True)
                elif converter == "convert":
                    subprocess.run([
                        "convert",
                        "-background", "none",
                        "-resize", f"{size}x{size}",
                        svg_path, output
                    ], check=True, capture_output=True)
                elif converter == "cairosvg":
                    import cairosvg
                    cairosvg.svg2png(
                        url=svg_path,
                        write_to=output,
                        output_width=size,
                        output_height=size,
                    )

                file_size = os.path.getsize(output)
                print(f"  [OK] {size}x{size}px ({file_size:,} bytes)")
                total += 1
            except (subprocess.CalledProcessError, Exception) as e:
                print(f"  [FAIL] {size}x{size}px — {e}")
                errors += 1

    print(f"\n{'='*60}")
    print(f"Genereret: {total} PNG filer")
    print(f"Fejl: {errors}")
    print(f"Mapper: {ICONS_DIR}")
    print(f"Stoerrelser: {SIZES}")
    print(f"{'='*60}")
    return errors == 0


if __name__ == "__main__":
    success = generate_sizes()
    sys.exit(0 if success else 1)
