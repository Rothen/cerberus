from cerberus.tcs import tcs_bus

class TCSBusReader:
    __tcs_bus_reader: tcs_bus.TCSBusReader

    def __init__(self, readPin: int):
        self.__tcs_bus_reader = tcs_bus.TCSBusReader(readPin)
        pass

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