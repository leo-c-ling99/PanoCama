#include "ws_wrapper.h"
#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <ArduinoJson.h>
#include <WiFiClientSecure.h>
#include <WebSocketsClient.h>
#include "config.h"

WebSocketsClient webSocket;
StaticJsonDocument<capacity> received;
ws_received_cmd received_flags = {.move_servo_pan=false, 
                                  .servo_pan_ds=0, 
                                  .move_servo_tilt=false,
                                  .servo_tilt_ds=0,
                                  .capture_single_pic=false, 
                                  .capture_single_pic_cam=1,
                                  .capture_pano=false,
                                  .capture_pano_cam=1,
                                  .stop_flag=false, 
                                  .num_received=0};

void wifi_connect()
{
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    Serial.printf("Trying to connect [%s] ", WiFi.macAddress().c_str());
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(500);
    }
    Serial.printf(" %s\n", WiFi.localIP().toString().c_str());
}

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length)
{
    switch (type)
    {
    case WStype_DISCONNECTED:
    {
        Serial.printf("[WSc] Disconnected!\n");
        break;
    }
    case WStype_CONNECTED:
    {
        Serial.printf("[WSc] Connected to url: %s\n", payload);
        break;
    }
    case WStype_TEXT:
    {
        Serial.printf("[WSc] get text: %s\n", payload);

        DeserializationError err = deserializeJson(received, payload);
        if (err)
        {
            Serial.print(F("deserializeJson() failed with code "));
            Serial.println(err.c_str());
        }
        else
        {
            received_flags.num_received += 1;
            // Flags any potential stop flags
            if (strcmp(received["type"], "stop") == 0) {
                received_flags.stop_flag = true;
                received_flags.num_received -= 1;
            } else if (strcmp(received["type"], "start") == 0) {
                received_flags.stop_flag = false;
                received_flags.num_received -= 1;
            // Parse any servo move commands
            } else if (strcmp(received["type"], "servo") == 0) {
                if (strcmp(received["dir"], "pan") == 0) {
                    received_flags.move_servo_pan = true;
                    received_flags.servo_pan_ds = atoi(received["mag"]);
                } else if (strcmp(received["dir"], "tilt") == 0) {
                    received_flags.move_servo_tilt = true;
                    received_flags.servo_tilt_ds = atoi(received["mag"]);
                } else {
                     received_flags.stop_flag -= 1;
                }
            // Parse any capture picture commands
            } else if (strcmp(received["type"], "cap") == 0) {
                if (strcmp(received["mode"], "single") == 0) {
                    received_flags.capture_single_pic = true;
                    received_flags.capture_single_pic_cam = atoi(received["cam"]);
                } else if (strcmp(received["mode"], "pano") == 0) {
                    received_flags.capture_pano = true;
                    received_flags.capture_pano_cam = atoi(received["cam"]);
                } else {
                    received_flags.stop_flag -= 1;
                }
            // Ignore message overwise
            } else {
                received_flags.stop_flag -= 1;
            }
        }
        break;
    }

    default:
    {
        break;
    }
    }

    return;
}

void init_ws()
{
    webSocket.begin(SERVER_URL, SERVER_PORT, UPLOAD_EXT);
    webSocket.onEvent(webSocketEvent);
    webSocket.setReconnectInterval(WS_RECONNECT_INTERVAL);
}