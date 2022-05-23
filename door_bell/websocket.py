#!/usr/bin/env python3

import websockets
import asyncio
import threading
import time

class MSGWorker (threading.Thread):
    def __init__(self, loop, ip: str = '0.0.0.0', port: int = 7700):
        threading.Thread.__init__(self)
        self.connected = set()
        self.loop = loop
        self.ip = ip
        self.port = port
        self.stopFlag = False

    def run(self):
        while not self.stopFlag:
            time.sleep(0.04)

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        try:
            await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected.remove(websocket)

    def sendData(self, data):
        for websocket in self.connected.copy():
            print("Sending data: %s" % data)
            coro = websocket.send(data)
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)