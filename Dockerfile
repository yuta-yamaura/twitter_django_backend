FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
# 作業ディレクトリの設定
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
# ファイルをコピー
COPY . .
# データベースファイルを永続化するためのボリュームを作成
VOLUME /app/db_data
ADD . /config/