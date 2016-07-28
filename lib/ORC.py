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



