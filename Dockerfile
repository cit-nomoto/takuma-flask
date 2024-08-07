FROM python:3.11.5-slim-bullseye

WORKDIR /takuma_app

# ホストのファイルをコンテナのtakuma_appディレクトリにコピー
COPY . .
# ホストのrequirements.txtをコンテナのtakuma_appディレクトリにコピー
RUN pip install -r requirements.txt

# Flaskのデバッグモードを有効にする（Pythonやhtmlの変更がブラウザのリロードだけで反映される）
ENV FLASK_DEBUG=1
# Flaskのアプリケーションファイルを指定
ENV FLASK_APP=main.py
