import asyncio

from typing import Optional, Union, List

from websockets import WebSocketClientProtocol

from app.db import DatabaseHandler
from app.schemas import TransactionBase

db = DatabaseHandler()


class StockCollectorHandler:

    def __init__(self, url: str, params: Union[str, List]):

        self.url = url
        self.params = params

    async def handle(self) -> None:

        websocket = await self._establish_connection(self.url, self.params)

        while True:

            response = await self._receive_response(websocket)

            try:
                model = await self._serialize(response)
            except (KeyError, IndexError):
                continue

            self._save_to_db(model)

    async def _establish_connection(self, url: str, params: str) -> WebSocketClientProtocol:
        pass

    async def _receive_response(self, websocket:  WebSocketClientProtocol) -> str:
        pass

    async def _serialize(self, response: str) -> Optional[TransactionBase]:
        pass

    def _save_to_db(self, model: TransactionBase) -> None:

        if model:
            asyncio.ensure_future(db.add_trade_to_db(model))
