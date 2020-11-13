import datetime
import json
import websockets

from typing import Optional, List, Union

from websockets import WebSocketClientProtocol

from app.abstract import StockCollectorHandler
from app.schemas import TransactionBase
from app.enums import TransactionTypeEnum, MarketEnum


class BitfinexStockHandler(StockCollectorHandler):

    async def _establish_connection(self, url: str, params: Union[str, List]) -> WebSocketClientProtocol:

        websocket = await websockets.connect(url)

        connection_dict = {"event": "subscribe", "channel": "trades", "symbol": params}

        await websocket.send(json.dumps(connection_dict))

        return websocket

    async def _receive_response(self, websocket: WebSocketClientProtocol) -> str:

        response = await websocket.recv()

        return response

    async def _serialize(self, response: str) -> Optional[TransactionBase]:

        json_response = json.loads(response)

        date = datetime.datetime.fromtimestamp(json_response[2][1] // 1000.0)

        if json_response[1] == 'te':

            return None

        amount = json_response[2][3]

        trade_type = TransactionTypeEnum.sale if amount < 0 else TransactionTypeEnum.purchase

        model = TransactionBase(
                market=MarketEnum.bitfinex,
                transaction_id=json_response[2][0],
                pair='BTC/USD',
                volume=amount,
                quantity=json_response[2][2],
                type=trade_type,
                date=date,
        )

        print(model)

        return model
