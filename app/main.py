import asyncio

from app.db import collection

from app.settings import BITFINEX_API_URL, BINANCE_API_URL

from app.binance_socket import BinanceStockHandler
from app.bitfinex_socket import BitfinexStockHandler


async def main() -> None:

    await collection.create_index([('market', 1), ('pair', 1)])

    await asyncio.gather(
        BitfinexStockHandler(url=BITFINEX_API_URL, params='tBTCUSD').handle(),
        BinanceStockHandler(url=BINANCE_API_URL, params=["btcusdt@aggTrade", "btcusdt@depth"]).handle()
    )

