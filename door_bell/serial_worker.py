#!/usr/bin/env python3

from serial import Serial
from ws_worker import WSWorker
import RPi.GPIO as GPIO
from mcp3008 import MCP3008
import threading
import time
from tcs_bus_reader import TCSBusReader
from consts import *
from datetime import datetime

class TCSWorker(threading.Thread):
    ws_worker: WSWorker

    _serial: Serial
    _stop_flag = bool

    def __init__(self, ws_worker: WSWorker):
        threading.Thread.__init__(self)

        self._stop_flag = False


    def run(self):
        self._serial = Serial("/dev/ttyS0", 9600)

        while not self._stop_flag:
            if self._serial.in_waiting > 0:
                line = self._serial.readline().decode("utf-8").replace('\r\n', '')

                if not line.startswith('GOT'):
                    continue

                parsed_line = line.replace('GOT: ', '')
                command_value = int(parsed_line, base=16)
                
                with open("commands.log", "a") as myfile:
                    myfile.write('%s:\t%s\n' % (datetime.now(), parsed_line))

                if not command_value in self.requests.keys():
                    print("Unknown TCS Bus Recieved: " + hex(command_value))
                    continue

                print("TCS Bus Recieved: " + hex(command_value))

                command = self.requests[command_value]
                command['fn']()        

            time.sleep(0.1)

    def write(self, data: str) -> None:
        self._serial.write(bytes(data), 'utf-8')
    
    def stop(self):
        self._stop_flag = True
        self._serial.close()
        self.join()