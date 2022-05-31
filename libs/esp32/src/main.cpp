#include "main.h"

TCSBusReader tcsReader(PIN_BUS_READ);
TCSBusWriter tcsWriter(PIN_BUS_WRITE);

uint32_t s_cmd = 0;
byte s_curCRC = 0;
byte s_calCRC = 0;

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
        tcsReader.read(&s_cmd, &s_curCRC, &s_calCRC);
        log_read_command();
        send_read_command();
    }

    if (Serial2.available())
    {
        tcsReader.disable();

        String incomingString = Serial2.readStringUntil('\n');
        uint32_t cmd = uint32_t(strtoul(incomingString.c_str(), NULL, 16));

        log_write_command(cmd);

        tcsWriter.write(cmd);
        tcsReader.enable();
    }
}

void log_read_command()
{
    Serial.println("Read command: ");
    print_hex(s_cmd, Serial);
}

void log_write_command(uint32_t cmd)
{
    Serial.println("Write command: ");
    print_hex(cmd, Serial);
}

void send_read_command()
{
    Serial2.print("GOT: 0x");
    print_hex(s_cmd, Serial2);
    Serial2.print(", CRC: ");
    Serial2.print(s_curCRC);
    Serial2.print(", CALC_CRC: ");
    Serial2.print(s_calCRC);
    Serial2.println();
}