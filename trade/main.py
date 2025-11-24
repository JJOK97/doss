"""
빗썸 자동매매 시스템
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.config import settings
from core.trader import Trader
from strategies import RSIStrategy
from api import router
from api import routes

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 스케줄러 및 트레이더
scheduler = AsyncIOScheduler()
strategy = RSIStrategy()
trader = Trader(strategy=strategy, symbol=settings.DEFAULT_SYMBOL)


def trading_job():
    """스케줄링된 거래 작업"""
    if not trader.is_running:
        return
    result = trader.execute_trade()
    if result:
        logger.info(f"거래 결과: {result}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작/종료"""
    logger.info("시스템 시작")

    # routes에 trader 전달
    routes.trader = trader

    # 스케줄러 등록 (수동 시작 모드)
    scheduler.add_job(
        trading_job,
        trigger=IntervalTrigger(seconds=settings.TRADE_INTERVAL_SECONDS),
        id='trading_job'
    )
    scheduler.start()
    trader.is_running = False  # /start 호출 전까지 대기

    yield

    logger.info("시스템 종료")
    scheduler.shutdown()


app = FastAPI(
    title="빗썸 자동매매",
    version="1.0.0",
    lifespan=lifespan
)

# 라우터 등록
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
