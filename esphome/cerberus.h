#include "esphome.h"
#include "tcs_bus.h"

TCSBusReader tcsReader(D7);
TCSBusWriter tcsWriter(D8);

uint32_t s_cmd = 0;
char s_curCRC = 0;
char s_calCRC = 0;

class Cerberus : public Component
{
public:
    void setup() override
    {
        // This will be called once to set up the component
        // think of it as the setup() call in Arduino
        tcsWriter.begin();
        tcsReader.begin();
    }
    void loop() override
    {
        // This will be called very often after setup time.
        // think of it as the loop() call in Arduino
        if (tcsReader.hasCommand())
        {
            tcsReader.read(&s_cmd, &s_curCRC, &s_calCRC);
            ESP_LOGD("custom", printHEX(s_cmd));
            ESP_LOGD("custom", s_curCRC);
            ESP_LOGD("custom", s_calCRC);
            notifyClients();
            logReadCommand();
        }
    }
};