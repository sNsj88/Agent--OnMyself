# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/20 12:44
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

# 获取项目根目录（config.py 通常在 app/ 下，所以向上一级）
ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")

    chat_model : str
    chat_base_url : str
    chat_api_key : str

    token_budget : int = 1000
    temperature: float = 0.3
    database_url : str = "mysql+asyncmy://root:root@localhost:3306/mewhelp"
    test_database_url : str= "mysql+asyncmy://root:root@localhost:3306/mewhelp"

    embed_model: str

    embed_base_url : str
    embed_api_key : str
    retrieval_top_k : int = 10
    retrieval_min_score : float
    milvus_uri: str = "data/milvus_knowledge.db"
settings = Settings()