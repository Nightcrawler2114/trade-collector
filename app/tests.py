import datetime

import pytest

from app.schemas import TransactionBase
from app.sockets import BinanceStockHandler, BitfinexStockHandler
from app.settings import BINANCE_API_URL, BITFINEX_API_URL


@pytest.mark.asyncio
async def test_binance_serialization():

    string = '{"e": "aggTrade", "E": 123456789, "s": "BNBBTC", "a": 12345, "p": "0.001", "q": "100", "f": 100,"l": 105, "t": 12345, "T": 123456785, "m": true, "M": true}'

    date = datetime.datetime.fromtimestamp(123456785 // 1000.0)

    model_to_compare = TransactionBase(
        market='Binance',
        transaction_id=12345,
        pair='BNBBTC',
        volume=0.001,
        quantitiy=100,
        type='sale',
        date=date
    )

    response = await BinanceStockHandler(url=BINANCE_API_URL)._serialize(response=string)

    assert model_to_compare == response


@pytest.mark.asyncio
async def test_bitfinex_serialization():
    string = '[17470,"tu",[401597395,1574694478808,0.005,7245.3]]'

    date = datetime.datetime.fromtimestamp(1574694478808 // 1000.0)

    model_to_compare = TransactionBase(
        market='Bitfinex',
        transaction_id='401597395',
        pair='BTC/USD',
        volume=7245.3,
        quantitiy=0.005,
        type='sale',
        date=date
    )

    response = await BitfinexStockHandler(url=BITFINEX_API_URL)._serialize(response=string)

    assert model_to_compare == response
