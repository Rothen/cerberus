#pragma once

#define TCS_MSG_START_MS 6 // a new message
#define TCS_ONE_BIT_MS 4   // a 1-bit is 4ms long
#define TCS_ZERO_BIT_MS 2  // a 0-bit is 2ms long

/**
 * @brief Helper function to print human readable hex message of tcs data to serial
 *
 * @param data the data to print
 */
void printHEX(uint32_t data)
{
    Serial.print("0x");
    uint8_t numChars = data > 0xFFFF ? 8 : 4;
    uint32_t mask = 0x0000000F;
    mask = mask << 4 * (numChars - 1);
    for (uint32_t i = numChars; i > 0; --i)
    {
        Serial.print(((data & mask) >> (i - 1) * 4), HEX);
        mask = mask >> 4;
    }
    Serial.print("\n");
}

class TCSBusReader
{
public:
    /**
     * @brief A reader class to read messages from TCS bus systems.
     *
     * @param readPin the pin that is connected to the data line of the TCS bus.
     */
    TCSBusReader(uint8_t readPin) : m_readPin(readPin), m_enabled(false)
    {
    }

    /**
     * @brief Must be called once during setup() phase
     */
    void begin()
    {
        pinMode(m_readPin, INPUT);
        enable();
    }

    /**
     * @brief Enables the reading of the bus via interrupts.
     *
     */
    void enable()
    {
        if (!m_enabled)
        {
            m_enabled = true;
            attachInterrupt(digitalPinToInterrupt(m_readPin), analyzeCMD, CHANGE);
        }
    }

    /**
     * @brief Disables the reading of the bus via interrupts
     *
     */
    void disable()
    {
        if (m_enabled)
        {
            m_enabled = false;
            detachInterrupt(digitalPinToInterrupt(m_readPin));
        }
    }

    /**
     * @brief Returns true if a new command has been received from the bus.
     *
     * @return true if a new command has been received.
     * @return false if no command is available.
     */
    bool hasCommand()
    {
        return s_cmdReady;
    }

    /**
     * @brief Reads the last message from the bus and also resets the #hasCommand() flag.
     *
     * @return uint32_t the last command from the bus
     */
    uint32_t read(uint32_t *cmd, byte *curCRC, byte *calCRC)
    {
        if (!s_cmdReady)
        {
            return 0;
        }
        uint32_t tmp_cmd = s_cmd;
        byte tmp_curCRC = s_curCRC;
        byte tmp_calCRC = s_calCRC;

        s_cmdReady = false;

        *cmd = tmp_cmd;
        *curCRC = tmp_curCRC;
        *calCRC = tmp_calCRC;

        return tmp_cmd;
    }

private:
    /**
     * @brief The interrupt method that counts the time for each high
     * or low bit and connects it to one big command.
     */
    static void IRAM_ATTR analyzeCMD()
    {
        // this method is magic from https://github.com/atc1441/TCSintercomArduino
        // TODO extract these to members
        static uint32_t curCMD;
        static uint32_t usLast;
        static byte curCRC;
        static byte calCRC;
        static byte curLength;
        static byte cmdIntReady;
        static byte curPos;
        uint32_t usNow = micros();
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
            curCMD = 0;
            curCRC = 0;
            calCRC = 1;
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
                    bitSet(curCMD, (curLength ? 33 : 17) - curPos);
                }
                calCRC ^= curBit;
                curPos++;
            }
            else if (curPos == 18)
            {
                if (curLength)
                {
                    if (curBit)
                    {
                        bitSet(curCMD, 33 - curPos);
                    }
                    calCRC ^= curBit;
                    curPos++;
                }
                else
                {
                    curCRC = curBit;
                    cmdIntReady = 1;
                }
            }
            else if (curPos >= 19 && curPos <= 33)
            {
                if (curBit)
                {
                    bitSet(curCMD, 33 - curPos);
                }
                calCRC ^= curBit;
                curPos++;
            }
            else if (curPos == 34)
            {
                curCRC = curBit;
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
            s_cmdLength = curLength; // todo this variable seems to be not used anywhere
            s_cmd = curCMD;
            s_curCRC = curCRC;
            s_calCRC = calCRC;
            curCMD = 0;
            curPos = 0;
            curCRC = 0;
            calCRC = 0;
        }
    }

    static volatile uint32_t s_cmd;
    static volatile uint8_t s_cmdLength;
    static volatile bool s_cmdReady;
    static volatile byte s_curCRC;
    static volatile byte s_calCRC;
    uint8_t m_readPin;
    bool m_enabled;
};

volatile uint32_t TCSBusReader::s_cmd = 0;
volatile uint8_t TCSBusReader::s_cmdLength = 0;
volatile bool TCSBusReader::s_cmdReady = false;
volatile byte TCSBusReader::s_curCRC = 0;
volatile byte TCSBusReader::s_calCRC = 0;

class TCSBusWriter
{
public:
    /**
     * @brief Allows to write to the TCS Bus.
     *
     * @param writePin the pin on which the bus cable is connected.
     */
    TCSBusWriter(uint8_t writePin) : m_writePin(writePin), m_writing(false)
    {
    }

    /**
     * @brief Must be called in the setup phase.
     *
     */
    void begin()
    {
        pinMode(m_writePin, OUTPUT);
    }

    /**
     * @brief Returns true if it is currently writing to the bus
     *
     * @return true if we are writing to the bus
     * @return false if we are not writing to the bus
     */
    bool isWriting()
    {
        return m_writing;
    }

    /**
     * @brief Writes the data to the bus. Can be a short command with 16 bits or a
     * long commands with 32.
     * Example codes:
     *   0x1100 door opener if the handset is not lifted up (short)
     *   0x1180 door opener if the handset is lifted up (short)
     *   0x1B8F9A41 specific bell code for a door (long)
     * @param data the data to write to the bus
     */
    void write(uint32_t data)
    {
        // this is magic from https://github.com/atc1441/TCSintercomArduino
        m_writing = true;
        int length = 16;
        char checksm = 1;
        bool isLongMessage = false;
        if (data > 0xFFFF)
        {
            length = 32;
            isLongMessage = 1;
        }
        digitalWrite(m_writePin, HIGH);
        // delay(TCS_MSG_START_MS);
        delayMicroseconds(TCS_MSG_START_MS * 1000);
        digitalWrite(m_writePin, !digitalRead(m_writePin));
        // delay(isLongMessage ? TCS_ONE_BIT_MS : TCS_ZERO_BIT_MS);
        delayMicroseconds(isLongMessage ? TCS_ONE_BIT_MS * 1000 : TCS_ZERO_BIT_MS * 1000);
        int curBit = 0;
        for (char i = length; i > 0; i--)
        {
            curBit = bitRead(data, i - 1);
            digitalWrite(m_writePin, !digitalRead(m_writePin));
            // delay(curBit ? TCS_ONE_BIT_MS : TCS_ZERO_BIT_MS);
            delayMicroseconds(curBit ? TCS_ONE_BIT_MS * 1000 : TCS_ZERO_BIT_MS * 1000);
            checksm ^= curBit;
        }
        digitalWrite(m_writePin, !digitalRead(m_writePin));
        // delay(checksm ? TCS_ONE_BIT_MS : TCS_ZERO_BIT_MS);
        delayMicroseconds(checksm ? TCS_ONE_BIT_MS * 1000 : TCS_ZERO_BIT_MS * 1000);
        digitalWrite(m_writePin, LOW);
        m_writing = false;
    }

private:
    uint8_t m_writePin;
    bool m_writing;
};