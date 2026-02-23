#ifndef BUTTON_MODULE_H
#define BUTTON_MODULE_H

#include <global.h>

void initButton();
void IRAM_ATTR buttonInterruptHandler();

#endif