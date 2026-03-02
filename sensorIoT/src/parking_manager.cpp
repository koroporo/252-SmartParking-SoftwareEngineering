#include "parking_manager.h"

void parking_manager(void *pvParameter)
{
    HCSR04 *sensor[NUM_SLOT];
    for (int i = 0; i < NUM_SLOT; i++)
    {
        sensor[i] = new HCSR04(slots[i].trigPin, slots[i].echoPin);
    }

    while (1)
    {
        for (int i = 0; i < NUM_SLOT; i++)
        {
            float current_distance = sensor[i]->dist();
            bool current_state = (current_distance > DISTANCE_THRESHOLD);

            if (current_state != slots[i].lastState)
            {
                slots[i].debounceCounter++;
                if (slots[i].debounceCounter >= 4)
                {
                    slots[i].lastState = current_state;
                    slots[i].debounceCounter = 0;
                    if (xSensor != NULL &&
                        xSemaphoreTake(xSensor, portMAX_DELAY) == pdPASS)
                    {
                        slots[i].isAvailable = current_state; // for LED at slot
                        xSemaphoreGive(xSensor);
                    }
                }
            }
            else
            {
                slots[i].debounceCounter = 0;
            }

            if (xSensor != NULL &&
                xSemaphoreTake(xSensor, portMAX_DELAY) == pdPASS)
            {
                slots[i].currentDistance = current_distance;
                xSemaphoreGive(xSensor);
            }

            vTaskDelay(pdMS_TO_TICKS(50));
        }

        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

// each sensor scan after 200ms