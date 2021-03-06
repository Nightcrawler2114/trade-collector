import asyncio

from pydantic import AnyUrl
from typing import Any

from schemas import TransactionBase
from db import DatabaseHandler


db = DatabaseHandler()


class StockCollectorHandler:

    def __init__(self, url: AnyUrl):

        self.url = url

    async def handle(self) -> None:

        websocket = await self._establish_connection(self.url)

        while True:

            response = await self._receive_response(websocket)

            try:
                model = await self._serialize(response)
            except (KeyError, IndexError):
                continue

            self._save_to_db(model)

    async def _establish_connection(self, url: AnyUrl) -> Any:
        pass

    async def _receive_response(self, websocket: Any) -> str:
        pass

    async def _serialize(self, response: str) -> TransactionBase or None:
        pass

    def _save_to_db(self, model: TransactionBase) -> None:

        if model:
            asyncio.ensure_future(db.add_trade_to_db(model))
