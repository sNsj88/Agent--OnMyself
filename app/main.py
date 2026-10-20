# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/20 19:44
"""
from fastapi import FastAPI

from app.api.chat import router as chat_router

app = FastAPI(title="MewHelp", version="0.1.0")

app.include_router(chat_router, prefix="/api")