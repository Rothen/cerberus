#include "tcs_bus_reader.h"
#include "tcs_bus_writer.h"

#define RING_UPSTAIRS 0x109E8141
#define RING_DOWNSTAIRS 0x009E8180
#define CANCEL_VOICE_CONTROL_SEQUENCE 0x3080
#define CANCEL_CONTROL_SEQUENCE 0x2480
#define OPEN_DOOR 0x109E8180
#define OPEN_VOICE_CHANNEL 0x309E8100

TCSBusWriter writer(6);
TCSBusReader reader(3);

int main()
{
    wiringPiSetup();
    reader.begin();
    reader.enable();

    while (true)
    {
        // std::cout << digitalRead(3) << '\n';
        if (reader.hasCommand())
        {
            uint32_t cmd = reader.read();
            std::cout << cmd;
        }
    }

    /*writer.begin();
    std::cout << "Writing ring upstairs" << '\n';
    delay(1000);
    writer.write(RING_UPSTAIRS);*/

    return 0;
}

/*



int main()
{
    wiringPiSetup();
    TCSBusReader reader(3);
    reader.begin();
    

    while (true)
    {
        if (reader.hasCommand()) {
                auto command_value = reader.read();
                std::cout << command_value << '\n';
        }
    }

    return 0;
}
*/