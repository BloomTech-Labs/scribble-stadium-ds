# Structured Experiments Format
## Purpose
### This format is intended to facilitate fast iteration over experiments by standardizing documentation and experiment setup. 

## Directory Structure
### Copy the template experiment named "2022.02.01.test" and work from the copied files, renaming the folder YYYY.MM.DD.experiment-name

### The experiment should also elaborate the following sections within 2-3 sentences. It must also contain an html comment with a short description like the following example.
#### Example: \<!--DESC Does Some Stuff--\>
#### The DESC is used by the update routine to extract the description while leaving other comments intact and must be included for automatically populating this document.

* Hypothesis
  * What are the conditions and expected outcome of the experiment?
* Methodology
  * How is the experiment set up?
  * What tests will be run and how?
* Results
  * What was the actual outcome without considering what was expected?
* Conclusions
  * Does the outcome support the hypothesis?
  * Why or why not?
* Reproduce
  * Start over by building your docker container and running the model to ensure reproducibility 
  * Run docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.02.01.test/docker-compose.yml up --build train_test_experiment to train a tesseract model using provided sample of kaggle data

## Experiments

### [Template Experiment - 202202070508](2022.02.01.test/)
#### This is the template. This directory should be copied and renamed for a new experiment.
