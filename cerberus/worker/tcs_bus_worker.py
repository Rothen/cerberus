#!/usr/bin/env python3

import threading
import time
from datetime import datetime
from reactivex import Subject

from cerberus.command_event import CommandEvent
from cerberus.tcs import TCSBusReader, TCSBusWriter
from cerberus.const import *


class TCSBusWorker(threading.Thread):
    tcs_bus_reader: TCSBusReader
    tcs_bus_writer: TCSBusWriter
    command_read: Subject[CommandEvent] = Subject()

    _run_flag: bool = False
    _pause_flag: bool = False
    _stop_flag = bool = False

    def __init__(self, tcs_bus_reader: TCSBusReader, tcs_bus_writer: TCSBusWriter):
        threading.Thread.__init__(self)

        self.tcs_bus_reader = tcs_bus_reader
        self.tcs_bus_writer = tcs_bus_writer

    def run(self) -> None:
        while not self._stop_flag:
            while self._pause_flag:
                time.sleep(0.1)
                pass

            self._run_flag = True

            if self.tcs_bus_reader.hasCommand():
                cmd_event = self.parse_command()
                self.write_to_log(cmd_event)
                self.command_read.on_next(cmd_event)

            self._run_flag = False
            time.sleep(0.1)
    
    def stop(self) -> None:
        self.command_read.on_completed()
        self._stop_flag = True
        self.join()

    def parse_command(self) -> CommandEvent:
        cmd, crc, calc_crc, cmd_length = self.tcs_bus_reader.read()
        print('read %s' % (hex(cmd)))
        return CommandEvent(cmd, crc, calc_crc, cmd_length)

    def write_command(self, cmd: int) -> None:
        while self._run_flag:
            time.sleep(0.1)
            pass
        
        self._pause_flag = True
        self.tcs_bus_reader.disable()
        self.tcs_bus_writer.write(cmd)
        self.tcs_bus_reader.enable()
        self._pause_flag = False

    def write_to_log(self, cmd_event: CommandEvent) -> None:
        with open("commands_log.csv", "a") as myfile:
            myfile.write("%s;%s;%s;%i;%i;%i;%i\n" % (datetime.now(), hex(cmd_event.original_command), hex(cmd_event.cmd), cmd_event.distance, cmd_event.crc, cmd_event.calc_crc, cmd_event.cmd_length))