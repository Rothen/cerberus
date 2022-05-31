#include <Arduino.h>
#include <tcs_bus.h>

#define D32 32
#define D33 33
#define PIN_BUS_READ D32
#define PIN_BUS_WRITE D33
#define RXD2 16
#define TXD2 17

void setup();
void loop();
void log_read_command();
void log_write_command(uint32_t cmd);
void send_read_command();