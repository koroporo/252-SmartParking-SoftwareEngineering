#include "global.h"

// Interrupt when button is pressed
void IRAM_ATTR buttonInterruptHandler() {
    // When button is pressed, release Semaphore to notify Check-in Task
    xSemaphoreGiveFromISR(btnSemaphore, NULL);
}

void initButton() {
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    // Activate interrupt on falling edge (FALLING - due to using INPUT_PULLUP)
    attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonInterruptHandler, FALLING);
}