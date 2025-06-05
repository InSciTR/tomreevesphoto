#!/usr/bin/env python3
"""
make_set_json.py

Usage:
    python make_set_json.py /absolute/or/relative/path/to/my-folder

The script drops <folder-name>.json one level above <folder-name>.
"""

import argparse
import json
import os
import re
from pathlib import Path

# ---------- helper lists ----------
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".tif", ".tiff"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".m4v", ".avi", ".mkv"}

def slugify(text: str) -> str:
    """Convert text to lowercase, dash-separated slug."""
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_-]+", "-", text)

def build_items(folder: Path) -> list[dict]:
    items = []
    for entry in sorted(folder.iterdir()):
        if entry.is_file():
            ext = entry.suffix.lower()
            if ext in IMAGE_EXTS | VIDEO_EXTS:
                items.append({
                    "src": f"{folder.name}/{entry.name}",
                    "type": "video" if ext in VIDEO_EXTS else "image",
                    "alt": ""
                })
    return items

def main():
    parser = argparse.ArgumentParser(description="Generate set JSON for a media folder")
    parser.add_argument("folder", help="Path to media folder")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        raise SystemExit(f"❌  {folder} is not a directory.")

    items = build_items(folder)
    if not items:
        raise SystemExit("❌  No supported media files found.")

    # Construct JSON payload
    title = folder.name.replace("-", " ").replace("_", " ").title()
    slug  = slugify(folder.name)
    cover = f"/sets/{folder.name}/{items[0]['src'].split('/')[-1]}"

    payload = {
        "title": title,
        "slug": slug,
        "cover": cover,
        "sortOrder": 1,
        "items": items
    }

    # Write next to the folder
    out_path = folder.parent / f"{folder.name}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"✅  Wrote {out_path}")

if __name__ == "__main__":
    main()