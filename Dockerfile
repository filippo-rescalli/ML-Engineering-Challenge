FROM python:3.8.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt