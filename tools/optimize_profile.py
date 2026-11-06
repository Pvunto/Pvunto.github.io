#!/usr/bin/env python3
"""Crea WebP responsive da assets/profilo.webp senza modificare l'originale."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "profilo.webp"
SIZES = (192, 384, 768)

if not SOURCE.is_file():
    raise SystemExit(f"File originale non trovato: {SOURCE}")

with Image.open(SOURCE) as opened:
    original = ImageOps.exif_transpose(opened).convert("RGB")
    for size in SIZES:
        image = original.copy()
        image.thumbnail((size, size), Image.Resampling.LANCZOS)
        target = ROOT / "assets" / f"profilo-{size}.webp"
        image.save(target, "WEBP", quality=82, method=6)
        print(f"{target.relative_to(ROOT)}: {image.width}x{image.height}, {target.stat().st_size:,} byte")
