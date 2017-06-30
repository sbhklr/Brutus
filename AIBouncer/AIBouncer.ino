/*------------------------------------------------------------------------ 
  IMPORTANT: DECLARATIONS DIFFER FROM PRIOR VERSIONS OF THIS LIBRARY.
  This is to support newer & more board types, especially ones that don't
  support SoftwareSerial (e.g. Arduino Due).  You can pass any Stream
  (e.g. Serial1) to the printer constructor.  See notes below.

  You may need to edit the PRINTER_FIRMWARE value in Adafruit_Thermal.h
  to match your printer (hold feed button on powerup for test page).
  ------------------------------------------------------------------------*/

#include <ZTimer.h>
#include "Flora.h"
#include "Adafruit_Thermal.h"
#include "logo.h"
#include "photo.h"

// Here's the new syntax when using SoftwareSerial (e.g. Arduino Uno) ----
// If using hardware serial instead, comment out or remove these lines:

#include "SoftwareSerial.h"
#define TX_PIN 6 // Arduino transmit  YELLOW WIRE  labeled RX on printer
#define RX_PIN 5 // Arduino receive   GREEN WIRE   labeled TX on printer
#define BAUD_RATE 19200
#define FLORA_PULSE_TIME 6000

#define PUSH_BUTTON_PIN 2
#define FLORA_LED_PIN 8

ZTimer floraTimer;
Flora flora = Flora(FLORA_LED_PIN);
SoftwareSerial softwareSerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&softwareSerial);     // Pass addr to printer constructor
int previousPushButtonValue = HIGH;

void setup() {
	flora.setColor(50,50,150);
	floraTimer.SetCallBack([&]() {
	    flora.update();    
	});
	floraTimer.SetWaitTime(FLORA_PULSE_TIME / Flora::steps / 2);
	floraTimer.ResetTimer(true);

	pinMode(LED_BUILTIN, OUTPUT);
	pinMode(PUSH_BUTTON_PIN, INPUT_PULLUP);
	softwareSerial.begin(BAUD_RATE);  // Initialize SoftwareSerial  
	Serial.begin(9600);
	//print();
}

String generateRandomNumber(int digits){
	String number = "";
	for(int i=0; i<digits; ++i){
	    number += random(10);
	}
	return number;
}

void printLine(String line, char justify = 'L', char fontSize = 'S', bool bold = false, bool underline = false, int feed = 0){
	
	if(bold) printer.boldOn();
	if(underline) printer.underlineOn();

	printer.justify(justify);
	printer.setSize(fontSize);
	printer.println(line);
	printer.boldOff();
	printer.underlineOff();

	if(feed > 0) printer.feed(feed);
}

void print(){
	flora.setBrightness(255);
  	flora.setColor(255,50,50);

	printer.begin();        // Init printer (same regardless of serial type)
	printReceipt(0,0,50,0,95,0);
	printer.sleep();      // Tell printer to sleep
	delay(3000L);         // Sleep for 3 seconds
	printer.wake();       // MUST wake() before printing again, even if reset
	printer.setDefault(); // Restore printer to defaults

	flora.setColor(50,50,150);
}

void readData(){
	while (Serial.available() > 0) {
		String faceInfo  = Serial.readStringUntil('\n');
		/*
		int makeupFee = faceInfo.substring(0,1);
		int pyjamaFee = faceInfo.substring(2,3);
		int hipsterFee = faceInfo.substring(4,5);
		int youngsterFee = faceInfo.substring(8,9);
		int badMoodFee = faceInfo.substring(11,12);
		int aggressiveFee = faceInfo.substring(14,15);
		*/
		//0;0;50;0;95.0;0
	}
}

String formattedCurrency(int number){
	if(number < 10) return "  " + String(number);
	if(number < 100) return " " + String(number);
	return String(number);
}

void printReceipt(int makeupFee, int pyjamaFee, int hipsterFee, int youngsterFee, int badMoodFee, int aggressiveFee){
	//Print logo
	printer.printBitmap(logo_width, logo_height, logo_data);
	printLine(F("ROOTS"), 'C', 'L', true, false, 1);

	//Print photo
	//printer.printBitmap(photo_width, photo_height, photo_data);
	printer.feed(1);
	printer.setLineHeight(36);

	int baseFee = 50;
	int totalFee = baseFee + makeupFee + pyjamaFee + hipsterFee + youngsterFee + badMoodFee + aggressiveFee;

	//Print Content
	printLine("Base Fee                DKK " + formattedCurrency(baseFee), 'L', 'S', false, false, 1);
	
	printLine(F("Appearance Cost"), 'L', 'S', true);
	printLine("No-Make-Up Fee          DKK " + formattedCurrency(makeupFee));
	printLine("Pajamas Fee             DKK " + formattedCurrency(pyjamaFee));
	printLine("Hipster Fee             DKK " + formattedCurrency(hipsterFee));
	printer.feed(1);

	printLine(F("General Cost"), 'L', 'S', true);
	printLine("Youngster Fee           DKK " + formattedCurrency(youngsterFee));
	printLine("Bad Mood Fee            DKK " + formattedCurrency(badMoodFee));	
	printLine("Aggressive Behavior Fee DKK " + formattedCurrency(aggressiveFee));
	printer.feed(1);

	//Print Total
	printLine("Total                   DKK " + formattedCurrency(totalFee), 'L', 'S', true, true, 1);	

	//Print Barcode	
	printer.setBarcodeHeight(100);

	String number = generateRandomNumber(13);
	char numberBuffer[13];
	number.toCharArray(numberBuffer, 13);

	printer.printBarcode(numberBuffer, EAN13);	
	printer.feed(2);
}

void loop() {
	floraTimer.CheckTime();
	int buttonValue = digitalRead(PUSH_BUTTON_PIN);
	
	if(buttonValue == previousPushButtonValue) return;
	previousPushButtonValue = buttonValue;

	if(buttonValue == LOW){
		print();
		delay(4000);
	} 

	delay(20);

}