#include "main.h"

TCSBusReader tcsReader(PIN_BUS_READ);
TCSBusWriter tcsWriter(PIN_BUS_WRITE);

uint32_t s_cmd = 0;
byte s_curCRC = 0;
byte s_calCRC = 0;

// Replace with your network credentials
const char *ssid = SSID;
const char *password = PASSWORD;

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

std::set<uint32_t> connectedClients = {};
std::set<uint32_t> loggedInClients = {};

String apiKey = API_KEY; // 278823297

void setup()
{
    Serial.begin(115200);
    tcsWriter.begin();
    tcsReader.begin();
    setupWifi();
}

void loop()
{
    ws.cleanupClients();

    if (tcsReader.hasCommand())
    {
        tcsReader.read(&s_cmd, &s_curCRC, &s_calCRC);
        notifyClients();
        logReadCommand();
    }
}

void setupWifi()
{
    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi..");
        Serial1.println("Connecting to WiFi..");
    }

    // Print ESP Local IP Address
    Serial.println(WiFi.localIP());

    setupWebSocketServer();

    // Start server
    server.begin();
}

void logReadCommand()
{
    Serial.print("Read command: ");
    printHEX(s_cmd);
}

void logWriteCommand(uint32_t cmd)
{
    Serial.print("Write command: ");
    printHEX(cmd);
}

void notifyClients()
{
    ws.textAll(String(s_cmd) + "," + String(s_curCRC) + "," + String(s_calCRC));
}

void login(AsyncWebSocketClient *client, void *arg, uint8_t *data, size_t len)
{
    AwsFrameInfo *info = (AwsFrameInfo *)arg;
    if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT)
    {
        data[len] = 0;
        String sentApiKey = String((char *)data);

        if (sentApiKey == apiKey)
        {
            loggedInClients.insert(client->id());
            Serial.printf("API Key is correct for client #%u\n", client->id());
        }
        else
        {
            Serial.printf("API Key is wrong for client #%u\n", client->id());
        }
    }
}

void handleWebSocketMessage(void *arg, uint8_t *data, size_t len)
{
    AwsFrameInfo *info = (AwsFrameInfo *)arg;
    if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT)
    {
        data[len] = 0;
        uint32_t transmittedCmd = String((char *)data).toInt();
        tcsReader.disable();
        tcsWriter.write(transmittedCmd);
        tcsReader.enable();
        logWriteCommand(transmittedCmd);
    }
}

void onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len)
{
    switch (type)
    {
    case WS_EVT_CONNECT:
        Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
        connectedClients.insert(client->id());
        break;
    case WS_EVT_DISCONNECT:
        Serial.printf("WebSocket client #%u disconnected\n", client->id());
        connectedClients.erase(client->id());
        loggedInClients.erase(client->id());
        break;
    case WS_EVT_DATA:
        if (loggedInClients.find(client->id()) == loggedInClients.end())
        {
            login(client, arg, data, len);
        }
        else
        {
            handleWebSocketMessage(arg, data, len);
        }
        break;
    case WS_EVT_PONG:
    case WS_EVT_ERROR:
        break;
    }
}

void setupWebSocketServer()
{
    ws.onEvent(onEvent);
    server.addHandler(&ws);
}