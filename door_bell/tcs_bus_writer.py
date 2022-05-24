import tcs_bus # type: ignore

class TCSBusWriter:
    __tcs_bus_writer: tcs_bus.TCSBusWriter

    def __init__(self, writePin: int):
        self.__tcs_bus_writer = tcs_bus.TCSBusWriter(writePin)
        pass

    def begin(self) -> None:
        self.__tcs_bus_writer.begin()

    def isWriting(self) -> bool:
        return self.__tcs_bus_writer.isWriting()

    def write(self, data: int) -> None:
        self.__tcs_bus_writer.write()