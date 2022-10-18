#!/usr/bin/env python3

from reactivex import Subject
import websockets
import asyncio
import time
from urllib.parse import parse_qs

from cerberus.api import APITokenContainer
from cerberus.const import *
from cerberus.command_event import CommandEvent
from cerberus.worker import TCSCommunicator

class WSWorker:
    ip: str
    port: int

    _api_token_container: APITokenContainer
    _subscription: Subject
    _stop_flag: bool
    _connected: set
    _ws_server: any
    _loop: asyncio.AbstractEventLoop
    _tcs_communicator: TCSCommunicator

    _requests: dict = {}

    def __init__(self, tcs_communicator: TCSCommunicator, ip: str = '0.0.0.0', port: int = 7700):
        self._tcs_communicator = tcs_communicator
        self.ip = ip
        self.port = port
        
        self._stop_flag = False
        self._connected = set()
        self.prepare_commands()

        self._api_token_container = APITokenContainer()
        self._subscription = self._tcs_communicator.command_read.subscribe(
            on_next = self.command_read
        )

    def prepare_commands(self) -> None:
        self._requests[COMMANDS_TO_TEXT[RING_UPSTAIRS]] = self.send_ring_upstairs
        self._requests[COMMANDS_TO_TEXT[RING_DOWNSTAIRS]] = self.send_ring_downstairs
        self._requests[COMMANDS_TO_TEXT[CANCEL_VOICE_CONTROL_SEQUENCE]] = self.send_cancel_voice_control_sequence
        self._requests[COMMANDS_TO_TEXT[CANCEL_CONTROL_SEQUENCE]] = self.send_cancel_control_sequence
        self._requests[COMMANDS_TO_TEXT[CANCEL_RING_CONTROL_SEQUENCE]] = self.send_cancel_ring_control_sequence
        self._requests[COMMANDS_TO_TEXT[OPEN_DOOR]] = self.send_open_door
        self._requests[COMMANDS_TO_TEXT[OPEN_VOICE_CHANNEL]] = self.send_open_voice_channel
        self._requests[COMMANDS_TO_TEXT[CONTROL_SEQUENCE]] = self.send_control_sequence

    def start(self):
        self._ws_server = websockets.serve(self.handler, self.ip, self.port)
        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self._ws_server)

    async def handler(self, websocket, path: str):
        params = parse_qs(path[path.find('?')+1:])

        if 'api_token' not in params or not self._api_token_container.check(params['api_token'][0]):
            print('API Token not registered.')
            await websocket.close(1008, 'API Token not registered.')
            return

        self._connected.add(websocket)
        print('API Token registered.')

        try:
            while True:
                command_value = await websocket.recv()
                if not command_value in self._requests:
                    continue

                print('Web Socket Recieved: ' + command_value)
                request_fn = self._requests[command_value]
                request_fn()


        except websockets.exceptions.ConnectionClosed:
            print('Close Connection')
            pass
        finally:
            self._connected.remove(websocket)
            pass

    def stop(self):
        self._subscription.dispose()
        self._stop_flag = True

        for websocket in self._connected.copy():
            self._loop.create_task(websocket.close(1001))
            self._connected.remove(websocket)

    def command_read(self, command_event: CommandEvent) -> None:
        self.send(COMMANDS_TO_TEXT[command_event.cmd])

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

    def send_cancel_ring_control_sequence(self) -> None:
        print("Writing " + hex(CANCEL_RING_CONTROL_SEQUENCE))
        self._tcs_communicator.write(CANCEL_RING_CONTROL_SEQUENCE)

    def send_open_door(self) -> None:
        print("Writing " + hex(OPEN_DOOR))
        self._tcs_communicator.write(OPEN_DOOR)


    def send_open_voice_channel(self) -> None:
        print("Writing " + hex(OPEN_VOICE_CHANNEL))
        self._tcs_communicator.write(OPEN_VOICE_CHANNEL)


    def send_control_sequence(self) -> None:
        print("Writing " + hex(CONTROL_SEQUENCE))
        self._tcs_communicator.write(CONTROL_SEQUENCE)
