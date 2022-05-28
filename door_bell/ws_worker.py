#!/usr/bin/env python3

import websockets
import asyncio
import threading
import time
from consts import *
from tcs_bus_writer import TCSBusWriter

class WSWorker (threading.Thread):
    ip: str
    port: int

    _stop_flag: bool
    _connected: set
    _ws_server: any
    _loop: asyncio.AbstractEventLoop
    _tcs_bus_writer: TCSBusWriter

    def __init__(self, tcs_bus_writer: TCSBusWriter, ip: str = '0.0.0.0', port: int = 7700):
        threading.Thread.__init__(self)

        self.tcs_bus_writer = tcs_bus_writer
        self.ip = ip
        self.port = port
        
        self._stop_flag = False
        self._connected = set()
        self.requests = WS_REQUESTS
        self.prepare_commands()

        self._ws_server = websockets.serve(self.handler, ip, port)
        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self._ws_server)

    def prepare_commands(self) -> None:
            self.requests['OPEN_DOOR']['fn'] = self.open_door
            self.requests['OPEN_VOICE_CHANNEL']['fn'] = self.open_voice_channel

    def run(self):
        while not self._stop_flag:
            time.sleep(0.04)

    async def handler(self, websocket, path):
        self._connected.add(websocket)
        try:
            while True:
                command_value = await websocket.recv()
                if not command_value in self.requests.keys():
                    continue

                print('Web Socket Recieved: ' + command_value)
                command = self.requests[command_value]
                command['fn']()


        except websockets.exceptions.ConnectionClosed:
            print('Close Connection')
            pass
        finally:
            self._connected.remove(websocket)
            pass

    def send_data(self, data):
        for websocket in self._connected.copy():
            print("Sending data: %s" % data)
            res = websocket.send(data)
            asyncio.run_coroutine_threadsafe(res, self._loop)
    
    def stop(self):
        self._stop_flag = True
        self.join()

    def open_door(self) -> None:
        print("Writing " + hex(OPEN_DOOR))
        self.tcs_bus_writer.write(OPEN_DOOR)

    def open_voice_channel(self) -> None:
        print("Writing " + hex(RING_UPSTAIRS))
        self.tcs_bus_writer.write(RING_UPSTAIRS)