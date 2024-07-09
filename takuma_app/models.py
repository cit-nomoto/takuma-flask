"""dbモデルの定義を行うモジュール"""
from flask_login import UserMixin # flask_loginのユーザ管理機能
from takuma_app import db # dbモジュールの読み込み

# Countテーブルの定義 (アクセスカウンタ用)
class Count(db.Model):
    """アクセスカウンタ用テーブル"""
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

# Userテーブルの定義
class User(db.Model, UserMixin): # UserMixinを継承(flask_loginのユーザ管理機能を使用するため)
    """ユーザ情報テーブル"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
