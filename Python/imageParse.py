import base64, string
import struct
from PIL import Image # Using Pillow

# logo_width  384 (176)
# logo_height 153

spacing = 0



 #Can be many different formats.
def imageParse(fileName):
    im = Image.open(fileName)
    im = im.resize((36,36), Image.ANTIALIAS)
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
                #print currentBlock
                #print '%03d\n' % int(currentBlock, 2)
                imgStr += '%03d' % int(currentBlock, 2)
                currentBlock = ''
    return imgStr
#int(imgStr, 2)
