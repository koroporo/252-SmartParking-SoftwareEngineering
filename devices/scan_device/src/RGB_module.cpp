#include "global.h"

void initLED() {
    pinMode(LED_R_PIN, OUTPUT);
    pinMode(LED_G_PIN, OUTPUT);
    pinMode(LED_B_PIN, OUTPUT);
    setLedDefault(); // Default startup color is Blue
}

// Hàm set màu (Giả sử LED common cathode - anode chung thì đảo ngược logic)
void setLedColor(int r, int g, int b) {
    digitalWrite(LED_R_PIN, r);
    digitalWrite(LED_G_PIN, g);
    digitalWrite(LED_B_PIN, b);
}

void setLedDefault() {
    // Blue color
    setLedColor(LOW, LOW, HIGH);
}

void setLedSuccess() {
    // Green color
    setLedColor(LOW, HIGH, LOW);
}

void setLedError() {
    // Red color
    setLedColor(HIGH, LOW, LOW);
}