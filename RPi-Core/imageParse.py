import base64, string
import struct
from PIL import Image # Using Pillow
from PIL import ImageEnhance

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        value = 128 + factor * (c - 128)
        return max(0, min(255, value))
    return img.point(contrast)

max_width = 384
imageWidth = 176
spacing = (max_width - imageWidth) / 2
imageHeight = 153

# Returns 8 Bit Int Array
def imageParse(fileName):
    parsedImageArray = []

    original = Image.open(fileName)    
    resized = original.resize((imageWidth,imageHeight), Image.ANTIALIAS)
    #contrast_image = change_contrast(resized, 175)
    dithered = resized.convert(mode='1')
    #dithered.save("dithered.jpg")    

    im = dithered    
    pix = im.load()
    print im.size #Get the width and hight of the image for iterating over    
    imgStr = ''
    currentBlock = '';
    for y in range(0, im.height):
        line = ''
        for x in range(0, im.width + spacing * 2):
            if(x > spacing and x < (im.width + spacing)):
                #(r,g,b) = pix[x-spacing,y]
                #if((r+b+g)/3 >= 128):
                if(pix[x-spacing,y] >= 128):
                    currentBlock += '0'
                else:
                    currentBlock += '1'
            else:
                currentBlock += '0'

            if(len(currentBlock)>=8):
                parsedImageArray.append(int(currentBlock, 2))
                currentBlock = ''
    return parsedImageArray
