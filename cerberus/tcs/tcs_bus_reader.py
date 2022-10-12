from cerberus.tcs import tcs_bus
from typing import Callable


class TCSBusReader:
    __tcs_bus_reader: tcs_bus.TCSBusReader
    __read_event_handlers: list[Callable[[int, int, int, int], None]] = []

    def __init__(self, readPin: int):
        self.__tcs_bus_reader = tcs_bus.TCSBusReader(readPin, self.__on_read_command)

    def __on_read_command(self, cmd: int, crc: int, calc_crc: int, cmd_length: int) -> None:
        for read_event_handler in self.__read_event_handlers:
            read_event_handler(cmd, crc, calc_crc, cmd_length)

    def register_read_event_handler(self, handler: Callable[[int, int, int, int], None]) -> None:
        self.__read_event_handlers.append(handler)

    def begin(self) -> None:
        self.__tcs_bus_reader.begin()

    def enable(self) -> None:
        self.__tcs_bus_reader.enable()

    def disable(self) -> None:
        self.__tcs_bus_reader.disable()

    def hasCommand(self) -> bool:
        return self.__tcs_bus_reader.hasCommand()

    def read(self) -> tuple :
        return self.__tcs_bus_reader.read()