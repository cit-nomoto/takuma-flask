"""必須モジュールの読み込み"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__) # Flaskアプリケーションのインスタンスを生成
app.config.from_object('takuma_app.config.Config') # configから, mysqlの接続情報読み込み

# SQLAlchemy関連
db = SQLAlchemy(app) # SQLAlchemyのインスタンスを生成

# ログインマネージャ関連
login_manager = LoginManager(app) # ログインマネージャのインスタンスを生成
login_manager.login_view = 'login'  # ログインページのエンドポイントを指定

from . import views, models

@login_manager.user_loader # ログインマネージャのユーザローダー
def load_user(user_id):
    """ユーザIDからユーザ情報を取得する"""
    return models.User.query.get(int(user_id)) # models.pyからUserテーブルを取得

def create_tables():
    """テーブルを作成する"""
    with app.app_context(): # アプリケーションコンテキストを取得
        db.create_all() # テーブルを作成

create_tables()
