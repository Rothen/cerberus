from serial import Serial
import time
from datetime import datetime
import re

from cerberus.command_event import CommandEvent
from cerberus.worker import TCSCommunicator

class UARTWorker(TCSCommunicator):
    name: str = 'UART Worker'
    _serial: Serial

    _got_regex = r"GOT: (0x?[a-fA-F0-9]+), CRC: (0|1), CALC_CRC: (0|1)"

    def __init__(self):
        TCSCommunicator.__init__(self)

    def start(self) -> None:
        print('Initializing UART /dev/ttyS0')
        self._serial = Serial("/dev/ttyS0", 9600)
        super().start()

    def _read_commmand(self) -> CommandEvent:
        if self._serial.in_waiting > 0:
            line = self._serial.readline().decode("utf-8").replace('\r\n', '')
            print('UART Incoming: %s' % (line))
            m = re.search('GOT: (0x[0-F]*), CRC: (0|1), CALC_CRC: (0|1)', 'abcdef')
            matches = re.findall(self._got_regex, line)
            if len(matches) > 1:
                return self.parse_command(matches)
        
        return None

    def _write_commmand(self, cmd: str) -> None:
        self._serial.write(bytes(cmd), 'utf-8')

    def parse_command(self, matches: list[str]) -> CommandEvent:
        try:
            cmd = int(matches[0], base=16)
            crc = int(matches[1], base=10)
            calc_crc = int(matches[2], base=10)
        except:
            return None

        return CommandEvent(cmd, crc, calc_crc)
    
    def stop(self):
        super().stop()
        self._serial.close()