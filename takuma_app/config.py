"""コンフィグを記載したモジュール"""
class Config:
    """コンフィグクラス"""
    SECRET_KEY = 'test-secret-key'
    # db種別://ユーザ名:パスワード@接続先/db名
    # docker-composeでは、localhostの代わりにコンテナ名が接続先になる
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@takuma-db:3306/sampledb'
    # オブジェクトの変更を追跡する機能、メモリを追加で喰うため推奨はFalse
    SQLALCHEMY_TRACK_MODIFICATIONS = False
