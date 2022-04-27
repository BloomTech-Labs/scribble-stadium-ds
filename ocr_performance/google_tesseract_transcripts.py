"""
google_vision_transcripts.py - Generates transcript and metadata files using
Google Vision API.

Usage : python -m ocr_performance.google_vision_transcripts from repo root

The image files are expected in <repo root>/data/photos

The Google vision transcripts are stored in <repo root>/data/google_transcripts
and the metadata in <repo root>/data/metadata.
Each metadata file contains 2 boolean values `low_confidence` and `flagged`:

low_confidence :: This is derived from data returned by GoogleVision and a
value of True implies that the associated transcription is not good.

flagged :: This is derived by checking if the transcriptions contain
words from the list in .../app/utils/moderation/bad_single.csv in the
scribble-stadium-ds repository - a True value implies that one or more words
from the list exist in the transcription.
"""

from os import listdir, makedirs
from os.path import dirname
from asyncio import get_event_loop
from argparse import ArgumentParser

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


async def transcribe(page_image_file, ocr, trans_dir):
    """
    page_image_file :: fully qualified image path
    ocr             :: the transcription object which
                       provides a transcribe()
                       method
    trans_dir       :: Path where generated
                       transcriptions are to be
                       placed
    """
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
    """
    Scans through the image files in PHOTOS_DIR and invokes the
    transcribe() function on each
    """
    image_files = [x for x in listdir(PHOTOS_DIR) if x.endswith('.jpg')]
    image_files.sort()

    for idx, image_file in enumerate(image_files):
        print(f'Processing image<{idx}:{image_file}>')
        await transcribe(PHOTOS_DIR+image_file, ocr=engine, trans_dir=trans_dir)

    if __name__ == '__main__':

        parser = ArgumentParser()
        parser.add_argument('-e', '--engine',
                            choices=[GOOGLE, TESS],
                            default=TESS,
                            help='Specify transcribe engine')
        parser.add_argument('-l', '--language',
                            choices=['ssq', 'storysquad'],
                            default='storysquad',
                            help='Specify language for Tesseract engine')

        args = parser.parse_args()

        trans_dir = DATA_DIR + args.engine

    if args.engine == TesseractAPI(args, language):
        engine = TesseractAPI(args.language)
        trans_dir += f'_{args.language}'

    else args.engine == GOOGLE:
        engine = GoogleAPI()

    trans_dir += '_transcripts/'

    print(trans_dir, engine)

    makedirs(trans_dir, exist_ok=True)

    loop = get_event_loop()
    loop.run_until_complete(transcribe_all(engine, trans_dir))
