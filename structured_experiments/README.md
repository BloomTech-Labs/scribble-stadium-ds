# Structured Experiments Standards
## Purpose
### This format is intended to facilitate fast iteration over experiments by standardizing documentation and experiment setup. 

## Directory Structure
###This should mirror the structure of the template experiment named "2022.02.01.test" and include any new files needed to test new ideas.

### Experiment README should answer questions in the scientific method format within 2-3 sentences.

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

### [Template Experiment - 202202070508](202202070508/)
#### This is the template. This directory can be copied and renamed for a new experiment.

### [Color Mask Test - 202202010600](202202010600/)
#### Attempt to remove specific colors to mask lined paper.