#include "servos_wrapper.h"

void servo_setup(void) {
    ledcSetup(PWN_CHANNEL_PAN, PWM_FREQ, PWM_RESOLUTION);
    ledcSetup(PWM_CHANNEL_TILT, PWM_FREQ, PWM_RESOLUTION);
    /* Attach the LED PWM Channel to the GPIO Pin */
    ledcAttachPin(SERVO_PAN_PIN, PWN_CHANNEL_PAN);
    ledcAttachPin(SERVO_TILT_PIN, PWM_CHANNEL_TILT);
}

void servo_move(const int channel, int duty_cycle) {
    // Cliping between effective bounds
    duty_cycle = max(SERVO_MIN, min(SERVO_MAX, duty_cycle));
    ledcWrite(channel, duty_cycle);
}
