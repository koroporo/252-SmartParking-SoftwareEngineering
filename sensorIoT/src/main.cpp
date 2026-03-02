#include "global.h"
#include "parking_manager.h"
#include "LCD_Display.h"
#include "taskWiFi.h"

void setup()
{
    Serial.begin(115200);
    xSensor = xSemaphoreCreateMutex();

    xTaskCreate(parking_manager, "task manager", 4096, NULL, 2, NULL);
    xTaskCreate(lcd_display, "task LCD", 4096, NULL, 2, NULL);
    xTaskCreate(task_WiFi, "task wiFi", 4096, NULL, 3, NULL);
}

void loop() {}