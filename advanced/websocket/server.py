# server.py
import asyncio
import websockets


async def echo(websocket, path):
    print("path:",path)
    async for message in websocket:
        await websocket.send('Echo: ' + message)

start_server = websockets.serve(echo, 'localhost', 8765)
print("hello")

# asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()