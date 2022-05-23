#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
from mcp3008 import MCP3008
from tcs_bus import wiringPiSetupGpio, TCSBusReader, TCSBusWriter

GPIO.setmode(GPIO.BCM)
wiringPiSetupGpio()

INTERRUPT_PIN = 22
READ_PIN = 17
WRITE_PIN = 23

adc = MCP3008()
tcs_reader = TCSBusReader(READ_PIN)
tcs_writer = TCSBusWriter(WRITE_PIN)

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    GPIO.setup(INTERRUPT_PIN, GPIO.OUT)
    GPIO.output(INTERRUPT_PIN, GPIO.HIGH)
    tcs_reader.begin()

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        GPIO.output(INTERRUPT_PIN, adc.read(0) >= 300)
        
        if tcs_reader.hasCommand():
            cmd = tcs_reader.read()

            print("TCS Bus: " + hex(cmd))