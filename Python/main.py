#!/usr/bin/python

import serial
from thermal_printer import ThermalPrinter
from facesApi import calculateFee
from imageParse import imageParse
from button_logic import ButtonTracker
import os
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

is_raspberry_pi = os.uname()[1] == "raspberrypi"

if is_raspberry_pi:
    import picamera

# Parse Arguments
noPrint = False
arduinoSerial = True
for eachArg in sys.argv:
    if eachArg == "noprint":
        noPrint = True
    if eachArg == "noserial":
        arduinoSerial = None


if arduinoSerial is not None:
    if is_raspberry_pi:
        arduinoSerial = serial.Serial('/dev/ttyACM0', 9600)
    else:
        arduinoSerial = serial.Serial('/dev/cu.usbmodem146221', 9600)
    command = arduinoSerial.readline() # wait till arduino is ready

def sendSerialMsg(status):
    if arduinoSerial is not None:
        arduinoSerial.write(status + "\n")

def buttonPressed(pin, time):
    # sendStatus("Analysing face...")
    sendSerialMsg('P')

    if is_raspberry_pi:
        pictureFileName = "photo.jpg"
        camera = picamera.PiCamera()
        camera.resolution = (864, 648)
        camera.brightness = 80
        camera.contrast = 75
        camera.rotation = 90
        #camera.hflip = True
        #camera.vflip = True
        camera.capture(pictureFileName)
    else:
        pictureFileName = "photoDummy3.jpg"

    with open(pictureFileName, mode='rb') as file: # b is important -> binary
        fileContent = file.read()

    fee = calculateFee(fileContent)
    if fee is not None:
        print "Makeup: " + str(fee.makeup)
        print "Pyjama: " + str(fee.pyjama)
        print "Hipster: " + str(fee.hipster)
        print "Youngster: " + str(fee.youngster)
        print "badMood: " + str(fee.badMood)
        print "Aggressive: " + str(fee.aggressive)

        photoData = imageParse(pictureFileName)

        #sendStatus("Printing...")
        if is_raspberry_pi and noPrint == False:
            thermal_printer = ThermalPrinter(photoData,384,153)
            thermal_printer.printReceipt(fee.makeup, fee.pyjama, fee.hipster, fee.youngster, fee.badMood, fee.aggressive)

    # ERROR Image not recognised
    else:
        sendSerialMsg('E')

    #sendStatus("Take your bill.")

buttonTracker1 = ButtonTracker(6, buttonPressed)
buttonTracker2 = ButtonTracker(13, buttonPressed)
buttonTracker3 = ButtonTracker(19, buttonPressed)

while True:    
    time.sleep(0.1)

    #if arduinoSerial is not None:
    #    command = arduinoSerial.readline()
    #    print command
