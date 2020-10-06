import joblib
import pandas as pd


def metrics(transcription: str):
    """
    Cleans and generates metrics for a single story transcription.

    Outputs a single row of a dataframe, with the following metrics as columns:

    Included metrics:
    - Length of story (in characters)
    - Average word length (in chars)
    - Number of quotation marks
    - Number of unique words (over 2 chars)
    """

    # Strip leading or tailing spaces and integers
    cleaned = transcription.strip().strip("/-0123456789")

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

    return df


def squad_score(row):
    """
    Scales, weights, and adds all metrics for a given transcription.

    Initial scaling based on pickled MinMaxScaler from training data.
    See squad_score_mvp notebook for more.

    Weights according to prescribed weights for Story Squad analysis.
    In version 0.1, weights initialized at 1 for all factors.

    Input: single row of a dataframe, including transcription and metrics
    Output: single integer value for Squad Score
    """
    # Instantiate weights
    weights = {
              "story_length": 1,
              "avg_word_len": 1,
              "quotes_number": 1,
              "unique_words": 1
              }

    # Scale metrics with pickled MinMax Scaler
    scaler = joblib.load('MinMaxScaler.pkl')
    scaled = scaler.transform([row[1:]])[0]

    # Generate scaler to create desired output range (~1-100)
    range_scaler = 30

    # Weight values
    sl = weights["story_length"] * scaled[0] * range_scaler
    awl = weights["avg_word_len"] * scaled[1] * range_scaler
    qn = weights["quotes_number"] * scaled[2] * range_scaler
    uw = weights["unique_words"] * scaled[3] * range_scaler

    # Add all values
    squad_score = sl + awl + qn + uw

    # Ensure squad_score is a positive value
    # This would only be necessary for 1-2 sentence-long stories
    # or test sentences
    if squad_score < 0:
        squad_score = 0

    return squad_score
