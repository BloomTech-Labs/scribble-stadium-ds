from os import path

import joblib
import nltk
import pandas as pd

PICKLE_PATH = path.join(path.dirname(__file__), "", "MinMaxScaler.pkl")
scaler = joblib.load(PICKLE_PATH)


def metrics(document: str):
    """
    Cleans and generates metrics for a single story transcription.

    Called within squad_score async function, so only need be run separately
    if metrics without a complexity metric are required.

    Input: story transcription as a string
    Output: a single row of a dataframe, with the following metrics as columns:

    Included metrics:
    - Length of story (in characters)
    - Average word length (in chars)
    - Number of quotation marks
    - Number of unique words (over 2 chars)
    - Number of adjectives (using nltk)
    """

    # Strip leading or tailing spaces and integers
    cleaned = document.strip().strip("/-0123456789")

    # Ensure all commas and periods are followed by a space
    cleaned = cleaned.replace(".", ". ").replace(",", ", ")

    # Remove any instances of multiple spaces
    cleaned = " ".join(cleaned.split())

    # Generate single row dataframe from transcription
    cols = ['transcription']
    df = pd.DataFrame([cleaned], columns=cols)

    # Generate metrics
    # Length of story
    df["story_length"] = df["transcription"].str.len()

    # Average word length
    word_count = (df["transcription"].str.split()).str.len()
    df["avg_word_len"] = df["story_length"] / word_count

    # Number of quotation marks
    df["quotes_num"] = df["transcription"].str.count('"')

    # Number of unique words, over 2 characters
    def over_two_chars(cleaned_transcription):
        """Returns number of unique 2+ char words in transcription."""
        word_list = cleaned_transcription.split()
        word_set = set()
        for x in word_list:
            if len(x) > 2:
                word_set.add(x)
        return len(word_set)

    df["unique_words_num"] = df["transcription"].apply(over_two_chars)

    # Number of adjectives
    def num_adj(transcription):
        """Returns number of adjectives in transcription."""
        tokens = nltk.word_tokenize(transcription)
        pos = nltk.pos_tag(tokens)
        adj_count = 1
        for word in pos:
            if word[1] == 'JJ':
                adj_count += 1
        return adj_count

    df["adj_num"] = df["transcription"].apply(num_adj)

    return df


async def squad_score(document: str, scaler):
    """
    Generates a complexity metric, Squad Score, for a given transcription.

    Calls metrics function to generate metrics, then scales, weights,
    and adds all metrics together to create Squad Score.

    Initial scaling based on pickled MinMaxScaler from training data.
    See squad_score_mvp notebook for more.

    In future iterations, weights can be adjusted based on additional analysis.
    In version 0.1, weights initialized at 1 for all factors.

    Input: story transcription as a string, and pickled scaler
    Output: single integer value for Squad Score

    Note that this is an async function. In order to run locally as an
    isolated function, must be run using:
    asyncio.run(squad_score(document, scaler))
    """

    # Generate metrics and single row DF from transcription
    row = metrics(document).iloc[0, :]

    # Instantiate weights
    weights = {
        "story_length": 1,
        "avg_word_len": 1,
        "quotes_number": 1,
        "unique_words": 1,
        "adj_num": 1
    }

    # Scale metrics with pickled MinMax Scaler
    scaled = scaler.transform([row[1:]])[0]

    # Generate scaler to create desired output range (~1-100)
    range_scaler = 30

    # Weight values
    sl = weights["story_length"] * scaled[0] * range_scaler
    awl = weights["avg_word_len"] * scaled[1] * range_scaler
    qn = weights["quotes_number"] * scaled[2] * range_scaler
    uw = weights["unique_words"] * scaled[3] * range_scaler
    an = weights["adj_num"] * scaled[4] * range_scaler

    # Add all values
    squad_score = sl + awl + qn + uw + an

    # Ensure squad_score is a positive value
    # This would only be necessary for 1-2 sentence-long stories
    # or test sentences
    if squad_score < 0:
        squad_score = 0

    return squad_score
