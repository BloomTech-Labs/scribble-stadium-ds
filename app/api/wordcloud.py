import pandas as pd
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

def _syllables(word):
    syllable_count = 0
    vowels = 'aeiouyAEIOUY'
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
        syllable_count += 1
    return syllable_count

def clean_text(story):
    # remove punctuation
    story = story.replace('"','')
    story = story.replace('.','')
    story = story.replace(',','')

    #tokenize words
    story = story.split(sep=' ')

    #remove '' from list
    story = [x for x in story if x != '']

    return story

@router.post('/wordcloud/text')
async def wordcloudtext(story):

    story_words = clean_text(story)

    # Create a dictionary to count occurences of words
    word_counts = dict()
    for word in story_words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

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
    words['syllables'] = words['word'].apply(_syllables)
    # https://medium.com/@mholtzscher/programmatically-counting-syllables-ca760435fab4

    # make a column for how BIG a word is
    words['complexity'] = words['syllables'] + words['len']

    # Return the words that have a complexity score >= 7
    res = list(words.loc[words['complexity'] >= 7, 'word'])

    return res
