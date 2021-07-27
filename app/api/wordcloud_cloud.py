import pandas as pd
from fastapi import APIRouter
import random
from wordcloud import WordCloud
from io import BytesIO
import base64
from .wordcloud_functions import clean_text, complexity_df


router = APIRouter()

@router.post('/wordcloud/cloud')
async def wordcloud(story):

    story_words = clean_text(story)

    words = complexity_df(story_words)

    word_size = list(zip(words.word, words.complexity))

    all_terms = []
    for term, prob in word_size:
        n = int(prob*10)
        new_terms = [term for j in range(n) if n > 0]  # a list of the term multiple times proportional to their BIGness
        all_terms.extend(new_terms)
    random.shuffle(all_terms)
    long_string = ','.join(all_terms)

    # Create a WordCloud object
    wordcloud = WordCloud(
        background_color="white",
        max_words=5000,
        contour_width=3,
        contour_color='steelblue',
        ).generate(long_string).to_image()

    # Convert WordCloud to JSON object
    img = BytesIO()
    wordcloud.save(img, "PNG")
    img.seek(0)  
    img_b64 = base64.b64encode(img.getvalue()).decode()

    return img_b64
