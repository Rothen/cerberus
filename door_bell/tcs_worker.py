#!/usr/bin/env python3

from ws_worker import WSWorker
import RPi.GPIO as GPIO
from mcp3008 import MCP3008
import threading
import time

class TCSWorker(threading.Thread):
    def __init__(self, interrupt_pin: int, tcs_reader, ws_worker: WSWorker, adc: MCP3008 = MCP3008()):
        threading.Thread.__init__(self)
        self.ws_worker = ws_worker
        self.stop_flag = False
        self.interrupt_pin = interrupt_pin
        self.adc = adc
        self.tcs_reader = tcs_reader
        GPIO.setup(self.interrupt_pin, GPIO.OUT)
        GPIO.output(self.interrupt_pin, GPIO.HIGH)

    def run(self):
        ts = time.time()
        
        while not self.stop_flag:
            GPIO.output(self.interrupt_pin, self.adc.read(0) >= 300)
            
            if time.time() - ts > 1:
                self.ws_worker.send_data('ping')
                ts = time.time()

            if self.tcs_reader.hasCommand():
                cmd = self.tcs_reader.read()
                self.ws_worker.send_data(cmd)
                print("TCS Bus: " + hex(cmd))
    
    def stop(self):
        self.stop_flag = True
        self.join()