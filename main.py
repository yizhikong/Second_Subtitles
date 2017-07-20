# -*- coding: cp936 -*-
import cv2
import numpy as np
import extract
import os
from ocr import *   

RECORD_FILE = 'record.txt'
DOCUMENT_FILE = 'document.txt'

def getExtractMsg(name):
    top, bottom, threshold = None, None, None

    # try to load the 
    if not os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, 'a') as f:
            print 'create record file'

    with open(RECORD_FILE, 'r') as f:
        print 'try loading...'
        lines = f.readlines()
        records = map(lambda x:x.strip().split(' '), lines)
        for record in records:
            print record[0]
            if name == record[0]:
                top, bottom, threshold = int(record[1]), int(record[2]), float(record[3])

    if top is None:
        print 'try to locate the position of subtitles... it needs some time...'
        top, bottom, threshold = extract.locate(name)
        with open(RECORD_FILE, 'a') as f:
            f.write(' '.join([name, str(top), str(bottom), str(threshold), '\n']))

    return top, bottom, threshold

def loadDocument():
    pairs, documents = [], {}
    with open('document.txt') as f:
        pairs = map(lambda x:x.strip().split('\t'), f.readlines())
    for p in pairs:
        documents[p[0].lower()] = p[0] + ': ' + p[1]
    return documents

def msc2Str(msc):
    # 1h = 60*60*1000 = 3600000msc
    # 1m = 60*1000 = 60000msc
    # 1s = 1000msc
    h, m, s, ms = str(msc/3600000), str(msc/60000%60), str(msc/1000%60), str(msc%1000)
    h = '0' + h if len(h) == 1 else h
    m = '0' + m if len(m) == 1 else m
    s = '0' + s if len(s) == 1 else s
    ms = '0' * (3 - len(ms)) + ms
    return '%s:%s:%s,%s' % (h, m, s, ms)

def addSubtitle(srt, idx, msc, content):
    srt += str(idx) + '\n'
    srt += msc2Str(msc) + ' --> ' + msc2Str(msc + 1000) + '\n'
    srt += content + '\n\n'
    return srt, idx + 2


if __name__ == '__main__':
    name = 'rwby.mp4'
    # load or extract the location of subtitles in this vedio
    top, bottom, threshold = getExtractMsg(name)
    print top, bottom, threshold
    # load the global documents
    documents = loadDocument()
    keys = documents.keys()
    ocur = {}
    # initialize the srt content
    srt, idx = '', 1

    capture = cv2.VideoCapture(name)

    for i in range(120, 130):
        t_msc = i * 1000
        capture.set(0, i * 1000)
        ret, img = capture.read()
        subtitle = extract.getSubtitle(img, top, bottom, threshold)
        if subtitle is not None:
            cv2.imwrite('subs/' + str(i) + '.jpg', subtitle)
            text = baiduOcr(subtitle)
            if len(text) > 0:
                text = text.lower()
                for key in keys:
                    try:
                        if key in text and key not in ocur:
                            srt, idx = addSubtitle(srt, idx, t_msc, documents[key])
                            ocur[key] = 1
                            break
                    except:
                        pass

    with open(name.split('.')[0]+'.srt', 'w') as f:
        f.write(srt)

