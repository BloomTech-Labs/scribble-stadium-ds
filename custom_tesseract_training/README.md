## As of 10/20/2021

-Our cohort focussed on adding cleaning and labelling more data. This effort paid off. We were
able to increase the accuracy of the model from 48% to 61% on a neat handwriting. The default model
(tesseract-ocr version 4.1.1) had a 2% accuracy for the same document (`full_sample2.png`). Google vision 
OCR has an accuracy of 95%.

-The model is still not doing a good job of transcribing children's handwriting images. This accuracies are
for the 5  of the 10 test images that were selected. (Photo 3121.jpg, Photo 3220 pg1.jpg, Story 3235 pg1.jpg, Photo 3202.jpg,Photo 3124 pg1.jpg)
The complete list is in `data README.md`. 
Model Name	                1       2       3       4       5
Tesseract - Base Model		2.58%	1.54%	1.88%	8.29%	0.00%
Google Vision		        80.00%	81.93%	81.93%	80.00%	95.65%
Custom Model with old data	2.02%	2.77%	1.88%	3.56%	0.00%
Custom Model with new data	2.03%	5.62%	1.88%	6.15%	0.00%

- The accuracies were doubled with preprocessing. (A blog post explaining on how to do this will be available
  to the onboarding cohort). The data pipeline in the `data management dir` was used for the preprocessing.
  In most causes sauvola thresholding (`sauvola_preprocessing`) works better than the regular binarization
  All preprocessing must include line removal. Use the data pipeline in the `data management dir`. complete
  directions will be included in a blog post.
  
- ## how to train the tesseract model

    - gpu box will be set up by the instructor
    - download the `pem` key to get permissions to get into the EE2 machine
    - In the terminal cd into the dir with the `pem` key and run the `ssh` command to get into the
      EE2 machine
    - git clone the ds repo ( If there is new data in repo, move it to `tesstrain\data\storysquad-ground-truth`dir)  
    - In root directory run the `source training_setup.sh` command
    - cd into tesstrain and activate virtual environment by running the command `source ocr\bin\activate`
      if it worked you should have switched to  `(ocr)` environment
    - In the `tesstrain` dir run this command to train the model `make training MODEL_NAME=storysquad START_MODEL=eng TESSDATA=/home/ubuntu/tesseract/tessdata`
    - Note: This takes about an hour to run. If you have any mismatches between ground_truth and snippet
      An error will be spit out. You need to go to the `storysquad-ground-truth` dir and fix the problem
      by either deleting or uploading a corresponding file. When that problem is fixed, just re-run the training
      command again and model will start from where an error was made. When the model gets to this point
      `At iteration 98/100/100, Mean rms=3.128%, delta=14.449%, char train=56.768%, word train=74.568%, skip ratio=0%, New best char error = 56.768 
      wrote best model:data/storysquad/checkpoints/storysquad56.768_98.checkpoint wrote checkpoint.
      Loaded 1/1 lines (1-1) of document data/storysquad-ground-truth/5220-1-014.lstmf
      Loaded 1/1 lines (1-1) of document data/storysquad-ground-truth/5220-1-014.lstmf`
      It has gone through all the files. There shouldn't any file related errors at this point.
    - once the model has finished training, the new model will be stored in `tesstrain\data`. The default 
      name right now is `storysquad.traineddata`. New models will overwrite the old ones if they are not not
      moved to another directory or renamed.
      
## how to run OCR-performance script in the EC2 box

- first things first : move your new model from `tesstrain/data` dir to `tessract\tessdata` dir
- Make sure your test pair (full image to be transcribed and ground-truth) are uploaded to the `tesstrain\dat`
  dir. You can create a dir for your test pairs in the `tesstrain/data` dir
- cd to (`tesstrain/data`)  
- note: make sure you activated the OCR environment and run `source  training_setup.sh`  
- Install the following packages ipython (`pip install ipython`), pytesseract `pip install pytesseract`,
  openCV (`pip install opencv`). If you get an error while trying to install any of these, you might be 
  required to upgrade pip (`pip install --upgrade pip`)
- run `ipython` command
- copy `ocr-inference.py` script found in `custom_tesseract_training/ocr-inference.py` and paste it in
  command line
- Note: if you have this error `ImportError: libGL.so.1: cannot open shared object file: No such file or directory`
  These two commands should fix it. run `sudo apt-get update` and then run `sudo apt-get install ffmpeg libsm6 libxext6 -y`
  Also note that you will have an error if the image path and custom model names (`lang = 'storysquad'` are incorrect
- There is an updated `ocr_inference.py` script, `models_comparison.py` found in the `models_comparison.py` which will
  let you compare multiple images and models including google vision OCR. check the `model_comparison` dir for
  instructions on how to run it in your IDE.
  
##what is next?
    - create more training data
    - build a preprocessing pipeline
    - hyperparameter tuning
    - automate the OCR_performance record process and connect the it an database

  
  
  



