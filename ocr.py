# -*- coding: cp936 -*-
import os
from pyocr import pyocr
from PIL import Image
import pytesseract

tools = pyocr.get_available_tools()[:]

def pyocrOcr(img):
    try:
        return tools[0].image_to_string(Image.fromarray(img), lang='eng')
    except:
        return ''

def pytesseractOcr(img):
    try:
        return pytesseract.image_to_string(Image.fromarray(img), lang='eng')
    except:
        return ''
