#include <Arduino.h>
#include <tcs_bus.h>
#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <set>
#include "secrets.h"

#define PIN_BUS_READ D7
#define PIN_BUS_WRITE D8

void setup();
void loop();
void logReadCommand();
void logWriteCommand(uint32_t cmd);
void setupWebSocketServer();
void setupWifi();
void notifyClients();
void login(AsyncWebSocketClient *client, void *arg, uint8_t *data, size_t len);
void handleWebSocketMessage(void *arg, uint8_t *data, size_t len);