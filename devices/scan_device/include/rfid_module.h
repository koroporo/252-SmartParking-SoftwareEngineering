#ifndef RFID_MODULE_H
#define RFID_MODULE_H

#include <global.h>

void initRFID();
String getUID(MFRC522 &mfrc522);

#endif