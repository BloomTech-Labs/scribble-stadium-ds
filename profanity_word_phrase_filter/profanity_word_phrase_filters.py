
import pandas as pd
from json import dumps

#global variables
filepath = '../profanity_word_phrase_filter/full_text.txt'
transcriptions = {'images': []}
flagged_list = []
df = pd.read_csv('bad_single.csv', usecols=[0], names=None)
# load in bad phrases
df2 = pd.read_csv('bad_phrases.csv', usecols=[0], names=None)
# convert to list
bad_words = df['Bad_words'].to_list()
bad_phrases = df2['Bad_phrases'].to_list()


def readFile(filepath):
    """
    :param filepath: inputs the text file of interest.
    :returns: a string of words
    This function opens the file in read mode, removes \n, which is created
    when a string is created from text, and puts the file into an array"""
    fileObj = open(filepath, "r")
    words = fileObj.read().replace('\n', ' ')
    fileObj.close()
    return words

# Function that removes punctuation from story
def remove_punctuation(transcriptions):
    """
    :param: transcriptions is the dictionary containing text file that has been
    converted into an array.
    :return: cleaned string of words
    This function removes punctuations from the story """
    parsed_string = dumps(transcriptions)
    punctuations = '''[],!.'"\\?'''
    for char in parsed_string:
        if char in punctuations:
            parsed_string = parsed_string.replace(char, '')
    return parsed_string


# Function that looks for bad phrases in story
def return_bad_phrases(transcriptions):
    """
    :params transcriptions:transcriptions is the dictionary
    containing text file that has been converted into an array
    :return: updated transcriptions dictionary
    This function searches for bad phrases in the story.it converts
    a dictionary to str using dumps to keep phrases in tact. The
    phrases are lowercased to match the list of bad phrases.the
    punctuation is then removed. """

    parsed_string = dumps(transcriptions)
    parsed_string = parsed_string.lower()
    parsed_string = remove_punctuation(parsed_string)
    for word in bad_phrases:
        if word in parsed_string:
            flagged_list.append(word)
    dict = {'possible_words' : flagged_list}
    return transcriptions.update(dict)


# Function that looks for single bad words in story
def return_bad_words(transcriptions):
    """
    :params transcriptions:transcriptions is the dictionary
    containing text file that has been converted into an array
    :return: updated transcriptions dictionary
    This function searches for bad words in the story. It converts
    a dictionary to str using dumps to keep words in tact. The
    phrases are lowercased to match the list of bad phrases.the
    punctuation is then removed. """

    parsed_string = list(transcriptions.values())[0][0]
    parsed_string = parsed_string.lower()
    parsed_string = remove_punctuation(parsed_string)
    parsed_string = parsed_string.split()
    for word in bad_words:
        if word in parsed_string:
            flagged_list.append(word)
    dict = {'possible_words' : flagged_list}
    return transcriptions.update(dict)


# Checks to see if any words have been added to the flagged_list
def flag_bad_words(transcriptions):
    """
    :params transcriptions:transcriptions is the dictionary
    containing the text file that has been converted into an array
    :return: updated transcriptions dictionary
    This function checks to see if any words have been added to the flagged_list. """

    if any(flagged_list):
        dict = {'flagged' : [True]}
        return transcriptions.update(dict)
    else:
        dict = {'flagged' : [False]}
        return transcriptions.update(dict)


transcriptions['images'].append(readFile(filepath))
return_bad_phrases(transcriptions)
return_bad_words(transcriptions)
print(flag_bad_words(transcriptions))
print(transcriptions)
