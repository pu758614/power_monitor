FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code

RUN apt-get update
RUN apt-get install -y vlc
RUN apt-get install -y nano
RUN pip install --upgrade pip
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get install -y cron

RUN crontab -l | { cat; echo '0 5 * * * /usr/local/bin/python /code/sync_api_data_script.py'; } | crontab


COPY . /code/