# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/21 16:47
"""
# app/db/repository.py
from datetime import datetime

from sqlalchemy import select

import app.db.base as db       # 用模块属性引用,便于测试 monkeypatch async_session
from app.db.models import Conversation, Faq, Message, Ticket

_TICKET_SEQ = 0

def _gen_ticket_no() -> str:
    global _TICKET_SEQ
    _TICKET_SEQ += 1
    return f"T{datetime.now():%Y%m%d%H%M%S}{_TICKET_SEQ:03d}"

async def create_conversation(user_id: str) -> int:
    async with db.async_session() as session:
        conv = Conversation(user_id=user_id)
        session.add(conv)
        await session.commit()
        await session.refresh(conv)
        return conv.id

async def get_conversation(conversation_id : int) -> Conversation | None:
    async with db.async_session() as session:
        stmt = select(Conversation).where(Conversation.id == conversation_id)
        result = await session.execute(stmt)
        return result.scalars().first()

async def append_message(conversation_id: int, role: str, content: str | None = None, tool_calls: list | None = None, tool_call_id: str | None = None) -> int:
    async with db.async_session() as session:
        message = Message(conversation_id=conversation_id, role=role, content=content, tool_calls=tool_calls, tool_call_id=tool_call_id)
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message.id

async def list_messages(conversation_id: int) -> list[Message]:
    async with db.async_session() as session:
        stmt = select(Message).where(Message.conversation_id == conversation_id)
        result = await session.execute(stmt)
        return result.scalars().all()

async def search_faq(keyword: str) -> list[Faq]:
    async with db.async_session() as session:
        stmt = select(Faq).where(Faq.question.like(f"%{keyword}%"))
        result = await session.execute(stmt)
        return result.scalars().all()

async def create_ticket(conversation_id: int, description: str, ticket_type: str) -> str:
    async with db.async_session() as session:
        conv = await session.get(Conversation, conversation_id)
        conv.status = "已转人工"
        ticket_no = _gen_ticket_no()
        ticket = Ticket(ticket_no=ticket_no, conversation_id=conv.id, description=description, ticket_type=ticket_type)
        session.add(ticket)
        await session.commit()
        return ticket_no