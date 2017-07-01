import base64, string
import struct
from PIL import Image # Using Pillow

# logo_width  384 (176)
# logo_height 153

spacing = 105

# Returns 8 Bit Int Array
def imageParse(fileName):
    parsedImageArray = []
    im = Image.open(fileName)
    im = im.resize((176,153), Image.ANTIALIAS)
    pix = im.load()
    print im.size #Get the width and hight of the image for iterating over
    (r,g,b) = pix[1,1]
    imgStr = ''
    currentBlock = '';
    for y in range(0, im.height):
        line = ''
        for x in range(0, im.width + spacing * 2):
            if(x > spacing and x < (im.width + spacing)):
                (r,g,b) = pix[x-spacing,y]
                if((r+b+g)/3 >= 128):
                    currentBlock += '1'
                else:
                    currentBlock += '0'
            else:
                currentBlock += '0'

            if(len(currentBlock)>=8):
                parsedImageArray.append(int(currentBlock, 2))
                currentBlock = ''
    return parsedImageArray
