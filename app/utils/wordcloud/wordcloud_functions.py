import pandas as pd
from collections import Counter

complex_words = pd.read_csv(
    'https://raw.githubusercontent.com/Lambda-School-Labs/scribble-stadium-ds/main/data/crop-cloud/complex_words.csv'
    )


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

    # tokenize words
    story = story.split()

    # remove '' from list
    story = [x for x in story if x != '']

    return story


def complexity_df(story_words):

    # Create a dictionary to count occurrences of words
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

    # make a column for how complex a word is

    # first setting words that are in the complex_words with their
    # set complexity these are words at higher grade levels, that
    # don't work with the complexity metric
    vdic = pd.Series(complex_words.complexity.values, index=complex_words.word).to_dict()
    words.loc[words.word.isin(vdic.keys()), 'complexity'] = words.loc[words.word.isin(vdic.keys()), 'word'].map(vdic)

    # then filling in the rest with the complexity metric
    words['complexity'] = words['complexity'].fillna(words['syllables'] + words['len'])
    words = words.astype({"complexity": int})

    return words


def story_word_count(words_df):
    # takes in the words df that is created
    # with the complexity_df function
    # counts all words per story submission
    word_count = sum(words_df['word'].value_counts())
    return word_count


def get_top_complex_words(words_df, num_of_words):
    # takes in the words df that is created
    # with the complexity_df function
    # and the amount of top words that are wanted
    # returns the top complex words
    words_df = words_df.sort_values(by=['complexity'], ascending=False)
    most_complex = words_df[:num_of_words]
    return most_complex
