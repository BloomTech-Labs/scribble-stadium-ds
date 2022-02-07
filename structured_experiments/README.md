# Structured Experiments Standards
## Purpose
### This format is intended to facilitate fast iteration over experiments by making documentation and experiment setup standardized. 

## Directory Structure
* Top level directory should be named using the date and time in the format YYYYMMDDHHMM which allows for uniquness.
* Place README and module directory inside top directory
* Top level should contain file intended for execution; ex "experiment.py"
* Create requirements.txt file at top level if new libraries are tested
* Utilize .gitignore for excluding items such as test images, venv, etc

### Experiment README should answer questions in the scientific method format within 2-3 sentences.
* Question
  * What question does the experiment seek to answer? ie "will increasing contrast help with text extraction?"
* Research
  * What research was done to learn about the question's requirements for testing?
* Hypothesis
  * Based on the research, what is the expected outcome?
* Test
  * Outline your experiment. This may require more than 2-3 sentences.
* Analyze
  * What outcome from the hypothesis do the results support?
  * What is the conclusion of the experiment?
* Share Results
  * Proofread all documentation
  * Review all custom code written for experiment
  * Create pull request for review on GitHub

## Experiments

### [Template Experiment - 202202070508](202202070508/)
#### This is the template. This directory can be copied and renamed for a new experiment.

###
####