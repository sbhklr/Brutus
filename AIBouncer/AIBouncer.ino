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
#include "logo.h"

// Here's the new syntax when using SoftwareSerial (e.g. Arduino Uno) ----
// If using hardware serial instead, comment out or remove these lines:

#include "SoftwareSerial.h"
#define TX_PIN 6 // Arduino transmit  YELLOW WIRE  labeled RX on printer
#define RX_PIN 5 // Arduino receive   GREEN WIRE   labeled TX on printer
#define BAUD_RATE 19200
#define FLORA_PULSE_TIME 6000

#define PUSH_BUTTON_PIN 2
#define FLORA_LED_PIN 8
#define PHOTO_WIDTH 36 
#define PHOTO_HEIGHT 36 
const int PHOTO_DATA_SIZE = PHOTO_WIDTH * PHOTO_HEIGHT / 8;

ZTimer floraTimer;
Flora flora = Flora(FLORA_LED_PIN);
SoftwareSerial softwareSerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&softwareSerial);     // Pass addr to printer constructor
int previousPushButtonValue = HIGH;

int serialDataMode = 0;
String currentBlock = "";

uint8_t photo_data[PHOTO_DATA_SIZE];
int currentPhotoDataIndex = 0;
String faceInfo = "";
// int imageSpacing = 104;


void setup() {
  flora.setBrightness(255);
	flora.setColor(50,50,150);
	floraTimer.SetCallBack([&]() {
	    flora.update();    
	});
	floraTimer.SetWaitTime(FLORA_PULSE_TIME / Flora::steps / 2);
	floraTimer.ResetTimer(true);

	pinMode(LED_BUILTIN, OUTPUT);
	pinMode(PUSH_BUTTON_PIN, INPUT_PULLUP);
	softwareSerial.begin(BAUD_RATE);  // Initialize SoftwareSerial  
	Serial.begin(115200);
  Serial.println("ready");
	//print();

  memset(photo_data, 0, PHOTO_DATA_SIZE);
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

  bool receivedData = false;
  
	while(Serial.available() > 0) {
    char currentChar = Serial.read();
    Serial.print(currentChar);
    
    if(currentChar == 'E'){
      serialDataMode = 0;
      Serial.println(faceInfo);
      Serial.println("end data");
    }

    if(serialDataMode == 1){
      faceInfo  = faceInfo + currentChar;
    }else if(serialDataMode == 2){
      /*
        if(currentBlock.length() == 3){ // add to array
          photo_data[currentPhotoDataIndex] = currentBlock.toInt();
          currentBlock = "";
          currentPhotoDataIndex++;
        }else{
          currentBlock = currentBlock + currentChar;
        }*/
    }

    if(currentChar == 'F'){
        serialDataMode = 1;
        Serial.println("start face");
    }else if(currentChar == 'I'){
      /*
        if(currentBlock.length() == 3){ // add to array
          photo_data[currentPhotoDataIndex] = currentBlock.toInt();
          currentBlock = "";
          currentPhotoDataIndex++;
        }else{
          currentBlock = currentBlock + currentChar;
        }*/
    }else if(currentChar == 'I'){
      Serial.println("start image");
      serialDataMode = 2;
    }else if(currentChar == 'D'){
      Serial.println(faceInfo);
    }else if(currentChar == 'P'){
      Serial.println("start to print");

      int makeupFee =  faceInfo.substring(0,2).toInt();
      int pyjamaFee = faceInfo.substring(2,4).toInt();
      int hipsterFee = faceInfo.substring(4,6).toInt();
      int youngsterFee = faceInfo.substring(8,10).toInt();
      int badMoodFee = faceInfo.substring(10,12).toInt();
      int aggressiveFee = faceInfo.substring(12,14).toInt();   
      
      Serial.print("makeupFee:");
      Serial.println(makeupFee);
      Serial.print("pyjamaFee:");
      Serial.println(pyjamaFee);
      Serial.print("hipsterFee:");
      Serial.println(hipsterFee);
      Serial.print("youngsterFee:");
      Serial.println(youngsterFee);
      Serial.print("badMoodFee:");
      Serial.println(badMoodFee);
      Serial.print("aggressiveFee:");
      Serial.println(aggressiveFee); 
      
      /*printer.begin();
      printReceipt(makeupFee, pyjamaFee, hipsterFee, youngsterFee, badMoodFee, aggressiveFee);
      printer.sleep();      // Tell printer to sleep
      delay(3000L);         // Sleep for 3 seconds
      printer.wake();       // MUST wake() before printing again, even if reset
      printer.setDefault(); // Restore printer to defaults*/

      // reset vars
      faceInfo = "";
      memset(photo_data, 0, PHOTO_DATA_SIZE);
      currentPhotoDataIndex = 0;
    }
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
	printer.printBitmap(PHOTO_WIDTH, PHOTO_HEIGHT, photo_data);
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
  readData();
 	int buttonValue = digitalRead(PUSH_BUTTON_PIN);
	
	if(buttonValue == previousPushButtonValue) return;
	previousPushButtonValue = buttonValue;

	if(buttonValue == LOW){
		// print();
    Serial.println("buttonPressed");
		delay(4000);
	} 

	delay(20);
}
