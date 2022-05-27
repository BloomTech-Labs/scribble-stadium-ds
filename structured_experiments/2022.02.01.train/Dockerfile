FROM scribble-ocr-train as tesseract_base_image

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY experiment.sh /train/tesstrain/experiment.sh
COPY setup_ground_truth.py /train/tesstrain/setup_ground_truth.py
COPY test_model.py /train/tesstrain/test_model.py
CMD ["sh" "/train/tesstrain/experiment.sh"]
