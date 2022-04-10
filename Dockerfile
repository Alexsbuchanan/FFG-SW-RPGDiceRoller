FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app

RUN apt update -y && apt upgrade -y
RUN apt install git -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python main.py