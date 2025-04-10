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
    gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 2233

ENV TZ="Asia/Shanghai"

CMD ["./start.sh"]