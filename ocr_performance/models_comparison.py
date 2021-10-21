'''
This python scripts tries to bring in the various comparison metrics in a single run. i.e.
from the tesseract base model {eng.trainedata}, custom model {storysquad.traineddata},
the custom model trained with new data {storysquadwnewdata.traineddata} and the google
vision model. All the different models are picked from models directory of the repo
(scribble-stadium-ds/models). Additionally this script provides the transcriptions
from various models in respective directories under scribble-stadium-ds/ocr_performance/data
'''

import os
from argparse import ArgumentParser
from asyncio import get_event_loop
from difflib import SequenceMatcher as SQ
from os import listdir, makedirs
from os.path import dirname

import cv2
import pytesseract

from app.utils.img_processing.google_api import GoogleAPI, NoTextFoundException
from app.utils.img_processing.tesseract_api import TesseractAPI

# global variables and services
DIR = dirname(__file__)
DATA_DIR = DIR + '/data/'
PHOTOS_DIR = DATA_DIR + 'photos/'
TRANSCRIPTS_DIR = DATA_DIR + 'transcripts/'
METADATA_DIR = DATA_DIR + 'metadata/'

GOOGLE = 'google'
TESS = 'tess'

os.environ["TESSDATA_PREFIX"] = '../models/'

gt_directory = 'data/gt_storysquad_transcripts/'
GV_directory = 'data/google_transcripts/'

directory = 'data/photos/'
# get the files in the directory to iterate through
filenames = []


def model_accuracy(filename, gt, GoogleVisionDocument):
    """
    This function gets the accuracy scores from GoogleVision transcription only.
    :param filename: Image file name ex. "Photo 3121.png"
    :param gt: Ground truth file. This text file must be exact match of the image name with NO extension
    ex. "Photo 3121"
    :param GoogleVisionDocument:
    :return: None
    """
    # TODO: Remove this function and use only one function for Accuracy Score all across.
    accuracyScore = SQ(None, gt, GoogleVisionDocument).ratio() * 100
    accuracyScore = round(accuracyScore, 2)
    print(f"[ACCURACY_SCORE] Accuracy of document {filename} GoogleVision vs GroundTruth is : {accuracyScore}%")


