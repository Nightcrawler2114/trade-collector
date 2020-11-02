import motor.motor_asyncio

try:
    from schemas import TransactionBase
    from settings import DATABASE_URL
except ImportError:
    from app.schemas import TransactionBase
    from app.settings import DATABASE_URL

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

db = client.trade_collection
collection = db.trades


class DatabaseHandler:

    def __init__(self):

        self.db = db
        self.collection = collection

    async def add_trade_to_db(self, transaction: TransactionBase) -> None:

        count = await self.collection.count_documents(transaction.__dict__)

        if count == 0:

            await self.collection.insert_one(transaction.__dict__)
