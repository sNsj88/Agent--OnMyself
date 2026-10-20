# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/20 19:44
"""
import json
import logging
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage

from app.config import settings
from app.core.llm import get_chat_model
from app.core.memory import SessionStore, trim_history
from app.core.prompts import CUSTOMER_SERVICE_PROMPT
from app.schemas.chat import ChatRequest

def get_model() -> BaseChatModel:
    return get_chat_model(streaming=True)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])
store = SessionStore()

@router.post("")
async def chat(req: ChatRequest, model: BaseChatModel = Depends(get_model)):
    un_trim_message = [*store.get(req.session_id), HumanMessage(req.message)]
    trim_message = trim_history(un_trim_message, max_token=settings.token_budget)
    messages = CUSTOMER_SERVICE_PROMPT.format_messages(messages=trim_message)

    async def event_stream() -> AsyncIterator[str]:
        chunks: list[str] = []
        try:
            async for chunk in model.astream(messages):
                text = ""
                if isinstance(chunk.content, str):
                    text = chunk.content
                if not text:
                    continue
                chunks.append(text)
                yield f"data: {json.dumps({'delta': text}, ensure_ascii=False)}\n\n"
        except Exception as e:
            logger.exception("上游 LLM 流式调用失败 session_id=%s", req.session_id)
            yield "event: error\n"
            yield f"data: {json.dumps({'message': '上游模型暂时不可用,请稍后重试'}, ensure_ascii=False)}\n\n"
            return
        store.append(req.session_id, HumanMessage(req.message), AIMessage("".join(chunks)))
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")