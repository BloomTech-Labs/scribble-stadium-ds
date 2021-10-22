 # import the necessary packages
from difflib import SequenceMatcher as SQ
import pytesseract
import argparse
import cv2

full_image = 'full_sample2.png'

image = cv2.imread(full_image)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
default = pytesseract.image_to_string(image)
custom = pytesseract.image_to_string(image, lang='storysquad')

print(default)
print(custom)

## compare accuracy of defualt model and fine -tuned model  

# read text from the ground-truth file
with open('../../Users/sylvi/Downloads/full_text.txt', "r") as f:
    target = f.read()

# calculate the accuracy of the model with respect to the ratio of
# sequences matched in between the predicted and ground-truth labels
def model_accuracy(model_name, target, type):
    accuracyScore = SQ(None, target, model_name).ratio() * 100
    accuracyScore = round(accuracyScore, 2)
    print("[INFO] accuracy of {} model: {}%...".format(type, accuracyScore))
    
    
model_accuracy(default, target, 'default')
model_accuracy(custom, target, 'custom')
