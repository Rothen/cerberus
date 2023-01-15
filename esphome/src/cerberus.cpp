#include "../include/cerberus.h"

void Cerberus::setup()
{
    tcsWriter.begin();
    tcsReader.begin();

    resetSensors();
}

void Cerberus::loop()
{
    if (anySensorTrue())
    {
        unsigned long currentMillis = esphome::millis();

        if(currentMillis - previousMillis > interval)
        {
            ESP_LOGD("read command", "Delay expired");
            resetSensors();

            previousMillis = currentMillis;
        }
    }
    else
    {
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

bool Cerberus::anySensorTrue()
{
    return ringingUpstairs ||
        ringingDownstairs ||
        cancelVoiceControlSequence ||
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

void Cerberus::setRingingUpstairs(bool ringingUpstairs)
{
    this->ringingUpstairs = ringingUpstairs;
    ringingUpstairsSensor->publish_state(ringingUpstairs);
}

void Cerberus::setRingingDownstairs(bool ringingDownstairs)
{
    this->ringingDownstairs = ringingDownstairs;
    ringingDownstairsSensor->publish_state(ringingDownstairs);
}

void Cerberus::setCancelVoiceControlSequence(bool cancelVoiceControlSequence)
{
    this->cancelVoiceControlSequence = cancelVoiceControlSequence;
    cancelVoiceControlSequenceSensor->publish_state(cancelVoiceControlSequence);
}

void Cerberus::setCancelControlSequence(bool cancelControlSequence)
{
    this->cancelControlSequence = cancelControlSequence;
    cancelControlSequenceSensor->publish_state(cancelControlSequence);
}

void Cerberus::setCancelRingControlSequence(bool cancelRingControlSequence)
{
    this->cancelRingControlSequence = cancelRingControlSequence;
    cancelRingControlSequenceSensor->publish_state(cancelRingControlSequence);
}

void Cerberus::setControlSequence(bool controlSequence)
{
    this->controlSequence = controlSequence;
    controlSequenceSensor->publish_state(controlSequence);
}

void Cerberus::onRingUpstairs()
{
    ESP_LOGD("read command", "Recieved RING_UPSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    setRingingUpstairs(true);
}

void Cerberus::onRingDownstairs()
{
    ESP_LOGD("read command", "Recieved RING_DOWNSTAIRS command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    setRingingDownstairs(true);
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
}

void Cerberus::onControlSequence()
{
    ESP_LOGD("read command", "Recieved CONTROL_SEQUENCE command (CRC: %d, Calc CRC: %d)", s_curCRC, s_calCRC);
    setControlSequence(true);
}

void Cerberus::resetSensors()
{
    setRingingUpstairs(false);
    setRingingDownstairs(false);
    setCancelVoiceControlSequence(false);
    setCancelControlSequence(false);
    setCancelRingControlSequence(false);
    setControlSequence(false);
}