FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code

RUN apt-get update
RUN apt-get install -y vlc
RUN pip install --upgrade pip
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/