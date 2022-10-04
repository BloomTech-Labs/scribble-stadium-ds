<!--DESC Template folder to use for experiments-->
 # Hypothesis:

Can I learn anything about the mechanism by which Tesseract is failing by observing \
the outputs of Tesseract and comparing them to the labeling and raw data?

# Methodology

In the Tesstest directory in the __init__.py, I made some changes to the test_model() \
function that is defined there so that the outputs of Tesseract are saved in lists.

I also changed the cells in the jupypter notebook as well to display a dataframe of the \
input raw data (ground_truth), labeling data, and the Tesseract output

To get the images to display in a nice way, I converted the image data into a sort of \
"HTML" link
# Results

The data was able to be nicely read in a DataFrame which I tweaked its appearance until \
it was easy to read

# Conclusions

Surprisingly, Tesseract was doing much better than I thought: it was getting all the correct words and letters\
for the most part.  Definitely much better than we believed by virtue of the 80% character error rate we were seeing.

The problem seemed to stem from Tesseract reading a bunch of extraneous text that was not part of the labeled text.


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
- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.07.19.notebook_template/docker-compose.yml up --build --force-recreate training_notebook` to start a docker container hosting Jupyter which you can use to view notebooks. Remember to be up in the /scribble-stadium-ds directory when doing this.

### Windows (Powershell)

- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.07.19.notebook_template/docker-compose.yml up --build --force-recreate training_notebook` to train a tesseract model using provided sample of kaggle data. Remember to be up in the /scribble-stadium-ds directory when doing this.

## 4. Open Jupyter and the Notebook

* Copy and paste the link in your shell beginning with `http://127.0.0.1:8888...` into your browser
* Open 
* Click run all to run model and output test metrics. 