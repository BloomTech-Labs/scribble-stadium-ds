echo 'Setting Up Synthetic Test Data for Tesseract Training'
python synthetic_data_generator.py /train/tesstrain/data/synthetic-ground-truth
echo 'Training Synthetic Test Model'
make training MODEL_NAME=synthetic START_MODEL=eng TESSDATA=/train/tessdata
echo 'Finished'