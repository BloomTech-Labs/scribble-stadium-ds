# from unittest import case
# from sklearn import preprocessing
from preprocessing_functions import *

def processing_pipeline(img, queue):
    """
    Takes and image and passes the image through a series of pre-processing steps

    Arguments:
    ___
    A .png or .jpg image

    Returns:
    ___
    A preprocessed image

    """
    newImage = img.copy()
    while len(queue) > 0:
        preprocessing_number = queue.pop(0)
        match preprocessing_number:
            case 0:
                newImage = get_grayscale(newImage)
            case 1:
                newImage = removeLines(newImage)
            case 2:
                newImage = remove_noise(newImage)
            case 3:
                newImage = adaptiveGaussianThresholding(newImage)
            case 4:
                newImage = erode(newImage)

    return newImage



    # img_grayscaled = get_grayscale(newImage)
    # img_delined = removeLines(img_grayscaled)
    # img_denoised = remove_noise(img_delined)
    # image_G_thresh = adaptiveGaussianThresholding(img_denoised, blockSize=5, c=2)
    # img_eroded = erode(image_G_thresh, kernelSize=2)
    # return img_eroded
