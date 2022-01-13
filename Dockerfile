
# Run this dockerfile using the command below from repo root for model training
# docker-compose -f docker-compose.yml up --build -d train
# After complete running the build run the command below
# docker exec -ti scribble-ocr-train bash
# to access the container
# For api testing run
# docker-compose -f docker-compose.yml up --build -d api
# Run this command within the command line once complete to start the container
# if it's not already running
# docker start scribble-ocr-api
# accessed from 127.0.0.1:8000

# Set docker image
FROM python:3.8-bullseye as tesseractbuild

# Skip the configuration part
ENV DEBIAN_FRONTEND noninteractive

# Update and install depedencies
RUN apt-get update && \
    apt-get install -y wget unzip bc vim libleptonica-dev git curl

# Packages to complie Tesseract
RUN apt-get install -y --reinstall make && \
    apt-get install -y g++ autoconf automake libtool pkg-config libpng-dev libjpeg62-turbo-dev libtiff5-dev libicu-dev \
        libpango1.0-dev autoconf-archive

# Set working directory
WORKDIR /app

# Compile Tesseract with training options
RUN cd .. && \
    mkdir train && cd train && \
    wget https://github.com/tesseract-ocr/tesseract/archive/4.1.1.zip && \
	unzip 4.1.1.zip && \
    cd tesseract-4.1.1 && ./autogen.sh && ./configure && make && make install && ldconfig && \
    make training && make training-install && \
    cd ..  && \
    git clone https://github.com/tesseract-ocr/tesstrain.git && \
    cd tesstrain && \
    mkdir data && cd data  && \
    cd /usr/local/share/tessdata && wget https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata_fast/blob/65727574dfcd264acbb0c3e07860e4e9e9b22185/osd.traineddata && \
    mv /usr/local/share/tessdata/ /train

RUN mkdir -p /train/langdata && cd /train/langdata && \
    wget https://raw.githubusercontent.com/tesseract-ocr/langdata_lstm/main/radical-stroke.txt && \
    wget https://raw.githubusercontent.com/tesseract-ocr/langdata_lstm/main/common.punc  && \
    wget https://raw.githubusercontent.com/tesseract-ocr/langdata_lstm/main/font_properties && \
    wget https://raw.githubusercontent.com/tesseract-ocr/langdata_lstm/main/Latin.unicharset  && \
    wget https://raw.githubusercontent.com/tesseract-ocr/langdata_lstm/main/Latin.xheights  && \
    mkdir eng && cd eng && \
    wget https://raw.githubusercontent.com/tesseract-ocr/langdata/main/eng/eng.training_text && \
    wget https://raw.githubusercontent.com/tesseract-ocr/langdata/main/eng/eng.punc && \
    wget https://raw.githubusercontent.com/tesseract-ocr/langdata/main/eng/eng.numbers && \
    wget https://raw.githubusercontent.com/tesseract-ocr/langdata/main/eng/eng.wordlist

RUN mkdir -p /usr/local/share/fonts/journal && \
    wget https://dl.dafont.com/dl/?f=journal -O /tmp/journal.zip && \
    unzip /tmp/journal.zip -d /usr/local/share/fonts/journal

# Update and install depedencies
RUN apt-get update && \
    apt-get install ffmpeg libsm6 libxext6 -y

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# Setting the TESSDATA_PREFIX
ENV TESSDATA_PREFIX=/train/tessdata

FROM tesseractbuild as tesseract_training
COPY start.sh /train/start.sh
WORKDIR /train/tesstrain

# Set docker image for api stage requirements for API testing
# Run this command within the command line
# docker start scribble-ocr-api
# API is accessed from 127.0.0.1:8000 through a web browser
FROM tesseractbuild as apitest

# Skip the configuration part
ENV DEBIAN_FRONTEND noninteractive

# Set working directory
WORKDIR /app
EXPOSE 8000
ENV GOOGLE_CREDS={}
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000


