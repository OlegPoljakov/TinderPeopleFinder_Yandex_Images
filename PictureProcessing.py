import sys

#sys.path.insert(1, 'pokedex-find-screen-part-1/pyimagesearch')

#from skimage import exposure
import numpy as np
import argparse
import imutils
import cv2
import glob, os


class ImageProcessing:
    def __init__(self):
        """Constructor"""
        pass

    ResizedPictures = []

    @staticmethod
    def printing(images):
        for img in images:
            print(img)

    @staticmethod
    def ResizeImageFunction(images):
        for img in images:
            base_dir = r''
            filename = img
            path = os.path.join(base_dir, filename)
            #print(path)
            image = cv2.imread(path)
            cv2.imshow("ROI", image)
            cv2.waitKey(0)

            image = imutils.resize(image, height=600)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape

            for r in range(height):
                for c in range(width):
                    if gray[r, c] == 0:
                        gray[r, c] = 255

            mask = np.ones(gray.shape[:2], dtype="uint8") * 255

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
            edged = cv2.dilate(gray, kernel)

            ret, edged = cv2.threshold(edged, 240, 255, cv2.THRESH_TOZERO)
            ret, edged = cv2.threshold(edged, 0, 255, cv2.THRESH_BINARY_INV)

            edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
            edged = cv2.morphologyEx(edged, cv2.MORPH_OPEN, kernel)

            cnts, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
            # screenCnt = None

            largestCont = cnts[0]
            cv2.drawContours(mask, [largestCont], -1, 0, -1)

            x, y, w, h = cv2.boundingRect(largestCont)
            roi = image[y:y + h, x:x + w]
            ImageProcessing.ResizedPictures.append(roi)
            # cv2.imshow("ROI", roi)
            # cv2.waitKey(0)
        return ImageProcessing.ResizedPictures





