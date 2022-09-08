<!--DESC Template folder to use for experiments-->
 Hypothesis
Building up my last notebook (2022.07.18), can I find a way to analyze exactly which
samples are contributing the most and least to the high character error rate?

# Methodology

I read the Jiwer documentation and found a way to use the Jiwer library to display character
error rates in the notebook

# Results

The character error rate is not capped at 100%. This means that some words are returning 
almost a 500% error rate, which is arguably skewing the data on the error rate of 88%.
When they are taken out, it drops the error rate to about 44%.

# Conclusions

It is possible that the Tesseract model is learning to "ignore" some of the data because of
how some of the words actively increase the error rates more than they should be.


# Reproduce
## 1. First Acquire the training data
### 
Run
- `git lfs pull --exclude .git -I  data/storysquad-ground-truth/`

- `git lfs pull --exclude .git -I  data/kaggle-ground-truth/`

This will use git-lfs to pull down all the client given training images

## 2. Execute the Template Experiment
### Linux & OSX
Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.02.01.template/docker-compose.yml up --build train_test_experiment`

### Windows (Powershell)
Run `docker-compose -f docker-compose.yml build train; docker-compose -f structured_experiments/2022.02.01.template/docker-compose.yml up --build train_test_experiment`
## 3. Execute the notebook container
### Linux & OSX
- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.08.18.notebook_template/docker-compose.yml up --build --force-recreate training_notebook` to start a docker container hosting Jupyter which you can use to view notebooks. Remember to be up in the /scribble-stadium-ds directory when doing this.

### Windows (Powershell)

- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.08.18.notebook_template/docker-compose.yml up --build --force-recreate training_notebook` to train a tesseract model using provided sample of kaggle data. Remember to be up in the /scribble-stadium-ds directory when doing this.

## 4. Open Jupyter and the Notebook

* Copy and paste the link in your shell beginning with `http://127.0.0.1:8888...` into your browser
* Open 
* Click run all to run model and output test metrics. 