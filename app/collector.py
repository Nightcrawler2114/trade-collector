import asyncio

from settings import BITFINEX_API_URL, BINANCE_API_URL
from sockets import BitfinexStockHandler, BinanceStockHandler


async def main() -> None:

    await asyncio.gather(
        BitfinexStockHandler(url=BITFINEX_API_URL).handle(),
        BinanceStockHandler(url=BINANCE_API_URL).handle()
    )


if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(main())
