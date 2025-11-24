"""
API 라우트
"""
from fastapi import APIRouter

from api.schemas import BuyRequest, SellRequest
from core.bithumb_client import bithumb_client

router = APIRouter()

# main.py에서 설정됨
trader = None


@router.get("/")
def get_status():
    """상태 조회"""
    return trader.get_status()


@router.get("/balance")
def get_balance():
    """잔고 조회"""
    coin_balance, krw_balance = bithumb_client.get_balance(trader.symbol)
    current_price = bithumb_client.get_current_price(trader.symbol)

    return {
        "symbol": trader.symbol,
        "coin_balance": coin_balance,
        "krw_balance": krw_balance,
        "current_price": current_price,
        "coin_value": coin_balance * current_price if current_price else 0,
        "total_value": (coin_balance * current_price if current_price else 0) + krw_balance
    }


@router.post("/start")
def start():
    """거래 시작"""
    trader.is_running = True
    return {"message": "시작됨"}


@router.post("/stop")
def stop():
    """거래 중지"""
    trader.is_running = False
    return {"message": "중지됨"}


@router.post("/buy")
def manual_buy(request: BuyRequest):
    """수동 매수"""
    coin_balance, krw_balance = bithumb_client.get_balance(trader.symbol)

    # 금액 계산
    if request.amount:
        amount = request.amount
    elif request.percent:
        amount = krw_balance * (request.percent / 100)
    else:
        amount = krw_balance

    if amount <= 5000:
        return {"error": "잔고 부족", "krw_balance": krw_balance}

    order_id = bithumb_client.buy_market_order(trader.symbol, amount)
    if order_id:
        return {"message": "매수 완료", "amount": amount, "order_id": order_id}
    return {"error": "매수 실패"}


@router.post("/sell")
def manual_sell(request: SellRequest):
    """수동 매도"""
    coin_balance, krw_balance = bithumb_client.get_balance(trader.symbol)
    current_price = bithumb_client.get_current_price(trader.symbol)

    # 수량 계산
    if request.amount and current_price:
        quantity = request.amount / current_price
    elif request.percent:
        quantity = coin_balance * (request.percent / 100)
    else:
        quantity = coin_balance

    if quantity <= 0:
        return {"error": "보유 코인 없음", "coin_balance": coin_balance}

    order_id = bithumb_client.sell_market_order(trader.symbol, quantity)
    if order_id:
        return {"message": "매도 완료", "quantity": quantity, "order_id": order_id}
    return {"error": "매도 실패"}
