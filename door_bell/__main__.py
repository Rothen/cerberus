#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import asyncio
from tcs_bus import wiringPiSetupGpio # type: ignore
from consts import *
from tcs_bus_reader import TCSBusReader
from tcs_bus_writer import TCSBusWriter
from tcs_tunnel_worker import TCSTunnelWorker
from ws_worker import WSWorker
from tcs_bus_worker import TCSBusWorker

GPIO.setmode(GPIO.BCM)
wiringPiSetupGpio()

tcs_bus_reader = TCSBusReader(READ_PIN)
tcs_bus_writer = TCSBusWriter(WRITE_PIN)
tcs_tunnel_worker = TCSTunnelWorker(INTERRUPT_PIN)
tcs_bus_worker = TCSBusWorker(tcs_bus_reader, tcs_bus_writer)
ws_worker = WSWorker(tcs_bus_worker)

def exit_signal_handler(sig, frame):
    tcs_tunnel_worker.stop()
    tcs_bus_worker.stop()
    ws_worker.stop()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_signal_handler)
    print('Initializing TCS Bus Reader')
    tcs_bus_reader.begin()
    print('Initializing TCS Bus Writer')
    tcs_bus_writer.begin()

    print('Starting Websocket Worker')
    ws_worker.start()
    print('Starting TCS Bus Worker')
    tcs_bus_worker.start()
    print('Starting TCS Tunnel Worker')
    tcs_tunnel_worker.start()

    asyncio.get_event_loop().run_forever()