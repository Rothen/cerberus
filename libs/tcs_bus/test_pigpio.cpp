#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <bitset>
#include <iomanip>

#include <pigpio.h>



volatile uint32_t lasttick = 0;

void alertHere(int gpio, int level, uint32_t tick)
{
    /*if (tick - lasttick > 800) 
    {
        lasttick = tick;
        std::cout << tick << '\n';
    }*/
    std::cout << tick << '\n';
}

int main()
{
    if (gpioInitialise() < 0) return 1;

    gpioSetMode(22, PI_INPUT);
    gpioSetAlertFunc(22, alertHere);

    while (true)
    {
        
        //}
    }

    return 0;
}