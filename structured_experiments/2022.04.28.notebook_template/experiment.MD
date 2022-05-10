<!--DESC Template folder to use for experiments-->
# Hypothesis
TODO: Create Template

# Methodology

TODO: Create Template

# Results

TODO: Create Template

# Conclusions

TODO: Create Template



# Reproduce

## 1. First Acquire the training data

### 
Run `git lfs pull --exclude .git -I  data/storysquad-ground-truth/`

This will use git-lfs to pull down all the client given training images

## 2. Execute the notebook container

### Linux & OSX
- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.04.28.notebook_template/docker-compose.yml up --build --force-recreate training_notebook` to start a docker container hosting Jupyter which you can use to view notebooks

### Windows (Powershell)

- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.04.28.notebook_template/docker-compose.yml up --build --force-recreate training_notebook` to train a tesseract model using provided sample of kaggle data

## 3. Open Jupyter and the Notebook

* Copy and paste the link in your shell beginning with `http://127.0.0.1:8888...` into your browser
* Open 
* Click run all to run model and output test metrics. 