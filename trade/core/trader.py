"""
트레이딩 엔진
"""
import logging
from typing import Optional

from core.config import settings
from core.bithumb_client import bithumb_client
from strategies.base import BaseStrategy

logger = logging.getLogger(__name__)


class Trader:
    """전략 기반 트레이더"""

    def __init__(self, strategy: BaseStrategy, symbol: str = None):
        self.strategy = strategy
        self.symbol = symbol or settings.DEFAULT_SYMBOL
        self.is_running = False

    def set_strategy(self, strategy: BaseStrategy):
        """전략 교체"""
        self.strategy = strategy
        logger.info(f"전략 변경: {type(strategy).__name__}")

    def execute_trade(self) -> Optional[dict]:
        """거래 실행"""
        try:
            # 데이터 조회
            ohlcv = bithumb_client.get_ohlcv(self.symbol)
            if ohlcv is None:
                logger.warning("데이터 없음")
                return None

            # 잔고 조회
            coin_balance, krw_balance = bithumb_client.get_balance(self.symbol)

            # 매수 확인
            if self.strategy.should_buy(ohlcv):
                return self._buy(krw_balance)

            # 매도 확인
            if self.strategy.should_sell(ohlcv):
                return self._sell(coin_balance)

            logger.info("신호 없음")
            return None

        except Exception as e:
            logger.error(f"거래 오류: {e}")
            return None

    def _buy(self, krw_balance: float) -> Optional[dict]:
        """매수 실행"""
        if krw_balance <= 5000:
            logger.info(f"잔고 부족: {krw_balance}원")
            return None

        order_id = bithumb_client.buy_market_order(self.symbol, krw_balance)
        if order_id:
            return {"action": "매수", "amount": krw_balance}
        return None

    def _sell(self, coin_balance: float) -> Optional[dict]:
        """매도 실행"""
        if coin_balance <= 0:
            logger.info("보유 코인 없음")
            return None

        order_id = bithumb_client.sell_market_order(self.symbol, coin_balance)
        if order_id:
            return {"action": "매도", "quantity": coin_balance}
        return None

    def get_status(self) -> dict:
        """상태 조회"""
        coin_balance, krw_balance = bithumb_client.get_balance(self.symbol)
        return {
            "symbol": self.symbol,
            "strategy": type(self.strategy).__name__,
            "is_running": self.is_running,
            "coin_balance": coin_balance,
            "krw_balance": krw_balance
        }
