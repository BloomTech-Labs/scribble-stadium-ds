import pandas as pd
from collections import Counter

def count_syllables(word):
    word = word.lower()
    syllable_count = 0
    vowels = 'aeiouy'
    if len(word) == 0:
        return 0
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith('e'):
        syllable_count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    if syllable_count == 0:
        syllable_count = 1
    return syllable_count
    

def clean_text(story):
    # remove weird characters
    whitelist = set("abcdefghijklmnopqrstuvwxyz' ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    story = ''.join(filter(whitelist.__contains__, story))

    #tokenize words
    story = story.split()

    #remove '' from list
    story = [x for x in story if x != '']

    return story


def complexity_df(story_words):

    # Create a dictionary to count occurences of words
    word_counts = Counter(story_words)

    # Convert the dictionary to a dataframe
    word_list = []
    count_list = []

    for k, v in word_counts.items():
        word_list.append(k)
        count_list.append(v)

    words = pd.DataFrame({'word': word_list, 'count': count_list})

    # make a column for letter counts
    words['len'] = words['word'].apply(len)

    # column for syllable count
    words['syllables'] = words['word'].apply(count_syllables)
    # https://medium.com/@mholtzscher/programmatically-counting-syllables-ca760435fab4

    # make a column for how BIG a word is
    words['complexity'] = words['syllables'] + words['len']

    return words