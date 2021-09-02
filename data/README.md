-# Story Squad Data

- Children's story submissions are not able to be made public due to [COPPA](https://www.ecfr.gov/cgi-bin/text-idx?SID=4939e77c77a1a1a08c1cbf905fc4b409&node=16%3A1.0.1.3.36&rgn=div5) guidelines, and our team decided to extend that to transcriptions as well out of precaution. 
- The `squad_score_metrics` csv file in this folder contains the Squad Score v1.1 metrics from all 167 provided stories in our training data set, and was generated from the `squad_score_mvp` [notebook](../notebooks/squad_score_mvp.ipynb). 
   - features: story_id, story_length, avg_word_len, quotes_num, unique_words_num, adj_num, squad_score
- The `rankings` csv file contains the hand-rankings of 25 stories in the dataset, which is the only piece of labeled data provided by the stakeholder.
   - features: ranking, story_id
- Anyone with access to the Story Squad data can download any of the notebooks in this repository to generate any additional needed csv files. The [README](../notebooks) in the notebooks folder will list any csv a notebook creates.
- Note: for anyone with access to Story Squad data, be advised that the human transcriptions of the stories corresponding to the following Story IDs are missing pages, and are therefore inaccurate and should be removed from any comparisons of human vs computer transcriptions: 3213, 3215, 3240, 5104, 5109, 5262

 As of 8/18/21
- The storysquad.traineddata model has been trained on all --32 files, as well about 50% of --52 files, this training data, as well as the .box and .lstmf files generated while running the model can be found in storysquad-ground-truth.
- The files in storysquad-ground-truth folder contain snippets of student handwriting as well as corresponding transcriptions. As per Jake Mallory "If the data does not contain the names of children it's safe. The idea is to protect the identity of the children, not the artifacts created by them." 
- All folders in --52 numbered 5236 and higher still need to be cleaned and ground truth nees to be edited, see list below
- These folders contain very few files, it appears that segmentation was unsuccessful:
          5209, 5214, 5216, 5223, 5233, 5243, 5246, 5251, 5252, 5253, 5256, 5259, 5262, 5263

- Use this link for instruction for preprocessing data which has been segmented (.tif & .gt.txt files) https://docs.google.com/document/d/18ivuF40EqTIzE-BJbbk-5Rmp7CFYZ2fp1Odow0wt2T4/edit?usp=sharing
