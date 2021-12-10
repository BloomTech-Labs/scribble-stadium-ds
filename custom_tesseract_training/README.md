# Workflow for Fine Tuning Tesseract Model in Docker 
## A guide for using Docker to fine tune Story Squad’s Tesseract model

### Contents:
* Connecting to Docker
* Data Storage
* Selecting the Hyperparameters
* Fine Tuning the Model
* Saving the Model
* Model Performance Logging
* Testing Model Against Baseline
* Previous Readme

### Prerequisites: 
* Make sure you’ve pulled the latest main branch
* Make sure the data has already been preprocessed, in the agreed upon conventions

## Connecting to Docker

(must have the DS repo cloned (https://github.com/Lambda-School-Labs/scribble-stadium-ds))

(all commands done in the terminal, with Docker open, in your base environment (you will connect to a virtual environment in docker)

* Run the Dockerfile using this command from the repo root. 
  * docker-compose -f docker.dev.yml up -d
    *  Note: You only need to do this step once.
   
* Run this command to access the container once the build is complete, or if you have already built the container before
  * docker exec -ti scribble-ocr bash
* cd to root
  * cd ..
* cd to train folder
  * cd train
* cd to tesstrain folder
  * cd tesstrain
* activate the virtual environment
  * source ocr/bin/activate
* install the required libraries:
  * pip install -r requirements.txt

For further information on the Dockerfile, see here: ​​https://github.com/BloomTech-Labs/scribble-stadium-ds/blob/main/Dockerfile_tesseract_training

## Data Storage
When using Docker all new training data must be placed in:

/train/tesstrain/data/storysquad-ground-truth
### Training Data and Label Naming Conventions
* Preprocess Data using agreed upon pipeline
* Label the data by transcribing the characters exactly how they appear (not fixing the spelling) in a plain .gt.txt file
* Ensure that images are saved with the .tif or .png extension and that the exact transcription (ground truth labels) are saved in .gt.txt
* Verify that name of each training example/label pair are exactly identical (excluding the .gt.txt and .tif extensions)
###Adding New Training Data in Docker
* Open the docker container using these instructions:
https://docs.google.com/document/d/16NF5IxDxllME934f9YaepYScPrShJJt10i5gEzErzgQ/edit#
* Ensure new data has been already uploaded to the repo already, e.g. in:
/data/new_data_repo
* Copy all the training data pairs across from the app/data directory to the ground truth directory:
  * cp -ra /app/data/<new_data>/. /train/tesstrain/data/storysquad-ground-truth
TEST THIS: May or may not need the a in -ra

## Selecting the Hyperparameters
### List of hyperparameters in tesseract
Below are the hyperparameters that can be changed in our custom Tesseract model. 

The command is listed, followed by what exactly it is/does, then the default value. We’ve also listed some sample options to go through and test for tuning.
 
Variables in training command:

    CORES              - No of cores to use for compiling leptonica/tesseract. Default: 4 /{could change based on machine you are running on}
    TESSDATA_REPO      - Tesseract model repo to use (_fast or _best). Default: _best {can’t hyperparameter tune on fast, integer based, truly just faster}
    MAX_ITERATIONS     - Max iterations. Default: 10000 /{could try 5000 to 15000 in 1000 increments}
    EPOCHS             - Set max iterations based on the number of lines for training. Default: none
    LEARNING_RATE      - Learning rate. Default: 0.0001 with START_MODEL, otherwise 0.002 /{could test from .001 to .0001 in .0001 increments}
    NET_SPEC           - Network specification. Default: [1,36,0,1 Ct3,3,16 Mp3,3 Lfys48 Lfx96 Lrx96 Lfx256 O1c\#\#\#]
    FINETUNE_TYPE      - Finetune Training Type - Impact, Plus, Layer or blank. Default: ''
    PSM                - Page segmentation mode. Default: 13. 
    0 = Orientation and script detection (OSD) only.
    1 = Automatic page segmentation with OSD.
    2 = Automatic page segmentation, but no OSD, or OCR.
    3 = Fully automatic page segmentation, but no OSD.
    4 = Assume a single column of text of variable sizes.
    5 = Assume a single uniform block of vertically aligned text.
    6 = Assume a single uniform block of text.
    7 = Treat the image as a single text line.
    8 = Treat the image as a single word.
    9 = Treat the image as a single word in a circle.
    10 = Treat the image as a single character.
    11 = Sparse text. Find as much text as possible in no particular order.
    12 = Sparse text with OSD.
    13 = Raw line. Treat the image as a single text line,
         bypassing hacks that are Tesseract-specific.
    RANDOM_SEED        - Random seed for shuffling of the training data. Default: 0
    RATIO_TRAIN        - Ratio of train / eval training data. Default: 0.90
    TARGET_ERROR_RATE  - Stop training if the character error rate (CER in percent) gets below this value. Default: 0.01
	OEM                - OCR Engine modes:
    0 = Legacy engine only.
    1 = Neural nets LSTM engine only.
    2 = Legacy + LSTM engines.
    3 = Default, based on what is available.
    
 
To hyperparameter tune: Add desired command in the terminal between START_MODEL and TESSDATA. 

 E.g.
  
`make training START_MODEL=eng PSM=7 RATIO_TRAIN=0.8 TESSDATA=/train/tessdata`

## Fine Tuning the model
All training is done through the terminal. 

Starting in the train/tesstrain directory, enter in the console:


* make training MODEL_NAME=storysquad START_MODEL=eng PSM=7 TESSDATA=/train/tessdata

  * Note: add changes to the hyperparameters between ‘START_MODEL’ and ‘TESSDATA’ commands

## Saving the trained model

Models are automatically saved to the name storysquad.traineddata, in tesstrain/data. New models will overwrite the old ones if not moved to another directory or renamed. 

So we recommend moving the trained model to another directory (e.g. creating a folder called “trained_models” in /train/tesstrain). This will make it easier to view the progress on models and keep them organized, also avoiding the problem of rewriting old ones. 
 
## Model Performance Logging
### Accessing training logs
Training logs are stored in tesstrain/data, so they can be accessed there.

If training yields good results, we should type up clearly what was changed and what our accuracies/results were on a text file in the repo. This will make another option for easier reading/quickly comparing different models.
 
## Testing Model Against Baseline
* Move your new model from `tesstrain/data` dir to `tessract\tessdata` dir
* Make sure your test pair (full image to be transcribed and ground-truth) are uploaded to the `tesstrain\dat` dir. You can create a dir for your test pairs in the tesstrain/data dir
* cd to (`tesstrain/data`)
* note: make sure you activated the OCR environment and run `source training_setup.sh`
* Install the following packages: ipython (`pip install ipython`), pytesseract (`pip install pytesseract`), openCV (`pip install opencv`). If you get an error while trying to install any of these, you might be required to upgrade pip (`pip install --upgrade pip`)
* run `ipython` command
* copy `ocr-inference.py` script found in custom_tesseract_training/ocr-inference.py and paste it in command line
  * Note: if you have this error ‘`ImportError: libGL.so.1: cannot open shared object file: No such file or directory`,’ These two commands should fix it: run `sudo apt-get update` and then run `sudo apt-get install ffmpeg libsm6 libxext6 -y` Also note that you will have an error if the image path and custom model names `lang = 'storysquad'` are incorrect
* There is an updated `ocr_inference.py` script, `models_comparison.py` found in the `models_comparison.py` which will let you compare multiple images and models including google vision OCR. check the `model_comparison` dir for instructions on how to run it in your IDE.
     - Use `scribble-stadium-ds/tesseract/tesstrain/plot` for scripts to plot Tesseract     LSTM Training and Validation Character Error Rate Percent.

# A collection of previous cohort readme updates:
### As of 10/20/2021
 * Our cohort focussed on adding, cleaning, and labelling more data. This effort paid off. We were able to increase the accuracy of the model from 48% to 61% on a neat handwriting. The default model (tesseract-ocr version 4.1.1) had a 2% accuracy for the same document (full_sample2.png). Google vision OCR has an accuracy of 95%
 * The model is still not doing a good job of transcribing children's handwriting images. This accuracies are for the 5 of the 10 test images that were selected. (Photo 3121.jpg, Photo 3220 pg1.jpg, Story 3235 pg1.jpg, Photo 3202.jpg,Photo 3124 pg1.jpg) The complete list is in data README.md. Model Name 1 2 3 4 5 Tesseract - Base Model 2.58% 1.54% 1.88% 8.29% 0.00% Google Vision 80.00% 81.93% 81.93% 80.00% 95.65% Custom Model with old data 2.02% 2.77% 1.88% 3.56% 0.00% Custom Model with new data 2.03% 5.62% 1.88% 6.15% 0.00
 * The accuracies were doubled with preprocessing. (A blog post explaining on how to do this will be available to the onboarding cohort). The data pipeline in the data management dir was used for the preprocessing. In most causes sauvola thresholding (sauvola_preprocessing) works better than the regular binarization All preprocessing must include line removal. Use the data pipeline in the data management dir. complete directions will be included in a blog post.


