#Research question: 
Is it possible to design a model to replace user input in [story_photo_transformer.py](../../../data_management/story_photo_transformer.py) and result in comparable transformed image quality?
is it possible using the sythetic dataset provided by generate.py and samples of user input provided by
story_photo_transformer.py to generate coordinates with less than 8pix mean average error.

##Assumptions:
(these should be tested but time does not allow)
1) A 3 layer fully connected network of 32 neurons each will not provide a low enough MAE
2) training on less than 1000 samples without synthetic data on any architecture will not provide low enough MAE
##Hypthoses:
1) Training a 3 layer fully connected network on synthetic data first will improve MAE on user generated data.
2) Adding convolution layers to the beginning of the model will improve MAE to below baseline levels
3) converting the input to grayscale and providing x and y axis value distribution information will lower MAE
   compared to the baseline model
4) Slicing the image into slices of 1/3 and only giving the model the corners will lower MAE of the baseline
##Testing environment
The notebooks for these hypotheses will be in the same root folder as this document, and will
possess the following basic structure.
- Results of !pip list
- System information, OS, CPU, GPU
- Statement of Hypothesis to be tested
  - explanation of how it relates to research question
- cells to load data sets
  - each cell will have an explanation of data that is loaded
- Summery of experiments to be performed
- Experimental sections contain
  - statement of experiment
    - how it relates to hypothesis 
  - Explanation of methodology
  - code cells to execute experiment
  - analysis of experimental results
- Analysis section explaining results and proving/disproving the hypothesis

## Hypotheses notebooks
1) does_synthetic_data_improve_mae.ipynb will test, "Training a 3 layer fully connected network on synthetic data first will improve MAE on user generated data."
   1) This notebook will establish the baseline model which will include
      1) training over 1000 epochs
      2) training completed with random initialization as well as constant intialization
      3) will provide a range of expected scores
      4) will use model performance on the user generated dataset as the validation score.
      
2) conv_layers_improve_mae.ipynb will test, "Adding convolution layers to the beginning of the model will improve MAE to below baseline levels."
   1) This notebook will compare the results of 3 different convolutional models to the baseline model
3) grayscale_will_improve_mae.ipynb will test, "converting the input to grayscale and providing x and y axis value distribution information will lower MAE compared to the baseline model."
   1) this notebook will convert the dataset to black and white first and then test vrs the baseline model
4) sliceing_will_improve_mae.ipynb will test, "Slicing the image into slices of 1/3 and only giving the model the corners will lower MAE of the baseline."
   1) this notebook will provide a model that slices the input up and and test it against the baseline model
