import twstock
import pandas as pd
from datetime import datetime, timedelta

def get_twstockData(sid):
    ## update db
    # twstock.__update_codes()

    # 取得XXX股票資料
    stock = twstock.Stock(sid)

    # 計算 60 天前的日期
    start_date = datetime.today() - timedelta(days=60)  # 計算 60 天前的日期

    # 轉換為 'YYYY-MM-DD' 格式，這樣可以傳入 `fetch_from()` 函數
    start_year = start_date.year
    start_month = start_date.month

    # 從 60 天前開始抓取資料
    df = pd.DataFrame(stock.fetch_from(start_year, start_month))

    # 設定 N 值（通常為 9）
    N = 9

    # 計算 RSV (Raw Stochastic Value)
    high = df['high']
    low = df['low']
    close = df['close']

    # 計算 N 日內的最高價、最低價
    high_roll = high.rolling(window=N).max()
    low_roll = low.rolling(window=N).min()

    # 計算 RSV
    RSV = (close - low_roll) / (high_roll - low_roll) * 100

    # 計算 K 和 D
    K = RSV.ewm(com=2).mean()  # 使用指數加權移動平均
    D = K.ewm(com=2).mean()

    # 計算 J 值
    J = 3 * K - 2 * D

    # 把結果輸出並將日期改為今天
    df['K'] = K
    df['D'] = D
    df['J'] = J
    # 轉換日期欄位
    df['date'] = pd.to_datetime(df['date'])

    # 顯示結果
    print('----' + sid + '----')
    print(df[['date', 'close', 'K', 'D', 'J']].tail(1))  # 顯示最後1天的 KDJ 值，日期為今天
    return df[['date', 'close', 'K', 'D', 'J']].tail(1)

