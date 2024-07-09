# flask基本機能のインポート
from flask import render_template, redirect, request, flash 
# flaskのログインマネージャ, セッション管理用のライブラリなどもあるが手っ取り早いので使用
from flask_login import login_user, logout_user, login_required, UserMixin, LoginManager, current_user 
# 必須モジュールのロード
from takuma_app import app, db 
# Userテーブルモデルの読み込み(ORM用)
from takuma_app.models import User, Count
# 売上予測関数
from takuma_app.predict.predict_sales import predict_sales 

# エンドポイントを記載
@app.route('/')
def index():
    #　アクセスカウンタの取得
    count = Count.query.filter_by(id=1).first()
    if count is None:
        count = Count(id=1, count=1)
        db.session.add(count)
    else:
        count.count += 1
    db.session.commit()
    # render_templateでtemplatesフォルダ内のhtmlを返す
    return render_template('index.html', count=count)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # POSTされた時ユーザ登録処理へ
    if request.method == 'POST':
        # フォームからユーザ名とパスワードを取得
        username = request.form['username']
        password = request.form['password']
        #　クエリ実行, usernamが一致するレコードの一番上を取得
        exist_user = User.query.filter_by(username=username).first()
        # 該当した場合メッセージを出力してリダイレクト
        if exist_user is not None:
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            flash('ユーザーが存在しないか、パスワードが間違っています')
            return redirect('/login')
        # セッション情報の追加
        login_user(user)
        return redirect('/mypage')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # セッション情報の削除
    logout_user()
    return redirect('/')

@app.route('/mypage')
@login_required
def mypage():
    # セッション情報からログインしているユーザのusernameを取得
    showname = current_user.username
    # shownameに代入してテンプレートを出力
    return render_template('mypage.html', showname=showname)

@app.route('/mypage/edit/username', methods=['GET', 'POST'])
@login_required
def edit_username():
    if request.method == 'POST':
        new_username = request.form['new_username']
        current_user.username = new_username
        db.session.commit()
        return redirect('/mypage')
    return render_template('edit/username.html')

@app.route('/mypage/edit/password', methods=['GET', 'POST'])
@login_required
def edit_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        # 現在のユーザのレコードを更新
        current_user.password = new_password
        db.session.commit() # 
        return redirect('/mypage')
    return render_template('edit/password.html')

@app.route('/mypage/delete', methods=['GET', 'POST'])
@login_required
def delete_user():
    if request.method == 'POST':
        # 現在のユーザのレコードを削除
        db.session.delete(current_user)
        db.session.commit()
        return redirect('/')
    return render_template('delete.html')

@app.route('/mypage/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        store_id = int(request.form['store_id'])
        item_id = int(request.form['item_id'])
        date = request.form['date']
        
        # /takuma_app/predict/predict_sales.pyから予測を行う関数を呼び出す
        predictions = predict_sales(store_id, item_id, date)
        # メッセージの記述
        prediction_message = f"店舗番号{store_id}の商品番号{item_id}は{predictions[0]}個売れます！！"

        # テンプレートに代入して出力
        return render_template('predict.html', predictions=predictions, prediction_message=prediction_message)

    return render_template('predict.html')