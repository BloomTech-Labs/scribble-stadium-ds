FROM scribble-ocr-train as tesseract_base_image

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY experiment.sh /train/tesstrain/experiment.sh
COPY synthetic_data_generator.py /train/tesstrain/synthetic_data_generator.py
CMD ["sh" "/train/tesstrain/experiment.sh"]
