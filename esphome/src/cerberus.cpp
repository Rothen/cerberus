#include "../include/cerberus.h"

void Cerberus::setup()
{
    tcsWriter.begin();
    tcsReader.begin();

    resetSensors();
}

void Cerberus::loop()
{
    if (anySensorTrue() && delay.isExpired())
    {
        ESP_LOGD("cerberus", "Delay expired");
        resetSensors();
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

bool Cerberus::anySensorTrue()
{
    return cancelVoiceControlSequence ||
        cancelControlSequence ||
        cancelRingControlSequence ||
        controlSequence;
}

void Cerberus::onOpenDoor()
{
    ESP_LOGD("cerberus", "Opening door");
    tcsReader.disable();
    tcsWriter.write(OPEN_DOOR);
    tcsReader.enable();
}

void Cerberus::onStateChanged(std::string state)
{
    ESP_LOGD("state changed", "Temperature has changed to %s", state.c_str());
}

void Cerberus::set(bool &sensorState, BinarySensor *binarySensor, bool state)
{
    sensorState = state;
    binarySensor->publish_state(sensorState);
    delay.start(1000, AsyncDelay::MILLIS);
}

void Cerberus::setRingingUpstairs(bool ringingUpstairs)
{
    set(this->ringingUpstairs, ringingUpstairsSensor, ringingUpstairs);
}

void Cerberus::setRingingDownstairs(bool ringingDownstairs)
{
    set(this->ringingDownstairs, ringingDownstairsSensor, ringingDownstairs);
}

void Cerberus::setCancelVoiceControlSequence(bool cancelVoiceControlSequence)
{
    set(this->cancelVoiceControlSequence, cancelVoiceControlSequenceSensor, cancelVoiceControlSequence);
}

void Cerberus::setCancelControlSequence(bool cancelControlSequence)
{
    set(this->cancelControlSequence, cancelControlSequenceSensor, cancelControlSequence);
}

void Cerberus::setCancelRingControlSequence(bool cancelRingControlSequence)
{
    set(this->cancelRingControlSequence, cancelRingControlSequenceSensor, cancelRingControlSequence);
}

void Cerberus::setControlSequence(bool controlSequence)
{
    set(this->controlSequence, controlSequenceSensor, controlSequence);
}

void Cerberus::setMode(const std::string &mode)
{
    this->mode = mode;
    ESP_LOGD("mode select", "Mode %s set", mode.c_str());
}

void Cerberus::onRingUpstairs()
{
    ESP_LOGD("read command", "Recieved RING_UPSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    setRingingUpstairs(true);
}

void Cerberus::onRingDownstairs()
{
    setRingingDownstairs(true);

    if (mode.compare(std::string("Delivery")) == 0)
    {
        ESP_LOGD("read command", "Recieved RING_DOWNSTAIRS command in delivery mode (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
        mode = std::string("Normal");
        onOpenDoor();
    }
    else if (mode.compare(std::string("Party")) == 0)
    {
        ESP_LOGD("read command", "Recieved RING_DOWNSTAIRS command in party mode (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
        onOpenDoor();
    }
    else
    {
        ESP_LOGD("read command", "Recieved RING_DOWNSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    }
}

void Cerberus::onCancelVoiceControlSequence()
{
    ESP_LOGD("read command", "Recieved CANCEL_VOICE_CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    setCancelVoiceControlSequence(true);
}

void Cerberus::onCancelControlSequence()
{
    ESP_LOGD("read command", "Recieved CANCEL_CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    setCancelControlSequence(true);
}

void Cerberus::onCancelRingControlSequence()
{
    ESP_LOGD("read command", "Recieved CANCEL_RING_CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    setCancelRingControlSequence(true);
    if (ringingDownstairs == true) {
        setRingingDownstairs(false);
    }
    if (ringingUpstairs == true) {
        setRingingUpstairs(false);
    }
}

void Cerberus::onControlSequence()
{
    ESP_LOGD("read command", "Recieved CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    setControlSequence(true);
}

void Cerberus::resetSensors()
{
    setCancelVoiceControlSequence(false);
    setCancelControlSequence(false);
    setCancelRingControlSequence(false);
    setControlSequence(false);
}