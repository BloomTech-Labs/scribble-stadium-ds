import logging
from os import listdir
from os.path import dirname
from asyncio import get_event_loop

from app.utils.img_processing.google_api import GoogleAPI, NoTextFoundException
# global variables and services
DIR = dirname(__file__)
DATA_DIR = DIR + '/../data/'
PHOTOS_DIR = DATA_DIR + 'photos/'
TRANSCRIPTS_DIR = DATA_DIR + 'transcripts/'
METADATA_DIR = DATA_DIR + 'metadata/'
GOOGLE_TRANSCRIPTS_DIR = DATA_DIR + 'google_transcripts/'

vision = GoogleAPI()

async def transcribe(page_image_file):

    file_name = page_image_file.split('/')[-1].split('.')[0]

    meta_file_name = METADATA_DIR + file_name
    trans_file_name = GOOGLE_TRANSCRIPTS_DIR + file_name
    
    with open(page_image_file, mode='rb') as pifd:
        page_image = pifd.read()

    low_confidence = None
    flagged = None
    trans_text = 'No Text Found'
    try:
        low_confidence, flagged, trans_text = await vision.transcribe(page_image)
    except NoTextFoundException:
         print('No Text Found')
         
    with open(meta_file_name,'w') as metafd:
        metafd.write(' '.join([str(low_confidence), str(flagged)]))
    with open(trans_file_name,'w') as transfd:
        transfd.write(trans_text)

        
        

async def transcribe_all():
    
    image_files = [ x for x in listdir(PHOTOS_DIR) if x.endswith('.jpg')]
    image_files.sort()
    
    for idx,image_file in enumerate(image_files):
        print(f'Processing image<{idx}:{image_file}>')
        await transcribe(PHOTOS_DIR+image_file)

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(transcribe_all())

