#include "global.h"

const char* ssid = "TECNO POVA 6";
const char* password = "zysion123";

const String GAS_URL = "https://script.google.com/macros/s/AKfycbwl_8-xCydH4kWoHjZLfoSlq9T5EJpZ8XnPGbhDGqN5ah5bv0D-MtXlI2M23A6GuKfP/exec"; 

SemaphoreHandle_t btnSemaphore;

// ================= TASK CHECK-IN =================
// Task: Wait for user to press button -> Read card -> Send to network
void TaskCheckIn(void *pvParameters) {
    while (1) {
        // Wait for button press (Block task until receiving Semaphore from interrupt)
        if (xSemaphoreTake(btnSemaphore, portMAX_DELAY) == pdTRUE) {
            Serial.println("Button pressed! Scanning Check-in card...");
            
            unsigned long startTime = millis();
            bool cardFound = false;
            
            while (millis() - startTime < 3000) {
                if (mfrc522_1.PICC_IsNewCardPresent() && mfrc522_1.PICC_ReadCardSerial()) {
                    String uid = getUID(mfrc522_1);
                    Serial.println("Check-in Card: " + uid);
                    
                    // Send data to Datacore
                    if(sendCheckInRequest(uid)) {
                        Serial.println("Check-in recorded successfully!");
                    } else {
                        Serial.println("Network error during Check-in.");
                    }
                    cardFound = true;
                    break;
                }
                vTaskDelay(50 / portTICK_PERIOD_MS);
            }
            if(!cardFound) Serial.println("Check-in card timeout.");
        }
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

// ================= TASK CHECK-OUT =================
// Task: Continuously scan cards on reader 2 in background -> Authenticate -> Change LED color
void TaskCheckOut(void *pvParameters) {
    while (1) {
        // Check if a card is present on module 2
        if (mfrc522_2.PICC_IsNewCardPresent() && mfrc522_2.PICC_ReadCardSerial()) {
            String uid = getUID(mfrc522_2);
            Serial.println("Check-out Card: " + uid);
            
            bool isValid = sendCheckOutRequest(uid);
            
            if (isValid) {
                Serial.println("VALID card. Open!");
                setLedSuccess(); 
            } else {
                Serial.println("INVALID card!");
                setLedError();   
            }
            
            // Keep LED state for 2 seconds then return to default Blue
            vTaskDelay(2000 / portTICK_PERIOD_MS);
            setLedDefault();
        }
        
        // Delay 100ms to yield CPU to other tasks
        vTaskDelay(100 / portTICK_PERIOD_MS);
    }
}

// ================= TASK POLL COMMAND =================
// Task: Continuously poll Datacore to check if any phone just scanned a valid QR code
void TaskPollCommand(void *pvParameters) {
    while (1) {
        if (WiFi.status() == WL_CONNECTED) {
            HTTPClient http;
            String url = GAS_URL + "?action=poll_command";
            http.begin(url);
            http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
            
            int httpCode = http.GET();
            if (httpCode == HTTP_CODE_OK) {
                String payload = http.getString();
                payload.trim();
                
                if (payload == "VALID") {
                    Serial.println("Command received from Web: Member card is VALID!");
                    setLedSuccess(); 
                    vTaskDelay(2000 / portTICK_PERIOD_MS);
                    setLedDefault();
                } else if (payload == "INVALID") {
                    Serial.println("Command received from Web: Member card is INVALID!");
                    setLedError();  
                    vTaskDelay(2000 / portTICK_PERIOD_MS);
                    setLedDefault();
                }
                // If payload is "NONE", do nothing
            }
            http.end();
        }
        
        // Wait 1.5 seconds before polling again (avoid overwhelming Google server)
        vTaskDelay(1500 / portTICK_PERIOD_MS);
    }
}

void setup() {
    Serial.begin(115200);
    
    // Initialize modules
    initLED();
    initRFID();
    initButton();
    connectWiFi();
    setupBlinkyLed();

    // Initialize Semaphore (Binary Semaphore)
    btnSemaphore = xSemaphoreCreateBinary();

    // Create concurrent tasks using FreeRTOS
    xTaskCreate(loopBlinkyLed, "Task_Blinky", 2048, NULL, 0, NULL); 
    xTaskCreatePinnedToCore(TaskCheckIn, "Task_CheckIn", 8192, NULL, 1, NULL, 1);     // Core 1
    xTaskCreatePinnedToCore(TaskCheckOut, "Task_CheckOut", 8192, NULL, 1, NULL, 1);   // Core 1
    xTaskCreatePinnedToCore(TaskPollCommand, "Task_PollCmd", 8192, NULL, 1, NULL, 0); // Core 0
    
}

void loop() {
    vTaskDelete(NULL); 
}