from enum import Enum


class TransactionTypeEnum(str, Enum):
    sale = 'sale'
    purchase = 'purchase'
