from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class SlideAsset:
    index: int
    kind: str  # image | video
    source: str


def enforce_video_distribution(
    assets: Iterable[SlideAsset], total_slides: int
) -> List[SlideAsset]:
    ordered = sorted(list(assets), key=lambda a: a.index)
    videos = [a for a in ordered if a.kind == "video"]
    images = [a for a in ordered if a.kind == "image"]

    even_slots = [i for i in range(2, total_slides + 1, 2)]
    result: List[SlideAsset] = []

    for idx in range(1, total_slides + 1):
        if idx in (1, total_slides):
            if images:
                item = images.pop(0)
            elif videos:
                item = videos.pop(0)
            else:
                item = SlideAsset(index=idx, kind="image", source="placeholder")
            result.append(SlideAsset(index=idx, kind=item.kind, source=item.source))
            continue

        if idx in even_slots and videos:
            item = videos.pop(0)
        elif images:
            item = images.pop(0)
        elif videos:
            item = videos.pop(0)
        else:
            item = SlideAsset(index=idx, kind="image", source="placeholder")
        result.append(SlideAsset(index=idx, kind=item.kind, source=item.source))

    return result
