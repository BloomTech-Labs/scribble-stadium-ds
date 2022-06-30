FROM scribble-ocr-train:latest as tesseract_base_image
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY experiment.sh /train/tesstrain/experiment.sh
COPY synthetic_data_generator.py /train/tesstrain/synthetic_data_generator.py
#Copy csv to the docker
COPY word_bank_02may2022.json /train/tesstrain/word_bank.json
CMD ["sh" "/train/tesstrain/experiment.sh"]