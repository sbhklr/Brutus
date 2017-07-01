#!/usr/bin/python

import serial
from thermal_printer import ThermalPrinter
from facesApi import calculateFee
from imageParse import imageParse
import os

is_raspberry_pi = os.uname()[1] == "raspberrypi"

arduinoSerial = None #serial.Serial('/dev/cu.usbmodem144211', 115200)
if arduinoSerial is not None:
    command = arduinoSerial.readline() # wait till arduino is ready

pictureFileName = "photo.jpg"

if is_raspberry_pi:
    import picamera
    camera = picamera.PiCamera()
    camera.capture(pictureFileName)
    #camera.hflip = True
    #camera.vflip = True

with open(pictureFileName, mode='rb') as file: # b is important -> binary
    fileContent = file.read()

def buttonPressed():
    # sendStatus("Analysing face...")
    fee = calculateFee(fileContent)    
    photoData = imageParse(pictureFileName)

    #sendStatus("Printing...")        
    if is_raspberry_pi:
        thermal_printer = ThermalPrinter(photoData,384,153)            
        thermal_printer.printReceipt(fee.makeup, fee.pyjama, fee.hipster, fee.youngster, fee.badMood, fee.aggressive)

    #sendStatus("Take your bill.")    

buttonPressed()

if arduinoSerial is not None:
    while True:
        command = arduinoSerial.readline()
        print command
