from datetime import datetime

from pydantic import BaseModel

try:
    from enums import TransactionTypeEnum
except ImportError:
    from app.enums import TransactionTypeEnum


class TransactionBase(BaseModel):
    market: str
    transaction_id: str
    pair: str
    volume: float
    quantitiy: float
    type: TransactionTypeEnum
    date: datetime

# * на какой бирже она произошла
# * какой у нее ID
# * по какой паре символов (например: BTC/USD - означает то, что были куплены битки за доллары, либо проданы битки за доллары)
# * по какой цене произошла сделка
# * количество: сколько было продано (куплено)
# * была ли это покупка или продажа
# * когда она произошла
