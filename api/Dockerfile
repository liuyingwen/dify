FROM python:3.10-slim

LABEL maintainer="takatost@gmail.com"

ENV FLASK_APP app.py
ENV EDITION SELF_HOSTED
ENV DEPLOY_ENV PRODUCTION
ENV CONSOLE_API_URL http://127.0.0.1:5001
ENV CONSOLE_WEB_URL http://127.0.0.1:3000
ENV SERVICE_API_URL http://127.0.0.1:5001
ENV APP_API_URL http://127.0.0.1:5001
ENV APP_WEB_URL http://127.0.0.1:3000

EXPOSE 5001

WORKDIR /app/api

RUN touch /etc/apt/sources.list
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update && \
    apt-get install -y bash curl wget vim gcc g++ python3-dev libc-dev libffi-dev nodejs

COPY requirements.txt /app/api/requirements.txt

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . /app/api/
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ARG COMMIT_SHA
ENV COMMIT_SHA ${COMMIT_SHA}

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]