from json import dumps

import pandas as pd

# global variables
filepath = '../profanity_word_phrase_filter/full_text.txt'
transcriptions = {'images': []}
flagged_list = []


def readFile(filepath):
    """
    :param filepath: inputs the text file of interest.
    :returns: a string of words
    This function opens the file in read mode, removes \n, which is created
    when a string is created from text, and puts the file into an array"""
    fileObj = open(filepath, "r") #opens the file in read mode
    words = fileObj.read().replace('\n', ' ') #put words in an array and remove \n
    fileObj.close()
    return words

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


def return_bad_phrases(transcriptions):
    """
    :params transcriptions:transcriptions is the dictionary
    containing text file that has been converted into an array
    :return: updated transcriptions dictionary
    This function searches for bad phrases in the story.it converts
    a dictionary to str using dumps to keep phrases in tact. The
    phrases are lowercased to match the list of bad phrases.the
    punctuation is then removed. """

    # Convert dict to str using dumps to keep phrases in tact
    parsed_string = dumps(transcriptions)
    # Lowercase to match list of bad phrases
    parsed_string = parsed_string.lower()
    # Remove punctuation
    parsed_string = remove_punctuation(parsed_string)
    df2 = pd.read_csv('bad_phrases.csv', usecols=[0], names=None)
    bad_phrases = df2['Bad_phrases'].to_list()
    # Returns list of matching words and puts in flagged_list global variable
    for word in bad_phrases:
        if word in parsed_string:
            flagged_list.append(word)
    dict_words = {'possible_words': flagged_list}
    return transcriptions.update(dict_words)


# Function that looks for single bad words in story
def return_bad_words(transcriptions):
    """
    :params transcriptions:transcriptions is the dictionary
    containing text file that has been converted into an array
    :return: updated transcriptions dictionary
    This function searches for bad words in the story. It converts
    a dictionary to str using dumps to keep words in tact. The
    phrases are lowercased to match the list of bad phrases.
    punctuations then removed. """

    # Parsing out just the story string from dict to avoid conflicts
    parsed_string = list(transcriptions.values())[0][0]
    # Lowercase to match list of bad words
    parsed_string = parsed_string.lower()
    # Remove punctuation
    parsed_string = remove_punctuation(parsed_string)
    # Splitting into list of strings to detect exact matches
    parsed_string = parsed_string.split()
    df = pd.read_csv('bad_single.csv', usecols=[0], names=None)
    bad_words = df['Bad_words'].to_list()
    # Finding matches and appending them to flagged_list
    for word in bad_words:
        if word in parsed_string:
            flagged_list.append(word)
    dict = {'possible_words': flagged_list}
    return transcriptions.update(dict)


def flag_bad_words(transcriptions):
    """
    :params transcriptions:transcriptions is the dictionary
    containing the text file that has been converted into an array
    :return: updated transcriptions dictionary
    This function checks to see if any words have been added to the flagged_list. """

    if any(flagged_list):
        dict_flagged = {'flagged': [True]}
        return transcriptions.update(dict_flagged)
    else:
        dict_flagged = {'flagged': [False]}
        return transcriptions.update(dict_flagged)

#return updated dictionary and check if the document has been flagged for profanity
transcriptions['images'].append(readFile(filepath))
return_bad_phrases(transcriptions)
return_bad_words(transcriptions)
flag_bad_words(transcriptions)
print(transcriptions)
