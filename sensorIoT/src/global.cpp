#include "global.h"

ParkingSlot slots[NUM_SLOT] = {
    {1, 4, 5, -1, false, 0, false},  // Slot_1: Trig_4, Echo_5
    {2, 6, 7, -1, false, 0, false},  // Slot_2: Trig_6, Echo_7
    {3, 12, 13, -1, false, 0, false} // Slot_3: Trig_12, Echo_13
};
SemaphoreHandle_t xSensor;
bool isWiFiconnected = false;