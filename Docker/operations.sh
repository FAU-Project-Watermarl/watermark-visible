#!/bin/bash

set -xe

docker build . -t watermark-python
docker run -it --name watermark watermark-python  
# python shuffledWatermark.py | tee shuffle.txt
# python extractWatermark.py | tee extract.txt

docker cp watermark:app/shuffle.txt '/c/Users/mhcd1/OneDrive/Desktop/FAU Classes/06 Spring 2023/ENG 44950  Engineer design/Watermark-Group-Project/WEB-APP/Docker'
docker cp watermark:app/extract.txt '/c/Users/mhcd1/OneDrive/Desktop/FAU Classes/06 Spring 2023/ENG 44950  Engineer design/Watermark-Group-Project/WEB-APP/Docker'