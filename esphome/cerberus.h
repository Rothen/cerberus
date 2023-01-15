#include "gpio.h"
#include "esphome.h"
#include "tcs_bus.h"

#define getCerberus(constructor) static_cast<Cerberus *>((&constructor)->get_component(0))

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

        BinarySensor *ringingUpstairsSensor = new BinarySensor();
        BinarySensor *ringingDownstairsSensor = new BinarySensor();
        bool ringingUpstairs = false;
        bool ringingDownstairs = false;

        unsigned long previousMillis = 0UL;
        unsigned long interval = 1000UL;

        void setup() override
        {
            tcsWriter.begin();
            tcsReader.begin();

            resetRingingSensors();
        }

        void loop() override
        {
            if (ringingUpstairs or ringingDownstairs) {
                unsigned long currentMillis = millis();

                if(currentMillis - previousMillis > interval)
                {
                    ESP_LOGD("read command", "Delay expired");
                    resetRingingSensors();

                    previousMillis = currentMillis;
                }
            } else {
                previousMillis = 0;
            }

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
        }

        void onOpenDoor()
        {
            ESP_LOGD("cerberus", "Opening door");
            tcsReader.disable();
            tcsWriter.write(OPEN_DOOR);
            tcsReader.enable();
        }

        void onStateChanged(std::string state)
        {
            ESP_LOGD("state changed", "Temperature has changed to %s", state.c_str());
        }

        void setRingingUpstairs(bool ringingUpstairs)
        {
            this->ringingUpstairs = ringingUpstairs;
            ringingUpstairsSensor->publish_state(ringingUpstairs);
        }

        void setRingingDownstairs(bool ringingDownstairs)
        {
            this->ringingDownstairs = ringingDownstairs;
            ringingDownstairsSensor->publish_state(ringingDownstairs);
        }

        void onRingUpstairs()
        {
            ESP_LOGD("read command", "Recieved RING_UPSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
            setRingingUpstairs(true);
        }

        void onRingDownstairs()
        {
            ESP_LOGD("read command", "Recieved RING_DOWNSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
            setRingingDownstairs(true);
        }

        void resetRingingSensors()
        {
            setRingingUpstairs(false);
            setRingingDownstairs(false);
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
