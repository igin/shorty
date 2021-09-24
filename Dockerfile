FROM python:alpine

WORKDIR /app

RUN apk update
RUN apk add git

COPY requirements-dev.txt requirements-dev.txt
RUN pip3 install -r requirements-dev.txt

COPY app /app