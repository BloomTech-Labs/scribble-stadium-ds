import sys
import jiwer
import pytesseract
from PIL import Image

def test_model(model_name, tessdata_path, test_image_paths, test_image_labels):
    test_extractions = [] #extractions and image list to do aid with post hoc analysis
    image_list = []
    for image_path in test_image_paths:
        extraction = pytesseract.image_to_string(
            Image.open(image_path), 
            lang=model_name,
            config=f'--tessdata-dir "{tessdata_path}"' # set in top level Dockerfile on L72 /train/tessdata
        )
        test_extractions.append(extraction)
        image_object = Image.open(image_path)
        image_list.append(image_object)
    word_error_rate = jiwer.wer(
        test_image_labels, 
        test_extractions, 
    )
    char_error_rate = jiwer.cer(
        test_image_labels, 
        test_extractions, 
    )
    print("word_error_rate, char_error_rate:", word_error_rate, char_error_rate)
    return min(word_error_rate, 1.0), min(1.0, char_error_rate), test_extractions, test_image_labels, image_list # trying to return test extractions for finding insights