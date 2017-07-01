#ifndef FLORA_H
#define FLORA_H

#include "Adafruit_NeoPixel.h"

#define FLORA_MAX_BRIGHTNESS 255

class Flora {	
 public:
 	static const int BrightnessStepSize = 2; 	
 	static const int steps = FLORA_MAX_BRIGHTNESS / BrightnessStepSize; 	
 	void update();
 	Flora(int ledPin);
 	void setColor(int r, int g, int b);
 	void setBrightness(int brightness);

 private: 	
 	int _colorR = 0;
 	int _colorG = 0;
 	int _colorB = 0;
 	int _ledPin;
 	int _currentLEDBrightness = 0;
	int _pulsateDirection = 1;
	Adafruit_NeoPixel _pixels;	
	void showPixels();
};

#endif