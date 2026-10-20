# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/20 19:18
"""
from langchain_openai import ChatOpenAI

from app.config import settings

def get_chat_model(streaming: bool = False) -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.chat_model,
        base_url=settings.chat_base_url,
        api_key=settings.chat_api_key,
        streaming=streaming,
        temperature=settings.chat_temperature,
    )
