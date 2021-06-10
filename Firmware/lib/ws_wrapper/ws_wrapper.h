#pragma once
#ifndef _WS_WRAPPER_H
#define _WS_WRAPPER_H

#include "config.h"
#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <ArduinoJson.h>
#include <WiFiClientSecure.h>
#include <WebSocketsClient.h>

#define WS_RECONNECT_INTERVAL   5000
// WiFi setup
#define WIFI_SSID ""
#define WIFI_PASS ""
#define SERVER_URL "192.168.0.15"
#define SERVER_PORT 8888
#define UPLOAD_EXT "/websocket"

// Struct to hold last recieved message
const size_t capacity = JSON_OBJECT_SIZE(5) + 50;
extern WebSocketsClient webSocket;
extern StaticJsonDocument<capacity> received;
struct ws_received_cmd {
    // Flags set by WebSocket
    // Move positions
    bool move_servo_pan;
    int servo_pan_ds;
    bool move_servo_tilt;
    int servo_tilt_ds;
    // Taking a picture
    bool capture_single_pic;
    int capture_single_pic_cam;
    bool capture_pano;
    int capture_pano_cam;
    // Start and stop cmds
    bool stop_flag;
    // Total number recieved
    int num_received;

};
extern struct ws_received_cmd received_flags;

void wifi_connect(void);
void init_ws(void);
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length);


#endif