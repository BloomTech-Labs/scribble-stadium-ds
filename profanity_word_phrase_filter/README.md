## Custom profanity filter

Most online platforms contain inappropriate language. Parents want to be certain
that Story squad (aka scribble stadium) is offering a safe environment for their
kiddos in compliance with the Children's Online Privacy Protection Rule (COPPA).
https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/childrens-online-privacy-protection-rule

It is important for submitted stories to be flagged as inappropriate if they 
contain any profanity. The stories will still be reviewed by a live person to make
sure the flagging is warranted. 
The previous cohort worked on using available libraries like profanity-filter
and profanity_Check but these could not sufficiently flag all profane words, newer
phrases and Scuntorpe like words.

Using a list of profanity phrases in (bad_phrases.csv) and profanity words in (bad_single.csv);
bad_phrases.csv has a total of 215 phrases/expressions and bad_single.csv has a total of 1395 words.
These words are updated accordingly to reflect what is currently flagged as inappropriate.
Profanity_word_phrase_filters.py uses both lists to search if an uploaded document
contains profanity. 
