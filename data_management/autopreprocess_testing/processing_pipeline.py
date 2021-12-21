from auto_preprocess import *

def processing_pipeline(img):
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
    img_grayscaled = get_grayscale(newImage)
    img_denoised = remove_noise(img_grayscaled)
    image_G_thresh = adaptiveGaussianThresholding(get_grayscale(img_denoised), blockSize=5, c=2)
    img_eroded = erode(image_G_thresh, kernelSize=2)
    return img_eroded