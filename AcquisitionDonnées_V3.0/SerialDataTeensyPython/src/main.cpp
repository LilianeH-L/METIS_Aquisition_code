#include <Arduino.h>
#include <Encoder.h>

unsigned long currentMicros;
int interval = 500;

//Values to change depending on tests to be made
const int numberOfElectrodes = 2;
const int numberOfEncoder = 4;

/* For reading myoware signals */
//Assign pins
const int analogPin1 = 15;
const int analogPin2 = 16;
const int analogPin3 = 21;
const int analogPin4 = 22;

/* For reading encoder signals */
//Name pins
const int encoder1_Pin1 = 2;
const int encoder1_Pin2 = 3;
const int encoder2_Pin1 = 10;
const int encoder2_Pin2 = 11;
const int encoder3_Pin1 = 17;
const int encoder3_Pin2 = 18;
const int encoder4_Pin1 = 19;
const int encoder4_Pin2 = 20;

//Assign pins
Encoder encod1(encoder1_Pin1, encoder1_Pin2);
Encoder encod2(encoder2_Pin1, encoder2_Pin2);
Encoder encod3(encoder3_Pin1, encoder3_Pin2);
Encoder encod4(encoder4_Pin1, encoder4_Pin2);

int electrodePin[4] = {analogPin1, analogPin2, analogPin3, analogPin4};
Encoder encoder[4] = {encod1, encod2, encod3, encod4};

//Variables for sending packages
byte counterElectrode = 0;
byte counterEncoder = 0;

uint16_t valueElectrode[numberOfElectrodes];
uint32_t valueEncoder[numberOfEncoder]; //Encoder returns long which is 32 bits on TeensyLC (not 64)
uint8_t valuesToSend[numberOfElectrodes*2 + numberOfEncoder*4];


//Interrupts *Pas nécessaire en ce moment*
/*
void interrupt_Encod1() {
  char i;
  i = digitalRead(encoder1_Pin2);
  if (i == 1)
    valueEncoder[0] += 1;
  else
    valueEncoder[0] -= 1;
}


void interrupt_Encod2() {
  char i;
  i = digitalRead(encoder2_Pin2);
  if (i == 1)
    valueEncoder[1] += 1;
  else
    valueEncoder[1] -= 1;
}
*/

void setup() {
  //Set baud rate
  Serial.begin(1000000);

  //Set ADC resolution
  analogReadResolution(12);

  //Reset encoder position
  /*
  for(int i = 0; i < numberOfEncoder; i++) {
    encoder[i].write(1600);
  }
  */
  //Vraisemblablement il accepte pas les tableaux d'encodeurs donc le code suivant est un patch temporaire
  encod1.write(5000);
  encod2.write(5000);
  encod3.write(5000);
  encod4.write(5000);
}


void loop() {
  //Set reference timer
  currentMicros = micros();
  
  //Execution time of all of this is approximately 100micros
  //Reset all counters
  counterElectrode = 0;
  counterEncoder = 0;

  //Read all electrode signals
  for(int i = 0; i < numberOfElectrodes; i++) {
    valueElectrode[i] = analogRead(electrodePin[i]);
  }

  //Read all encoder signals
  /*
  for(int i = 0; i < numberOfEncoder; i++) {
    //valueEncoder[i] = abs(encoder[i].read());
  }
  */
  valueEncoder[0] = abs(encod1.read());
  valueEncoder[1] = abs(encod2.read());
  valueEncoder[2] = abs(encod3.read());
  valueEncoder[3] = abs(encod4.read());


  //Decompose all values from electrodes
  for(int i = 0; i < sizeof(valuesToSend); i++) {
    //Decompose all values from electrodes
    if(counterElectrode < numberOfElectrodes) {
      //We decompose valueElectrode in 2 : 
        //First value is for the MSB byte
        //Second value is for the LSB byte
      valuesToSend[i] = valueElectrode[counterElectrode] & 255; 
      valuesToSend[i + 1] = (valueElectrode[counterElectrode] >> 8) & 255;
      
      i++;
      counterElectrode++;
    }

    //Decompose all values from encoders
    else if(counterEncoder < numberOfEncoder) {
      //Meaning we are intaking encoder values
        //First value is for the MSB byte etc.
        //Last value is for the LSB byte
      valuesToSend[i] = valueEncoder[counterEncoder] & 255;
      valuesToSend[i + 1] = (valueEncoder[counterEncoder] >> 8) & 255;
      valuesToSend[i + 2] = (valueEncoder[counterEncoder] >> 16) & 255;
      valuesToSend[i + 3] = (valueEncoder[counterEncoder] >> 24) & 255;
  
      i++; i++; i++;
      counterEncoder++;
      }
  }

    //Send package to python every interval
    Serial.write(valuesToSend, sizeof(valuesToSend));
    Serial.send_now();

  //Wait for a certain interval of time
  while(micros() < currentMicros + interval) {} //Wait [interval]us 
}

