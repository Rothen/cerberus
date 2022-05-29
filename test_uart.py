import serial
from time import sleep
from datetime import datetime

RING_UPSTAIRS = 0x109E8141
RING_DOWNSTAIRS = 0x009E8180
CANCLE_VOICE_CHANNEL_A = 0x3080
CANCLE_ACTIVITY = 0x2480 #  0x2401
OPEN_DOOR = 0x109E8180
OPEN_VOICE_CHANNEL = 0x309E8100
CONTROL_SEQUENCE = 0x5802

ser = serial.Serial("/dev/ttyS0", 9600)

while True:
    while ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").replace('\r\n', '')
        print(line)
        lines = line.split(', ')

        if len(lines) > 1:
            parsed_cmd = lines[0].replace('GOT: ', '')
            parsed_crc = lines[1].replace('CRC: ', '')
            parsed_calc_crc = lines[2].replace('CALC_CRC: ', '')

            cmd = int(parsed_cmd, base=16)
            crc = int(parsed_crc, base=10)
            calc_crc = int(parsed_calc_crc, base=10)

            with open("commands.log", "a") as myfile:
                    myfile.write('%s:\t%s;%s;%s\n' % (datetime.now(), parsed_cmd, parsed_crc, parsed_calc_crc))
        else:
            parsed_cmd = lines[0].replace('SEND: ', '')
            cmd = int(parsed_cmd, base=16)

    sleep(0.1)