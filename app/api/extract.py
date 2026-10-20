# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/20 22:53
"""
import logging

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.runnables import Runnable

from app.core.llm import get_chat_model
from app.core.prompts import EXTRACT_PROMPT
from app.schemas.extract import AfterSalesTicket, ExtractRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/extract", tags=["extract"])

def get_extractor() -> Runnable:
    model_with_structured = get_chat_model().with_structured_output(AfterSalesTicket)
    return EXTRACT_PROMPT.pipe(model_with_structured)

@router.post("", response_model=AfterSalesTicket)
async def extract(
req: ExtractRequest, extractor: Runnable = Depends(get_extractor)
) -> AfterSalesTicket:
    try:
        return await extractor.ainvoke({"text": req.text})
    except Exception as exc:
        logger.exception("结构化提取失败")
        raise HTTPException(status_code=502, detail="上游模型暂时不可用,请稍后重试") from exc