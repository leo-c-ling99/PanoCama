#pragma once
#ifndef _CAMERA_WRAPPER_H
#define _CAMERA_WRAPPER_H

#include <Wire.h>
#include <ArduCAM.h>
#include <SPI.h>
#include "memorysaver.h"
#include "config.h"

// Camera Pins
#define CAMERA_1_SCK    18
#define CAMERA_1_MISO   19
#define CAMERA_1_MOSI   23
//#define CAMERA_1_SCK    14
//#define CAMERA_1_MISO   12
//#define CAMERA_1_MOSI   13
#define CAMERA_1_CS     5
#define CAMERA_1_SCL    22
#define CAMERA_1_SDA    21
/*
#define CAMERA_2_SCK    18
#define CAMERA_2_MISO   19
#define CAMERA_2_MOSI   23
*/
#define CAMERA_2_SCK    14
#define CAMERA_2_MISO   12
#define CAMERA_2_MOSI   13
#define CAMERA_2_CS     15
#define CAMERA_2_SCL    14
#define CAMERA_2_SDA    13

#define SPI_FREQUENCY   4000000

extern ArduCAM cam1;
extern ArduCAM cam2;
//extern SPIClass SPI1;
const size_t buffer_size = 16384;
extern uint8_t image_buffer[buffer_size];

// Setup SPI for each camera
void init_camera(ArduCAM& cam, SPIClass& spi, int cs, TwoWire& i2c);
void init_cameras(void);
// Take a picture and stores it in the imageBuffer
//   Returns the len of the image left
void start_capture(ArduCAM& cam);
size_t start_picture_read(ArduCAM& cam);
size_t fill_picture_buffer(ArduCAM& cam, size_t len);
#endif