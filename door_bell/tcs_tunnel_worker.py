import RPi.GPIO as GPIO
from mcp3008 import MCP3008
import threading

class TCSTunnelWorker(threading.Thread):
    interrupt_pin: int
    mcp_3008 = MCP3008

    _stop_flag = bool

    def __init__(self, interrupt_pin: int, mcp_3008: MCP3008 = MCP3008()):
        threading.Thread.__init__(self)

        self.interrupt_pin = interrupt_pin
        self.mcp_3008 = mcp_3008

        self._stop_flag = False

        GPIO.setup(self.interrupt_pin, GPIO.OUT)
        GPIO.output(self.interrupt_pin, GPIO.HIGH)

    def run(self):
        while not self._stop_flag:
            GPIO.output(self.interrupt_pin, self.mcp_3008.read(0) >= 500)
    
    def stop(self):
        self._stop_flag = True
        self.join()