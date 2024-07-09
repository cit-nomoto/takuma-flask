from takuma_app import app # app.pyからappをimport

if __name__ == '__main__': # このファイルが直接実行された場合
    app.run(host='0.0.0.0') # ホストを指定してFlaskアプリケーションを起動
