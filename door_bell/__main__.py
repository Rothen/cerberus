#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
from ws_worker import WSWorker
import asyncio
from tcs_worker import TCSWorker
from tcs_bus import wiringPiSetupGpio # type: ignore
from tcs_bus_reader import TCSBusReader
from tcs_bus_writer import TCSBusWriter
from consts import *
from ws_worker import WSWorker
import RPi.GPIO as GPIO
from mcp3008 import MCP3008
import threading
from tcs_bus_reader import TCSBusReader
from consts import *

GPIO.setmode(GPIO.BCM)
wiringPiSetupGpio()

class WK(threading.Thread):
    interrupt_pin: int
    mcp_3008 = MCP3008

    _stop_flag = bool

    def __init__(self, interrupt_pin: int, mcp_3008: MCP3008 = MCP3008()):
        threading.Thread.__init__(self)

        self.interrupt_pin = interrupt_pin
        self.mcp_3008 = mcp_3008

        self._stop_flag = False

        GPIO.setup(self.interrupt_pin, GPIO.OUT)
        GPIO.output(self.interrupt_pin, GPIO.HIGH)

    def run(self):
        minimum = 10000
        while not self._stop_flag:
            value = self.mcp_3008.read(0)

            if value < minimum:
                minimum = value
                print(value)
                
            GPIO.output(self.interrupt_pin, self.mcp_3008.read(0) >= 500)
    
    def stop(self):
        self._stop_flag = True
        self.join()

tcs_bus_reader = TCSBusReader(READ_PIN)
tcs_bus_writer = TCSBusWriter(WRITE_PIN)
wk = WK(INTERRUPT_PIN)
ws_worker = WSWorker(tcs_bus_writer)
tcs_worker = TCSWorker(tcs_bus_reader, ws_worker)

def exit_signal_handler(sig, frame):
    tcs_worker.stop()
    ws_worker.stop()
    wk.stop()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_signal_handler)
    print('Initializing TCS Bus Reader')
    tcs_bus_reader.begin()
    print('Initializing TCS Bus Writer')
    tcs_bus_writer.begin()

    print('Starting Websocket Thread')
    ws_worker.start()
    print('Starting TCS Thread')
    tcs_worker.start()
    print('Starting WK')
    wk.start()

    asyncio.get_event_loop().run_forever()