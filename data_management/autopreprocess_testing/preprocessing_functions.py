import cv2
import numpy as np


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image, kernelSize=5):
    return cv2.medianBlur(image, kernelSize)


# thresholding
# set's each pixel to zero if it is below a certain threshold otherwise sets it to 255
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def adaptiveThresholding(image, blockSize=11, c=2):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, c)


def adaptiveGaussianThresholding(image, blockSize=11, c=2):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, c)


# dilation
def dilate(image, kernelSize=3):
    kernel = np.ones((kernelSize, kernelSize), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image, kernelSize=3):
    kernel = np.ones((kernelSize, kernelSize), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# Deskewing steps (courtesy of Carl)

def getSkewAngle(cvImage) -> float:
    """
    Calculate skew angle of an image.
    Input: image
    Output: angle
    """

    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Dilate pixels to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 10))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    minAreaRect = cv2.minAreaRect(largestContour)

    # Uncomment next 2 lines to display largest contour used to determine skew angle
    # cv2.drawContours(newImage, [largestContour], 0, (0,255,0), 3)
    # Image.fromarray(newImage).show()

    # Determine the angle.
    angle = minAreaRect[-1]
    if angle > 45:
        angle = angle - 90
    return angle

def rotateImage(cvImage, angle: float):
    """
    Rotates image
    Input: image, angle to rotate
    Output: rotated image
    """

    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image using the above functions
def deskew(cvImage):
    """
    Straightens (de-skews) an image
    Input: image
    Output: straigntened image
    """

    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, angle)