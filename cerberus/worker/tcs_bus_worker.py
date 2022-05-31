#!/usr/bin/env python3

from cerberus.command_event import CommandEvent
from cerberus.tcs import TCSBusReader, TCSBusWriter
from cerberus.const import *
from cerberus.worker import TCSCommunicator

class TCSBusWorker(TCSCommunicator):
    name: str = 'TCS Bus Worker'
    _tcs_bus_reader: TCSBusReader
    _tcs_bus_writer: TCSBusWriter

    def __init__(self, tcs_bus_reader: TCSBusReader, tcs_bus_writer: TCSBusWriter):
        TCSCommunicator.__init__(self)

        self._tcs_bus_reader = tcs_bus_reader
        self._tcs_bus_writer = tcs_bus_writer

    def start(self) -> None:
        print('Initializing TCS Bus Reader')
        self._tcs_bus_reader.begin()
        print('Initializing TCS Bus Writer')
        self._tcs_bus_writer.begin()
        super().start()

    def _read_commmand(self) -> CommandEvent:
        if self._tcs_bus_reader.hasCommand():
            return self.parse_command()
        
        return None

    def _write_commmand(self, cmd: int) -> None:
        self._tcs_bus_reader.disable()
        self._tcs_bus_writer.write(cmd)
        self._tcs_bus_reader.enable()

    def parse_command(self) -> CommandEvent:
        cmd, crc, calc_crc, cmd_length = self._tcs_bus_reader.read()

        return CommandEvent(cmd, crc, calc_crc, cmd_length)