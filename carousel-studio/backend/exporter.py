from __future__ import annotations

import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Sequence

from PIL import Image, ImageDraw, ImageFont


def _font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def render_png_slides(
    slides: Sequence[str], outdir: Path, watermark: str
) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    for idx, text in enumerate(slides, start=1):
        image = Image.new("RGB", (1080, 1080), (245, 245, 245))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 1080, 80), fill=(20, 20, 20))
        draw.text((24, 24), watermark, fill=(255, 255, 255), font=_font(26))
        draw.text((80, 180), f"Slide {idx}", fill=(0, 0, 0), font=_font(64))
        draw.multiline_text(
            (80, 300), text, fill=(30, 30, 30), font=_font(38), spacing=12
        )
        path = outdir / f"slide_{idx:02d}.png"
        image.save(path)
        files.append(path)

    return files


def build_mp4_from_pngs(png_dir: Path, output_file: Path, fps: int = 1) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return False

    cmd = [
        ffmpeg,
        "-y",
        "-framerate",
        str(fps),
        "-i",
        str(png_dir / "slide_%02d.png"),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(output_file),
    ]
    run = subprocess.run(cmd, capture_output=True, text=True)
    return run.returncode == 0


def build_export_zip(slides: Sequence[str], output_zip: Path, watermark: str) -> Path:
    work = output_zip.parent / "_build"
    png_dir = work / "png"
    mp4 = work / "carousel.mp4"

    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)

    pngs = render_png_slides(slides, png_dir, watermark)
    build_mp4_from_pngs(png_dir, mp4)

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in pngs:
            zf.write(file, arcname=f"png/{file.name}")
        if mp4.exists():
            zf.write(mp4, arcname="mp4/carousel.mp4")

    shutil.rmtree(work)
    return output_zip
