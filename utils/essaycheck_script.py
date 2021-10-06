from pathlib import Path
import os

"""
This is a script that scans the repo for full essay images. Place this script in the top-level directory and run it from the command line. 
The results will show how many png, jpg, and tif files are in the repo, and it will show how many files are likely to be images of full essays.
This script does not remove those files.
The user would need to evaluate those files and remove any full essays that might have been inadvertently uploaded. 
"""

def file_size(path):
    """
    this function returns the file size in bytes
    """
    if os.path.isfile(path):
        file_info = os.stat(path)
        return (file_info.st_size)

imageFileCount = []
likely_snippet = 0
possibly_full_essay = 0
pngCounter = 0
jpgCounter = 0
tifCounter = 0
total_files = 0

for path in Path('.').rglob('*.png'):
    pngCounter += 1
    total_files += 1
    size_of_file = (file_size(path))
    imageFileCount.append(size_of_file)

for path in Path('.').rglob('*.jpg'):
    jpgCounter += 1
    total_files += 1
    size_of_file = (file_size(path))
    imageFileCount.append(size_of_file)

for path in Path('.').rglob('*.tif'):
    tifCounter += 1
    total_files += 1
    size_of_file = (file_size(path))
    imageFileCount.append(size_of_file)

"""
The following code checks to see what files are likely to be full essay images vs. snippets.
I set the cutoff to 260000 bytes because the smallest full essay image was 410 KB(410000 bytes), and
the largest image snippet after data cleaning approached 180KB (180000 bytes) 
I wanted to allow room for error. In the future, this threshold will probably need to be adjusted depending on
what is done during the data cleaning step. For example, clipped images from the original essay tend to be smaller than
clipped images that have additional color changes applied during the data cleaning process.

"""
for file in imageFileCount:
    if size_of_file <= 260000:
       likely_snippet += 1
    else:
        possibly_full_essay+= 1

print(f'There are a total of {pngCounter} files ending in .png')
print(f'There are a total of {jpgCounter} files ending in .jpg')
print(f'There are a total of {tifCounter} files ending in .tif')
print(f'There are a total of {total_files} image files')
print(f'The number of files that are likely snippets: {likely_snippet}')
print(f'The total number of files that are possibly full essays: {possibly_full_essay}')
