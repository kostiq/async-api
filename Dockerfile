FROM python:3-slim

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY async-api async-api