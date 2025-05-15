FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
# 作業ディレクトリの設定
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /config/