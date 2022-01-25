# Story Squad Data

- According to https://www.ftc.gov/tips-advice/business-center/guidance/complying-coppa-frequently-asked-questions-0#F.%20Photos, FAQ F.2 states:

   COPPA applies to photos, videos, and audio files that contain children’s images or voices. It also applies to geolocation data contained in these files sufficient to identify street name and name of city or town. Finally, it applies to any persistent identifiers collected via the children’s upload of their photos. Therefore, in order to offer an app without parental notice and consent, the operator must take the following steps:

      1. Pre-screen the children’s photos in order to delete any that depict images of children or to delete the applicable portion of the photo, if possible. The operator must also delete any other personal information, for example, geolocation metadata, contained in the photos prior to posting them through the app. Note that if an operator does not pre-screen, then it may be subject to civil penalties under COPPA if any personal information is collected from children without the operator first notifying parents and obtaining their consent; and
      2. Ensure that any persistent identifiers are used only to support the internal operations of the app (as that term is defined in the Rule – see 16 C.F.R. 312.2) and are not used or disclosed to contact a specific individual, including through behavioral advertising, to amass a profile on a specific individual, or for any other purpose.
      
Therefore, according to the above rule, the app needs to ensure that all personal identification markers are removed during the processessing of the images.
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


  
