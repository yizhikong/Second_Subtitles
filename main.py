# -*- coding: cp936 -*-
import cv2
import numpy as np
import extract
import os
from ocr import *   

RECORD_FILE = 'record.txt'

if __name__ == '__main__':
    name = 'rwby.mp4'
    capture = cv2.VideoCapture(name)

    top, bottom, threshold = None, None, None

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

    print top, bottom, threshold

    for i in range(120, 3000):
        capture.set(0, i * 1000)
        ret, img = capture.read()
        subtitle = extract.getSubtitle(img, top, bottom, threshold)
        if subtitle is not None:
            cv2.imwrite('subs/' + str(i) + '.jpg', subtitle)
            text = pyocrOcr(subtitle)
            if len(text) > 0:
                print text

            