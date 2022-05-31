#include <pybind11/pybind11.h>
#include <wiringPi.h>
#include "reader_writer/tcs_bus_reader.h"
#include "reader_writer/tcs_bus_writer.h"

namespace py = pybind11;

PYBIND11_MODULE(tcs_bus, m) {
    py::class_<TCSBusReader>(m, "TCSBusReader")
        .def(py::init([](uint8_t readPin) { return new TCSBusReader(readPin); }))
        .def("begin", &TCSBusReader::begin)
        .def("enable", &TCSBusReader::enable)
        .def("disable", &TCSBusReader::disable)
        .def("hasCommand", &TCSBusReader::hasCommand)
        .def("read", [](TCSBusReader &tcs_bus_reader) {
            uint32_t cmd = 0;
            uint8_t crc = 0;
            uint8_t calcCrc = 0;
            uint8_t length = 0;
            
            tcs_bus_reader.read(&cmd, &crc, &calcCrc, &length);

            return std::make_tuple(cmd, crc, calcCrc, length);
        });

    py::class_<TCSBusWriter>(m, "TCSBusWriter")
        .def(py::init([](uint8_t writePin) { return new TCSBusWriter(writePin); }))
        .def("begin", &TCSBusWriter::begin)
        .def("isWriting", &TCSBusWriter::isWriting)
        .def("write", &TCSBusWriter::write);

    m.def("wiringPiSetup", &wiringPiSetup);
    m.def("wiringPiSetupGpio", &wiringPiSetupGpio);
    m.def("wiringPiSetupPhys", &wiringPiSetupPhys);
    m.def("wiringPiSetupSys", &wiringPiSetupSys);
}