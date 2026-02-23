#include "global.h"

// Initialize 2 RFID objects with different SS and RST pins
MFRC522 mfrc522_1(SS_PIN_1, RST_PIN_1);
MFRC522 mfrc522_2(SS_PIN_2, RST_PIN_2);

void initRFID() {
    SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
    mfrc522_1.PCD_Init(); // Initialize reader 1
    mfrc522_2.PCD_Init(); // Initialize reader 2
    Serial.println("Initialized 2 MFRC522 RFID modules.");
}

// Function to read and convert card UID to String
String getUID(MFRC522 &mfrc522) {
    String uidString = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        uidString += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
        uidString += String(mfrc522.uid.uidByte[i], HEX);
    }
    uidString.toUpperCase();
    
    // Stop encrypted communication with card
    mfrc522.PICC_HaltA();
    return uidString;
}