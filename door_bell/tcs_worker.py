#!/usr/bin/env python3

from ws_worker import WSWorker
import RPi.GPIO as GPIO
from mcp3008 import MCP3008
import threading
import time
from tcs_bus_reader import TCSBusReader
from consts import *
from datetime import datetime

class TCSWorker(threading.Thread):
    interrupt_pin: int
    tcs_bus_reader: TCSBusReader
    ws_worker: WSWorker
    mcp_3008 = MCP3008
    requests: dict

    _stop_flag = bool

    def __init__(self, tcs_bus_reader: TCSBusReader, ws_worker: WSWorker):
        threading.Thread.__init__(self)

        self.tcs_bus_reader = tcs_bus_reader
        self.ws_worker = ws_worker
        self.requests: dict = TCS_REQUESTS
        self.prepare_commands()

        self._stop_flag = False

    def prepare_commands(self) -> None:
            self.requests[RING_UPSTAIRS]['fn'] = self.on_ring_upstairs
            self.requests[RING_DOWNSTAIRS]['fn'] = self.on_ring_downstairs
            self.requests[CANCLE_VOICE_CHANNEL_A]['fn'] = self.on_cancle_voice_channel_a
            self.requests[CANCLE_VOICE_CHANNEL_B]['fn'] = self.on_cancle_voice_channel_b


    def run(self):
        while not self._stop_flag:
            if self.tcs_bus_reader.hasCommand():
                command_value = self.tcs_bus_reader.read()
                
                with open("commands.log", "a") as myfile:
                    myfile.write(str(datetime.now()) + ":\t" + hex(command_value) + "\n")

                if not command_value in self.requests.keys():
                    print("Unknown TCS Bus Recieved: " + hex(command_value))
                    continue

                print("TCS Bus Recieved: " + hex(command_value))

                command = self.requests[command_value]
                command['fn']()

            time.sleep(0.1)
    
    def stop(self):
        self._stop_flag = True
        self.join()

    cancel_voice_channel_sequence_counter: int = 0

    def on_ring_upstairs(self) -> None:
        self.ws_worker.send_data(WEB_SOCKET_COMMANDS[RING_UPSTAIRS])

    def on_ring_downstairs(self) -> None:
        self.ws_worker.send_data(WEB_SOCKET_COMMANDS[RING_DOWNSTAIRS])

    def on_cancle_voice_channel_a(self) -> None:
        if self.cancel_voice_channel_sequence_counter == 0:
            self.cancel_voice_channel_sequence_counter = 1
        elif self.cancel_voice_channel_sequence_counter == 1:
            self.cancel_voice_channel_sequence_counter == 2
        else:
            self.cancel_voice_channel_sequence_counter = 0

    def on_cancle_voice_channel_b(self) -> None:
        if self.cancel_voice_channel_sequence_counter == 3:
            self.cancel_voice_channel_sequence_counter = 4
        elif self.cancel_voice_channel_sequence_counter == 4:
            self.cancel_voice_channel_sequence_counter == 0
            self.ws_worker.send_data(WEB_SOCKET_COMMANDS[CANCLE_VOICE_CHANNEL_B])
        else:
            self.cancel_voice_channel_sequence_counter = 0