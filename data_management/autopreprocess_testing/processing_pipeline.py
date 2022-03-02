# from unittest import case
# from sklearn import preprocessing
from preprocessing_functions import *

PREPROCESSING_STEPS = {
    "grayscale": get_grayscale,
    "remove_lines": removeLines,
    "remove_noise": remove_noise,
    "adaptive_gaussian_thresholding": adaptiveGaussianThresholding,
    "erode": erode
}


def processing_pipeline(img, queue=None): # Default parameter list will be treated as global
    """
    Takes and image and passes the image through a series of pre-processing steps

    Arguments:
    ___
    A .png or .jpg image

    Returns:
    ___
    A preprocessed image
    
    """
    new_image = img.copy()
    if queue is None:
        queue = [0,1,2,3,4]
    # queue = queue or [0,1,2,3,4] None value is not changed Or means first list if None
    while len(queue) > 0:
        preprocessing_number = queue.pop(0)

        # Corresponds to preprocessing function
        prepocessing_function = PREPROCESSING_STEPS.get(preprocessing_number)
        new_image = prepocessing_function(new_image)

    return new_image
    