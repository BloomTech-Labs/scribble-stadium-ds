import pytesseract
import jiwer

from PIL import Image
from os import listdir
from os.path import join, isfile

TEST_PATH = '/train/tesstrain/data/storysquad-ground-truth' 
extractions = []
ground_truths = []
count = 0

for file_name in listdir(TEST_PATH):
    file_path = join(TEST_PATH, file_name)
    if count < 100 and file_path.endswith(".png") and isfile(file_path):
        extraction = pytesseract.image_to_string(
            Image.open(file_path), 
            lang='kaggle',
            config='--tessdata-dir "/train/tessdata"' # set in top level Dockerfile on L72
        )
        ground_truth = None
        ground_truth_path = file_path.replace(".png", ".gt.txt")
        if isfile(ground_truth_path):
            with open(ground_truth_path, mode='r') as f:
                ground_truth = f.read()
            extractions.append(extraction)
            ground_truths.append(ground_truth)
            count += 1
    else:
        continue


word_error_rate = jiwer.wer(
    ground_truths, 
    extractions, 
)
print(f"Model had word error rate of {100 * word_error_rate}%")

char_error_rate = jiwer.cer(
    ground_truths, 
    extractions, 
)

print(f"Model had char error rate of {100 *char_error_rate}%")

