# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/20 17:02
"""
from langchain_core.messages import BaseMessage
from langchain_core.messages.utils import count_tokens_approximately, trim_messages

class SessionStore:

    def __init__(self):
        self._session: dict[int, list[BaseMessage]] = {}

    def get(self, session_id: int) -> list[BaseMessage]:
        return self._session.get(session_id, [])

    def append(self, session_id: int, *message: BaseMessage) -> None:
        self._session.setdefault(session_id, []).extend(message)

def trim_history(messages: list[BaseMessage], max_token: int) -> list[BaseMessage]:
    return trim_messages(
        messages,
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=max_token,
        start_on="human",
        allow_partial=False,
    )