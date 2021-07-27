import pandas as pd
from fastapi import APIRouter
from .wordcloud_functions import clean_text, complexity_df

router = APIRouter()

@router.post('/wordcloud/text')
async def wordcloudtext(story):

    story_words = clean_text(story)

    words = complexity_df(story_words)

    # Return the words that have a complexity score >= 7
    complex_words = list(words.loc[words['complexity'] >= 7, 'word'])

    return complex_words
