import asyncio

from sockets import BitfinexStockHandler, BinanceStockHandler

from settings import BITFINEX_API_URL, BINANCE_API_URL


async def main() -> None:

    await asyncio.gather(
        BitfinexStockHandler(url=BITFINEX_API_URL).handle(),
        BinanceStockHandler(url=BINANCE_API_URL).handle()
    )


if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(main())
