#include <Arduino.h>
#include <Wire.h>

const int analogPin = 15;
uint16_t value = 0;


void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
}

void loop() {
    value = analogRead(analogPin);
    Serial.print((String)value + "%\n");
    delay(50);
}