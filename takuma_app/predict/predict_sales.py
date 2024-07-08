import pandas as pd # データフレーム操作用
import joblib # モデル読み込み用
from takuma_app.predict.train_model import make_model # モデル作成用関数
import os # ファイル読み書き用

def preprocess_data_for_prediction(store_id, item_id, date):
    # 前処理
    data = pd.DataFrame({
        'store': [store_id],
        'item': [item_id],
        'date': [pd.to_datetime(date)]
    })
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['day'] = data['date'].dt.day
    data['dayofweek'] = data['date'].dt.dayofweek
    return data[['store', 'item', 'year', 'month', 'day', 'dayofweek']]

def predict_sales(store_id, item_id, date):
    # モデルが作成されていない場合、作成
    if not os.path.exists('/takuma_app/predict/sales_model.pkl'):
        make_model()
    # モデルの読み込み
    model = joblib.load('/takuma_app/predict/sales_model.pkl')
    # 入力データの前処理
    data = preprocess_data_for_prediction(store_id, item_id, date)

    # 予測
    prediction = model.predict(data)
    return prediction
