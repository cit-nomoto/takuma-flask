from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__) # flask定義
app.config.from_object('takuma_app.config.Config') # configから, mysqlの接続情報読み込み

#db情報の定義
db = SQLAlchemy(app)

# ログインマネージャ関連
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # ログインページのエンドポイントを指定

from . import views, models

# ログインセッションの管理
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

# models.pyからUserテーブルを作成
def create_tables():
    with app.app_context():
        db.create_all()

create_tables()