def trancribe_w_tesseract(directory, filenames):
    """
    This function takes in the directory and the filesnames and provide the transcriptions from various tesseract
    models
    :param directory: directory from where the images are populated
    :param filenames: filenames
    :return: None
    """
    for file in filenames:
        full_image = directory + file
        print('Opening file :', full_image)
        image = cv2.imread(full_image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        default = pytesseract.image_to_string(image)
        custom = pytesseract.image_to_string(image, lang='storysquad')
        customnewdata = pytesseract.image_to_string(image, lang='storysquadwnewdata')

        print('----- Default output below ----- \n', default)
        print('----- Custom output ----- \n', custom)
        print('----- Custom with new data output ----- \n', customnewdata)

        # Uncomment the row below if you want to stop to review the outputs
        # input("Please see outputs above and Press Enter to continue when ready to progress further... \n")

        # Transcribe model outputs to a local directory
        trans_dir = DATA_DIR + 'default_storysquad_transcripts/'
        makedirs(trans_dir, exist_ok=True)

        with open(trans_dir + file.split('.')[0:-1][0], 'w') as f:
            f.write(default)

        trans_dir = DATA_DIR + 'custom_storysquad_transcripts/'
        makedirs(trans_dir, exist_ok=True)
        with open(trans_dir + file.split('.')[0:-1][0], 'w') as f:
            f.write(custom)

        trans_dir = DATA_DIR + 'custom_new_data_storysquad_transcripts/'
        makedirs(trans_dir, exist_ok=True)
        with open(trans_dir + file.split('.')[0:-1][0], 'w') as f:
            f.write(customnewdata)

        # compare accuracy of default model and fine-tuned model
        txt_filename = gt_directory + file.split('.')[0:-1][0]
        print('Opening Ground Truth Text file :', txt_filename)

        # Uncomment the row below if you want to stop to review the outputs
        # input("Please see outputs above and Press Enter to continue when ready to progress further...")
        with open(txt_filename, "r") as f:
            target = f.read()

        # calculate the accuracy of the model with respect to the ratio of
        # sequences matched in between the predicted and ground-truth labels
        def model_accuracy_local(model_name, target, type):
            accuracyScore = SQ(None, target, model_name).ratio() * 100
            accuracyScore = round(accuracyScore, 2)
            print("[ACCURACY_SCORE] Accuracy of Tesseract {} model: {}%...".format(type, accuracyScore))

        model_accuracy_local(default, target, 'default')
        model_accuracy_local(custom, target, 'custom')
        model_accuracy_local(customnewdata, target, 'customnewdata')

        gt_transcription_file = gt_directory + file.split(".")[0:-1][0]
        gv_transcription_file = GV_directory + file.split(".")[0:-1][0]
        print(
            f'[INFO] Comparing files GroundTruth:{gt_transcription_file} vs GoogleVision:{gv_transcription_file}')
        gt_transcription = gt_directory + file.split(".")[0:-1][0]
        gv_transcription = GV_directory + file.split(".")[0:-1][0]
        model_accuracy(file, gt_transcription, gv_transcription)


async def transcribe(page_image_file, ocr, trans_dir):
    '''
    page_image_file :: fully qualified image path
    ocr             :: the transcription object which
                       provides a transcribe()
                       method
    trans_dir       :: Path where generated
                       transcriptions are to be
                       placed,
    '''
    # Extract the file name without the '.jpg' suffix
    file_name = page_image_file.split('/')[-1].split('.')[0]

    trans_file_name = trans_dir + file_name

    # Read data from the image file into page_image
    with open(page_image_file, mode='rb') as pifd:
        page_image = pifd.read()

    low_confidence = None
    flagged = None
    trans_text = 'No Text Found'
    try:
        low_confidence, flagged, trans_text = \
            await ocr.transcribe(page_image)

    except NoTextFoundException:
        print('No Text Found')

    with open(trans_file_name, 'w') as transfd:
        transfd.write(trans_text)


async def transcribe_all(engine, trans_dir):
    '''
    Scans through the image files in PHOTOS_DIR and invokes the
    transcribe() function on each
    '''
    image_files = [x for x in listdir(PHOTOS_DIR) if x.endswith('.jpg') or x.endswith('.png') or x.endswith('.tif')]
    image_files.sort()

    for idx, image_file in enumerate(image_files):
        print(f'Processing image<{idx}:{image_file}>')
        await transcribe(PHOTOS_DIR + image_file, ocr=engine, trans_dir=trans_dir)
        print('Model Accuracy Metrics \n')
        image_file = image_file.split('.')[0]
        with open(gt_directory + image_file, "r") as f:
            gt_file = f.read()
        with open(GV_directory + image_file, "r") as f:
            gv_file = f.read()
        print('[INFO] GroundTruth version is \n', gt_file)
        print('[INFO] GoogleVision Transcribed version is \n', gv_file)
        # Uncomment the row below if you want to stop to review the outputs
        # input("Please see outputs above and Press Enter to continue when ready to progress further...")


if __name__ == '__main__':

    # Crawl through the directory and populate files
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".png") or filename.endswith(".tif") or filename.endswith(".jpg"):
                filenames.append(filename)
    print('[INFO] Files found--> \n', filenames)

    # Google Vision Transcription Code
    parser = ArgumentParser()
    parser.add_argument('-e', '--engine', choices=[GOOGLE, TESS],
                        default=GOOGLE,
                        help='Specify transcribe engine')
    parser.add_argument('-l', '--language', choices=['ssq', 'storysquad'],
                        default='storysquad',
                        help='Specify language for Tesseract engine')

    args = parser.parse_args()

    trans_dir = DATA_DIR + args.engine
    if args.engine == GOOGLE:
        engine = GoogleAPI()
    else:
        engine = TesseractAPI(args.language)
        trans_dir += f'_{args.language}'
    trans_dir += '_transcripts/'

    print("Transcript dir:", trans_dir)
    print("Engine: ", engine)

    makedirs(trans_dir, exist_ok=True)

    loop = get_event_loop()
    loop.run_until_complete(transcribe_all(engine, trans_dir))

    # Code for tesseract transcription
    trancribe_w_tesseract(directory, filenames)
