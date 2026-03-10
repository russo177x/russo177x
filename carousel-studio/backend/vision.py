from __future__ import annotations

from pathlib import Path
from typing import Iterable

VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv"}


def classify_media(files: Iterable[str]) -> dict:
    media = []
    has_image = False
    has_video = False

    for path in files:
        suffix = Path(path).suffix.lower()
        kind = "video" if suffix in VIDEO_EXTS else "image"
        has_image = has_image or kind == "image"
        has_video = has_video or kind == "video"
        media.append({"path": path, "kind": kind})

    mode = "mixed" if has_image and has_video else ("video" if has_video else "image")
    return {"mode": mode, "items": media}
