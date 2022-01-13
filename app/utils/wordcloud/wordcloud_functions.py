import pandas as pd
from collections import Counter
import re
from os import path

filepath = path.join(
    path.dirname(__file__), "..", "..", "..", "data", "crop-cloud", "complex_words.csv"
)

complex_words = pd.read_csv(filepath)


# Takes in the story and how many words needed
# Creates a dataframe of the story and calculates complexity
# Returns a list of the top complex words
def complexity_df(story_string, num_of_words_needed=20):

    # Counts syllables for each word
    def count_syllables(word):
        word = word.lower()
        syllable_count = 0
        vowels = "aeiouy"
        if len(word) == 0:
            return 0
        if word[0] in vowels:
            syllable_count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                syllable_count += 1
        if word.endswith("e"):
            syllable_count -= 1
        if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
            syllable_count += 1
        if syllable_count == 0:
            syllable_count = 1
        return syllable_count

    # Clean the story
    cleaned = re.sub("[^-9A-Za-z ]", "", story_string).lower()
    cleaned_words = cleaned.split()

    word_counts = Counter(cleaned_words)

    # Convert the dictionary to a dataframe
    word_list = []
    count_list = []

    for k, v in word_counts.items():
        word_list.append(k)
        count_list.append(v)

    words = pd.DataFrame({"word": word_list, "count": count_list})

    # make a column for letter counts
    words["len"] = words["word"].apply(len)

    # column for syllable count
    words["syllables"] = words["word"].apply(count_syllables)
    # https://medium.com/@mholtzscher/programmatically-counting-syllables-ca760435fab4

    # make a column for how complex a word is

    # first setting words that are in the complex_words with their set complexity
    # these are words at higher grade levels, that don't work with the complexity metric
    vdic = pd.Series(
        complex_words.complexity.values, index=complex_words.word
    ).to_dict()
    words.loc[words.word.isin(vdic.keys()), "complexity"] = words.loc[
        words.word.isin(vdic.keys()), "word"
    ].map(vdic)

    # then filling in the rest with the complexity metric
    words["complexity"] = words["complexity"].fillna(words["syllables"] + words["len"])
    words = words.astype({"complexity": int})

    # Dividing the complexity of each word by how many times
    # the word is used in the story
    words["complexity"] = words["complexity"] / words["count"]

    # Sorting the words so that the most complex are at the top
    words = words.sort_values(by=["complexity"], ascending=False)

    # returns the selected number of words and their complexities
    temp = words[["word", "complexity"]][:num_of_words_needed]
    word_complexities = dict(zip(temp.word, temp.complexity))

    return word_complexities


def story_word_count(story_string):
    # takes in the story as a string
    # counts all words per story submission
    cleaned = re.sub("[^-9A-Za-z ]", "", story_string).lower()
    cleaned_words_count = len(cleaned.split())
    return cleaned_words_count
