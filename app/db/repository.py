# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/21 16:47
"""
# app/db/repository.py
from datetime import datetime

from sqlalchemy import select, func

import app.db.base as db       # 用模块属性引用,便于测试 monkeypatch async_session
from app.db.models import Conversation, Faq, Message, Ticket, KnowledgeChunk, QaExtractionStaging

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

from app.db.models import KnowledgeChunk, QaExtractionStaging  # 合并进已有 import 行

async def insert_knowledge_chunk(
        category: str, questions: str, answer: str,
        section_path: str | None = None, content_type: str | None = None,
        is_key_clause: int = 0,
) -> int:
    async with db.async_session() as s:
        row = KnowledgeChunk(
            category=category, questions=questions, answer=answer,
            section_path=section_path, content_type=content_type,
            is_key_clause=is_key_clause,
        )
        s.add(row)
        await s.commit()
        return row.id

async def list_pending_chunks() -> list[KnowledgeChunk]:
    async with db.async_session() as s:
        result = await s.execute(
            select(KnowledgeChunk)
            .where(KnowledgeChunk.vectorize_status == "pending")
            .order_by(KnowledgeChunk.id)
        )
        return list(result.scalars())

async def mark_chunk_vectorized(chunk_id: int, vector_id: str) -> None:
    async with db.async_session() as s:
        row = await s.get(KnowledgeChunk, chunk_id)
        if row is not None:
            row.vector_id = vector_id
            row.vectorize_status = "done"
            await s.commit()

async def set_chunk_neighbors(chunk_id: int, prev_id: int | None, next_id: int | None) -> None:
    async with db.async_session() as s:
        row = await s.get(KnowledgeChunk, chunk_id)
        if row is not None:
            row.prev_chunk_id = prev_id
            row.next_chunk_id = next_id
            await s.commit()

async def count_chunks_by_status(status: str) -> int:
    async with db.async_session() as s:
        result = await s.execute(
            select(func.count()).select_from(KnowledgeChunk)
            .where(KnowledgeChunk.vectorize_status == status)
        )
        return int(result.scalar_one())

async def list_all_questions() -> list[str]:
    async with db.async_session() as s:
        result = await s.execute(select(KnowledgeChunk.questions))
        return list(result.scalars())

async def insert_staging(batch_no: str, source_ref: str | None, question: str, answer: str) -> int:
    async with db.async_session() as s:
        row = QaExtractionStaging(
            batch_no=batch_no, source_ref=source_ref, question=question, answer=answer
        )
        s.add(row)
        await s.commit()
        return row.id

async def list_staging_by_status(status: str) -> list[QaExtractionStaging]:
    async with db.async_session() as s:
        result = await s.execute(
            select(QaExtractionStaging)
            .where(QaExtractionStaging.status == status)
            .order_by(QaExtractionStaging.id)
        )
        return list(result.scalars())

async def set_staging_status(ids: list[int], status: str) -> None:
    if not ids:
        return
    async with db.async_session() as s:
        for i in ids:
            row = await s.get(QaExtractionStaging, i)
            if row is not None:
                row.status = status
        await s.commit()

async def list_conversations_with_messages() -> list[tuple[int, list[Message]]]:
    async with db.async_session() as s:
        conv_ids = list((await s.execute(select(Conversation.id).order_by(Conversation.id))).scalars())
        out = []
        for cid in conv_ids:
            msgs = list((await s.execute(
                select(Message).where(Message.conversation_id == cid).order_by(Message.id)
            )).scalars())
            out.append((cid, msgs))
        return out