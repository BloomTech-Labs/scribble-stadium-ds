## Custom profanity filter

Most online platforms contain inappropriate language. Parents want to be certain
that Story Squad (aka Scribble Stadium) is offering a safe environment for their
children.

It is important for submitted stories to be flagged as inappropriate if they 
contain any profanity.The stories also have to be reviewed manually to ensure 
flagging by the system is warranted. 

Libraries like profanity-filter and profanity_check could not sufficiently flag all
profane words especially newer phrases.

Using a list of profanity phrases in (bad_phrases.csv) and profanity words in (bad_single.csv),
profanity_words_phrase_filters.py can be used on a string of text to identify and flag words and phrases as inappropriate.

These words are updated accordingly to reflect what is currently flagged as inappropriate.
The file "profanity_word_phrase_filters.py" uses both lists to search for profanity in uploaded documents.	
 
