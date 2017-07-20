# -*- coding: cp936 -*-
import os
from pyocr import pyocr
from PIL import Image
import pytesseract
import urllib, urllib2, base64
import cv2
from aip import AipOcr

APP_ID = '9847639'
API_KEY = 'pdzaE9xIkhi9Gfc8jjq4aQe9'
SECRET_KEY = '1ignfqNkML9USC1qgSXedrLia3HqkYFQ'
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

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

def baiduOcr(img):
    cv2.imwrite('temp.jpg', img)
    img = open('temp.jpg', 'rb').read()

    options = {
      'detect_direction': 'true',
      'language_type': 'CHN_ENG',
    }

    result = aipOcr.basicGeneral(img, options)
    try:
        return result['words_result'][0]['words']
    except:
        return ''

def testBaiduOcr(name):
    img = open(name, 'rb').read()

    options = {
      'detect_direction': 'true',
      'language_type': 'ENG',
    }

    result = aipOcr.basicGeneral(img, options)
    try:
        return result['words_result'][0]['words']
    except:
        return ''