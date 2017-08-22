import RPi.GPIO as GPIO
import time


class ButtonTracker:
    def __init__(self, pushButtonPin, callback):        
        GPIO.setup(pushButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)        
        self.pushButtonPin = pushButtonPin
        self.previousPushButtonValue = 1
        self.lastButtonPressed = 0        
        self.callback = callback
        GPIO.add_event_detect(self.pushButtonPin, GPIO.BOTH)
        GPIO.add_event_callback(self.pushButtonPin, self.onPushButtonChanged)

    def processButtonReleased(self):        
        self.callback(self.pushButtonPin, self.lastButtonPressed)

    def currentMillis(self):
        return int(round(time.time() * 1000))

    def onPushButtonChanged(self, pin):            
        value = GPIO.input(pin)  
        
        if (self.previousPushButtonValue == 0 and value == 1):
            self.processButtonReleased()
        elif (self.previousPushButtonValue == 1 and value == 0):            
            self.lastButtonPressed = self.currentMillis()        
        self.previousPushButtonValue = value
        time.sleep(0.05) #slight pause to debounce
    