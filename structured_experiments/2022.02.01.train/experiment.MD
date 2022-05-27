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

## Linux & OSX

### First Acquire the training data
Run `git lfs pull --exclude .git -I  data/storysquad-ground-truth/`

This will use git-lfs to pull down all the client given training images

### Execute the training container
- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.02.01.template/docker-compose.yml up --build train_test_experiment` to train a tesseract model using provided sample of kaggle data

## Windows (Powershell)

### First Acquire the training data
Run `git lfs ls-files -n -I data/storysquad-ground-truth | ForEach-Object { git lfs pull --exclude *.tiff -I $_}`

This will use git-lfs to pull down all the client given training images

### Execute the training container
- Run `docker-compose -f docker-compose.yml build train; docker-compose -f structured_experiments/2022.02.01.template/docker-compose.yml up --build train_test_experiment` to train a tesseract model using provided sample of kaggle data