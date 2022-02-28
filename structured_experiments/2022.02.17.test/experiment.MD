# Hypothesis

Larger dataset produces higher model accuracy. kaggle dataset of over 40000 will lead to a higher accuracy
compared with storyaquad data of 500. This will serve as a baseline to text bigger dataset.

# Methodology

Kaggle data at  https://www.kaggle.com/ssarkar445/handwriting-recognitionocr has 400000 training data and 40000 testing data. For the purpose of this experiment the testing data of 40000 together with the corresponding csv data was used. 

The script in the file 'setup_ground_truth.py' is useful to open the kaggle data and to also read the CSV file.
It is useful for replacing file types "jpg" and "png" with "gt.txt".

From the main github branch run the command in # Reproduce to train your model. Some of the data cannot be read by tesseract which will output an error. The data can be manually removed and the process restarted or a code can be written to allow the training to continue uninterrupted.

# Results

At iteration 6665/10000/10000, Mean rms=1.708%, delta=6.109%, char train=33.509%, word train=60.683%, skip ratio=0%,  New worst char error = 33.509 wrote checkpoint.
test_experiment          | Finished! Error rate = 32.122
test_experiment          | Loaded 1/1 lines (1-1) of document data/kaggle-ground-truth/TEST_39432.lstmf
test_experiment          | num_docs > 0:Error:Assert failed:in file imagedata.cpp, line 658
test_experiment          | make: *** [Makefile:292: data/kaggle/checkpoints/kaggle_checkpoint] Illegal instruction
test_experiment          | make: *** Deleting file 'data/kaggle/checkpoints/kaggle_checkpoint'
test_experiment          | Finished


# Conclusions
The Character error rate is 33.509% and the accuracy rate of the model is 66.5%

# Reproduce

- Run `docker-compose -f docker-compose.yml build train && docker-compose -f structured_experiments/2022.02.17.test/docker-compose.yml up --build train_test_experiment` to train a tesseract model using provided sample of kaggle data
