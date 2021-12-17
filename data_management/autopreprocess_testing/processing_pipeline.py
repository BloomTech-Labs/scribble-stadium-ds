import cv2

def processing_pipeline(img):
    """
    Adds contour to image 
    TESTING PURPOSES ONLY
    """
    newImage = img.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
    dilate = cv2.dilate(thresh, kernel, iterations=5)
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    largestContour = contours[0]
    return cv2.drawContours(newImage, [largestContour], 0, (0,255,0), 3)