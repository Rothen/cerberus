#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
from mcp3008 import MCP3008
from websocket import MSGWorker
import websockets
import asyncio
from tcs_worker import TCSWorker
from tcs_bus import wiringPiSetupGpio, TCSBusReader, TCSBusWriter

GPIO.setmode(GPIO.BCM)
wiringPiSetupGpio()

INTERRUPT_PIN = 22
READ_PIN = 17
WRITE_PIN = 23

OPEN_DOOR = 0x109E8180
OPEN_VOICE_CHANNEL = 0x309e8100
RING_UPSTAIRS = 0x109E8141
RING_DOWNSTAIRS = 0x009E8180

'''
0x3080, 0x3080, 0x2480, 0x2480, after voice channel
'''

adc = MCP3008()
tcs_reader = TCSBusReader(READ_PIN)
tcs_writer = TCSBusWriter(WRITE_PIN)
loop = asyncio.get_event_loop()
msg_worker = MSGWorker(loop)
worker = TCSWorker(INTERRUPT_PIN, adc, tcs_reader, msg_worker)
ws_server = websockets.serve(msg_worker.handler, '0.0.0.0', 7700)

def signal_handler(sig, frame):
    worker.stopFlag = True
    msg_worker.stopFlag = True
    worker.join()
    msg_worker.join()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    tcs_reader.begin()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        msg_worker.start()
        worker.start()
        
        ws_server = websockets.serve(msg_worker.handler, '0.0.0.0', 7700)
        loop.run_until_complete(ws_server)
        loop.run_forever()
    except KeyboardInterrupt:
        msg_worker.stopFlag = True
        print("Exiting program...")