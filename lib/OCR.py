import csv
import glob
import pyocr
import pyocr.builders
import sys
from PIL import Image, ImageFilter, ImageEnhance

from numpy import *

class OCR(object):
    def __init__(self):
        # there are three possible tools
        self.tools = pyocr.get_available_tools()
        self.maxsize = 1028
        #self.size = 
        if len(self.tools) == 0:
            print("No OCR tools found")
            sys.exit(1)
        else:
            tool_names = [tool.get_name() for tool in self.tools]
            try: 
                index = tool_names.index('Tesseract (sh)')
                self.tool = self.tools[index]
                print("Will use tool '%s'" % (tool.get_name()))
            except:
                print "exception happened"
                sys.exit(1)
        self.langs = tool.get_available_languages()
    def get_image(self, file):
        img = Image.open(file)
        #img.thumbnail(self.maxsize, Image.NEAREST)
        return img

    def image_preprocess(self, img):
        # rotate
        if img.size[0] < img.size[1]:
            img = img.rotate(90,  expand=1)
        # resize
        self.width, self.height = img.size
        ratio = float(self.maxsize)/self.width
        new_size = (int(ratio * self.width), int(ratio * self.height))
        img = img.resize(new_size, Image.ANTIALIAS)
        img = img.filter(ImageFilter.SHARPEN)
        img = img.convert("L")
        return img

    def pre_process2(self, img):
        image = ImageEnhance.Contrast(img)
        im = array(img)
        im = (100.0/255) * im + 100
        img = Image.fromarray(im)
        return img

    def image_process(self, img, builder):
        text = self.tool.image_to_string(img, lang="eng", builder=builder)
        return text

    #def _get_email(self):
    #def _get_first_name(self):
    #def _get_last_name(self):
    #def _get_tel(self):
    #def _get_fax(self):
    #def _get_mobile(self):

def write_to_file(tmpfile,txt,mode = "wb"):
    with open(tmpfile, mode) as f:
        #writer = csv.writer(f, delimiter='=')
        for i in txt:
            f.write("{0}: {1}\n".format(i.content.encode('utf-8'), i.position))
            #writer.writerow([repr(i.content), i.position])
        f.write("\n")

if __name__ == "__main__":
    ocr = OCR()
    #files = glob.glob('/home/eijmmmp/BCReader/image/*')
    files = ['/home/eijmmmp/BCReader/image/real.jpg', '/home/eijmmmp/BCReader/image/real03.jpg', '/home/eijmmmp/BCReader/image/real11.jpg']
    #files = ['/home/eijmmmp/BCReader/image/real03.jpg','/home/eijmmmp/BCReader/image/real03_pro.jpg']
    for f in files:
        print f + '\n'
        img = ocr.get_image(f)
        wordbox = ocr.image_process(img, builder=pyocr.builders.LineBoxBuilder())
        write_to_file(f + ".txt", wordbox)

        img0 = ocr.image_preprocess(img)
        wordbox = ocr.image_process(img0, builder=pyocr.builders.LineBoxBuilder())
        write_to_file(f + ".txt", wordbox, mode='ab')
        img0.save(f + "preprocessed_0_.jpg")

        img2 = ocr.pre_process2(img0)
        wordbox = ocr.image_process(img2, builder=pyocr.builders.LineBoxBuilder())
        write_to_file(f + ".txt", wordbox, mode='ab')
        img2.convert('RGB').save(f + "preprocessed_2_.jpg")


## Digits - Only Tesseract (not 'libtesseract' yet !)
#digits = tool.image_to_string(
#    Image.open('image/test-digits.png'),
#    lang=lang,
#    builder=pyocr.tesseract.DigitBuilder()
#)

#import math
#k=1
#math.sqrt(math.pow(word_boxes[k].position[0][0] - word_boxes[k].position[1][0], 2) + math.pow(word_boxes[k].position[0][0] - word_boxes[k].position[1][1],2))
#
#for i in word_boxes: print i.content + ": " + "{0}".format(i.position)
#
#
#for i in line_and_word_boxes: print i.content + ": " + "{0}".format(i.position)
#
#from PIL import ImageFilter
#from StringIO import StringIO
#
#
#def process_image(url):
#    image = _get_image(url)
#    image.filter(ImageFilter.SHARPEN)
#    return pytesseract.image_to_string(image)
#
#
#def _get_image(url):
#    return Image.open(StringIO(requests.get(url).content))

