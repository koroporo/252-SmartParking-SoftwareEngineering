#include <Arduino.h>
#include <stdint.h>

#include <fsm.h>

const int TRIG_PIN = 5;
const int ECHO_PIN = 18;

void setup(){
    // put init code here, to run once
    Serial.begin(115200);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    fsm_init();
}

void loop(){
  // Main code, run repeatedly
  digitalWrite(TRIG_PIN, LOW); 
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); //Begin caption signal send to the sensor via the TRIG_PIN
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW); //End caption
  
  uint32_t duration = pulseIn(ECHO_PIN, HIGH,300000); // Time-of-Flight in micros (Time for the signal to travel between the sensor and the object)
  int32_t distance = duration * 0.034 / 2; // Speed of sound = 340m/s = 0.034 cm/micros

  State current_state = fsm_update(distance);

  // Logs
  Serial.print("Dist: ");
  Serial.print(distance);
  Serial.print("cm | ");
  Serial.print("Status: ");
  if (current_state == OCCUPIED) Serial.println("CONFIRMED");
  else if (current_state == DETECTION) Serial.println("Checking...");
  else Serial.println("Vacant");

  delay(500); // No need to be faster right now (2 sensor-check/s)
}