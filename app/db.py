import motor.motor_asyncio

from settings import DATABASE_URL

from schemas import TransactionBase

# mongodb+srv://vladmongo:vladmongo@cluster0.5fu91.mongodb.net/test

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://vladmongo:vladmongo@cluster0.5fu91.mongodb.net/test')

db = client.vladmongo
collection = db.trades

class DatabaseHandler():

    def __init__(self):

        self.db = db
        self.collection = collection

    async def add_trade_to_db(self, data: dict):

        model = TransactionBase(**data)

        await self.collection.insert_one(**model)