import httplib, urllib, base64, json







fileName = "img2.jpg"
with open(fileName, mode='rb') as file: # b is important -> binary
    fileContent = file.read()


# Return format Makeup;Pyjama;Hipster;Youngsster;BadMood;Aggressive
def getFaceData(imageContent):
    faceInfo = ''

    subscription_key = '9e5fa5720aea424e85a93282173aad81'

    uri_base = 'westcentralus.api.cognitive.microsoft.com'

    # Request headers.
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    })

    # The URL of a JPEG image to analyze.
    body = "{'url':'https://scontent-ams3-1.cdninstagram.com/t51.2885-15/e35/19534308_302035696911316_6605913838757871616_n.jpg'}"

    body = imageContent

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)

        # Makeup;Pyjama;Hipster;Youngsster;BadMood;Aggressive

        # No makeup
        faceAttributes = parsed[0]['faceAttributes']
        if(faceAttributes['gender'] == 'female' and (not faceAttributes['makeup']['eyeMakeup'] or not faceAttributes['makeup']['lipMakeup'])):
            faceInfo += '50;'
        else:
            faceInfo += '0;'

        if any("headwear" in s for s in faceAttributes['accessories']):
            faceInfo += '50;'
        else:
            faceInfo += '0;'

        if(faceAttributes['facialHair']['beard'] > 0.5 and faceAttributes['facialHair']['moustache'] > 0.5):
            faceInfo += '50;'
        else:
            faceInfo += '0;'

        youngsterAge = 24
        if(faceAttributes['age'] < youngsterAge):
            faceInfo += '{0};'.format(round((youngsterAge-faceAttributes['age'])*15))
        else:
            faceInfo += '0;'

        happinessThreshold = 0.5
        if(faceAttributes['emotion']['happiness'] < happinessThreshold):
            faceInfo += '{0};'.format(round(100-faceAttributes['emotion']['happiness']*100))
        else:
            faceInfo += '0;'

        aggressiveThreshold = 0.2
        if(faceAttributes['emotion']['anger'] > aggressiveThreshold or
        faceAttributes['emotion']['contempt'] > aggressiveThreshold or
        faceAttributes['emotion']['disgust'] > aggressiveThreshold or
        faceAttributes['emotion']['fear'] > aggressiveThreshold or
        faceAttributes['emotion']['sadness'] > aggressiveThreshold):
            faceInfo += '50'
        else:
            faceInfo += '0'



        #[0].faceAttributes.makeup.eyeMakeup + '\n'
        #print parsed[0].faceAttributes.makeup.lipMakeup + '\n'

        #print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e, e))
    print faceInfo
    return faceInfo

    ####################################
faceInfo = getFaceData(fileContent)

print 'Makeup;Pyjama;Hipster;Youngsster;BadMood;Aggressive\n'

# This should do it
# TODO 'pip install pyserial'
# If pip is not installed on mac 'sudo easy_install pip'
#
# import serial
# arduinoSerial = serial.Serial('/dev/tty.usbserial', 9600)
# arduinoSerial.write(faceInfo+'\n')
