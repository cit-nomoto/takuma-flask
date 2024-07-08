from takuma_app import db # dbモジュールの読み込み
from flask_login import UserMixin # flask_loginのユーザ管理機能

# Userテーブルの定義 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
   
