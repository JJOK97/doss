"""
전략 기본 인터페이스
"""
from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """모든 전략의 기본 클래스"""

    @abstractmethod
    def should_buy(self, ohlcv: pd.DataFrame) -> bool:
        """매수 여부 반환"""
        pass

    @abstractmethod
    def should_sell(self, ohlcv: pd.DataFrame) -> bool:
        """매도 여부 반환"""
        pass
