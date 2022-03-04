"""
Base code for batch pre-processing
1. Gets file from directory
2. Does some pre-processing on it
3. Puts processed file in new directory
"""

import cv2
import os
import glob
from PIL import Image
from processing_pipeline import processing_pipeline

# Change to current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Test image directory
source_dir = os.getcwd() + '/test_images'
# Processed image directory
target_dir = os.getcwd() + '/processed_test_images/'

# Get list of all image paths
supported_file_extensions = ["jpg", "jpeg", "png", "tif", "tiff"]
img_files = []
for ext in supported_file_extensions:
    img_files += glob.glob(source_dir + f"/**/*.{ext}", recursive=True)

# Process each image and save in target directory
for file_path in img_files:
    file_name = os.path.basename(file_path)
    img = cv2.imread(file_path)
    img = processing_pipeline(img)
    processed_path = target_dir + file_name
    PILimage = Image.fromarray(img)
    PILimage.save(processed_path, dpi=(300,300))
