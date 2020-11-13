from enum import Enum


class TransactionTypeEnum(str, Enum):
    sale = 'sale'
    purchase = 'purchase'


class MarketEnum(str, Enum):

    bitfinex = 'Bitfinex'
    binance = 'Binance'