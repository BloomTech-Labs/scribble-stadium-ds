import os

import cv2
from PIL import Image


def full_essay_checker(directory, max_height):
    """
    :param directory:
    :param max_height:
    :return: None
    This function will generate and display the files in the directory
    passed in the arguments above by walking the tree and checking
    if any of the .png, .tif, .jpg or .jpeg file in the directory
    is not having too much height which may be the indicator of a full
    child story that should not be publicly accessible due to child's safety.
    """
    # Check if the directory exists
    if os.path.isdir(directory):
        max_height = max_height  # This number can be changed in order to come up with
        # Walk the directory
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Get file paths with specific extensions
                if filename.endswith(".png") or filename.endswith(".tif") \
                        or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    file_to_check = os.path.join(root, filename)

                    # Get image dimensions
                    image = Image.open(file_to_check)
                    width, height = image.size

                    # Check if the image height is more than the max_height
                    # if it is then print file name:height in console and display to the user
                    if height > max_height:
                        print('Potential Full Essay Information (file:height shown) -->', file_to_check, height)
                        # Display the image to the user
                        img = cv2.imread(file_to_check)
                        cv2.imshow('Potential Full Essay Image {Press any key to continue}', img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
    else:
        print('Directory not accessible!')


# Run the function to find the files that do not have a corresponding txt files
full_essay_checker(directory="../data",
                   max_height=200)  # max_height can be changed for any other threshold
