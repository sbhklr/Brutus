import RPi.GPIO as GPIO
import time
from threading import Timer


class ButtonTracker:

    def registerEvents(self):
        GPIO.add_event_detect(self.pushButtonPinA, GPIO.BOTH)
        GPIO.add_event_callback(self.pushButtonPinA, self.onPushButtonChanged)
        GPIO.add_event_detect(self.pushButtonPinB, GPIO.BOTH)
        GPIO.add_event_callback(self.pushButtonPinB, self.onPushButtonChanged)
        GPIO.add_event_detect(self.pushButtonPinC, GPIO.BOTH)
        GPIO.add_event_callback(self.pushButtonPinC, self.onPushButtonChanged)

    def deregisterEvents(self):
        GPIO.remove_event_detect(self.pushButtonPinA)
        GPIO.remove_event_detect(self.pushButtonPinB)
        GPIO.remove_event_detect(self.pushButtonPinC)

    def __init__(self, pushButtonPinA, pushButtonPinB, pushButtonPinC, callback):
        self.pushButtonPinA = pushButtonPinA
        self.pushButtonPinB = pushButtonPinB
        self.pushButtonPinC = pushButtonPinC
        self.callback = callback
            
        GPIO.setup(self.pushButtonPinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)        
        GPIO.setup(self.pushButtonPinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)        
        GPIO.setup(self.pushButtonPinC, GPIO.IN, pull_up_down=GPIO.PUD_UP)        
        self.registerEvents()
            
        self.previousPushButtonValueA = 1
        self.previousPushButtonValueB = 1
        self.previousPushButtonValueC = 1
        self.lastButtonPressed = 0   
        self.buttonPressedThreshold = 1000     

    def processButtonReleased(self,pin):
        timestamp = self.currentMillis()
        if timestamp - self.lastButtonPressed < self.buttonPressedThreshold:            
            return        

        self.lastButtonPressed = timestamp

        valueA = 1 if GPIO.input(self.pushButtonPinA) == 0 or pin == self.pushButtonPinA else 0
        valueB = 1 if GPIO.input(self.pushButtonPinB) == 0 or pin == self.pushButtonPinB else 0
        valueC = 1 if GPIO.input(self.pushButtonPinC) == 0 or pin == self.pushButtonPinC else 0

        buttonPressedValues = [valueA, valueB, valueC]        
        #self.callback(pinValues, self.lastButtonPressed) 
        self.callbackTimer = Timer(0.5, self.callback, (buttonPressedValues, self.lastButtonPressed))
        self.callbackTimer.start()       

    def currentMillis(self):
        return int(round(time.time() * 1000))

    def onPushButtonChanged(self, pin):            
        valueA = GPIO.input(self.pushButtonPinA)
        valueB = GPIO.input(self.pushButtonPinB)
        valueC = GPIO.input(self.pushButtonPinC)  
        
        if (self.previousPushButtonValueA == 0 and valueA == 1):
            self.processButtonReleased(self.pushButtonPinA)

        if (self.previousPushButtonValueB == 0 and valueB == 1):
            self.processButtonReleased(self.pushButtonPinB)

        if (self.previousPushButtonValueC == 0 and valueC == 1):
            self.processButtonReleased(self.pushButtonPinC)
                
        self.previousPushButtonValueA = valueA
        self.previousPushButtonValueB = valueB
        self.previousPushButtonValueC = valueC
        time.sleep(0.05) #slight pause to debounce
    