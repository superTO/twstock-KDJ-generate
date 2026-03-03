import yfinance as yf

def get_twstockData(sid):
    # 抓取近 3 個月的資料 (確保 KDJ 平滑計算有足夠的緩衝空間)
    df = yf.download(sid, period="3mo", progress=False, multi_level_index=False)
    
    if df.empty:
        print(f"找不到 {sid} 的資料，請確認代號是否正確。")
        return None

    # yfinance 回傳的欄位開頭大寫：Open, High, Low, Close
    N = 9
    
    # 計算 RSV
    low_roll = df['Low'].rolling(window=N).min()
    high_roll = df['High'].rolling(window=N).max()
    
    # 計算 RSV (避免最高等於最低時產生的錯誤)
    df['RSV'] = (df['Close'] - low_roll) / (high_roll - low_roll) * 100
    df['RSV'] = df['RSV'].fillna(50) # 預設值

    # 計算 K, D (使用指數加權移動平均 ewm)
    # adjust=False 是為了符合遞歸公式：今日K = 2/3 * 昨日K + 1/3 * 今日RSV
    df['K'] = df['RSV'].ewm(com=2, adjust=False).mean()
    df['D'] = df['K'].ewm(com=2, adjust=False).mean()
    
    # 計算 J 值
    df['J'] = 3 * df['K'] - 2 * df['D']

    # 將 Date 索引轉換為一般欄位
    df.reset_index(inplace=True)

    print(f'---- {sid} (yfinance) ----')
    result = df[['Date', 'Close', 'K', 'D', 'J']].tail(1) # 顯示最後1天的 KDJ 值，日期為今天
    print(result)
    
    return result

# test
# get_twstockData('2812.TW')