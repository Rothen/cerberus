from serial import Serial
import time
from datetime import datetime

from cerberus.command_event import CommandEvent
from cerberus.worker import TCSCommunicator

class UARTWorker(TCSCommunicator):
    name: str = 'UART Worker'
    _serial: Serial

    def __init__(self):
        TCSCommunicator.__init__(self)

    def start(self) -> None:
        print('Initializing UART /dev/ttyS0')
        self._serial = Serial("/dev/ttyS0", 9600)
        super().start()

    def _read_commmand(self) -> CommandEvent:
        if self._serial.in_waiting > 0:
            line = self._serial.readline().decode("utf-8").replace('\r\n', '')
            lines = line.split(', ')
            print('UART Incoming Line: %s' % (line))

            if len(lines) > 1:
                return self.parse_command(lines)
        
        return None

    def _write_commmand(self, cmd: str) -> None:
        self._serial.write(bytes(cmd), 'utf-8')

    def parse_command(self, lines: list[str]) -> CommandEvent:
        parsed_cmd = lines[0].replace('GOT: ', '')
        parsed_crc = lines[1].replace('CRC: ', '')
        parsed_calc_crc = lines[2].replace('CALC_CRC: ', '')

        cmd = int(parsed_cmd, base=16)
        crc = int(parsed_crc, base=10)
        calc_crc = int(parsed_calc_crc, base=10)

        return CommandEvent(cmd, crc, calc_crc)
    
    def stop(self):
        super().stop()
        self._serial.close()

    ''' GOT: 0x25648975, CRC: 0, CALC_CRC: 0 '''