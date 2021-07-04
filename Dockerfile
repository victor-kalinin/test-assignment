FROM python:3.8-slim

EXPOSE 3000
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./