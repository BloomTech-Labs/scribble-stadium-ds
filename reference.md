## Purpose
The DS side of Scribble Stadium has a somewhat larger repo compared to other projects. As such, we wanted to make a quick 
reference guide to help make the transition easier. We hope you find this helpful in your Scribble
adventures!

## Contents
- `app`
- `assets`
- `data`
- `data_management`
- `models`
- `notebooks`
- `structured_experiments`
- `tesstrain`


### `app`
**The `api` folder houses the endpoints that comprise the DS API:** 

- `clustering`: This endpoint takes a list of cohort and submission objects and then returns clusters based on cohort in groups of four.
- `db`: database functions : This gets a SQLAlchemy database connection. Uses this environment variable if it exists: `DATABASE_URL=dialect://user:password@host/dbname`. Otherwise uses a SQLite database for initial local development.
- `models`:  This contains endpoints for text and illustration submissions, along with line graph, histogram, and crop cloud requests.
- `submission`: Contains a function that takes a submission object and calls the Google Vision API to text annotate the passed s3 link, then passes those concatenated transcriptions to the SquadScore method. Also contains a function that checks the illustration against the Google Vision SafeSearch API and flags if explicit content is detected.
- `visualization`: This contains endpoints for Story Squad’s main visualizations: line graphs, histograms, and the crop cloud.
 
**The `app/tests` and `app/utils` folders house the tests and utility functions the API utilizes.**

### `assets`
**This folder is where some DS architecture and examples are housed in the `.png` format**

### `data`
**This folder contains the base image data and Scribble Stadium image data that Tesseract uses to train its OCR model**

### `data_management`
**The main folder is `autopreprocess_testing` which houses the preprocessing that was attempted by BloomTech learners. \
The other files in the directory are needed for the photo transformer `story_photo_transformer.py`, which is used in \
an experiment in the `structured_experiments` files**

### `models`
**This houses the different models tried throughout the project's lifetime. The `storysquadalldata4.traineddata` \
did the best; however, it still needs more work to be used on children's handwriting**

### `notebooks`
**Research was performed here in the different `.ipynb` files**

### `structured_experiments`
**Contains the experiments that Learners performed**

### `tesstrain`
**Has a modified tesseract Makefile for use in docker**
