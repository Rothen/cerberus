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

class Cerberus : public Component, public CustomAPIDevice
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

            register_service(&Cerberus::onOpenDoor, "open_door");
            register_service(&Cerberus::onStartWasherCycle, "start_washer_cycle", {"cycle_duration", "silent", "string_argument"});
            subscribe_homeassistant_state(&Cerberus::onStateChanged, "sensor.temperature");
        }

        void loop() override
        {
            if (tcsReader.hasCommand())
            {
                tcsReader.read(&s_cmd, &s_curCRC, &s_calCRC);

                switch (s_cmd)
                {
                case RING_UPSTAIRS:
                    onRingUpstairs();
                    break;
                case RING_DOWNSTAIRS:
                    onRingDownstairs();
                    break;
                case CANCEL_VOICE_CONTROL_SEQUENCE:
                    onCancelVoiceControlSequence();
                    break;
                case CANCEL_CONTROL_SEQUENCE:
                    onCancelControlSequence();
                    break;
                case CANCEL_RING_CONTROL_SEQUENCE:
                    onCancelRingControlSequence();
                    break;
                case CONTROL_SEQUENCE:
                    onControlSequence();
                    break;
                default:
                    ESP_LOGD("read command", "Unknown command recieved %d (CRC: %d, Calc CRC: %d)", s_cmd, s_curCRC, s_calCRC);
                }
            }

            if (is_connected()) {
                // Example check to see if a client is connected
            }
        }
        void onOpenDoor()
        {
            ESP_LOGD("custom", "Hello World!");

            if (is_connected()) {
            // Example check to see if a client is connected
            }
        }
        void onStartWasherCycle(int cycle_duration, bool silent, std::string string_argument)
        {
            ESP_LOGD("custom", "Starting washer cycle!");
            tcsReader.disable();
            tcsWriter.write(OPEN_DOOR);
            tcsReader.enable();
            // do something with arguments

            // Call a homeassistant service
            call_homeassistant_service("homeassistant.service");
        }

        void onStateChanged(std::string state)
        {
            ESP_LOGD("state changed", "Temperature has changed to %s", state.c_str());
        }

        void onRingUpstairs()
        {
            ESP_LOGD("read command", "Recieved RING_UPSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
        }

        void onRingDownstairs()
        {
            ESP_LOGD("read command", "Recieved RING_DOWNSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
        }

        void onCancelVoiceControlSequence()
        {
            ESP_LOGD("read command", "Recieved CANCEL_VOICE_CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
        }

        void onCancelControlSequence()
        {
            ESP_LOGD("read command", "Recieved CANCEL_CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
        }

        void onCancelRingControlSequence()
        {
            ESP_LOGD("read command", "Recieved CANCEL_RING_CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
        }

        void onControlSequence()
        {
            ESP_LOGD("read command", "Recieved CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
        }
};
