#ifndef NETWORK_MODULE_H
#define NETWORK_MODULE_H

#include <global.h>

void connectWiFi();
bool sendCheckInRequest(String uid);
bool sendCheckOutRequest(String uid);

#endif