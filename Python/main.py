#!/usr/bin/python

import serial
import facesApi
import time
from thermal_printer import ThermalPrinter
from facesApi import calculateFee
from imageParse import imageParse

arduinoSerial = None #serial.Serial('/dev/cu.usbmodem144211', 115200)
if arduinoSerial is not None:
    command = arduinoSerial.readline() # wait till arduino is ready

fileName = "img2.jpg"

with open(fileName, mode='rb') as file: # b is important -> binary
    fileContent = file.read()

def buttonPressed():
    # sendStatus("Analysing face...")
    fee = calculateFee(fileContent)    
    photoData = imageParse(fileName)

    #sendStatus("Printing...")        
    #thermal_printer = ThermalPrinter(photoData,384,153)
    thermal_printer = ThermalPrinter()
    thermal_printer.printReceipt(fee.makeup, fee.pyjama, fee.hipster, fee.youngster, fee.badMood, fee.aggressive)

    #sendStatus("Take your bill.")    

buttonPressed()

if arduinoSerial is not None:
    while True:
        command = arduinoSerial.readline()
        print command
