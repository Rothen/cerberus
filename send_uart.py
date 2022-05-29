import serial
from time import sleep

RING_UPSTAIRS = 0x109E8141
RING_DOWNSTAIRS = 0x009E8180
CANCLE_VOICE = 0x3080
CANCLE_ACTIVITY = 0x2480 #  0x2401
OPEN_DOOR = 0x109E8180
OPEN_VOICE_CHANNEL = 0x309E8100
CONTROL_SEQUENCE = 0x5802

ser = serial.Serial("/dev/ttyS0", 9600)    #Open port with baud rate
ser.write(bytes('%s\n' % (hex(CANCLE_ACTIVITY)), 'utf-8'))
sleep(0.1)
ser.write(bytes('%s\n' % (hex(CANCLE_ACTIVITY)), 'utf-8'))
ser.close()