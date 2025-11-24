"""
API 요청/응답 스키마
"""
from pydantic import BaseModel
from typing import Optional


class BuyRequest(BaseModel):
    amount: Optional[float] = None      # 원화 금액
    percent: Optional[float] = None     # 잔고의 비율 (0-100)


class SellRequest(BaseModel):
    amount: Optional[float] = None      # 원화 금액 기준 매도
    percent: Optional[float] = None     # 보유 코인의 비율 (0-100)
