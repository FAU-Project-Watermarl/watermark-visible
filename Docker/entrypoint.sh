#!/bin/bash

set -xe

ls

# Create virtuan enviroment
# python -m venv venv
# source venv/bin/activate

# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# install neccesary packages
# pip install opencv-python
# pip install pytesseract
# pip install ffmpeg
# apt install tesseract-ocr -y

#sudo apt install tesseract-ocr -y

# docker run -it --entrypoint bash watermark-python 

# python shuffledWatermark.py | tee shuffle.txt
# python extractWatermark.py | tee extract.txt


python shuffledWatermark.py | tee shuffle.txt
python extractWatermark.py | tee extract.txt



#docker build . -t watermark-python
# docker run -i --name watermark watermark-python 

#docker run --name watermark -d -i  watermark-python bash


# docker cp watermark:app/shuffle.txt /
# docker cp watermark:app/extract.txt /


#  docker run --name watermark -it --entrypoint bash watermark-python
#  docker run --name watermark -it -d --entrypoint bash watermark-python
