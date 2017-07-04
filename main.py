import cv2
import numpy as np
import extract

if __name__ == '__main__':
    name = 'rwby.mp4'
    capture = cv2.VideoCapture(name)
    top, bottom, threshold = extract.locate(name)
    print top, bottom, threshold
    for i in range(120, 3000):
        capture.set(0, i * 1000)
        ret, img = capture.read()
        subtitle = extract.getSubtitle(img, top, bottom, threshold)
        if subtitle is not None:
            cv2.imwrite('subs/' + str(i) + '.jpg', subtitle)

            