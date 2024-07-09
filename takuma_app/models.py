from takuma_app import db # dbモジュールの読み込み
from flask_login import UserMixin # flask_loginのユーザ管理機能

# Userテーブルの定義 
class User(db.Model, UserMixin): # UserMixinを継承(flask_loginのユーザ管理機能(ログイン、ログアウト)を使用するため)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Countテーブルの定義 (アクセスカウンタ用)
class Count(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
       return '<Count %r>' % self.id
