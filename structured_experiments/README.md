#Structured Experiments
##How to use the template folder
- Copy the template folder within your branch
- Rename the folder to YYYY.MM.DD.<my_experiment> where <my_experiment> is the name of your experiment
- Add a brief (1 sentence) description at the top of the experiment.md file replacing the sample after DESC
- Create and/or include any files needed within the folder except data files
  - Data is set up in the docker compose file with different data streams being managed using git lfs
  - When using a different data set the volume must be set to that directory in the docker-compose under the volume label
- Edit the Dockerfile, docker-compose, experiment.sh, requirements files as needed for repeatability
- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/YYYY.MM.DD.my_experiment/docker-compose.yml up --build train_test_experiment` to train a tesseract model
  - change the directory `YYYY.MM.DD.my_experiment` to the directory which matches your experiment to train your model
- Document your experiment in the experiment.md file which can be renamed if needed

##Documenting Experiments
###Below are labels borrowed from the scientific method along with sample questions. These should be elaborated upon in 2-5 sentences.
- Hypothesis
  - What is being tested?
  - What results are expected?
- Methodology
  - How was the experiment performed?
  - Anything specific required during setup, runtime, etc?
- Results
  - What was the output of the experiment?
- Conclusions
  - What does the result tell you about the hypothesis?
  - Was the hypothesis correct? Why?
- Reproduce
  - Has the experiment been reproduced?
  - Does the reproduction support the original results?

<!--DO NOT CHANGE OR REMOVE ANYTHING BELOW THIS LINE-->
##Experiment Directory
###[2022.02.01.test](2022.02.01.test)
#### Template folder to use for experiments
