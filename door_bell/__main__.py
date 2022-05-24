#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
from ws_worker import WSWorker
import asyncio
from tcs_worker import TCSWorker
from tcs_bus import wiringPiSetupGpio, TCSBusReader, TCSBusWriter
from consts import *

GPIO.setmode(GPIO.BCM)
wiringPiSetupGpio()

tcs_reader = TCSBusReader(READ_PIN)
tcs_writer = TCSBusWriter(WRITE_PIN)

ws_worker = WSWorker()
tcs_worker = TCSWorker(INTERRUPT_PIN, tcs_reader, tcs_writer, ws_worker)

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

    asyncio.get_event_loop().run_forever()