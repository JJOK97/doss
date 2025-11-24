"""
RSI 전략
"""
import logging
import pandas as pd
from strategies.base import BaseStrategy
from core.config import settings

logger = logging.getLogger(__name__)


def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    """RSI 계산 (Wilder's Smoothing)"""
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-2]


class RSIStrategy(BaseStrategy):
    """단순 RSI 전략"""

    def __init__(self, period: int = None, oversold: float = None, overbought: float = None):
        self.period = period or settings.RSI_PERIOD
        self.oversold = oversold or settings.RSI_OVERSOLD
        self.overbought = overbought or settings.RSI_OVERBOUGHT

    def should_buy(self, ohlcv: pd.DataFrame) -> bool:
        """RSI < 30이면 매수"""
        if len(ohlcv) < self.period + 2:
            return False
        rsi = calculate_rsi(ohlcv['close'], self.period)
        logger.info(f"RSI: {rsi:.1f} (매수 기준: {self.oversold})")
        return rsi < self.oversold

    def should_sell(self, ohlcv: pd.DataFrame) -> bool:
        """RSI > 70이면 매도"""
        if len(ohlcv) < self.period + 2:
            return False
        rsi = calculate_rsi(ohlcv['close'], self.period)
        logger.info(f"RSI: {rsi:.1f} (매도 기준: {self.overbought})")
        return rsi > self.overbought
