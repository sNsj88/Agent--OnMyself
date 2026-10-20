# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/20 12:44
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    chat_model : str
    chat_base_url : str
    chat_api_key : str

    token_budget : int = 1000
    temperature = 0.3

settings = Settings()