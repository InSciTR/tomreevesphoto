#!/usr/bin/env python3
"""
convert_media_set.py  —  v2  (06-05-2025)

• Images ▸ WEBP (max-edge, quality)              ── Pillow
• Videos ▸ H.264 MP4 (progressive, web-ready)    ── ffmpeg
      – max width 1920 px (or custom)
      – CRF-23 for good balance (or custom)
      – AAC 128 kbps audio (or --mute to strip)
      – +faststart for instant autoplay

> python convert_media_set.py ~/Pictures/my-set -m 1600 \
      --vmax 1080 --vcrf 23 --fps 30
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image                 # pip install pillow
from tqdm import tqdm                 # pip install tqdm

# ────────── configurable lists ──────────
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".heic"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".webm"}

# ────────── helpers ──────────
def iter_media(folder: Path) -> Iterable[Path]:
    return sorted(
        (p for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTS | VIDEO_EXTS),
        key=lambda p: p.name.lower()
    )

def process_image(src: Path, dst: Path, max_px: int, quality: int) -> None:
    with Image.open(src) as im:
        im.thumbnail((max_px, max_px), Image.LANCZOS)
        im.save(dst, "WEBP", quality=quality, method=6)

def process_video(
    src: Path,
    dst: Path,
    max_w: int,
    crf: int,
    fps: int | None,
    mute: bool
) -> None:
    """
    Transcode to MP4/H.264 ready for HTML <video autoplay loop muted>.
    """
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg not found in $PATH")

    scale_filter = f"scale='min(iw,{max_w})':-2"
    vf_parts = [scale_filter]
    if fps:
        vf_parts.append(f"fps={fps}")
    vf = ",".join(vf_parts)

    audio_flag = ["-an"] if mute else ["-c:a", "aac", "-b:a", "128k"]

    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(src),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "slow", "-profile:v", "high",
        "-movflags", "+faststart",
        "-crf", str(crf),
        *audio_flag,
        str(dst)
    ]
    subprocess.run(cmd, check=True)

# ────────── CLI + driver ──────────
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Resize images to WEBP and transcode videos for fast web delivery."
    )
    ap.add_argument("folder", help="Media folder path")
    ap.add_argument("-m", "--max", type=int, default=1600,
                    help="Max width/height for images (default 1600)")
    ap.add_argument("-q", "--quality", type=int, default=82,
                    help="WEBP quality 0-100 (default 82)")
    # ─ video-specific ─
    ap.add_argument("--vmax", type=int, default=1920,
                    help="Max video width (default 1920)")
    ap.add_argument("--vcrf", type=int, default=23,
                    help="ffmpeg CRF value 0-51 lower=better (default 23)")
    ap.add_argument("--fps", type=int, default=None,
                    help="Force frame-rate (e.g. 30). Omit to keep source.")
    ap.add_argument("--mute", action="store_true",
                    help="Strip audio (HTML5 autoplay works best muted).")
    args = ap.parse_args()

    src_dir = Path(args.folder).expanduser().resolve()
    if not src_dir.is_dir():
        sys.exit(f"❌  {src_dir} is not a directory")

    out_dir = src_dir / "converted"
    out_dir.mkdir(exist_ok=True)

    files = list(iter_media(src_dir))
    if not files:
        sys.exit("❌  No supported media found.")

    for i, path in enumerate(tqdm(files, desc="Processing", unit="file"), start=1):
        num = f"TR{i:03}"
        if path.suffix.lower() in IMAGE_EXTS:
            dst = out_dir / f"{num}.webp"
            process_image(path, dst, args.max, args.quality)
        else:
            dst = out_dir / f"{num}.mp4"   # always emit .mp4
            process_video(path, dst, args.vmax, args.vcrf, args.fps, args.mute)

    print(f"✅  {len(files)} file(s) written to {out_dir}")

if __name__ == "__main__":
    main()