#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import asyncio
from cerberus.const import *
from cerberus.tcs import TCSBusReader, TCSBusWriter, wiringPiSetupGpio
from cerberus.worker import TCSTunnelWorker, WSWorker, TCSBusWorker, UARTWorker

GPIO.setmode(GPIO.BCM)
wiringPiSetupGpio()

use_uart = False

tcs_bus_worker = TCSBusWorker(TCSBusReader(READ_PIN), TCSBusWriter(WRITE_PIN))

uart_worker = UARTWorker()
tcs_tunnel_worker = TCSTunnelWorker(INTERRUPT_PIN)

ws_worker = WSWorker(uart_worker if use_uart else tcs_bus_worker)

def exit_signal_handler(sig, frame):
    if not use_uart:
        tcs_tunnel_worker.stop()

    ws_worker.stop()

    GPIO.cleanup()

    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_signal_handler)

    if not use_uart:
        print('Starting TCS Tunnel Worker')
        tcs_tunnel_worker.start()

    print('Starting Websocket Worker')
    ws_worker.start()

    asyncio.get_event_loop().run_forever()