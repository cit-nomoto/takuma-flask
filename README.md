Python(flask)+MySQLのWeb開発デモ
====
## Overview
Dockerを使用しFlaskとMySQLのコンテナを接続.  
基本的なユーザ管理機能と, デモ用データを用いての売上予測に対応. 

## Requirements
Docker-Composeが動く環境

## Usage
基本的には    
`docker-compose up --build`
後に  
`127.0.0.1:5000`
へアクセスすることでトップページが閲覧できる　　

## Description

画面は
- 初期画面　 
- 新規登録画面　
- ログイン画面
- マイページ
- パスワード変更画面
- ユーザ名変更画面
- ユーザ削除画面
- 売上予測画面

の計8つ. 

ディレクトリ構造は以下のようになっている. 
<pre>
.
├── Dockerfile
├── README.md
├── docker-compose.yml
├── requirements.txt
└── takuma_app
    ├── __init__.py
    ├── app.py
    ├── config.py
    ├── models.py
    ├── predict
    │   ├── predict_sales.py
    │   └── train_model.py
    ├── templates
    │   ├── base.html
    │   ├── delete.html
    │   ├── edit
    │   │   ├── password.html
    │   │   └── username.html
    │   ├── index.html
    │   ├── login.html
    │   ├── mypage.html
    │   ├── predict.html
    │   └── register.html
    ├── train.csv
    └── views.py
</pre>

使用パッケージ（requirements.txt）  
- Flask: Webフレームワーク
- flask_sqlalchemy: flask用ORM
- flask_login: flask用ログインマネージャ
- PyMySQL: mysql接続用
- cryptography: mysql接続用
- pandas: データフレーム操作
- scikit-learn: 機械学習アルゴリズム詰め合わセット
- joblib: モデル出力用


主なファイルは以下の通り  

環境構築関連
- `Dockerfile`: コンテナの構成ファイル、今回はpythonコンテナのみに使用
- `docker-compose.yml`: コンテナ間の連携用
- `requirements.txt`: pythonの必要パッケージを記載したテキスト, Dockerfileによりコンテナ構築時自動でインストールされる
  
flask関連
- `app.py`：サーバの実行
- `takuma_app/models.py`: DBテーブル関連のクラス  
- `takuma_app/views.py`: ルーティング関連（MVCで言うところのC）
- `takuma_app/templates`:htmlテンプレート
- `__init__.py`,`config.py`: DB, flask_loginの設定など
  
予測関連 
- `test.csv`: 売上予測デモ用学習データ(kaggle)
- `takuma_app/predict/`: 売上予測実施とモデル作成などのプログラム(基本的にはGoogle Colabと同じ)

