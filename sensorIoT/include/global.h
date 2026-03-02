#ifndef __GLOBAL_H__
#define __GLOBAL_H__

#include <Arduino.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

#define DISTANCE_THRESHOLD 5 //cm
#define NUM_SLOT 3

#define SDA_PIN 8
#define SCL_PIN 9

struct ParkingSlot {
    int id;
    int trigPin;
    int echoPin;

    float currentDistance;
    bool isAvailable;
    int debounceCounter;
    bool lastState; 
};

extern ParkingSlot slots[NUM_SLOT];
extern SemaphoreHandle_t xSensor;
extern bool isWiFiconnected;

#endif