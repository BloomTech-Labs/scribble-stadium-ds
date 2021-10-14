from json import loads, dumps
import pandas as pd
from profanity_filter import ProfanityFilter
from profanity_check import predict, predict_prob

#global variables
filepath = '/content/Story 3121'
transcriptions = {'images': [],
          'metadata': []}
df = pd.read_csv('bad_single.csv', usecols=[0], names=None)
df2 = pd.read_csv('bad_phrases.csv', usecols=[0], names=None)
bad_words = df['Bad_words'].to_list()
bad_phrases = df2['Bad_phrases'].to_list()
# combine lists
bad_words_combined = bad_words + bad_phrases

