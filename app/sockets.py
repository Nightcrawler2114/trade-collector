import asyncio
import websockets
import json
import datetime

from pydantic import AnyUrl
from typing import Any

from schemas import TransactionBase

from abstract import StockCollectorHandler


class BitfinexStockHandler(StockCollectorHandler):

    async def _establish_connection(self, url: AnyUrl) -> Any:

        websocket = await websockets.connect(url)

        await websocket.send('{ "event": "subscribe", "channel": "trades", "symbol": "tBTCUSD"}')

        return websocket

    async def _receive_response(self, websocket: Any) -> str:

        response = await websocket.recv()

        return response

    async def _serialize(self, response: str) -> TransactionBase or None:

        json_response = json.loads(response)

        date = datetime.datetime.fromtimestamp(json_response[2][1] // 1000.0)

        if json_response[1] == 'te':

            return None

        model = TransactionBase(
                market='Bitfinex',
                transaction_id=json_response[2][0],
                pair='BTC/USD',
                volume=json_response[2][3],
                quantitiy=json_response[2][2],
                type='sale',
                date=date,
        )

        print(model)

        return model


class BinanceStockHandler(StockCollectorHandler):

    async def _establish_connection(self, url: AnyUrl) -> Any:

        websocket = await websockets.connect(url)

        await websocket.send('{"method": "SUBSCRIBE", "params": ["btcusdt@aggTrade", "btcusdt@depth"], "id": 1}')

        return websocket

    async def _receive_response(self, websocket: Any) -> str:

        response = await websocket.recv()

        return response

    async def _serialize(self, response: str) -> TransactionBase or None:

        json_response = json.loads(response)

        if json_response['e'] == 'trade' or 'aggTrade':

            date = datetime.datetime.fromtimestamp(json_response['T'] // 1000.0)

            model = TransactionBase(
                market='Binance',
                transaction_id=json_response['t'],
                pair=json_response['s'],
                volume=json_response['p'],
                quantitiy=json_response['q'],
                type='sale',
                date=date,
            )

            print(model)

            return model

        return None
