# Story Squad Data

- Children's story submissions are not able to be made public due to [COPPA](https://www.ecfr.gov/cgi-bin/text-idx?SID=4939e77c77a1a1a08c1cbf905fc4b409&node=16%3A1.0.1.3.36&rgn=div5) guidelines, and our team decided to extend that to transcriptions as well out of precaution. 
- The `squad_score_metrics` csv file in this folder contains the Squad Score v1.1 metrics from all 167 provided stories in our training data set, and was generated from the `squad_score_mvp` [notebook](../notebooks/squad_score_mvp.ipynb). 
   - features: story_id, story_length, avg_word_len, quotes_num, unique_words_num, adj_num, squad_score
- The `rankings` csv file contains the hand-rankings of 25 stories in the dataset, which is the only piece of labeled data provided by the stakeholder.
   - features: ranking, story_id
- Anyone with access to the Story Squad data can download any of the notebooks in this repository to generate any additional needed csv files. The [README](../notebooks) in the notebooks folder will list any csv a notebook creates.
- Note: for anyone with access to Story Squad data, be advised that the human transcriptions of the stories corresponding to the following Story IDs are missing pages, and are therefore inaccurate and should be removed from any comparisons of human vs computer transcriptions: 3213, 3215, 3240, 5104, 5109, 5262

###  As of 10/20/2021
-It is important to understand how data labelling was done for files in order to keep track of the model
performance. 
- Folder 32 and 52 were cleaned in 03/21. They binarized (B&W) the images and segmented them into snippets
using a script in command line. Here is the link for the resources they used. https://dabordel.medium.com/if-i-cant-read-children-s-handwriting-how-can-an-ocr-3f5edcdcfd7b

- Folders 31 and part of 51 were cleaned and labelled. Folder 31 was not preprocessed before clipping the images
into snippets. For folder 51 only (5125, 5126, 5129, 5130, 5131, 5132) images were cleaned. Please note files
5127 and 5128 were not available.   
  
### As of 9/26/21
 - The complex_words.csv was added to the crop-cloud folder. The csv contains words that do not work well with the complexity function that is currently being utilized. It also contains the grade level (Middle School, High School, College, or Post College) and set complexity scores for each word. This is used in the complexity_df function located in "app/utils/wordcloud/wordcloud_functions.py". This is meant to be a temporary location to store the dataset until a better solution is implemented.

- The 10 files used to benchmark the ML models can be found in slack under the channel "Labspt_ds" in a zip file called "starysquad-ground-truth-10-documents-summary.zip". the names of the files can also be found in the ds repository under "scribble-stadium-ds\data\starysquad-ground-truth-10-documents-summary".


### As of 8/18/21
- The storysquad.traineddata model has been trained on all --32 files, as well about 50% of --52 files, this training data, as well as the .box and .lstmf files generated while running the model can be found in storysquad-ground-truth.
- The files in storysquad-ground-truth folder contain snippets of student handwriting as well as corresponding transcriptions. As per Jake Mallory "If the data does not contain the names of children it's safe. The idea is to protect the identity of the children, not the artifacts created by them." 
- All folders in --52 numbered 5236 and higher still need to be cleaned and ground truth nees to be edited, see list below
- These folders contain very few files, it appears that segmentation was unsuccessful:
          5209, 5214, 5216, 5223, 5233, 5243, 5246, 5251, 5252, 5253, 5256, 5259, 5262, 5263

- Use this link for instruction for preprocessing data which has been segmented (.tif & .gt.txt files) https://docs.google.com/document/d/18ivuF40EqTIzE-BJbbk-5Rmp7CFYZ2fp1Odow0wt2T4/edit?usp=sharing


  
