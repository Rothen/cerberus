#!/usr/bin/env python3

import websockets
import asyncio
import threading
import time

class WSWorker (threading.Thread):
    def __init__(self, loop, ip: str = '0.0.0.0', port: int = 7700):
        threading.Thread.__init__(self)
        self.connected = set()
        self.loop = loop
        self.ip = ip
        self.port = port
        self.stop_flag = False
        self.ws_server = None
        self.ws_server = websockets.serve(self.handler, '0.0.0.0', 7700)

    def run(self):
        while not self.stop_flag:
            time.sleep(0.04)

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        try:
            await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected.remove(websocket)

    def send_data(self, data):
        for websocket in self.connected.copy():
            print("Sending data: %s" % data)
            coro = websocket.send(data)
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)
    
    def stop(self):
        self.stop_flag = True
        self.join()