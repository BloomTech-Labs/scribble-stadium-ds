import pandas as pd
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class ComplexWords(BaseModel):
    """The submission entry in string form"""
    text: str

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

    return story

@router.post('/wordcloud/text')
async def wordcloudtext(story):

    words = clean_text(story)

    word_counts = dict()
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # # put this in a dataframe
    # # make a column of word counts
    # words = pd.DataFrame({'word': word_counts.keys(), 
    #                      'count': word_counts.values()})

    # # make a column for letter counts
    # words['len'] = words['word'].apply(len)

    # # column for syllable count
    # words['syllables'] = words['word'].apply(_syllables)
    # # https://medium.com/@mholtzscher/programmatically-counting-syllables-ca760435fab4

    # # make a column for how BIG a word is
    # words['complexity'] = words['syllables'] + words['len']

    # res = set(words.loc[words['complexity'] > 7, 'word'])
   
    # return res
    complex_word = []

    for k, v in word_counts.items():
        if v > 1:
            complex_word.append(k)
    
    return complex_word



 



    # # make a column for how BIG a word is
    # words['complexity'] = words['syllables'] + words['len']

    # complex_words = list(words.loc[words['len'] >= 3, 'word'])

    # return complex_words
