echo 'Setting Up Kaggle Test Data for Tesseract Training'
python setup_ground_truth.py /train/tesstrain/data/kaggle-ground-truth
echo 'Training Kaggle Test Model'
make training MODEL_NAME=kaggle START_MODEL=eng TESSDATA=/train/tessdata MAX_ITERATIONS=100
cp data/kaggle.traineddata /train/tessdata/kaggle.traineddata
echo 'Finished Training Model'
echo 'Testing Kaggle Model'
python test_model.py
echo 'Finished Testing Model'