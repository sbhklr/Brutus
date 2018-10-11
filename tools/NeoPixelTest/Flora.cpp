#include "Flora.h"
#include <Arduino.h>

//Flora Pixel Defines
#define AMOUNT_OF_FLORA_PIXELS 9


Flora::Flora(int ledPin) : _ledPin(ledPin){
	pinMode(_ledPin, OUTPUT);
	_pixels = Adafruit_NeoPixel(AMOUNT_OF_FLORA_PIXELS, _ledPin, NEO_GRB + NEO_KHZ800);
	_pixels.begin();		
}

void Flora::setColor(int r, int g, int b){
	_colorR = r;
	_colorG = g;
	_colorB = b;
	showPixels();	
}

void Flora::setBrightness(int brightness) {
	_currentLEDBrightness = brightness;
	showPixels();
}

void Flora::update() {
	showPixels();
	if(_currentLEDBrightness + BrightnessStepSize > FLORA_MAX_BRIGHTNESS || _currentLEDBrightness - BrightnessStepSize < 0) _pulsateDirection *= -1;
  	_currentLEDBrightness = _currentLEDBrightness + (BrightnessStepSize * _pulsateDirection);  
}

void Flora::showPixels(){		
	_pixels.setBrightness(_currentLEDBrightness);

	for(int i=0; i<AMOUNT_OF_FLORA_PIXELS; i++){
		_pixels.setPixelColor(i, _pixels.Color(_colorR,_colorG,_colorB));	  
	}
	_pixels.show();      
}
