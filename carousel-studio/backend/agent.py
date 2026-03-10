from __future__ import annotations

import os
from textwrap import shorten
from typing import List

FRAMEWORK_HINTS = {
    "Hook Curiosidade": "Abertura Curiosa",
    "Autoridade Stats": "Autoridade",
    "Beneficio Direto": "Beneficio",
    "Lista Impacto": "Lista Valiosa",
    "Problema Solucao": "Problema/Solucao",
    "Passo a Passo": "Passo a Passo",
    "Provocacao Viral": "Pergunta Impactante",
    "Demo Showcase": "Demo orientada por gameplay",
}


class CopyAgent:
    def __init__(self) -> None:
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")

    @property
    def provider(self) -> str:
        return "groq" if self.groq_key else "ollama"

    def split_copy(
        self, raw_text: str, slides: int, template_name: str, niche: str
    ) -> List[str]:
        framework = FRAMEWORK_HINTS.get(template_name, "Framework geral")
        chunks = [c.strip() for c in raw_text.split("\n") if c.strip()]
        if not chunks:
            chunks = [raw_text.strip()] if raw_text.strip() else ["Sem texto enviado"]

        output: List[str] = []
        for idx in range(slides):
            source = chunks[idx % len(chunks)]
            prefix = f"S{idx + 1:02d} | {niche} | {framework}: "
            output.append(prefix + shorten(source, width=180, placeholder="..."))
        return output
