import asyncio

from sockets import get_data_from_bitfinex, get_data_from_binance


if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(get_data_from_bitfinex())
    asyncio.get_event_loop().run_forever()