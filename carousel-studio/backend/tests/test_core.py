import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent import CopyAgent
from uxrules import SlideAsset, enforce_video_distribution
from vision import classify_media


class CoreBehaviorTests(unittest.TestCase):
    def test_classify_media_mixed(self) -> None:
        result = classify_media(["cover.jpg", "clip.mp4", "photo.png"])
        self.assertEqual(result["mode"], "mixed")
        self.assertEqual(
            [item["kind"] for item in result["items"]], ["image", "video", "image"]
        )

    def test_video_distribution_respects_boundaries(self) -> None:
        assets = [
            SlideAsset(index=1, kind="video", source="v1.mp4"),
            SlideAsset(index=2, kind="image", source="i1.jpg"),
            SlideAsset(index=3, kind="video", source="v2.mp4"),
            SlideAsset(index=4, kind="image", source="i2.jpg"),
        ]
        distributed = enforce_video_distribution(assets, total_slides=8)

        self.assertEqual(distributed[0].kind, "image")
        self.assertEqual(distributed[-1].kind, "image")
        self.assertEqual(len(distributed), 8)

    def test_agent_split_copy_count(self) -> None:
        agent = CopyAgent()
        output = agent.split_copy(
            raw_text="Linha 1\nLinha 2",
            slides=5,
            template_name="Provocacao Viral",
            niche="Games",
        )
        self.assertEqual(len(output), 5)
        self.assertTrue(output[0].startswith("S01 | Games"))


if __name__ == "__main__":
    unittest.main()
