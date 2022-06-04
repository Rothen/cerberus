#!/usr/bin/env python3

import threading
import time
from datetime import datetime
from reactivex import Subject, operators as op
from abc import ABC, abstractmethod

from cerberus.command_event import CommandEvent

class TCSCommunicator(threading.Thread, ABC):
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
                if cmd_event.distance <= 3:
                    self.command_read.on_next(cmd_event)
                    self.write_to_log(cmd_event)
                else:
                    self.write_to_error(cmd_event)

                print('TCS Bus Read %s (%s)' % (hex(cmd_event.cmd), hex(cmd_event.original_command)))

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
        self._write_to(cmd_event, "commands_log.csv")

    def write_to_error_log(self, cmd_event: CommandEvent) -> None:
        self._write_to(cmd_event, "error_log.csv")

    def _write_to(self, cmd_event: CommandEvent, file_name: str) -> None:
        with open(file_name, "a") as log_file:
            log_file.write("%s;%s;%s;%i;%i;%i;%i\n" % (datetime.now(), hex(cmd_event.original_command), hex(cmd_event.cmd), cmd_event.distance, cmd_event.crc, cmd_event.calc_crc, cmd_event.cmd_length))