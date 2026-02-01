#ifndef FSM_H
#define FSM_H
#include <stdint.h>
#include <stdbool.h>
const uint32_t DISTANCE_THRESHOLD = 50; // cm
const uint32_t CONFIRMATION_TIME = 10000; // ms
typedef enum {
    IDLE,
    DETECTION,
    OCCUPIED
} State;

void fsm_init();
State fsm_update(uint32_t distance);

#endif