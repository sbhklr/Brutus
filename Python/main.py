import serial
import facesApi
import time

from facesApi import getFaceData

arduinoSerial = serial.Serial('/dev/cu.usbmodem144211', 9600)
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

    arduinoSerial.write(faceInfo + ';');


    # arduinoSerial.write(';')
    # arduinoSerial.write('\n')

    #time.sleep(5)
    #sendStatus("Take your bill.")
    print 'sent\n'

buttonPressed()

while True:
    command = arduinoSerial.readline()
    print command
