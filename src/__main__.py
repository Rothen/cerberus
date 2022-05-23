#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
from mcp3008 import MCP3008
# from tcs_bus_reader import TCSBusReader
import ctypes
from ctypes import cdll
import pathlib

GPIO.setmode(GPIO.BCM)

SEND = 22

# reader = TCSBusReader(RECIEVE)
adc = MCP3008()

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    print("Button pressed!")

if __name__ == '__main__':
    libname = pathlib.Path().absolute() / "tcs_bus_reader.so"
    mylib = ctypes.CDLL(libname)
    mylib.setup(0)
    mylib.new_tcs_bus_reader(0)
    mylib.begin()

    GPIO.setup(SEND, GPIO.OUT)
    GPIO.output(SEND, GPIO.HIGH)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        GPIO.output(SEND, adc.read(0) >= 300)
        
        if mylib.hasCommand():
            cmd = mylib.read()

            print("TCS Bus: " + hex(cmd))