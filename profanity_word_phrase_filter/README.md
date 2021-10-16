## Custom profanity filter

Most online platforms contain inappropriate language. Parent's want to be certain
that Story squad (aka scribble stadium) is offering a safe environment for their
kiddos. In compliance to the children's Online Protection rule (COPPA)
https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/childrens-online-privacy-protection-rule

It's important for the submitted stories to be flagged as inappropriate if they 
contain any profanity. The stories will still be viewed by a human eye to make
sure that the flagging is warranted. 
The previous cohort worked on using the available libraries like profanity-filter
and profanity_Check but they were not sufficient in flagging all words and newer
phrases and Scuntorpe like words.

Using a list of profanity phrases in (bad_phrases.csv) and profanity words in (bad_single.csv).
bad_phrases.csv has a total of 215 phrases/expressions and bad_single.csv has a total of 1395 words.
These words can updated according to reflect what is currently flagged as inappropriate.
profanity_word_phrase_filters.py uses both lists to search if an uploaded document
contains profanity. 
