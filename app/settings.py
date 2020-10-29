import os


DATABASE_URL = os.getenv('MONGO_DB_URL')

BITFINEX_API_URL = 'wss://api-pub.bitfinex.com/ws/2'
BINANCE_API_URL = 'wss://stream.binance.com:9443/ws/btcusdt@trade'