/*------------------------------------------------------------------------ 
  IMPORTANT: DECLARATIONS DIFFER FROM PRIOR VERSIONS OF THIS LIBRARY.
  This is to support newer & more board types, especially ones that don't
  support SoftwareSerial (e.g. Arduino Due).  You can pass any Stream
  (e.g. Serial1) to the printer constructor.  See notes below.

  You may need to edit the PRINTER_FIRMWARE value in Adafruit_Thermal.h
  to match your printer (hold feed button on powerup for test page).
  ------------------------------------------------------------------------*/

#include "ZTimer.h"
#include "Flora.h"
#include "Adafruit_Thermal.h"

// Here's the new syntax when using SoftwareSerial (e.g. Arduino Uno) ----
// If using hardware serial instead, comment out or remove these lines:
#define FLORA_LED_PIN 8
#define CAMERA_LED_PIN 7

#define FLORA_PULSE_TIME 6000
#define BAUD_RATE 9600


ZTimer floraTimer;
Flora flora = Flora(FLORA_LED_PIN);
Adafruit_NeoPixel cameraLedPixel;

void setup() {
  flora.setBrightness(255);
	flora.setColor(50,50,150);
	floraTimer.SetCallBack([&]() {
	    flora.update();    
	});
	floraTimer.SetWaitTime(FLORA_PULSE_TIME / Flora::steps / 2);
	floraTimer.ResetTimer(true);

  pinMode(CAMERA_LED_PIN, OUTPUT);
  cameraLedPixel = Adafruit_NeoPixel(1, CAMERA_LED_PIN, NEO_GRB + NEO_KHZ800);
  cameraLedPixel.begin();  
  setCameraLed(255,0,0);
  
	Serial.begin(BAUD_RATE);
  Serial.println("ready");

  
}

void processSerialCommands(){
	while(Serial.available() > 0) {
    char currentChar = Serial.read();
    if(currentChar == 'P'){
      setCameraLed(255,255,255);
      delay(800);
      setCameraLed(255,0,0);
    }
 	}
}

void setCameraLed(int r, int g, int b){
  cameraLedPixel.setBrightness(100);
  cameraLedPixel.setPixelColor(0, cameraLedPixel.Color(r,g,b));     
  cameraLedPixel.show(); 
}

void loop() {
	floraTimer.CheckTime();
  processSerialCommands();
	delay(200);
}

