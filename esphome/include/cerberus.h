#pragma once

#include "async_delay.h"
#include "gpio.h"
#include "esphome.h"
#include "tcs_bus.h"

using namespace esphome;
using namespace esphome::binary_sensor;
using namespace esphome::select;

#define getCerberus(constructor) static_cast<Cerberus *>(const_cast<custom_component::CustomComponentConstructor *>(&constructor)->get_component(0))

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
        uint8_t s_curCRC = 0;
        uint8_t s_calCRC = 0;

        BinarySensor *ringingUpstairsSensor = new BinarySensor();
        BinarySensor *ringingDownstairsSensor = new BinarySensor();
        BinarySensor *cancelVoiceControlSequenceSensor = new BinarySensor();
        BinarySensor *cancelControlSequenceSensor = new BinarySensor();
        BinarySensor *cancelRingControlSequenceSensor = new BinarySensor();
        BinarySensor *controlSequenceSensor = new BinarySensor();

        bool ringingUpstairs = false;
        bool ringingDownstairs = false;
        bool cancelVoiceControlSequence = false;
        bool cancelControlSequence = false;
        bool cancelRingControlSequence = false;
        bool controlSequence = false;

        std::string mode = "Normal";

        AsyncDelay asyncDelay;

        void setup() override;
        void loop() override;

        bool anySensorTrue();

        void onOpenDoor();
        void onStateChanged(std::string state);

        void set(bool &sensorState, BinarySensor *binarySensor, bool state);
        void setRingingUpstairs(bool ringingUpstairs);
        void setRingingDownstairs(bool ringingDownstairs);
        void setCancelVoiceControlSequence(bool cancelVoiceControlSequence);
        void setCancelControlSequence(bool cancelControlSequence);
        void setCancelRingControlSequence(bool cancelRingControlSequence);
        void setControlSequence(bool controlSequence);
        void setMode(const std::string &mode);

        void onRingUpstairs();
        void onRingDownstairs();
        void onCancelVoiceControlSequence();
        void onCancelControlSequence();
        void onCancelRingControlSequence();
        void onControlSequence();


        void resetSensors();
};