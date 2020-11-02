import datetime
import json
import websockets

from pydantic import AnyUrl
from websockets import WebSocketClientProtocol

try:
    from abstract import StockCollectorHandler
    from schemas import TransactionBase
except ImportError:
    from app.abstract import StockCollectorHandler
    from app.schemas import TransactionBase


class BitfinexStockHandler(StockCollectorHandler):

    async def _establish_connection(self, url: AnyUrl) -> WebSocketClientProtocol:

        websocket = await websockets.connect(url)

        await websocket.send('{ "event": "subscribe", "channel": "trades", "symbol": "tBTCUSD"}')

        return websocket

    async def _receive_response(self, websocket: WebSocketClientProtocol) -> str:

        response = await websocket.recv()

        return response

    async def _serialize(self, response: str) -> TransactionBase or None:

        json_response = json.loads(response)

        date = datetime.datetime.fromtimestamp(json_response[2][1] // 1000.0)

        if json_response[1] == 'te':

            return None

        amount = json_response[2][3]

        type_ = 'sale' if amount < 0 else 'purchase'

        model = TransactionBase(
                market='Bitfinex',
                transaction_id=json_response[2][0],
                pair='BTC/USD',
                volume=amount,
                quantitiy=json_response[2][2],
                type=type_,
                date=date,
        )

        print(model)

        return model


class BinanceStockHandler(StockCollectorHandler):

    async def _establish_connection(self, url: AnyUrl) -> WebSocketClientProtocol:

        websocket = await websockets.connect(url)

        await websocket.send('{"method": "SUBSCRIBE", "params": ["btcusdt@aggTrade", "btcusdt@depth"], "id": 1}')

        return websocket

    async def _receive_response(self, websocket: WebSocketClientProtocol) -> str:

        response = await websocket.recv()

        return response

    async def _serialize(self, response: str) -> TransactionBase or None:

        json_response = json.loads(response)

        if json_response['e'] == 'trade' or 'aggTrade':

            date = datetime.datetime.fromtimestamp(json_response['T'] // 1000.0)

            type_ = 'sale' if json_response['s'] else 'purchase'

            model = TransactionBase(
                market='Binance',
                transaction_id=json_response['t'],
                pair=json_response['s'],
                volume=json_response['p'],
                quantitiy=json_response['q'],
                type=type_,
                date=date,
            )

            print(model)

            return model

        return None
