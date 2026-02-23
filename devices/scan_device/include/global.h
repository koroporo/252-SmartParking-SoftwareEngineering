#ifndef GLOBAL_H
#define GLOBAL_H

#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/semphr.h>

// ================= CẤU HÌNH WIFI & API =================
extern const char* ssid;
extern const char* password;
extern const String GAS_URL; // URL Google Apps Script của bạn

// ================= CẤU HÌNH PINOUT =================
// Cấu hình SPI dùng chung cho 2 module RFID
#define SPI_SCK      18
#define SPI_MISO     19
#define SPI_MOSI     23

// RFID 1 (Check-in)
#define RST_PIN_1    22
#define SS_PIN_1     5

// RFID 2 (Check-out)
#define RST_PIN_2    21
#define SS_PIN_2     15

// LED RGB (Sử dụng PWM hoặc Digital Out)
#define LED_R_PIN    27
#define LED_G_PIN    26
#define LED_B_PIN    25

// Nút nhấn (Button Check-in)
#define BUTTON_PIN   4

// ================= KHAI BÁO BIẾN TOÀN CỤC =================
extern MFRC522 mfrc522_1; // Module Check-in
extern MFRC522 mfrc522_2; // Module Check-out

// Khai báo Semaphore cho RTOS (Dùng để đồng bộ nút nhấn)
extern SemaphoreHandle_t btnSemaphore;

// ================= INCLUDE CÁC MODULE KHÁC =================
// Bằng cách include tại đây, file main.cpp chỉ cần include global.h
#include "RGB_module.h"
#include "button_module.h"
#include "rfid_module.h"
#include "wifi_module.h"
#include "blinkyled.h"

#endif