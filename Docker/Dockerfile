FROM python:bullseye  

WORKDIR /app

COPY ./app/ .
COPY ./entrypoint.sh .

EXPOSE 5678

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN chmod a+x ./entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]