CXX = g++
dir = tcs_bus/
reader_writer_dir = $(dir)reader_writer/
read_write_objects = tcs_bus_reader.o tcs_bus_writer.o
pybind11_includes = -fPIC -I/usr/include/python3.9 -I/home/pi/.local/lib/python3.9/site-packages/pybind11/include
pybind11_suffix = .cpython-39-arm-linux-gnueabihf.so

all: pybind

pybind: tcs_bus_pybind.o $(read_write_objects)
	$(CXX) -O3 -Wall -shared -o cerberus/tcs/tcs_bus$(pybind11_suffix) tcs_bus_pybind.o $(read_write_objects) -lwiringPi -llgpio

tcs_bus_pybind.o: $(dir)tcs_bus_pybind.cpp
	$(CXX) $(pybind11_includes) -c $(dir)tcs_bus_pybind.cpp

tcs_bus_reader.o: $(reader_writer_dir)tcs_bus_reader.cpp $(reader_writer_dir)tcs_bus_reader.h $(reader_writer_dir)common.h
	$(CXX) -c $(reader_writer_dir)tcs_bus_reader.cpp

tcs_bus_writer.o: $(reader_writer_dir)tcs_bus_writer.cpp $(reader_writer_dir)tcs_bus_writer.h $(reader_writer_dir)common.h
	$(CXX) -c $(reader_writer_dir)tcs_bus_writer.cpp

clean :
	-rm *.o