"""ビュー関数を記述するモジュール"""
from flask import render_template, redirect, request, flash # flask基本機能のインポート
from flask_login import login_user, logout_user, login_required, UserMixin, LoginManager, current_user # flaskのログインマネージャ, セッション管理用のライブラリなどもあるが手っ取り早いので使用
from takuma_app import app, db # 必須モジュールのロード
from takuma_app.models import User, Count # Userテーブルモデルの読み込み(ORM用)
from takuma_app.predict.predict_sales import predict_sales # 売上予測関数

# ヘルパー関数
def get_user_by_username(username):
    """ユーザ名からユーザ情報を取得する"""
    return User.query.filter_by(username=username).first()

def update_current_user(field, value):
    """現在のユーザ情報を更新する"""
    setattr(current_user, field, value) # ユーザ情報を更新
    db.session.commit()

# エンドポイントを記載
@app.route('/')
def index():
    """トップページ"""
    #　アクセスカウンタの取得
    count = Count.query.filter_by(id=1).first() or Count(id=1, count=0)
    count.count += 1
    db.session.commit()
    # render_templateでtemplatesフォルダ内のhtmlを返す
    return render_template('index.html', count=count)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """新規登録画面"""
    # POSTされた時ユーザ登録処理へ
    if request.method == 'POST':
        # フォームからユーザ名とパスワードを取得
        # ちょっと癖のある変数定義, (x, y) = (a, b) は x = a, y = b と同義
        (username, password) = (request.form['username'], request.form['password'])
        #　クエリ実行, usernameが一致するレコードの一番上を取得
        exist_user = User.query.filter_by(username=username).first()
        # 該当した場合メッセージを出力してリダイレクト
        if exist_user :
            flash('既にそのユーザー名が存在します')
            return redirect('/register')
        # userの追加
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('ユーザー登録完了')
        return redirect('/login')
    # テンプレートエンジンを使ってregister.htmlを描画
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ログイン画面"""
    if request.method == 'POST':
        (username, password) = (request.form['username'], request.form['password'])
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            flash('ユーザーが存在しないか、パスワードが間違っています')
            return redirect('/login')
        # セッション情報の追加
        login_user(user)
        return redirect('/mypage')
    return render_template('login.html')

@app.route('/logout')
@login_required # ログインしていないとアクセスできない
def logout():
    """ログアウト処理"""
    # セッション情報の削除
    logout_user()
    return redirect('/')

@app.route('/mypage')
@login_required
def mypage():
    """マイページ"""
    # セッション情報からログインしているユーザのusernameを取得
    showname = current_user.username
    # shownameに代入してテンプレートを出力
    return render_template('mypage.html', showname=showname)

@app.route('/mypage/edit/username', methods=['GET', 'POST'])
@login_required
def edit_username():
    """ユーザ名の変更画面"""
    if request.method == 'POST':
        new_username = request.form['new_username']
        update_current_user('username', new_username)
        db.session.commit()
        return redirect('/mypage')
    return render_template('edit/username.html')

@app.route('/mypage/edit/password', methods=['GET', 'POST'])
@login_required
def edit_password():
    """パスワードの変更画面"""
    if request.method == 'POST':
        new_password = request.form['new_password']
        # 現在のユーザのレコードを更新
        update_current_user('password', new_password)
        db.session.commit()
        return redirect('/mypage')
    return render_template('edit/password.html')

@app.route('/mypage/delete', methods=['GET', 'POST'])
@login_required
def delete_user():
    """ユーザ削除画面"""
    if request.method == 'POST':
        # 現在のユーザのレコードを削除
        db.session.delete(current_user)
        db.session.commit()
        return redirect('/')
    return render_template('delete.html')

@app.route('/mypage/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """売上予測画面"""
    if request.method == 'POST':
        (store_id, item_id) = (int(request.form['store_id']), int(request.form['item_id']))
        date = request.form['date']
        # /takuma_app/predict/predict_sales.pyから予測を行う関数を呼び出す
        predictions = predict_sales(store_id, item_id, date)
        # メッセージの記述
        prediction_message = f"店舗番号{store_id}の商品番号{item_id}は{predictions[0]}個売れます！！"
        # テンプレートに代入して出力
        return render_template(
            'predict.html',
            predictions=predictions,
            prediction_message=prediction_message
            )
    return render_template('predict.html')
