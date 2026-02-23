#include <global.h>

void setupBlinkyLed() {
    pinMode(2, OUTPUT); 
}

void loopBlinkyLed(void *pvParameters) {
    while (1) {
        digitalWrite(2, HIGH); 
        vTaskDelay(1000 / portTICK_PERIOD_MS); 
        digitalWrite(2, LOW); 
        vTaskDelay(1000 / portTICK_PERIOD_MS); 
    }
}