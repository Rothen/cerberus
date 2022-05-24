#!/usr/bin/env python3

import websockets
import asyncio
import threading
import time

class WSWorker (threading.Thread):
    ip: str
    port: int

    _stop_flag: bool
    _connected: set
    _ws_server: any
    _loop: asyncio.AbstractEventLoop

    def __init__(self, ip: str = '0.0.0.0', port: int = 7700):
        threading.Thread.__init__(self)

        self.ip = ip
        self.port = port
        
        self._stop_flag = False
        self._connected = set()

        self._ws_server = websockets.serve(self.handler, ip, port)
        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self._ws_server)

    def run(self):
        while not self._stop_flag:
            time.sleep(0.04)

    async def handler(self, websocket, path):
        self._connected.add(websocket)
        try:
            await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self._connected.remove(websocket)

    def send_data(self, data):
        for websocket in self._connected.copy():
            print("Sending data: %s" % data)
            res = websocket.send(data)
            asyncio.run_coroutine_threadsafe(res, self._loop)
    
    def stop(self):
        self._stop_flag = True
        self.join()