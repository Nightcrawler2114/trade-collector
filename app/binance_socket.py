import datetime
import json
import websockets

from typing import Optional, Union, List

from websockets import WebSocketClientProtocol

from app.abstract import StockCollectorHandler
from app.schemas import TransactionBase
from app.enums import TransactionTypeEnum, MarketEnum


class BinanceStockHandler(StockCollectorHandler):

    async def _establish_connection(self, url: str, params:  Union[str, List]) -> WebSocketClientProtocol:

        websocket = await websockets.connect(url)

        connection_dict = {"method": "SUBSCRIBE", "params": params, "id": 1}

        await websocket.send(json.dumps(connection_dict))

        return websocket

    async def _receive_response(self, websocket: WebSocketClientProtocol) -> str:

        response = await websocket.recv()

        return response

    async def _serialize(self, response: str) -> Optional[TransactionBase]:

        json_response = json.loads(response)

        if json_response['e'] in ('trade', 'aggTrade'):

            date = datetime.datetime.fromtimestamp(json_response['T'] // 1000.0)

            trade_type = TransactionTypeEnum.sale if json_response['s'] else TransactionTypeEnum.purchase

            model = TransactionBase(
                market=MarketEnum.binance,
                transaction_id=json_response['t'],
                pair=json_response['s'],
                volume=json_response['p'],
                quantity=json_response['q'],
                type=trade_type,
                date=date,
            )

            print(model)

            return model

        return None
