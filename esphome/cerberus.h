#include "esphome.h"
#include "gpio.h"
#include "tcs_bus.h"

#define RING_UPSTAIRS 0x109E8141
#define RING_DOWNSTAIRS 0x009E8180 // 0x009E8181 0x009E8182
#define CANCEL_VOICE_CONTROL_SEQUENCE 0x3080
#define CANCEL_CONTROL_SEQUENCE 0x2480
#define CANCEL_RING_CONTROL_SEQUENCE 0x2400
#define OPEN_DOOR 0x109E8180 // 0x109E8181
#define OPEN_VOICE_CHANNEL 0x309E8100
#define CONTROL_SEQUENCE 0x5802

class Cerberus : public Component
{
public:
    TCSBusReader tcsReader = TCSBusReader(D2);
    TCSBusWriter tcsWriter = TCSBusWriter(D1);

    uint32_t s_cmd = 0;
    byte s_curCRC = 0;
    byte s_calCRC = 0;

    void setup() override
    {
        tcsWriter.begin();
        tcsReader.begin();
    }

    void loop() override
    {
        if (tcsReader.hasCommand())
        {
            tcsReader.read(&s_cmd, &s_curCRC, &s_calCRC);

            switch (s_cmd)
            {
            case RING_UPSTAIRS:
                onRingUpstairs() break;
            case RING_DOWNSTAIRS:
                onRingDownstairs() break;
            case CANCEL_VOICE_CONTROL_SEQUENCE:
                onCancelVoiceControlSequence() break;
            case CANCEL_CONTROL_SEQUENCE:
                onCancelControlSequence() break;
            case CANCEL_RING_CONTROL_SEQUENCE:
                onCancelRingControlSequence() break;
            case CONTROL_SEQUENCE:
                onControlSequence() break;
            default:
                ESP_LOGD("read comman", "Unknown command recieved %d (CRC: %d, Calc CRC: %d)", s_cmd, s_curCRC, s_calCRC);
            }
        }
    }

    void onRingUpstairs()
    {
        ESP_LOGD("read comman", "Recieved RING_UPSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    }

    void onRingDownstairs()
    {
        ESP_LOGD("read comman", "Recieved RING_DOWNSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    }

    void onCancelVoiceControlSequence()
    {
        ESP_LOGD("read comman", "Recieved CANCEL_VOICE_CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    }

    void onCancelControlSequence()
    {
        ESP_LOGD("read comman", "Recieved CANCEL_CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    }

    void onCancelRingControlSequence()
    {
        ESP_LOGD("read comman", "Recieved CANCEL_RING_CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    }

    void onControlSequence()
    {
        ESP_LOGD("read comman", "Recieved CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    }
};
