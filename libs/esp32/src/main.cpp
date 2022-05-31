#include <Arduino.h>
#include <tcs_bus.h>

#define D32 32
#define D33 33
#define PIN_BUS_READ D32
#define PIN_BUS_WRITE D33

TCSBusReader tcsReader(PIN_BUS_READ);
TCSBusWriter tcsWriter(PIN_BUS_WRITE);

uint32_t s_cmd = 0;
byte s_curCRC = 0;
byte s_calCRC = 0;

#define RXD2 16
#define TXD2 17



void setup()
{
    Serial.begin(9600);
    Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
    tcsWriter.begin();
    tcsReader.begin();
}

void loop()
{
    if (tcsReader.hasCommand())
    {
        Serial.println("in command");
        Serial2.println("in command");
        uint32_t cmd = tcsReader.read(&s_cmd, &s_curCRC, &s_calCRC);

        Serial.print("GOT: 0x");
        Serial2.print("GOT: 0x");
        printHEX(s_cmd);
        Serial.print(", CRC: ");
        Serial2.print(", CRC: ");
        Serial.print(s_curCRC);
        Serial2.print(s_curCRC);
        Serial.print(", CALC_CRC: ");
        Serial2.print(", CALC_CRC: ");
        Serial.print(s_calCRC);
        Serial2.print(s_calCRC);
        Serial.println();
        Serial2.println();
    }

    if (Serial2.available())
    {
        Serial.println("in serial 2");
        Serial2.println("in serial 2");
        tcsReader.disable();
        String incomingString = Serial2.readStringUntil('\n');
        uint32_t cmd = uint32_t(strtoul(incomingString.c_str(), NULL, 16));

        Serial2.print(incomingString);
        printHEX(cmd);
        Serial2.println();

        tcsWriter.write(cmd);
        tcsReader.enable();
    }

    if (Serial.available())
    {
        Serial.println("in serial");
        Serial2.println("in serial");
        tcsReader.disable();
        String incomingString = Serial.readStringUntil('\n');
        uint32_t cmd = uint32_t(strtoul(incomingString.c_str(), NULL, 16));

        Serial.print("SEND: 0x");
        printHEX(cmd);
        Serial.println();

        tcsWriter.write(cmd);
        tcsReader.enable();
    }
}

/*#define TCS_MSG_START_US 6000 // a new message
#define TCS_ONE_BIT_US 4000                            // a 1-bit is 4ms long
int TCS_ZERO_BIT_US = 1800;                           // a 0-bit is 2ms long

bool maxBuffer[69];
uint32_t intbuffer;

void printHEX(uint32_t data)
{
    uint8_t numChars = data > 0xFFFF ? 8 : 4;
    uint32_t mask = 0x0000000F;
    mask = mask << 4 * (numChars - 1);
    for (uint32_t i = numChars; i > 0; --i)
    {
        Serial.print(((data & mask) >> (i - 1) * 4), HEX);
        mask = mask >> 4;
    }
}

void reset()
{
    intbuffer = 0;
    for (uint16_t i = 0; i < 69; i++)
    {
        maxBuffer[i] = 0;
    }
}

void IRAM_ATTR analyzeCMD()
{
    detachInterrupt(digitalPinToInterrupt(PIN_BUS_READ));

    for (uint16_t i = 0; i < 69; i++)
    {
        delayMicroseconds(TCS_ZERO_BIT_US);
        maxBuffer[i] = digitalRead(PIN_BUS_READ);
    }

    uint8_t messageLength = 16;
    uint8_t slider = 1;

    if (maxBuffer[0] == maxBuffer[1])
    {
        messageLength = 32;
        slider = 2;
    }

    for (uint8_t currentBit = messageLength; currentBit > 0; currentBit--)
    {
        if (maxBuffer[slider] == maxBuffer[slider + 1])
        {
            bitSet(intbuffer, currentBit-1);
            slider++;

            if (maxBuffer[slider + 1] == maxBuffer[slider + 2]) {
                slider++;
            }
        }

        slider++;
    }

    // printHEX(intbuffer);

    // Serial.println("");
    for (uint16_t i = 0 ; i < 69; i++)
    {
        Serial.print(maxBuffer[i]);
    }
    Serial.print(" : ");
    Serial.println(TCS_ZERO_BIT_US);
    // Serial.println("Stop interrupt");
    TCS_ZERO_BIT_US = TCS_ZERO_BIT_US + 5;
    delay(50);
    reset();
    attachInterrupt(digitalPinToInterrupt(PIN_BUS_READ), analyzeCMD, FALLING);
}

void setup()
{
    Serial.begin(9600);
    pinMode(PIN_BUS_READ, INPUT);
    reset();
    attachInterrupt(digitalPinToInterrupt(PIN_BUS_READ), analyzeCMD, FALLING);
}

void loop()
{
    //
}*/