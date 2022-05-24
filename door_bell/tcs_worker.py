#!/usr/bin/env python3

from ws_worker import WSWorker
import RPi.GPIO as GPIO
from mcp3008 import MCP3008
import threading
import time
from tcs_bus_reader import TCSBusReader
from tcs_bus_writer import TCSBusWriter

class TCSWorker(threading.Thread):
    interrupt_pin: int
    tcs_bus_reader: TCSBusReader
    tcs_bus_writer: TCSBusWriter
    ws_worker: WSWorker
    mcp_3008 = MCP3008

    _stop_flag = bool

    def __init__(self, interrupt_pin: int, tcs_bus_reader: TCSBusReader, tcs_bus_writer: TCSBusWriter, ws_worker: WSWorker, mcp_3008: MCP3008 = MCP3008()):
        threading.Thread.__init__(self)

        self.interrupt_pin = interrupt_pin
        self.tcs_bus_reader = tcs_bus_reader
        self.tcs_bus_writer = tcs_bus_writer
        self.ws_worker = ws_worker
        self.mcp_3008 = mcp_3008

        self._stop_flag = False

        GPIO.setup(self.interrupt_pin, GPIO.OUT)
        GPIO.output(self.interrupt_pin, GPIO.HIGH)

    def run(self):
        ts = time.time()
        
        while not self._stop_flag:
            GPIO.output(self.interrupt_pin, self.mcp_3008.read(0) >= 300)
            
            if time.time() - ts > 1:
                self.ws_worker.send_data('ping')
                ts = time.time()

            if self.tcs_bus_reader.hasCommand():
                cmd = self.tcs_bus_reader.read()
                self.ws_worker.send_data(cmd)
                print("TCS Bus: " + hex(cmd))
    
    def stop(self):
        self._stop_flag = True
        self.join()