'''
ocr_performance.py - Define CompareTranscriptions class
'''
from argparse import ArgumentParser
from csv import writer
from re import compile as rcompile
from os.path import dirname
from tensorflow.keras.models import load_model
from joblib import load
from glob import glob
from path import Path
from sklearn.metrics.pairwise import cosine_similarity

# Get the name of the directory where this file
# is located.
DIR = dirname(__file__)

# Match characters that are not blank space, digits or
# letters in the alphabet.
rex = rcompile('[^a-zA-Z 0-9]')

# Convert cosine_similarity value to cos error
# cosine_similarity of 1 implies identical text
# so 1 minus that value is a measure of error.


def COS_ERROR(x): return abs(round((1-x)*1e7, 0))

# Convert all letters to lower case, replace ',' and '-' with blank
# space and finally remove all characters that are not blank space, digits
# or letters


def tokenize(x):
    return rex.sub('', x.lower().replace(',', ' ').replace('-', ' '))


# Setup globals
MODELS_DIR = DIR + '/../models/'
DATA_DIR = DIR + '/../data/'

ENCODER = MODELS_DIR + 'encoder.h5'
ENCODED_REF_DTM = MODELS_DIR + 'encoded_ref_dtm.pkl'
TFIDF = MODELS_DIR + 'tfidf.pkl'
FILE_ROOTS = MODELS_DIR+'file_roots.pkl'

REFERENCE_TRANSCRIPTS_DIR = DATA_DIR + 'transcripts'

GOOGLE = 'google'
TESS = 'tess'
REFERENCE = 'ref'


class CompareTranscriptions():
    '''
    CompareTranscriptions - compare hypothesis transcriptions against
    reference and compute error value.
    '''

    def __init__(self):
        # Load the model saved in encoder.h5
        self.encoder = load_model(ENCODER)
        # Load the TfIDF vectorizer saved in tfidf.pkl
        self.tfidf = load(TFIDF)
        # Load the encoded reference DTM saved in encoded_ref_dtm.pkl
        self.encoded_ref_dtm = load(ENCODED_REF_DTM)
        # Load transcript file roots list from file_roots.pkl
        self.file_roots = load(FILE_ROOTS)

        self.transcripts = None
        self.encoded_dtm = None

    def load_hypothesis_transcriptions(self, transcripts_dir):
        '''
        Given the location of the hypothesis transcriptions
        dir, load all the transcripts into self.transcripts
        '''
        def read_transcript(file_name):
            '''
            Read and return the content of all transcript files
            that have file_name as prefix.
            e.g. A file name of .../google_transcripts/3102
            would mean that the conents of
            .../google_transcripts/3102-1
            and
            .../google_transcripts/3102-2
            would be read and returned.
            '''

            # generate the list of all file names that match
            # the wild carded file name
            file_names = glob(f'{file_name}*')
            ret = ''

            for fname in file_names:
                with open(fname) as fd:
                    ret += fd.read()+'\n\n'

            return ret

        with Path(transcripts_dir):
            self.transcripts = [read_transcript(x) for x in self.file_roots]

        self.transcripts = list(map(tokenize, self.transcripts))

    def generate_encoded_dtm(self):
        # Use the TfIDF vectorizer to vectorize the transcripts
        dtm = self.tfidf.transform(self.transcripts).todense()
        # Run the vectors through the encoder to reduce
        # dimensionality
        self.encoded_dtm = self.encoder.predict(dtm)

    def mean_cosine_similarity(self, engine):
        cossim = []
        for idx, ref in enumerate(self.encoded_ref_dtm):
            cossim.append(
                cosine_similarity([ref],
                                  [self.encoded_dtm[idx]])[0][0])

        # Convert cosine_similarity values into COS_ERROR values
        # and store in coserr
        coserr = [COS_ERROR(x) for x in cossim]

        # Use the Path context manager to change the current
        # working directory to DATA_DIR within the context.
        with Path(DATA_DIR):
            engine += '_cos_error'
            with open(f'{engine}.csv', 'w') as fd:
                csv_wr = writer(fd)
                # Write header row
                csv_wr.writerow(['img_name', f'{engine}'])
                # Write out image name, cos error tuples to
                # CSV file
                csv_wr.writerows(zip(self.file_roots, coserr))

        # Compute mean cosine similarity value for all the vectors
        sim = sum(cossim)/len(cossim)

        return sim

    def compute_error(self, engine, hypothesis_transcripts_dir):
        self.load_hypothesis_transcriptions(hypothesis_transcripts_dir)
        self.generate_encoded_dtm()

        mcs = self.mean_cosine_similarity(engine)

        # Compute and return the error value
        return COS_ERROR(mcs)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-e', '--engine', choices=[GOOGLE, TESS, REFERENCE],
                        default=TESS,
                        help='Specify transcribe engine')
    parser.add_argument('-l', '--language', choices=['ssq', 'storysquad'],
                        default='storysquad',
                        help='Specify language for Tesseract engine')

    args = parser.parse_args()

    engine = args.engine
    trans_dir = DATA_DIR
    if engine != REFERENCE:
        trans_dir += args.engine + '_'
    if engine == TESS:
        trans_dir += f'{args.language}_'
        engine += f'_{args.language}'
    trans_dir += 'transcripts/'

    print(trans_dir)

    comparator = CompareTranscriptions()

    gerr = comparator.compute_error(engine, trans_dir)

    print(gerr)
