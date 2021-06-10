#include <Arduino.h>
#include <camera_wrapper.h>
#include <servos_wrapper.h>
#include <ws_wrapper.h>
#include "config.h"

// Flags set by WebSocket
//extern struct ws_received_cmd received_flags;

void take_send_single(ArduCAM& cam) {
	start_capture(cam);
  	Serial.println("CAM Capturing");


	int total_time = 0;

	total_time = millis();
	while (!cam.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK));
	total_time = millis() - total_time;
	Serial.print("capture total_time used (in miliseconds):");
	Serial.println(total_time, DEC);

	total_time = 0;
  
  	Serial.println("CAM Capture Done!");
  	total_time = millis();

	size_t len = start_picture_read(cam);
	Serial.println(len);
	size_t payload_len;
	// Start send
	while (len > 0) {
		Serial.println(len);
		payload_len = len - fill_picture_buffer(cam, len);
		len -= payload_len;
		// Wait until message has been sent
		while (!webSocket.sendBIN(image_buffer, payload_len)) {
			Serial.println("Send Failed");
			delay(500);
		}
	}
	// Sent text to acknowledge that message has been fully sent
	while (!webSocket.sendTXT("Pic Complete")) {
			delay(1000);
	}

	total_time = millis() - total_time;
  Serial.print("send total_time used (in miliseconds):");
  Serial.println(total_time, DEC);
  Serial.println("CAM send Done!");
}

void take_send_pano() {
	for (int pan_pos = SERVO_MIN; pan_pos < SERVO_MAX; pan_pos += 3) {
		Serial.println(pan_pos);
		servo_move(PWN_CHANNEL_PAN, pan_pos);
		delay(1000);
		take_send_single(cam1);
		take_send_single(cam2);
	}

	Serial.println("Pano Complete");
}

void setup() {
	Serial.begin(115200);
	// Setup WiFi and WebSockets
	wifi_connect();
	init_ws();
	// Setup Cameras
	init_cameras();
	// Setup Servos
	servo_setup();
}

void loop() {
	webSocket.loop();

	if (!received_flags.stop_flag && received_flags.num_received > 0) {
		Serial.println("Flags Set");

		// Check if any move servos flags set
		if (received_flags.move_servo_pan) {
			servo_move(PWN_CHANNEL_PAN, received_flags.servo_pan_ds);

			// Remove Flags
			received_flags.move_servo_pan = false;
			received_flags.servo_pan_ds = 0;
			received_flags.num_received -= 1;
			delay(1000);
		} 
		if (received_flags.move_servo_tilt) {
			servo_move(PWM_CHANNEL_TILT, received_flags.servo_tilt_ds);

			// Remove Flags
			received_flags.move_servo_tilt = false;
			received_flags.servo_tilt_ds = 0;
			received_flags.num_received -= 1;
			delay(1000);
		}

		// Check for take single picture command
		if (received_flags.capture_single_pic) {
			if (received_flags.capture_single_pic_cam == 1) {
				take_send_single(cam1);
			} else {
				take_send_single(cam2);
			}
			
			received_flags.capture_single_pic = false;
			received_flags.capture_single_pic_cam = false;
			received_flags.num_received -= 1;
			delay(1000);
		}

		// Check for take Panoramic
		if (received_flags.capture_pano) {
			take_send_pano();
			received_flags.capture_pano = false;
			received_flags.capture_pano_cam = false;
			received_flags.num_received -= 1;
			delay(1000);
		}
	} 
}