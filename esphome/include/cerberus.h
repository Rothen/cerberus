#pragma once

#ifndef CERBERUS_H
#define CERBERUS_H

#include "gpio.h"
#include "esphome.h"
#include "tcs_bus.h"

using namespace esphome;
using namespace esphome::binary_sensor;

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
        byte s_curCRC = 0;
        byte s_calCRC = 0;

        BinarySensor *ringingUpstairsSensor = new BinarySensor();
        BinarySensor *ringingDownstairsSensor = new BinarySensor();
        bool ringingUpstairs = false;
        bool ringingDownstairs = false;

        unsigned long previousMillis = 0UL;
        unsigned long interval = 1000UL;

        void setup() override;
        void loop() override;
        void onOpenDoor();
        void onStateChanged(std::string state);
        void setRingingUpstairs(bool ringingUpstairs);
        void setRingingDownstairs(bool ringingDownstairs);
        void onRingUpstairs();
        void onRingDownstairs();
        void resetRingingSensors();
        void onCancelVoiceControlSequence();
        void onCancelControlSequence();
        void onCancelRingControlSequence();
        void onControlSequence();
};

#endif