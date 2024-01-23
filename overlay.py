import cv2 as cv
import numpy as np


def genesis(img):
    # stream=cv.videoCapture(port)
    while True:
        # ret, frame = stream.read()
        #
        # if frame == None:
        #     print("No frame received (stream canceled?). Ending Process")
        #
        # operate=frame.copy()
        frame = cv.imread(img, cv.COLOR_BGR2RGB)

        grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        grayFrame = cv.GaussianBlur(grayFrame, (15, 15), 0)

        darkMask = cv.inRange(grayFrame, 50, 100)

        maskFrame = cv.bitwise_and(grayFrame, darkMask)
        maskFrame = cv.Canny(maskFrame, 80, 150)

        h, w = maskFrame.shape

        mask = np.zeros_like(grayFrame)

        trapMask = np.array([[(0, h), (0, 75), (w, 75), (w, h)]])

        mask = cv.fillPoly(mask, trapMask, 255)

        mask = cv.bitwise_and(maskFrame, mask)

        lineys = cv.HoughLinesP(mask, 1, np.pi / 180, 50, maxLineGap=150)
        xv = []
        yv = []
        xv2 = []
        yv2 = []

        if lineys is None:
            print("Hough Line Transform Failed! Ending Process")
            break
        else:
            for line in lineys:
                print(line)
                print(line[0])
                x1, y1, x2, y2 = line[0]
                rise = y1 - y2
                run = x1 - x2

                if run != 0:
                    print(rise / run)
                    slope = rise / run

                else:
                    slope = 999999999

                if -0.1 < slope < 0.1:
                    continue

                if slope > 0:
                    xv.append(x1)
                    xv.append(x2)
                    yv.append(y1)
                    yv.append(y2)

                elif slope < 0:
                    xv2.append(x1)
                    xv2.append(x2)
                    yv2.append(y1)
                    yv2.append(y2)

                else:
                    print("Vertical line found, divByZero avoided.")

        rightTop = (int(min(xv)), int(min(yv)))
        print(rightTop)
        rightBottom = (int(max(xv)), int(max(yv)))
        print(rightBottom)
        leftTop = (int(min(xv2)), int(min(yv2)))
        print(leftTop)
        leftBottom = (int(max(xv2)), int(max(yv2)))
        print(leftBottom)

        cv.line(frame, leftBottom, leftTop, (0, 0, 255), 20)
        cv.line(frame, rightBottom, rightTop, (0, 0, 255), 20)

        leftSlope = (leftTop[1] - leftBottom[1]) / (leftTop[0] - leftBottom[0])
        rightSlope = (rightTop[1] - rightBottom[1]) / (rightTop[0] - rightBottom[0])

        if rightTop[1] < leftTop[1]:
            yTop = rightTop[1]
            meanX = (rightTop[0] + ((rightTop[1] - leftBottom[1]) / rightSlope) + rightBottom[0]) / 2

        else:
            yTop = rightTop[1]
            meanX = (rightTop[0] + ((rightTop[1] - leftBottom[1]) / leftSlope) + leftBottom[0]) / 2

        if rightBottom[1] < leftBottom[1]:
            yBottom = leftBottom[1]
            meanX2 = (rightBottom[0] + leftTop[0] - (rightTop[1] - leftBottom[1]) / rightSlope) / 2

        slope2 = (yTop - leftBottom[1]) / (meanX - (rightBottom[0] + leftTop[0] - (rightTop[1] - leftBottom[1]) / rightSlope) / 2)
        slopeFinder = (h - leftBottom[1]) / slope2 + (rightBottom[0] + leftTop[0] - (rightTop[1] - leftBottom[1]) / rightSlope) / 2

        cv.line(frame, (int(meanX), int(yTop)), (int(slopeFinder), int(h)),(255,0,55),20)

        cv.imshow("frame", frame)
        cv.waitKey(0)
