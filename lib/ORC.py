#import pytesseract
#import requests
#from PIL import Image
#from PIL import ImageFilter
#from StringIO import StringIO
#
#
#def process_image(url):
#    image = _get_image_from_url(url)
#    image.filter(ImageFilter.SHARPEN)
#    return pytesseract.image_to_string(image)
#
#def _get_image(file):
#    try:
#        return Image.open(StringIO(requests.get(file).content))
#    except requests.exceptions.MissingSchema:
#        return Image.open(file)
#    except requests.exceptions.InvalidURL as e:
#        print str(e)


from PIL import Image
import sys

import pyocr
import pyocr.builders

test = "image/real.jpg"


# there are three possible tools
tools = pyocr.get_available_tools()

if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

tool = tools[1]  # The tools are returned in the recommended order of usage
print("Will use tool '%s'" % (tool.get_name()))

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'

txt = tool.image_to_string(
    Image.open(test),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)
word_boxes = tool.image_to_string(
    Image.open(test),
    lang="eng",
    builder=pyocr.builders.WordBoxBuilder()
)
line_and_word_boxes = tool.image_to_string(
    Image.open(test), lang="eng",
    builder=pyocr.builders.LineBoxBuilder()
)

# Digits - Only Tesseract (not 'libtesseract' yet !)
digits = tool.image_to_string(
    Image.open('image/test-digits.png'),
    lang=lang,
    builder=pyocr.tesseract.DigitBuilder()
)

import math
math.sqrt(math.pow(word_boxes[k].position[0][0] - word_boxes[k].position[1][0], 2) + math.pow(word_boxes[k].position[0][0] - word_boxes[k].position[1][1],2))

for i in word_boxes: print i.content + ": " + "{0}".format(i.position)


for i in line_and_word_boxes: print i.content + ": " + "{0}".format(i.position)


