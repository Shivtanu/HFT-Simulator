import asyncio
import websockets
import json

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.callbacks = []

    def register_callback(self, callback):
        self.callbacks.append(callback)

    async def connect(self):
        async with websockets.connect(self.uri) as ws:
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                for callback in self.callbacks:
                    callback(data)
