# Story Squad Data

- Children's story submissions are not able to be made public due to [COPPA](https://www.ecfr.gov/cgi-bin/text-idx?SID=4939e77c77a1a1a08c1cbf905fc4b409&node=16%3A1.0.1.3.36&rgn=div5) guidelines, and our team decided to extend that to transcriptions as well out of precaution. 
- The `squad_score_metrics` csv file in this folder contains the Squad Score v1.1 metrics from all 167 provided stories in our training data set, and was generated from the `squad_score_mvp` [notebook](../notebooks/squad_score_mvp.ipynb). 
   - features: story_id, story_length, avg_word_len, quotes_num, unique_words_num, adj_num, squad_score
- The `rankings` csv file contains the hand-rankings of 25 stories in the dataset, which is the only piece of labeled data provided by the stakeholder.
   - features: ranking, story_id
- Anyone with access to the Story Squad data can download any of the notebooks in this repository to generate any additional needed csv files. The [README](../notebooks) in the notebooks folder will list any csv a notebook creates.
- Note: for anyone with access to Story Squad data, be advised that the human transcriptions of the stories corresponding to the following Story IDs are missing pages, and are therefore inaccurate and should be removed from any comparisons of human vs computer transcriptions: 3213, 3215, 3240, 5104, 5109, 5262