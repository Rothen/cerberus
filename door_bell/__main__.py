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

GPIO.setmode(GPIO.BCM)
wiringPiSetupGpio()

tcs_bus_reader = TCSBusReader(READ_PIN)
tcs_bus_writer = TCSBusWriter(WRITE_PIN)

ws_worker = WSWorker()
tcs_worker = TCSWorker(INTERRUPT_PIN, tcs_bus_reader, tcs_bus_writer, ws_worker)

def signal_handler(sig, frame):
    tcs_worker.stop()
    ws_worker.stop()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    tcs_bus_reader.begin()
    ws_worker.start()
    tcs_worker.start()

    asyncio.get_event_loop().run_forever()