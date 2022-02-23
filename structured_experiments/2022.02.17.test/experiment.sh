echo 'Setting Up Kaggle Test Data for Tesseract Training'
python setup_ground_truth.py /train/tesstrain/data/kaggle-ground-truth
echo 'Training Kaggle Test Model'
make training MODEL_NAME=kaggle START_MODEL=eng TESSDATA=/train/tessdata
echo 'Finished'