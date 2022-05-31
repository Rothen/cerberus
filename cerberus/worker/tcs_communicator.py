#!/usr/bin/env python3

import threading
import time
from datetime import datetime
from reactivex import Subject
from abc import abstractmethod

from cerberus.command_event import CommandEvent

class TCSCommunicator(threading.Thread):
    command_read: Subject[CommandEvent] = Subject()

    name: str
    _read_flag: bool = False
    _write_flag: bool = False
    _stop_flag: bool = False

    def __init__(self):
        threading.Thread.__init__(self)

    @abstractmethod
    def _read_commmand(self) -> CommandEvent:
        pass

    @abstractmethod
    def _write_commmand(self, cmd: int) -> None:
        pass

    def run(self) -> None:
        while not self._stop_flag:
            while self._write_flag:
                time.sleep(0.1)
                pass

            self._read_flag = True

            cmd_event: CommandEvent = self._read_commmand()

            if cmd_event is not None:
                self.command_read.on_next(cmd_event)
                self.write_to_log(cmd_event)
                print('Read %s' % (hex(cmd_event.cmd)))

            self._read_flag = False
            time.sleep(0.1)
    
    def stop(self) -> None:
        self.command_read.on_completed()
        self._stop_flag = True
        self.join()
    
    def write(self, cmd: int) -> None:
        while self._read_flag:
            time.sleep(0.1)

        self._write_commmand(cmd)

    def write_to_log(self, cmd_event: CommandEvent) -> None:
        with open("commands_log.csv", "a") as myfile:
            myfile.write("%s;%s;%s;%i;%i;%i;%i\n" % (datetime.now(), hex(cmd_event.original_command), hex(cmd_event.cmd), cmd_event.distance, cmd_event.crc, cmd_event.calc_crc, cmd_event.cmd_length))