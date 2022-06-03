#!/usr/bin/env python3

from reactivex import Subject
import websockets
import asyncio
import threading
import time

from cerberus.api import APITokenContainer
from cerberus.const import *
from cerberus.command_event import CommandEvent
from cerberus.worker import TCSCommunicator

class WSWorker (threading.Thread):
    ip: str
    port: int

    _api_token_container: APITokenContainer
    _subscription: Subject
    _stop_flag: bool
    _connected: set
    _ws_server: any
    _loop: asyncio.AbstractEventLoop
    _tcs_communicator: TCSCommunicator

    def __init__(self, tcs_communicator: TCSCommunicator, ip: str = '0.0.0.0', port: int = 7700):
        threading.Thread.__init__(self)

        self._tcs_communicator = tcs_communicator
        self.ip = ip
        self.port = port
        
        self._stop_flag = False
        self._connected = set()
        self.requests = WS_REQUESTS
        self.prepare_commands()

        self._api_token_container = APITokenContainer()
        self._subscription = self._tcs_communicator.command_read.subscribe(
            on_next = self.command_read
        )

        self._ws_server = websockets.serve(self.handler, ip, port)
        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self._ws_server)

    def start(self) -> None:
        super().start()
        print('Starting %s' % (self._tcs_communicator.name))
        self._tcs_communicator.start()

    def prepare_commands(self) -> None:
        self.requests['RING_UPSTAIRS']['fn'] = self.send_ring_upstairs
        self.requests['RING_DOWNSTAIRS']['fn'] = self.send_ring_downstairs
        self.requests['CANCEL_VOICE_CONTROL_SEQUENCE']['fn'] = self.send_cancel_voice_control_sequence
        self.requests['CANCEL_CONTROL_SEQUENCE']['fn'] = self.send_cancel_control_sequence
        self.requests['OPEN_DOOR']['fn'] = self.send_open_door
        self.requests['OPEN_VOICE_CHANNEL']['fn'] = self.send_open_voice_channel
        self.requests['CONTROL_SEQUENCE']['fn'] = self.send_control_sequence

    def run(self):
        while not self._stop_flag:
            time.sleep(0.04)

    async def handler(self, websocket, path: str):
        token = websocket.recv()

        if not self._api_token_container.check(token):
            websocket.close(1008, 'API Token not registered.')

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

    def stop(self):
        self._tcs_communicator.stop()
        self._subscription.dispose()
        self._stop_flag = True

        for websocket in self._connected.copy():
            websocket.close(1001)
            self._connected.remove(websocket)

        self.join()

    def command_read(self, command_event: CommandEvent) -> None:
        self.send(hex(command_event.cmd))

    def send(self, data: str):
        print("WS Sending data: %s" % data)
        for websocket in self._connected.copy():
            res = websocket.send(data)
            asyncio.run_coroutine_threadsafe(res, self._loop)

    def send_ring_upstairs(self) -> None:
        print("Writing " + hex(RING_UPSTAIRS))
        self._tcs_communicator.write(RING_UPSTAIRS)


    def send_ring_downstairs(self) -> None:
        print("Writing " + hex(RING_DOWNSTAIRS))
        self._tcs_communicator.write(RING_DOWNSTAIRS)


    def send_cancel_voice_control_sequence(self) -> None:
        print("Writing " + hex(CANCEL_VOICE_CONTROL_SEQUENCE))
        self._tcs_communicator.write(CANCEL_VOICE_CONTROL_SEQUENCE)


    def send_cancel_control_sequence(self) -> None:
        print("Writing " + hex(CANCEL_CONTROL_SEQUENCE))
        self._tcs_communicator.write(CANCEL_CONTROL_SEQUENCE)


    def send_open_door(self) -> None:
        print("Writing " + hex(OPEN_DOOR))
        self._tcs_communicator.write(OPEN_DOOR)


    def send_open_voice_channel(self) -> None:
        print("Writing " + hex(OPEN_VOICE_CHANNEL))
        self._tcs_communicator.write(OPEN_VOICE_CHANNEL)


    def send_control_sequence(self) -> None:
        print("Writing " + hex(CONTROL_SEQUENCE))
        self._tcs_communicator.write(CONTROL_SEQUENCE)
