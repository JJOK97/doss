"""
설정 관리 모듈
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 빗썸 API 키
    BITHUMB_API_KEY: str
    BITHUMB_SECRET_KEY: str

    # 거래 설정
    DEFAULT_SYMBOL: str = "BTC"
    TRADE_INTERVAL_SECONDS: int = 60

    # RSI 설정
    RSI_PERIOD: int = 14
    RSI_OVERSOLD: float = 30.0
    RSI_OVERBOUGHT: float = 70.0

    # 로깅
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
