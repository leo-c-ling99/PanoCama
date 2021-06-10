# PanoCama
Have you ever want to take a panoramic photo, automatically? The PanoCama is a low-cost device for taking wide-angle photographs. With its dual-cameras, it's able to roughly measure depth for fast environmental mapping.

This camera system was made with the mini-pan tilt system from Adafruit, an ESP32 DEVKIT, and two ArduCAM 2MP cameras. Image stitching and stereo vision components are performed using the OpenCV library for Python.

Project for EE 327: Electronic System Design II.

## Organization
The code I developed over the course is ordered here into Firmware, Image Processing, and Web sections. This project is organized as multiple proof of concepts for the various sections rather than one project with all components nicely interfaced together. Firmware is primarily C/C++ code developed for an ESP32 DEVKIT V1 for the Arduino Environment developed using PlatformIO. Image Processing is primarily Python code exploring the OpenCV library. Web is mostly setup code for an Tornado server with WebSockets and a webpage interface. PCB contains the two boards designed for this project. 

As of now, to interface the ESP32 with the Tornado Webserver, the address of the server and the local WiFi password must be changed within the main.cpp file.

3D mount: https://cad.onshape.com/documents/40f7b32b21ebe9fb9dda074d/w/69e21c5f167fa995fddc0409/e/9e02c831b684e933273a17e4

### Copyright © 2021 Leo Ling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.