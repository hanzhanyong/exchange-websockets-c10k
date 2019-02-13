import aiohttp
import asyncio
import websockets


# async def hello():
#     url = "wss://ws.exx.com/websocket"
#     proxy = "http://127.0.0.1:1087"
#     async with websockets.connect(url,) as websocket:

#         payload = await websocket.recv()
#         print(f"{payload}")
async def main():
    url = "wss://kline.exx.com/websocket"
    proxy = "http://127.0.0.1:1087"
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url, proxy=proxy) as ws:
            await ws.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
