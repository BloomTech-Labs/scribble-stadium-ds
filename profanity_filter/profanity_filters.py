from json import loads, dumps
import pandas as pd
from profanity_filters import ProfanityFilter
from profanity_check import predict, predict_prob

#global variables
filepath = 'profanity_filter/full_text.txt'
transcriptions = {'images': [],
          'metadata': []}
transcriptions['images'].append(readFile(filepath))
df = pd.read_csv('bad_single.csv', usecols=[0], names=None)
# load in bad phrases
df2 = pd.read_csv('bad_phrases.csv', usecols=[0], names=None)
# convert to list
bad_words = df['Bad_words'].to_list()
bad_phrases = df2['Bad_phrases'].to_list()
# combine lists
bad_words_combined = bad_words + bad_phrases
flagged_list = []


def readFile(filepath):
    fileObj = open(filepath, "r")  # opens the file in read mode
    words = fileObj.read().replace('\n', ' ')  # puts the file into an array
    fileObj.close()
    return words

# Function that looks for single bad words in story
def return_bad_words(transcriptions):
    # Parsing out just the story string from dict to avoid conflicts
    parsed_string = list(transcriptions.values())[0][0]
    # Lowercase to match list of bad words
    parsed_string = parsed_string.lower()
    # Remove punctuation
    parsed_string = remove_punctuation(parsed_string)
    # Splitting into list of strings to detect exact matches
    parsed_string = parsed_string.split()
    # Finding matches and appending them to flagged_list
    for word in bad_words:
        if word in parsed_string:
            flagged_list.append(word)
    # Returns dictionary with list of matches
    dict = {'possible_words' : flagged_list}
    return transcriptions.update(dict)


# Checks to see if any words have been added to the flagged_list
def flag_bad_words(transcriptions):
    if any(flagged_list):
        dict = {'flagged' : [True]}
        return transcriptions.update(dict)
    else:
        dict = {'flagged' : [False]}
        return transcriptions.update(dict)

# call functions on transcriptions
print(return_bad_phrases(transcriptions))
print(return_bad_words(transcriptions))
# Scunthorpe Problem solved!
print(transcriptions)