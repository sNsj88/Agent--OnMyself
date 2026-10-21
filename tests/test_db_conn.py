# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/21 16:19
"""
# tests/test_db_conn.py
from sqlalchemy import text

async def test_test_db_reachable_and_tables_exist(_test_engine, db_clean):
    async with _test_engine.connect() as conn:
        rows = (await conn.execute(text("SHOW TABLES"))).scalars().all()
    assert {"conversations", "messages", "faq", "tickets"} <= set(rows)