# Hypothesis
More data helps machine learning to improve its accuracy. By artificially creating more
data this will help increase the data used to learn thus improving accuracy.

# Methodology


This is a continuation of previous experiment. The script created handwritten images based on the images from a folder and
inputted text. The limitations encountered on the previous experiment was that most character images are the same as other 
same character image. The prior experiment suggested to perform the following:

"Would need to create different variations of the characters and possibly make connected character
images which would need the code to be edited to detect the characters next to it".

This script creates a random amount of images and add strings to the "list_of_string_pairs" under the "synthetic_data_generator.py".
This list contains ([title], [string]). 

A word bank dictionary was created using multiple public datasets. See Read me for source of each dataset found. All rights reserved to the creators.

The word bank was utilized to generate random amount of sentenses and stored them to the "list_of_string_pairs". We can easily change the number of sentences generated.

The loop to create the sentences was modified to improve processing.



# Results

Successfully created synthetic images and text file for each string. No images for upper case letters or many
special characters. Model did not improve.

# Conclusions

This is a useful way of creating new data to help train the tesseract model. Nevertheless, adding more data did not help to reduce the error rate significally.


# Reproduce

- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.05.17.synthetic_generation/docker-compose.yml up --build train_test_experiment` to train a tesseract model using synthetic data


