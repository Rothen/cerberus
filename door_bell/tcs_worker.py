#!/usr/bin/env python3

from websocket import MSGWorker
import RPi.GPIO as GPIO
import threading
import time

class TCSWorker(threading.Thread):
    def __init__(self, INTERRUPT_PIN: int, adc, tcs_reader, msg_worker: MSGWorker):
        threading.Thread.__init__(self)
        self.msg_worker = msg_worker
        self.stopFlag = False
        self.INTERRUPT_PIN = INTERRUPT_PIN
        self.adc = adc
        self.tcs_reader = tcs_reader
        GPIO.setup(self.INTERRUPT_PIN, GPIO.OUT)
        GPIO.output(self.INTERRUPT_PIN, GPIO.HIGH)

    def run(self):
        ts = time.time()
        
        while not self.stopFlag:
            GPIO.output(self.INTERRUPT_PIN, self.adc.read(0) >= 300)
            
            if time.time() - ts > 1:
                self.msg_worker.sendData('ping')
                ts = time.time()

            if self.tcs_reader.hasCommand():
                cmd = self.tcs_reader.read()
                self.msg_worker.sendData(cmd)
                print("TCS Bus: " + hex(cmd))