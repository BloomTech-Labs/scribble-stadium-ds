FROM scribble-ocr-train as tesseract_base_image

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY experiment.sh /train/tesstrain/experiment.sh
COPY setup_ground_truth.py /train/tesstrain/setup_ground_truth.py
COPY synthetic_data_generator.py /train/tesstrain/synthetic_data_generator.py
CMD ["sh" "/train/tesstrain/experiment.sh"]
