#include "TCSBus.h"
import RPi.GPIO as GPIO
import pigpio
pi = pigpio.pi()

s_cmd = 0
s_cmdLength = 0
s_cmdReady = False
curCMD = 0
usLast = 0
curCRC = 0
calCRC = 0
curLength = 0
cmdIntReady = 0
curPos = 0

def printHEX(data):
    numChars = 8 if data > 0xFFFF else 4
    mask = 0x0000000F
    mask = mask << 4 * (numChars - 1)
    for i in range(numChars, 0, -1):
        print(hex(((data & mask) >> (i - 1) * 4)))
        mask = mask >> 4

class TCSBusReader:
    def __init__(self, readPin):
        self.m_readPin = readPin
        self.m_enabled = False
        pass

    def begin(self):
        GPIO.setup(self.m_readPin, GPIO.IN)
        self.enable()

    def enable(self):
        if not self.m_enabled:
            self.m_enabled = True
            GPIO.add_event_detect(self.m_readPin, GPIO.BOTH,
                                  callback=self.analyzeCMD)

            # attachInterrupt(digitalPinToInterrupt(m_readPin), analyzeCMD, CHANGE)

    def disable(self):
        if self.m_enabled:
            self.m_enabled = False
            GPIO.remove_event_detect(self.m_readPin)

    def hasCommand(self):
        global s_cmdReady

        return s_cmdReady

    def read(self):
        global s_cmd
        global s_cmdReady

        if s_cmdReady:
            return 0

        tmp = s_cmd
        s_cmdReady = False
        return tmp

    def inject(self, cmd):
        global s_cmd
        global s_cmdReady

        s_cmdReady = 1
        s_cmd = cmd

    def analyzeCMD(self, channel):
        ''' this method is magic from https://github.com/atc1441/TCSintercomArduino
        TODO extract these to members'''
        global s_cmd
        global s_cmdLength
        global s_cmdReady
        global curCMD
        global usLast
        global curCRC
        global calCRC
        global curLength
        global cmdIntReady
        global curPos

        usNow = pi.get_current_tick()
        timeInUS = usNow - usLast
        usLast = usNow
        curBit = 4
        if (timeInUS >= 1000 and timeInUS <= 2999):
            curBit = 0
        elif (timeInUS >= 3000 and timeInUS <= 4999):
            curBit = 1
        elif (timeInUS >= 5000 and timeInUS <= 6999):
            curBit = 2
        elif (timeInUS >= 7000 and timeInUS <= 24000):
            curBit = 3
            curPos = 0

        if (curPos == 0):
            if (curBit == 2):
                curPos = curPos + 1

            curCMD = 0
            curCRC = 0
            calCRC = 1
            curLength = 0
        elif (curBit == 0 or curBit == 1):
            if (curPos == 1):
                curLength = curBit
                curPos = curPos + 1
            elif (curPos >= 2 and curPos <= 17):
                if (curBit):
                    curCMD = curCMD | (0b1 << ((33 if curLength else 17) - curPos))

                calCRC ^= curBit
                curPos = curPos + 1
            elif (curPos == 18):
                if (curLength):
                    if (curBit):
                        curCMD = curCMD | (0b1 << (33 - curPos))

                    calCRC ^= curBit
                    curPos = curPos + 1
                else:
                    curCRC = curBit
                    cmdIntReady = 1
            elif (curPos >= 19 and curPos <= 33):
                if (curBit):
                    curCMD = curCMD | (0b1 << (33 - curPos))
                    
                calCRC ^= curBit
                curPos = curPos + 1
            elif (curPos == 34):
                curCRC = curBit
                cmdIntReady = 1
        else:
            curPos = 0

        if (cmdIntReady):
            cmdIntReady = 0
            if (curCRC == calCRC):
                s_cmdReady = 1
                s_cmdLength = curLength; # todo this variable seems to be not used anywhere
                s_cmd = curCMD
            curCMD = 0
            curPos = 0