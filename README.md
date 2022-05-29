g++ -O3 -Wall -shared -fPIC $(python3 -m pybind11 --includes) tcs/tcs_bus_reader.cpp tcs/tcs_bus_writer.cpp tcs/tcs_bus.cpp -o door_bell/tcs_bus$(python3-config --extension-suffix) -lwiringPi -llgpio



g++ -O3 -Wall tcs/tcs_bus_reader.cpp tcs/tcs_bus_writer.cpp tcs/test.cpp -o tcs/test -lwiringPi -llgpio

g++ -O3 -Wall tcs/test_pigpio.cpp -o tcs/test_pigpio -lpigpio