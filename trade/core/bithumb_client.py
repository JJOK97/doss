"""
빗썸 API 클라이언트 (API 2.0)
"""
import logging
from typing import Optional
import python_bithumb
import pandas as pd

from core.config import settings

logger = logging.getLogger(__name__)


class BithumbClient:
    """빗썸 API 2.0 클라이언트"""

    def __init__(self):
        self._bithumb = python_bithumb.Bithumb(
            settings.BITHUMB_API_KEY,
            settings.BITHUMB_SECRET_KEY
        )

    def get_current_price(self, symbol: str) -> Optional[float]:
        """현재가 조회"""
        try:
            price = python_bithumb.get_current_price(f"KRW-{symbol}")
            return float(price) if price else None
        except Exception as e:
            logger.error(f"가격 조회 실패: {e}")
            return None

    def get_ohlcv(self, symbol: str, interval: str = "minute60", count: int = 200) -> Optional[pd.DataFrame]:
        """OHLCV 데이터 조회"""
        try:
            df = python_bithumb.get_ohlcv(f"KRW-{symbol}", interval=interval, count=count)
            return df
        except Exception as e:
            logger.error(f"OHLCV 조회 실패: {e}")
            return None

    def get_balance(self, symbol: str) -> tuple[float, float]:
        """잔고 조회 (코인, 원화)"""
        try:
            # 코인 잔고
            coin_balance = self._bithumb.get_balance(f"KRW-{symbol}")
            # 원화 잔고
            krw_balance = self._bithumb.get_balance("KRW")

            return float(coin_balance or 0), float(krw_balance or 0)
        except Exception as e:
            logger.error(f"잔고 조회 실패: {e}")
            return 0.0, 0.0

    def buy_market_order(self, symbol: str, krw_amount: float) -> Optional[str]:
        """시장가 매수"""
        try:
            result = self._bithumb.buy_market_order(f"KRW-{symbol}", krw_amount)
            if result:
                logger.info(f"매수 체결: {symbol}, {krw_amount}원")
                return str(result.get('uuid', result))
            return None
        except Exception as e:
            logger.error(f"매수 실패: {e}")
            return None

    def sell_market_order(self, symbol: str, quantity: float) -> Optional[str]:
        """시장가 매도"""
        try:
            result = self._bithumb.sell_market_order(f"KRW-{symbol}", quantity)
            if result:
                logger.info(f"매도 체결: {symbol}, {quantity}")
                return str(result.get('uuid', result))
            return None
        except Exception as e:
            logger.error(f"매도 실패: {e}")
            return None


bithumb_client = BithumbClient()
