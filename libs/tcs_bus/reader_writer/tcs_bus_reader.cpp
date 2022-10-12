#include "tcs_bus_reader.h"

void empty_fn(uint32_t a, uint8_t b, uint8_t c, uint8_t d){ }
// std::function<void(uint32_t, uint8_t, uint8_t, uint8_t)>& f = {}

volatile uint32_t TCSBusReader::s_cmd = 0;
volatile uint8_t TCSBusReader::s_cmdLength = 0;
volatile bool TCSBusReader::s_cmdReady = false;
volatile uint8_t TCSBusReader::s_crc = 0;
volatile uint8_t TCSBusReader::s_calcCrc = 0;
volatile bool TCSBusReader::m_enabled = false;
std::function<void(uint32_t, uint8_t, uint8_t, uint8_t)> TCSBusReader::m_callback = empty_fn;

TCSBusReader::TCSBusReader(uint8_t readPin)
    : m_readPin(readPin)
{
}

void TCSBusReader::begin()
{
    pinMode(m_readPin, INPUT);
    wiringPiISR(m_readPin, INT_EDGE_BOTH,  analyzeCMD);
    enable();
}

void TCSBusReader::enable()
{
    m_enabled = true;
}

void TCSBusReader::disable()
{
    m_enabled = false;
}

bool TCSBusReader::hasCommand()
{
    return s_cmdReady;
}

void TCSBusReader::read(uint32_t *cmd, uint8_t *curCrc, uint8_t *calcCrc, uint8_t *cmdLength)
{
    if (!s_cmdReady)
    {
        return;
    }

    *cmd = s_cmd;
    *curCrc = s_crc;
    *calcCrc = s_calcCrc;
    *cmdLength = s_cmdLength;
    s_cmdReady = false;
}

void TCSBusReader::analyzeCMD()
{
    // this method is magic from https://github.com/atc1441/TCSintercomArduino
    // TODO extract these to members

    if (!m_enabled) {
        return;
    }

    static uint32_t curCmd;
    static uint32_t usLast;
    static byte curCrc;
    static byte calcCrc;
    static byte curLength;
    static byte cmdIntReady;
    static byte curPos;
    uint32_t usNow = micros();

    if (usNow - usLast < 1000) {
        return;
    }

    uint32_t timeInUS = usNow - usLast;
    usLast = usNow;
    byte curBit = 4;

    if (timeInUS >= 1000 && timeInUS <= 2999)
    {
        curBit = 0;
    }
    else if (timeInUS >= 3000 && timeInUS <= 4999)
    {
        curBit = 1;
    }
    else if (timeInUS >= 5000 && timeInUS <= 6999)
    {
        curBit = 2;
    }
    else if (timeInUS >= 7000 && timeInUS <= 24000)
    {
        curBit = 3;
        curPos = 0;
    }

    if (curPos == 0)
    {
        if (curBit == 2)
        {
            curPos++;
        }
        curCmd = 0;
        curCrc = 0;
        calcCrc = 1;
        curLength = 0;
    }
    else if (curBit == 0 || curBit == 1)
    {
        if (curPos == 1)
        {
            curLength = curBit;
            curPos++;
        }
        else if (curPos >= 2 && curPos <= 17)
        {
            if (curBit)
            {
                curCmd |= (1UL << ((curLength ? 33 : 17) - curPos));
            }
            calcCrc ^= curBit;
            curPos++;
        }
        else if (curPos == 18)
        {
            if (curLength)
            {
                if (curBit)
                {
                    curCmd |= 1UL << (33 - curPos);
                }
                calcCrc ^= curBit;
                curPos++;
            }
            else
            {
                curCrc = curBit;
                cmdIntReady = 1;
            }
        }
        else if (curPos >= 19 && curPos <= 33)
        {
            if (curBit)
            {
                curCmd |= 1UL << (33 - curPos);
            }
            calcCrc ^= curBit;
            curPos++;
        }
        else if (curPos == 34)
        {
            curCrc = curBit;
            cmdIntReady = 1;
        }
    }
    else
    {
        curPos = 0;
    }

    if (cmdIntReady)
    {
        cmdIntReady = 0;
        s_cmdReady = 1;
        s_cmdLength = (curLength) ? 32 : 16;
        s_cmd = curCmd;
        s_crc = curCrc;
        s_calcCrc = calcCrc;
        curCmd = 0;
        curCrc = 0;
        calcCrc = 0;
        curPos = 0;
        m_callback(s_cmd, s_crc, s_calcCrc, s_cmdLength);
    }
}