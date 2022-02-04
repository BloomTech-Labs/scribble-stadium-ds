# Hypothesis
TODO: Template

# Methodology

TODO: Template

# Results

TODO: Template

# Conclusions

TODO: Template



# Reproduce

- Got to [Kaggle OCR Dataset] and download *test* images and corresponding csv
- Place test images and label csv in data/kaggle-ground-truth in this repository (don't commit this)
- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.02.01.test/docker-compose.yml up --build train_test_experiment` to train a tesseract model using this data