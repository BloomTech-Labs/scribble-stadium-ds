from json import loads, dumps
import pandas as pd
from profanity_filter import ProfanityFilter
from profanity_check import predict, predict_prob

#global variables
filepath = '/content/Story 3121'
transcriptions = {'images': [],
          'metadata': []}
flagged_list = []
df = pd.read_csv('bad_single.csv', usecols=[0], names=None)
df2 = pd.read_csv('bad_phrases.csv', usecols=[0], names=None)
bad_words = df['Bad_words'].to_list()
bad_phrases = df2['Bad_phrases'].to_list()
# combine lists
bad_words_combined = bad_words + bad_phrases

# Function that removes punctuation from story
def remove_punctuation(transcriptions):
    parsed_string = dumps(transcriptions)
    punctuations = '''[],!.'"\\?'''
    for char in parsed_string:
        if char in punctuations:
            parsed_string = parsed_string.replace(char, '')
    return parsed_string


# Function that looks for bad phrases in story
def return_bad_phrases(transcriptions):
    # Convert dict to str using dumps to keep phrases in tact
    parsed_string = dumps(transcriptions)
    # Lowercase to match list of bad phrases
    parsed_string = parsed_string.lower()
    # Remove punctuation
    parsed_string = remove_punctuation(parsed_string)
    # Returns list of matching words and puts in flagged_list global variable
    for word in bad_phrases:
        if word in parsed_string:
            flagged_list.append(word)
    # Returns dictionary with list of matches
    dict = {'possible_words' : flagged_list}
    return transcriptions.update(dict)


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

