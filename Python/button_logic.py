pushButtonPin = 8
previousPushButtonValue = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(pushButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pushButtonPin, GPIO.BOTH)
GPIO.add_event_callback(pushButtonPin, onPushButtonChanged)

def onPushButtonChanged(pin):    
    global previousPushButtonValue  
    global lastButtonPressed  
    value = GPIO.input(pushButtonPin)    

    if (previousPushButtonValue == 0 and value == 1):
        print("Button pressed")
        lastButtonPressed = currentMillis()        
    elif (previousPushButtonValue == 1 and value == 0):        
        processButtonReleased()
    previousPushButtonValue = value
    time.sleep(0.05) #slight pause to debounce