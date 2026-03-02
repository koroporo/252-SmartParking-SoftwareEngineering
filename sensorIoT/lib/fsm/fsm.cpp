#include  <Arduino.h>
#include <stdint.h>
#include <assert.h>

#include <fsm.h>

#define ERROR(condition, message) \
    if (!(condition)) { \
        Serial.print("FSM ERROR: "); \
        Serial.println(message); \
        while(1); \
    }

uint32_t startTime; // ms
State current_state;
State next_state;

void fsm_init(){
    current_state = IDLE;
    next_state = IDLE;
    startTime = 0;
}

void idle(uint32_t distance){
    ERROR(startTime == 0, "startTime should always be 0 in IDLE state !\n")
    if (distance > 0 && distance < DISTANCE_THRESHOLD) {
        startTime = millis();
        next_state = DETECTION;
    }
}

void obstacles_detection(uint32_t distance){
    if (millis() - startTime > CONFIRMATION_TIME && distance < DISTANCE_THRESHOLD){
        startTime = 0;
        next_state = OCCUPIED;
    }
    else if (millis() - startTime <= CONFIRMATION_TIME && distance >= DISTANCE_THRESHOLD){
        startTime = 0;
        next_state = IDLE;
    }
}

void occupied(uint32_t distance){
    if (distance >= DISTANCE_THRESHOLD){
        startTime = 0; // Already done but just to be sure
        next_state = IDLE;
    }
}

State fsm_update(uint32_t distance){
    ERROR(distance<0,"Negative distance !\n");
    switch (current_state)
    {
    case IDLE:
        idle(distance);
        break;
    case DETECTION:
        obstacles_detection(distance);
        break;
    case OCCUPIED:
        occupied(distance);
        break;
    default:
        break;
    }
    current_state = next_state;
    return current_state;
}
