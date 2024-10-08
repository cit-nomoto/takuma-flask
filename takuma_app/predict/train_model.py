"""モデルの訓練を行うモジュール"""
import pandas as pd # データフレーム操作、csvの読み込み用
from sklearn.ensemble import RandomForestRegressor # 機械学習アルゴリズム
import joblib # モデルの保存用

# データの前処理を行う関数
def preprocess_train_data(data):
    """訓練データの前処理を行う関数"""
    data['year'] = data['date'].dt.year # date型を要素ごとに割当
    data['month'] = data['date'].dt.month
    data['day'] = data['date'].dt.day
    data['dayofweek'] = data['date'].dt.dayofweek
    return data

def make_model():
    """モデルの作成を行う関数"""
    # データの読み込み
    train_data = pd.read_csv('/takuma_app/train.csv', parse_dates=['date'])
    # 前処理の実施
    train_data = preprocess_train_data(train_data)

    # 特徴量とターゲットの選定
    features = ['store', 'item', 'year', 'month', 'day', 'dayofweek']
    target = 'sales'

    x_train = train_data[features]
    y_train = train_data[target]
    # モデルのトレーニング
    # 生成に時間がかかるので精度を極限まで低くした、デモ用
    # 理想的にはn_estimators=100以上、random_state=42あたりが精度が高い
    # しかし、初回の演算時間と生成されるモデルの容量も大きくなるので、今回の値に
    model = RandomForestRegressor(n_estimators=5, random_state=0)
    model.fit(x_train, y_train)

    # モデルの保存
    joblib.dump(model, '/takuma_app/predict/sales_model.pkl')
