FROM scribble-ocr-train as tesseract_base_image

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY mytesseract mytesseract
RUN cd mytesseract &&  pip install .
CMD ["jupyter", "notebook", "--allow-root"]
