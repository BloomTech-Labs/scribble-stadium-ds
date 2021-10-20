
# Run this dockerfile using the command below from repo root
# docker-compose -f docker.dev.yml up -d
# After complete running the build run the command below
# docker exec -ti scribble-ocr bash
# to access the container

# Set docker image
FROM ubuntu:18.04

# Skip the configuration part
ENV DEBIAN_FRONTEND noninteractive

# Update and install depedencies
RUN apt-get update && \
    apt-get install -y wget unzip bc vim python3-pip libleptonica-dev git zsh curl python3-venv

# Packages to complie Tesseract
RUN apt-get install -y --reinstall make && \
    apt-get install -y g++ autoconf automake libtool pkg-config libpng-dev libjpeg8-dev libtiff5-dev libicu-dev \
        libpango1.0-dev autoconf-archive

# Set working directory
WORKDIR /app

# Copy requirements into the container at /app
COPY requirements.txt ./

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
    python3 -m venv ocr && \
    mkdir data && cd data  && \
    cd /usr/local/share/tessdata && wget https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata_fast/blob/65727574dfcd264acbb0c3e07860e4e9e9b22185/osd.traineddata && \
    mv /usr/local/share/tessdata/ /train

# Setting the TESSDATA_PREFIX prefix
ENV TESSDATA_PREFIX=/train/tessdata

# Installing libraries can happen later due to specific version not been able to install
RUN python3 -m pip install --upgrade pip

# Set the locale
RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
