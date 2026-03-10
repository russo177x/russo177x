from __future__ import annotations

import json
from pathlib import Path
from typing import List, Literal
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent import CopyAgent
from exporter import build_export_zip
from uxrules import SlideAsset, enforce_video_distribution
from vision import classify_media

BASE = Path(__file__).parent
TEMPLATES_DIR = BASE / "templates"
EXPORTS_DIR = BASE / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)


class BrandSettings(BaseModel):
    handle: str = "@nflbrinsider"
    name: str = "NFL BRASIL"
    copyright: str = "2026"


class GenerateRequest(BaseModel):
    niche: Literal["NFL", "F1", "Games", "Noticias"]
    template: str
    raw_text: str
    slide_count: int = Field(default=8, ge=5, le=15)
    assets: List[str] = Field(default_factory=list)
    brand: BrandSettings = BrandSettings()


app = FastAPI(title="Instagram Carousel Studio", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = CopyAgent()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "provider": agent.provider}


@app.get("/api/themes")
def themes() -> dict:
    return json.loads((TEMPLATES_DIR / "themes.json").read_text(encoding="utf-8"))


@app.get("/api/templates")
def templates() -> list[dict]:
    return json.loads((TEMPLATES_DIR / "templates.json").read_text(encoding="utf-8"))


@app.get("/api/layouts")
def layouts() -> dict:
    return json.loads((TEMPLATES_DIR / "layouts.json").read_text(encoding="utf-8"))


@app.get("/api/capability")
def capability() -> dict:
    return {
        "can_build_similar": True,
        "supported_slide_range": [5, 15],
        "supported_layouts": ["Template Autoral", "Template Twitter"],
        "notes": [
            "Mosaico editorial com adaptação de densidade de cards por quantidade de slides",
            "Cards estilo social feed com identidade visual e branding por conta",
            "Pipeline atual cobre geração de copy, distribuição de mídia e export PNG/MP4",
        ],
    }


@app.get("/api/examples/games-news")
def games_news_example() -> dict:
    examples = json.loads((TEMPLATES_DIR / "examples.json").read_text(encoding="utf-8"))
    return examples["games_news_nike"]


@app.post("/api/generate")
def generate(req: GenerateRequest) -> dict:
    media = classify_media(req.assets)
    slides = agent.split_copy(req.raw_text, req.slide_count, req.template, req.niche)
    distributed = enforce_video_distribution(
        [
            SlideAsset(index=i + 1, kind=m["kind"], source=m["path"])
            for i, m in enumerate(media["items"])
        ],
        req.slide_count,
    )
    return {
        "provider": agent.provider,
        "mode": media["mode"],
        "slides": [
            {
                "index": idx + 1,
                "text": text,
                "asset_kind": (
                    distributed[idx].kind if idx < len(distributed) else "image"
                ),
            }
            for idx, text in enumerate(slides)
        ],
    }


@app.post("/api/export")
def export(req: GenerateRequest) -> dict:
    slides = agent.split_copy(req.raw_text, req.slide_count, req.template, req.niche)
    watermark = f"{req.brand.handle} | {req.brand.name} | ©{req.brand.copyright}"
    path = EXPORTS_DIR / f"carousel_{uuid4().hex}.zip"
    build_export_zip(slides, path, watermark)
    return {"zip_path": str(path), "slides": len(slides)}
