#include "tcs_bus.h"

namespace py = pybind11;

PYBIND11_MODULE(tcs_bus, m) {
    py::class_<TCSBusReader>(m, "TCSBusReader")
        .def(py::init([](uint8_t readPin) { return new TCSBusReader(readPin); }))
        .def("begin", &TCSBusReader::begin)
        .def("enable", &TCSBusReader::enable)
        .def("disable", &TCSBusReader::disable)
        .def("hasCommand", &TCSBusReader::hasCommand)
        .def("read", &TCSBusReader::read)
        .def("inject", &TCSBusReader::inject);

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