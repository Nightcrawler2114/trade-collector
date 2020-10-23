import asyncio
import websockets

from db import DatabaseHandler


db = DatabaseHandler()


async def get_data_from_bitfinex():

    uri = "wss://api-pub.bitfinex.com/ws/2"

    async with websockets.connect(uri) as websocket:

        await websocket.send('{ "event": "subscribe", "channel": "trades", "symbol": "tBTCUSD"}')

        response = await websocket.recv()
        print(response)  


async def get_data_from_binance():

    uri = "wss://stream.binance.com:9443@trade"

    async with websockets.connect(uri) as websocket:

        # await websocket.send('{ "event": "subscribe", "channel": "trades", "symbol": "tBTCUSD"}')

        response = await websocket.recv()
        print(response)  