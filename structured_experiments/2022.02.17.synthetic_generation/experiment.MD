# Hypothesis
More data helps machine learning to improve its accuracy. By artificially creating more
data this will help increase the data used to learn thus improving accuracy.

# Methodology

I've created a script that will create handwritten images based on the images from a folder and
inputted text. Some limitations that I could view is the fact that most character images are the same as other 
same character image. Would need to create different variations of the characters and possibly make connected character
images which would need the code to be edited to detect the characters next to it.
- To create more images add strings to the "list_of_string_pairs" under the "synthetic_data_generator.py".
It works with a pair of ([title], [string]).



# Results

Successfully created synthetic images and text file for each string. No images for upper case letters or many
special characters.

# Conclusions

This is a useful way of creating new data to help train the tesseract model.
Need more diverse ways of creating new strings to create more data.

# Reproduce

- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.02.17.synthetic_generation/docker-compose.yml up --build train_test_experiment` to train a tesseract model using synthetic data