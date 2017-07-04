import cv2
import numpy as np

def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    canny = cv2.Canny(gray, 50, 150)
    return canny

def shift(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    sumImg1 = gray - np.vstack((gray[-1:], gray[:-1]))
    sumImg2 = gray - np.hstack((gray[:,-1:], gray[:,:-1]))
    return sumImg1 + sumImg2

def getborderImg(name):
    capture = cv2.VideoCapture(name)
    bFrame = None
    ret, cFrame = capture.read()
    cFrame = np.array(cFrame, dtype=int)
    height, width = cFrame.shape[:2]

    for i in range(0, 1600):
        ret, cFrame = capture.read()

    sumCount, borderImg = 0, np.zeros(cFrame.shape[:2], dtype=float)
    stride, sCount = 23, 0
    for i in range(0, 1600):
        if sCount == stride:
            sCount = 0
        else:
            sCount += 1
            ret, cFrame = capture.read()
            continue

        ret, cFrame = capture.read()
        borderImg += canny(cFrame)
        sumCount += 1

    borderImg /= sumCount
    cv2.imwrite(name.split('.')[0] + '_borderImg.bmp', np.array(borderImg, dtype='uint8'))
    return borderImg

def locate(name):
    borderImg = getborderImg(name)
    height, width = borderImg.shape
    shift = height * 3 / 4
    top, bottom, threshold = rawLocate(borderImg[shift:])
    return top + shift, bottom + shift, threshold

def rawLocate(borderImg, appearWidth=3, disappearWidth=3, thresholdRate=0.5):
    height, _ = borderImg.shape

    ''' count the sum of each row '''
    rowSum = []
    for i in range(height):
        rowSum.append(borderImg[i].sum())

    ''' find the threshold '''
    sortedRowSum = sorted(rowSum)
    background = sum(sortedRowSum[:10]) / 10
    subtitle = sum(sortedRowSum[-10:]) / 10
    threshold = (subtitle - background) * thresholdRate + background

    ''' smooth the rowSum '''
    size = 3
    for i in range(len(rowSum) - size):
        rowSum[i] = sum(rowSum[i:i+size]) / size

    ''' get the row number '''
    # top is the begin index of subtitle, bottom is the end index
    top, bottom = 0, height - 1

    if appearWidth > 3:
        print 1, top, bottom

    idx = len(rowSum) - 1
    # search bottom
    # barWidth is the width of judge bar
    while idx >= appearWidth:
        if rowSum[idx] > threshold:
            flag = True
            # judge a bar, not a single line
            for w in range(1, appearWidth):
                if rowSum[idx - w] < threshold:
                    flag = False
            if flag:
                bottom = idx
                break
        idx -= 1

    if appearWidth > 3:
        print 2, top, bottom

    # search top
    while idx >= disappearWidth:
        if rowSum[idx] < threshold:
            flag = True
            # judge a bar, not a single line
            for w in range(1, disappearWidth):
                if rowSum[idx - w] > threshold:
                    flag = False
            if flag:
                top = idx
                break
        idx -= 1

    if appearWidth > 3:
        print 3, top, bottom

    subTitleWidth = bottom - top
    top -= subTitleWidth / 2
    bottom += subTitleWidth

    if appearWidth > 3:
        print 4, top, bottom

    # cv2.imwrite(name.split('.')[0] + '_subtitle.bmp', np.array(borderImg[top:bottom], dtype='uint8'))
    return top, bottom, threshold

def getSubtitle(img, top, bottom, threshold):
    block = img[top:bottom]
    border = canny(block)
    # rough judge
    if sum(border[border.shape[0]/2]) < threshold/2:
        return None
    left, right, threshold = rawLocate(np.rollaxis(border, 1), 5, 20, 0.4)
    return img[top:bottom, left:right]

if __name__ == '__main__':
    name = 'rwby.mp4'
    capture = cv2.VideoCapture(name)
    # top, bottom, threshold = locate(name)
    top, bottom, threshold = 670, 700, 22398
    print top, bottom, threshold
    for i in range(119, 3000):
        print i
        capture.set(0, i * 1000)
        ret, img = capture.read()
        subtitle = getSubtitle(img, top, bottom, threshold)
        if subtitle is not None:
            cv2.imwrite('subs/' + str(i) + '.jpg', subtitle)