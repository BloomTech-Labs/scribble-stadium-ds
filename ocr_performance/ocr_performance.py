'''
ocr_performance.py - Define CompareTranscriptions class
'''
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
GOOGLE_TRANSCRIPTS_DIR = DATA_DIR + 'google_transcripts'


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

    def mean_cosine_similarity(self):
        cossim = []
        for idx, ref in enumerate(self.encoded_ref_dtm):
            cossim.append(
                cosine_similarity([ref],
                                  [self.encoded_dtm[idx]])[0][0])

        # Compute mean cosine similarity value for all the vectors
        sim = sum(cossim)/len(cossim)

        return sim

    def compute_error(self, hypothesis_transcripts_dir):
        self.load_hypothesis_transcriptions(hypothesis_transcripts_dir)
        self.generate_encoded_dtm()

        mcs = self.mean_cosine_similarity()

        # Compute and return the error value
        return round((1-mcs)*1e7, 0)


if __name__ == '__main__':

    comparator = CompareTranscriptions()

    rerr = comparator.compute_error(REFERENCE_TRANSCRIPTS_DIR)

    print(rerr)

    herr = comparator.compute_error(GOOGLE_TRANSCRIPTS_DIR)

    print(herr)
