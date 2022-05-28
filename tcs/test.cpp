#include "tcs_bus.h"

#define RING_UPSTAIRS 0x109E8141
#define RING_DOWNSTAIRS 0x009E8180
#define CANCLE_VOICE_CHANNEL_A 0x3080
#define CANCLE_VOICE_CHANNEL_B 0x2480
#define OPEN_DOOR 0x109E8180
#define OPEN_VOICE_CHANNEL 0x309E8100

TCSBusWriter writer(6);

int main()
{
    wiringPiSetup();
    writer.begin();
    std::cout << "Writing ring upstairs" << '\n';
    delay(1000);
    writer.write(RING_UPSTAIRS);

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