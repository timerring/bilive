FROM python:3.10-slim

LABEL maintainer="timerring"

WORKDIR /app

COPY . /app

COPY ./assets/msyh.ttf /usr/share/fonts/msyh.ttf

RUN apt-get update && apt-get install vim -y \
    && apt-get install -y ffmpeg \
    && apt-get install -y procps \
    && apt-get install lsof -y \
    && apt-get install curl -y \
    && pip install -r requirements.txt

ENV BILIVE_PATH=/app
ENV TZ="Asia/Shanghai"

EXPOSE 2233

CMD ["python", "-m", "src.upload.upload"]