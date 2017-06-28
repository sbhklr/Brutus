import base64, string
import struct
from PIL import Image
im = Image.open("img1.jpg") #Can be many different formats.
im = im.resize((175,175), Image.ANTIALIAS)
pix = im.load()
print im.size #Get the width and hight of the image for iterating over
(r,g,b) = pix[1,1]
imgStr = ''
print 'binary:'
for y in range(0, im.width):
    line = ''
    for x in range(0, im.width):
        (r,g,b) = pix[x,y]
        if((r+b+g)/3 >= 128):
            line += '1'
        else:
            line += '0'
    imgStr += line
    print line
        # print '{0}-{1}'.format(x, y)

print 'decimal:'
imgInt = int(imgStr, 2)
print imgInt
print 'hex:'
print hex(int(imgStr, 2))
print 'base64:'
print base64.b64encode(bytes(imgInt))

# Manual Base64 
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + \
           string.digits #+ '-_'
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)
SIGN_CHARACTER = '$'

def num_encode(n):
    if n < 0:
        return SIGN_CHARACTER + num_encode(-n)
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0: break
    return ''.join(reversed(s))
print 'base{0}(special):'.format(BASE)
print num_encode(imgInt)
