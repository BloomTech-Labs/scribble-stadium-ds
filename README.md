## Story Squad - Data Science
[![Maintainability](https://api.codeclimate.com/v1/badges/146d9feb7549b988077a/maintainability)](https://codeclimate.com/github/Lambda-School-Labs/Labs26-StorySquad-DS-TeamB/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/146d9feb7549b988077a/test_coverage)](https://codeclimate.com/github/Lambda-School-Labs/Labs26-StorySquad-DS-TeamB/test_coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Story Squad Banner](assets/story_squad_banner.png)](http://www.youtube.com/watch?v=-cDqvmmtuiE)


### About
The repository contains a **Rest API** (`app/`), **OCR Model Training Pipeline**  (`data/ and data_management/`), and a series of **dockerized OCR modeling experiments** (`structured_experiments/`). 

### Brief History
[Story Squad](https://www.storysquad.education/) is the dream of a former teacher, Graig Peterson, to create opportunities for children to have creative writing and drawing time off-screen. Here's how it works: child users of the website are provided a new chapter in an ongoing story each weekend. They read the story, and then follow both a writing and drawing prompt to spend an hour off-screen writing and drawing. When they're done, they upload photos of each, and this is where our data science team comes in. The stories are transcribed into text, analyzed for complexity, screened for inappropriate content, and then sent to a moderator. Once all submissions have been checked over on moderation day, our clustering algorithm groups the submissions by similar complexity and creates Squads of 4 to head into a game of assigning points and voting for the best submissions in head-to-head pairings within the cluster! Then it starts all over again the following weekend.

**Want to hear an overview of all our project features?** Click the Story Squad banner above for a link to our product video from 10/22/20! Or keep scrolling to read more thorough information on each feature.

## Quickstart Guide

### Required Dependencies

- [Docker](https://docs.docker.com/get-docker/)
- [Git LFS](https://git-lfs.github.com/)

Clone the repository by running the following on Linux/OSX:

`GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/BloomTech-Labs/scribble-stadium-ds.git`

or the following on Windows:

```posh
set GIT_LFS_SKIP_SMUDGE=1  
git clone https://github.com/BloomTech-Labs/scribble-stadium-ds.git
```

**☝️ use the above to avoid downloading all training data**

### Running Data Science Code
Each of the components of this repository have been dockerized and can be intialized by executing the correct docker command.

#### Running API


#### Running Model Training Base Container
A Docker base image has been created that bundles Tesseract with all the necessary python libraries to train a model. The following will build the image locally.

`docker-compose -f docker-compose.yml up --build -d train`

Once the docker completes building the image, run the container using the following command:-

`docker exec -ti scribble-ocr-train bash`

This will place your shell inside of the running docker container (debian operating system). The directory structure of the container is shown below:-

------------

    │
    └── train              <- directory with tools to train the tesseract ocr
        │
        ├── tessdata       <-  directory that house all the models. Currently only
        │                      eng.trainedata is available. The trained models are placed here. 
        │
        ├── tesstrain      <- tesstrain directory through which the training will be
        │                     run.
        │                   
        └── data           <- house `storysquad-ground-truth` which has all the training
                              material for tesseract to learn from. This directory is mounted 
                              from `scribble-stadium-ds/data`. More data can be uploaded if 
                              it becomes available.
     
--------

To train a model from within the container use:

`make training MODEL_NAME=storysquad START_MODEL=eng TESSDATA=/train/tessdata`

To use a different trainingset than `storysquad`, add another folder within the `data/` folder of this repository named `<MODEL_NAME>-ground-truth`. Then you can use your new `MODEL_NAME` as an input in the make command above. You can test this with `MODEL_NAME=testsquad`. This should start runnign correctly and fail because there are not enough examples to train a model.

Additionally you can replace layers of the LSTM model by using the `make finetune` route.

`make finetune MODEL_NAME=storysquad START_MODEL=eng TESSDATA=/train/tessdata`

You can also optionally specifiy the following arguments to more granularly control the network structure. For more information on this see [here](https://tesseract-ocr.github.io/tessdoc/tess4/TrainingTesseract-4.00.html#lstmtraining-command-line)

- *FINETUNE_INDEX* - Essentially the number of layers from the original LSTM model to keep. By default that LSTM has 7 layers and the default index is to keep 5
- *FINETUNE_LAYERS* - The layers you'd like to append to the end of the existing network. Default is `[Lfx256 O1c111]`

☝️ The default parameters keep 5 of the 7 original layers and introduce 2 smaller ones to the end of the network(LSTM 256 Output Layer and softmax layer).


For hyperparameter tuning refer https://tesseract-ocr.github.io/tessdoc/tess4/TrainingTesseract-4.00.html#lstmtraining-command-line

#### Running a Structured Experiment
A series of completed experiments exist within folders in `structured_experiments/`. Each folder represents an experiment completed in the hopes of identifying succesful strategies for training better handwriting OCR models. Each experiment is dockerized and can be executed via docker commands. The `experiment.MD` file in each experiment folder provides a detailed overview of what the experiment does, the conclusions drawn, and commands to recreate it.   To run the template experiment `2022.02.01.test`, simply run the command provided:

`docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.02.01.test/docker-compose.yml up --build train_test_experiment`

Or on Windows:

`docker-compose -f docker-compose.yml build train; docker-compose -f structured_experiments/2022.02.01.test/docker-compose.yml up --build train_test_experiment``docker exec -ti scribble-ocr-train bash`

For information on how to build your own experiment, please consult the contribution guide located in the wiki [here](https://github.com/BloomTech-Labs/scribble-stadium-ds/wiki)
 

#### Support 
For more information on developing with scribble stadium. Please visit the wiki [here](https://github.com/BloomTech-Labs/scribble-stadium-ds/wiki)


## License
 
The MIT License (MIT)

Copyright (c) 2015 Chris Kibble

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.




