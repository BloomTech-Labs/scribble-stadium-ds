# pull official base image
FROM python:3.8-slim-buster

# set working directory
WORKDIR /usr/src/app

# install python dependencies
RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt && \
python -m nltk.downloader punkt && \
python -m nltk.downloader averaged_perceptron_tagger

# add app
COPY . .
