#include "taskWiFi.h"

static const char *WIFI_SSID = "CALLMECHUNG";
static const char *WIFI_PASS = "28032005";

void WiFi_Connect()
{
    WiFi.begin(WIFI_SSID, WIFI_PASS);

    isWiFiconnected = false;
    uint32_t t = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - t < 5000)
    {
        Serial.print(".");
        vTaskDelay(pdMS_TO_TICKS(500));
    }

    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.print("\nWiFi connected time out. Retry later!!!\n");
    }
    else
    {
        Serial.print("WiFi connected successfully");
        isWiFiconnected = true;
    }
}

void task_WiFi(void *pvParameter)
{
    vTaskDelay(pdMS_TO_TICKS(2000));
    Serial.println("Setting up WiFi");
    while (1)
    {
        if (WiFi.status() != WL_CONNECTED)
        {
            isWiFiconnected = false;
            Serial.print("\nWiFi lost connection\n");
            WiFi_Connect();
        }
        else
        {
            Serial.println("WiFi OK");
        }
        vTaskDelay(pdMS_TO_TICKS(5000));
    }
}