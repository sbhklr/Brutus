import serial
import facesApi
import time

from facesApi import getFaceData
from imageParse import imageParse

arduinoSerial = serial.Serial('/dev/cu.usbmodem144211', 115200)
command = arduinoSerial.readline() # wait till arduino is ready

fileName = "img2.jpg"
with open(fileName, mode='rb') as file: # b is important -> binary
    fileContent = file.read()

def buttonPressed():
    # sendStatus("Analysing face...")
    faceInfo = getFaceData(fileContent)
    # faceInfo = "000050009500"

    #sendStatus("Printing...")
    #print faceInfo
    print 'Makeup;Pyjama;Hipster;Youngsster;BadMood;Aggressive\n'

    # faceInfoData = (faceInfo + ';\n').encode()
    #arduinoSerial.write((faceInfo + ';\n').encode())
    #arduinoSerial.write(bytes(faceInfo + ';\n'))
    # bytes(faceInfo + ';\n')
    arduinoSerial.write('E')
    arduinoSerial.write('F' + faceInfo)
    print faceInfo
    photoData = imageParse(fileName)
    print photoData

    time.sleep(0.5)
    arduinoSerial.write('E')
    time.sleep(0.5)
    arduinoSerial.write('DE')
    time.sleep(0.5)
    #arduinoSerial.write('I' + photoData + ';');

    # arduinoSerial.write('PE')

    # arduinoSerial.write('\n')

    #time.sleep(5)
    #sendStatus("Take your bill.")
    print 'sent\n'

print "button pressed"
buttonPressed()

print "button pressed end"
while True:
    command = arduinoSerial.readline()
    print command
