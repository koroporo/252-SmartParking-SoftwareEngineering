#include "LCD_Display.h"

void lcd_display(void *pvParameter)
{
    LiquidCrystal_I2C lcd(0x27, 20, 4);
    Wire.begin(SDA_PIN, SCL_PIN);

    lcd.init();
    lcd.backlight();

    while (1)
    {
        if (!isWiFiconnected)
        {
            lcd.setCursor(0, 0);
            lcd.printf("WiFi is connecting  ");
            lcd.setCursor(0, 1);
            lcd.printf("                    ");
            lcd.setCursor(0, 2);
            lcd.printf("                    ");
            lcd.setCursor(0, 3);
            lcd.printf("                    ");
            vTaskDelay(pdMS_TO_TICKS(500));
            continue;
        }

        lcd.setCursor(0, 0);
        lcd.printf("  --PARKING SLOT--  ");
        for (int i = 0; i < NUM_SLOT; i++)
        {
            float current_distance;
            bool current_state;

            if (xSensor != NULL &&
                xSemaphoreTake(xSensor, portMAX_DELAY) == pdPASS)
            {
                // I deleted all of the previous code :D
                current_distance = slots[i].currentDistance;
                current_state = slots[i].isAvailable;

                xSemaphoreGive(xSensor);
            }

            lcd.setCursor(0, i + 1);
            lcd.printf("S%d: %-5s | %4.1fcm",
                       slots[i].id,
                       current_state ? "FREE" : "BUSY",
                       current_distance);
        }
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}