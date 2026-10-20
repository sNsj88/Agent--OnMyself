# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/20 16:25
"""
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id : str = Field(min_length=1, description="会话ID，同一个会话用一个ID")
    message: str = Field(min_length=1, description="用户本轮的消息")
