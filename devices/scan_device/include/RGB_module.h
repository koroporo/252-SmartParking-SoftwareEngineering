#ifndef LED_MODULE_H
#define LED_MODULE_H

#include <global.h>

void initLED();
void setLedColor(int r, int g, int b);
void setLedDefault(); 
void setLedSuccess(); 
void setLedError();   

#endif