import pandas as pd
from fastapi import APIRouter, Query
from .wordcloud_functions import clean_text, complexity_df, count_syllables
import json

router = APIRouter()

@router.post('/wordcloud/update')
async def wordcloudtext(story, metric: str = Query('len_count', enum=['len_count', 'len', 'syl', 'syl_count'])):

    story_words = clean_text(story)

    words = complexity_df(story_words)

    metrics = ['len', 'syl', 'len_count', 'syl_count']
    if metric == 'len':
        words['complexity'] = words['word'].apply(len)

    elif metric == 'syl':
        words['complexity'] = words['word'].apply(count_syllables)

    elif metric == 'len_count':
        words['len'] = words['word'].apply(len)
        words['complexity'] = words['len'] / words['count']

    elif metric == 'syl_count':
        words['syl'] = words['word'].apply(count_syllables)
        words['complexity'] = words['syl'] / words['count']
    
    else:
        raise ValueError(f"metric must be one of {['len', 'syl', 'len_count', 'syl_count']} but got '{metric}'")


    # # Return the words that have a complexity score >= 7
    # complex_words = list(words.loc[words['complexity'] >= 7, 'word'])

    # scale the complexities so the sum is 1000
    words['complexity'] = words['complexity'] / words['complexity'].sum()
    word_complexities = dict(zip(words.word, words.complexity))

    return word_complexities

