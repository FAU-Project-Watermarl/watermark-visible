#!/bin/bash

set -xe

docker build . -t watermark-python
docker run -i --name watermark watermark-python  
# python shuffledWatermark.py | tee shuffle.txt
# python extractWatermark.py | tee extract.txt

#docker cp watermark:app/shuffle.txt '/c/Users/mhcd1/OneDrive/Desktop/FAU Classes/06 Spring 2023/ENG 44950  Engineer design/Watermark-Group-Project/WEB-APP/Docker/videos'
#docker cp watermark:app/extract.txt '/c/Users/mhcd1/OneDrive/Desktop/FAU Classes/06 Spring 2023/ENG 44950  Engineer design/Watermark-Group-Project/WEB-APP/Docker/videos'
docker cp watermark:app/extract.txt ../public/videos
# docker cp watermark:app/watermarkedVideoA.mp4 '/c/Users/mhcd1/OneDrive/Desktop/FAU Classes/06 Spring 2023/ENG 44950  Engineer design/Watermark-Group-Project/WEB-APP/Docker/videos'
# docker cp watermark:app/watermarkedVideoB.mp4 '/c/Users/mhcd1/OneDrive/Desktop/FAU Classes/06 Spring 2023/ENG 44950  Engineer design/Watermark-Group-Project/WEB-APP/Docker/videos'
docker cp watermark:app/watermarkedVideoA.mp4 ../public/videos
docker cp watermark:app/watermarkedVideoB.mp4 ../public/videos
# docker cp watermark:app/shuffledWatermarkOutput.mp4 '/c/Users/mhcd1/OneDrive/Desktop/FAU Classes/06 Spring 2023/ENG 44950  Engineer design/Watermark-Group-Project/WEB-APP/Docker/videos'
docker cp watermark:app/shuffledWatermarkOutput.mp4 ../public/videos
docker cp watermark:app/lowWatermarkedVideoB.mp4 ../public/videos
docker cp watermark:app/lowWatermarkedVideoA.mp4 ../public/videos
#docker cp watermark:app/. ../public/videos
docker stop watermark
docker container rm watermark

exit