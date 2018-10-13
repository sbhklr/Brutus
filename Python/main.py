#!/usr/bin/python

import serial
from thermal_printer import ThermalPrinter
from facesApi import calculateFee
from imageParse import imageParse
from sendStatus import sendStatus
from multiprocessing import Process
import os
import sys
import time
from time import sleep
import evdev #SEE: https://python-evdev.readthedocs.io/en/latest/apidoc.html#
from neopixel import *

#######################################
displayIP = "192.168.1.121"


########## NEO PIXEL SETUP ############
LED_COUNT      = 9      # Number of LED pixels.
LED_PIN_FLORA  = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

blueColor = Color(0, 0, 255)
redColor = Color(0, 255, 0)
greenColor = Color(255, 0, 0)
blackColor = Color(0,0,0)

def setCameraLed(color):
    flora.setPixelColor(0,color)
    flora.show()

def flashLedGreen():
    setCameraLed(greenColor)
    time.sleep(0.8)
    setCameraLed(blueColor)

def flashLedRed():
    for i in range(3):
        setCameraLed(redColor);
        time.sleep(0.2)
        setCameraLed(blackColor);
        time.sleep(0.2)
    setCameraLed(blueColor)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
for i in range(strip.numPixels()):
    strip.setPixelColor(i, blueColor)    
strip.show()

flora = Adafruit_NeoPixel(1, LED_PIN_FLORA, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
flora.begin()
setCameraLed(blueColor)

#######################################


is_raspberry_pi = os.uname()[0] == "Linux"

print "Running on: " + str(os.uname())

# Parse Arguments
noPrint = False
noSerial = False
noHttp = False
noCamera = False

for eachArg in sys.argv:
    if eachArg == "noprint":
        noPrint = True
    if eachArg == "noserial":
        noSerial = True
    if eachArg == "nohttp":
        noHttp = True
    if eachArg == "nocamera":
        noCamera = True

if is_raspberry_pi:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    from button_logic import ButtonTracker

    usbButton = evdev.InputDevice('/dev/input/event0')
    print("Input Device event0: " + str(usbButton))

    if noCamera == False:
        import picamera
        camera = picamera.PiCamera()
        camera.resolution = (864, 648)
        camera.brightness = 60
        camera.contrast = 45
        camera.rotation = 90
        #camera.hflip = True
        #camera.vflip = True


if noHttp:
    def sendStatus(ip, status, delay):
        print status
else:
    from sendStatus import sendStatus

if noSerial == False:
    if is_raspberry_pi:
        arduinoSerial = serial.Serial('/dev/ttyACM0', 9600)
    else:
        arduinoSerial = serial.Serial('/dev/cu.usbmodem146221', 9600)
    command = arduinoSerial.readline() # wait till arduino is ready

def sendSerialMsg(status):
    if noSerial == False:
        arduinoSerial.write(status + "\n")

def buttonPressed(pins=[], timestamp=0):
    #print("Pressed buttons: ", pins)        

    if is_raspberry_pi and noCamera == False:
        pictureFileName = "photo.jpg"
        camera.start_preview()
        sleep(0.25)
        camera.capture(pictureFileName)
        camera.stop_preview()
    else:
        pictureFileName = "photoDummy2.jpg"

    sendStatus(displayIP, "Analysing face...", 0)
    sendSerialMsg('P')
    flashLedGreen()

    with open(pictureFileName, mode='rb') as file: # b is important -> binary
        fileContent = file.read()

    fee = calculateFee(fileContent)
    if fee is not None:
        # Messages
        sendStatus(displayIP, "Estimated age " + str(int(round(fee.age))), 0)
        if fee.hasHeadwear:
            sendStatus(displayIP, "Headwear detected", 1)
        if fee.hasMakeup:
            sendStatus(displayIP, "Makeup detected", 1 * 2)
        elif fee.gender == "female":
            sendStatus(displayIP, "No makeup detected", 1 * 2)
        if fee.hasFacialHair:
            sendStatus(displayIP, "Beard detected", 1 * 3)
        if fee.isAggressive:
            sendStatus(displayIP, "Aggressive behavior detected", 1 * 4)
        elif sum(pins) > 1:
            fee.aggressive = 50
            sendStatus(displayIP, "Aggressive behavior detected", 1 * 4)
        if fee.hasBadMood:
            sendStatus(displayIP, "Bad mood detected", 1 * 5)

        # Add aggressive fee if multi press of button happens
        print "Makeup: " + str(fee.makeup)
        print "Underdressed: " + str(fee.pyjama)
        print "Hipster: " + str(fee.hipster)
        print "Youngster: " + str(fee.youngster)
        print "Oldie: " + str(fee.oldie)
        print "badMood: " + str(fee.badMood)
        print "Aggressive: " + str(fee.aggressive)

        photoData = imageParse(pictureFileName)
        
        if is_raspberry_pi and noPrint == False:
            sendStatus(displayIP, "Printing...", 1 * 6)
            thermal_printer = ThermalPrinter(photoData,384,153)
            thermal_printer.printReceipt(fee)
            sendStatus(displayIP, "Done.", 0)
        else:
            sendStatus(displayIP, "Done.", 1 * 6)    
    else:
        sendSerialMsg('E')
        flashLedRed()
        sendStatus(displayIP, "No face detected.", 0)         

if is_raspberry_pi:
    #To use custom made button use ButtonTracker
    #buttonTracker = ButtonTracker(6, 13, 19, buttonPressed)    

    for event in usbButton.read_loop():     
        if event.type == evdev.ecodes.EV_KEY and event.value == evdev.events.KeyEvent.key_up:       
            #print(evdev.categorize(event))
            buttonPressed([], time.time())
    print("THE END.")

else:
    buttonPressed()
