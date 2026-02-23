#include "global.h"

void connectWiFi() {
    Serial.print("Connecting to WiFi");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected successfully!");
}

// Hàm gửi HTTP GET lên Google Apps Script cho việc Check-in
bool sendCheckInRequest(String uid) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        String url = GAS_URL + "?action=check_in&uid=" + uid;
        http.begin(url);
        http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS); // Required for Google Scripts
        
        int httpCode = http.GET();
        bool success = false;
        if (httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            Serial.println("Server response: " + payload);
            if(payload == "OK") success = true;
        } else {
            Serial.printf("HTTP GET error: %s\n", http.errorToString(httpCode).c_str());
        }
        http.end();
        return success;
    }
    return false;
}

// Function to send HTTP GET to Google Apps Script for Check-out
bool sendCheckOutRequest(String uid) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        String url = GAS_URL + "?action=check_out&uid=" + uid;
        http.begin(url);
        http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
        
        int httpCode = http.GET();
        bool isValid = false;
        if (httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            Serial.println("Server response: " + payload);
            if(payload == "VALID") isValid = true;
        }
        http.end();
        return isValid;
    }
    return false;
}