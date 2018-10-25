/*------------------------------------------------------------------------ 
  IMPORTANT: DECLARATIONS DIFFER FROM PRIOR VERSIONS OF THIS LIBRARY.
  This is to support newer & more board types, especially ones that don't
  support SoftwareSerial (e.g. Arduino Due).  You can pass any Stream
  (e.g. Serial1) to the printer constructor.  See notes below.

  You may need to edit the PRINTER_FIRMWARE value in Adafruit_Thermal.h
  to match your printer (hold feed button on powerup for test page).
  ------------------------------------------------------------------------*/

#include "Flora.h"

#define FLORA_LED_PIN 6
Flora flora = Flora(FLORA_LED_PIN);

void setup() {
  flora.setBrightness(255);
	flora.setColor(50,50,150);
  flora.update();
}

void loop() {	
	delay(200);
}
