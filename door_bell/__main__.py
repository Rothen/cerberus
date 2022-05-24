#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
from ws_worker import WSWorker
import websockets
import asyncio
from tcs_worker import TCSWorker
from tcs_bus import wiringPiSetupGpio, TCSBusReader, TCSBusWriter
from consts import *

GPIO.setmode(GPIO.BCM)
wiringPiSetupGpio()

loop = asyncio.get_event_loop()

tcs_reader = TCSBusReader(READ_PIN)
tcs_writer = TCSBusWriter(WRITE_PIN)

ws_worker = WSWorker(loop)
tcs_worker = TCSWorker(INTERRUPT_PIN, tcs_reader, ws_worker)

def signal_handler(sig, frame):
    tcs_worker.stop()
    ws_worker.stop()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    tcs_reader.begin()
    ws_worker.start()
    tcs_worker.start()
    
    loop.run_until_complete(ws_worker.ws_server)
    loop.run_forever()