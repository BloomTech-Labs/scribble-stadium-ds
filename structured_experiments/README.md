# Structured Experiments Standards
## Purpose
### This format is intended to facilitate fast iteration over experiments by standardizing documentation and experiment setup. 

## Directory Structure
* Top level directory should be named using the date and time in the format YYYYMMDDHHMM allowing for uniqueness.
* Place README and module directory inside top directory
* Top level should contain file intended for execution
* Create requirements.txt file at top level if new libraries are tested
* Utilize .gitignore for excluding items such as test images or scratch files

### Experiment README should answer questions in the scientific method format within 2-3 sentences.
* Question
  * What question does the experiment seek to answer? ie "will doing A help do B?"
* Research
  * What research was done to learn more about the question?
* Hypothesis
  * Based on research, what is the expected outcome?
* Test
  * Outline your experiment. This may require more than 2-3 sentences.
* Analyze
  * What outcome from the hypothesis do the results support?
  * What is resulting conclusion?
* Share Results
  * Proofread all documentation
  * Review all custom code written for experiment
  * Create pull request for review on GitHub

## Experiments

### [Template Experiment - 202202070508](202202070508/)
#### This is the template. This directory can be copied and renamed for a new experiment.

### [Color Mask Test - 202202010600](202202010600/)
#### Attempt to remove specific colors to mask lined paper.