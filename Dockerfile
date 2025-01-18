FROM python:3.10-slim

MAINTAINER timerring

WORKDIR /app

COPY . /app

COPY ./assets/msyh.ttf /usr/share/fonts/msyh.ttf

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install vim -y \
    && apt-get install -y ffmpeg \
    && apt-get install -y procps \
    && apt-get install lsof -y

ENV BILIVE_PATH=/app
ENV TZ="Asia/Shanghai"

EXPOSE 2233

CMD ["nohup", "python", "-m", "src.upload.upload", ">", "/app/logs/uploadLog/upload-$(date +%Y%m%d-%H%M%S).log", "2>&1", "&"]