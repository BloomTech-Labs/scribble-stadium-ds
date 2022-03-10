"""
Base code for batch pre-processing
1. Gets file from directory
2. Does some pre-processing on it
3. Puts processed file in new directory
"""
import sys
import queue
import cv2
import os
import glob
from PIL import Image
from processing_pipeline import processing_pipeline 

# Get list of all image paths
def get_all_images(source_dir):

    supported_file_extensions = ["jpg", "jpeg", "png", "tif", "tiff"]
    img_files = []
    for ext in supported_file_extensions:
        img_files += glob.glob(source_dir + f"/**/*.{ext}", recursive=True)
    return img_files

# Change to current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Test image directory; Please choose your source file from the command line, the default directory is below, 
# using the sys module and argv method you can change the file by using the following syntax on the command line:
# python3 filepath directorypath (Ex: .\data_management\autopreprocess_testing\preprocess_directory.py 
# .\data_management\autopreprocess_testing\preprocess_directory.py) REMEMBER TO PUT A SPACE BETWEEN filepath and directorypath
default_directory = '/test_images22622/'
if len(sys.argv) > 1:
    default_directory = sys.argv[1]

source_dir = os.getcwd() + default_directory
# Processed image directory, I also changed the file folder, user needs to change the folder to the one they wish to train images on.
target_dir = os.getcwd() + '/processed_test_images/'
img_files = get_all_images(source_dir)

# Process each image and save in target directory
queue = ["grayscale","remove_lines","remove_noise","adaptive_gaussian_thresholding","erode"]
for file_path in img_files:
    file_name = os.path.basename(file_path)
    img = cv2.imread(file_path)
    img = processing_pipeline(img, queue.copy())
    processed_path = target_dir + file_name
    PILimage = Image.fromarray(img)
    PILimage.save(processed_path, dpi=(300,300))
