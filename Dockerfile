FROM python:3.10-slim

LABEL maintainer="timerring"

WORKDIR /app

COPY . /app

COPY ./assets/msyh.ttf /usr/share/fonts/msyh.ttf

RUN apt-get update && apt-get install -y \
    ffmpeg \
    procps \
    lsof \
    curl \
    vim \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV BILIVE_PATH=/app
ENV TZ="Asia/Shanghai"

EXPOSE 2233

CMD ["python", "-m", "src.upload.upload"]