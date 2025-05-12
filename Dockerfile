FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
WORKDIR /config
ADD requirements.txt /config/
RUN pip install -r requirements.txt
ADD . /config/