# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/22 16:09
"""

from openai import AsyncOpenAI

from app.config import settings

def _client() -> AsyncOpenAI:
    return AsyncOpenAI(base_url=settings.embed_base_url, api_key=settings.embed_api_key)

async def embed_texts(texts: list[str]) -> list[list[float]]:
    resp = await _client().embeddings.create(model=settings.embed_model, input=texts)
    results = []
    for one in resp.data:
        results.append(one.embedding)
    return results

async def embed_query(text: str) -> list[float]:
    return (await embed_texts([text]))[0]