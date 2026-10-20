# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/20 16:25
"""
from enum import Enum

from pydantic import BaseModel, Field

class ExtractRequest(BaseModel):
    text: str = Field(min_length=1, description="用户的售后描述原文")

class RequestType(str, Enum):
    REFUND = "退款"
    EXCHANGE = "换货"
    REPAIR = "维修"
    COMPLAINT = "投诉"
    OTHER = "其他"

class AfterSalesTicket(BaseModel):
    """从用户的售后信息中提取售后工单"""

    order_id: str | None = Field(description="工单ID")
    request_type : RequestType = Field(description="用户的售后意图")
    expected_solution : str = Field(description="用户的处理方案，一句话概括")
