
import pandas as pd
from json import dumps

#global variables
filepath = '../profanity_word_phrase_filter/full_text.txt'
transcriptions = {'images': [],
          'metadata': []}
flagged_list = []
df = pd.read_csv('bad_single.csv', usecols=[0], names=None)
# load in bad phrases
df2 = pd.read_csv('bad_phrases.csv', usecols=[0], names=None)
# convert to list
bad_words = df['Bad_words'].to_list()
bad_phrases = df2['Bad_phrases'].to_list()


def readFile(filepath):
    fileObj = open(filepath, "r")  # opens the file in read mode
    words = fileObj.read().replace('\n', ' ')  # puts the file into an array
    fileObj.close()
    return words

transcriptions['images'].append(readFile(filepath))

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


# Checks to see if any words have been added to the flagged_list
def flag_bad_words(transcriptions):
    if any(flagged_list):
        dict = {'flagged' : [True]}
        return transcriptions.update(dict)
    else:
        dict = {'flagged' : [False]}
        return transcriptions.update(dict)

# call functions on transcriptions
return_bad_phrases(transcriptions)
return_bad_words(transcriptions)
# Scunthorpe Problem solved!
print(transcriptions)
