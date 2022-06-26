import csv
import sys
import os

from PIL import Image


def main():
    name_of_script = sys.argv[0] # should be setup_ground_truth.py
    kaggle_folder = sys.argv[1].strip()
    with open(f'{kaggle_folder}/written_name_test.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            image_filename = row[0]
            if os.path.exists(f'{kaggle_folder}/{image_filename}'): # allows user to use only sample of images if they want
                ground_truth_text = row[1]
                ground_truth_filename = image_filename.replace("jpg", "gt.txt")
                with open(f'{kaggle_folder}/{ground_truth_filename}', mode='w') as ground_truth_file:
                    ground_truth_file.write(ground_truth_text)
                if "png" not in image_filename:
                    im = Image.open(f'{kaggle_folder}/{image_filename}')
                    im.save(f'{kaggle_folder}/{image_filename.replace("jpg", "png")}', dpi=(300,300))
if __name__ == "__main__":
    main()
