#include <Arduino.h>
#include <Wire.h>

const int ledPin = 5;
const int analogPin = 15;
uint16_t value = 0;
byte command = 0;
bool counter = false;

void checkForCommand()
{
  if(Serial.available() > 0)
  {
    command = Serial.read();
  }
}


void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  while(!counter)
  {
    checkForCommand();
    if(command != 0)
    {
      counter = true;
    }
  }

  switch(command)
  {
    case 1:
      value = analogRead(analogPin);
      Serial.print((String)value + "%\n");
      delay(10);

      checkForCommand();
    break;

    case 2:
      digitalWrite(ledPin, HIGH);
      delay(1);

      checkForCommand();
      if(command != 2)
      {
        digitalWrite(ledPin, LOW);
      }
    break;
  }
}

