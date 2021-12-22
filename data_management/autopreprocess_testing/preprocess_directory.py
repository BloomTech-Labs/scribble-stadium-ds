"""
Base code for batch pre-processing
1. Gets file from directory
2. Does some pre-processing on it
3. Puts processed file in new directory
"""

import cv2
import os
from PIL import Image
from processing_pipeline import processing_pipeline

# Change to current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Test image directory
source_dir = os.getcwd() + '/test_images'
# Processed image directory
target_dir = os.getcwd() + '/processed_test_images'

# Process all images in directory
# Name format: preprocessing_sample_#.jpg
exists = True
i = 1
while exists:
    img_path = source_dir + "/preprocessing_sample_" + str(i) + ".jpg"
    if os.path.isfile(img_path):
        img = cv2.imread(img_path)
        img = processing_pipeline(img)
        processed_path = target_dir + "/preprocessing_sample_" + str(i) + "_PROCESSED.jpg"
        cv2.imwrite(processed_path, img)
        i += 1
        # Image.fromarray(img).show()
    else:
        exists = False
