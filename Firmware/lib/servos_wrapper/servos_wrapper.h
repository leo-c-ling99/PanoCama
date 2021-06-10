#pragma once
#ifndef _SERVOS_WRAPPER_H
#define _SERVOS_WRAPPER_H
#include <Arduino.h>
#include "config.h"

// Motor pins
#define PWN_CHANNEL_PAN     0
#define PWM_CHANNEL_TILT    1
#define PWM_FREQ            50
#define PWM_RESOLUTION      8
#define PWM_DUTY_CYCLE      0
// Servos
#define SERVO_PAN_PIN       27
#define SERVO_TILT_PIN      25
#define SERVO_MIN   5
#define SERVO_MAX   33

// Intializes PWM pins for both servo motors
void servo_setup(void);

/* Set the duty cycle for a given channel, moving servo
*       const int channel: The channel to output PWM duty cycle to
*       const int duty_cycle: The duty cycle to output   */
void servo_move(const int channel, const int duty_cycle);
#endif