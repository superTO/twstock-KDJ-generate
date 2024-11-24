from calculate_KDJ import get_twstockData
from line_message import push_message_api
import argparse

# 從檔案中讀取股票代碼
def read_stock_list(file_path):
    with open(file_path, 'r') as file:
        stock_list = [line.strip() for line in file if line.strip()]
    return stock_list


if __name__ == "__main__":
    # 使用 argparse 解析命令列參數
    parser = argparse.ArgumentParser(description="LINE Bot Message Sender")
    parser.add_argument("--token", required=True, help="LINE Channel Access Token")
    parser.add_argument("--user_id", required=True, help="LINE User ID")

    args = parser.parse_args()

# 設定檔案路徑
stock_file = 'stockList.txt'  # 儲存股票代碼的檔案
stock_list = read_stock_list(stock_file)

# 儲存所有訊息
messages = []

# 遍歷股票代碼，處理每一隻股票
for stock_code in stock_list:
    last_row = get_twstockData(stock_code)  # 獲取股票資料
    
    # 將 numpy.datetime64 轉換為字串，格式化為 YYYY-MM-DD
    date_str = str(last_row['date'].values[0])[:10]
    
    if last_row['J'].values[0] < 0:
        # 格式化資料，加入股票代號
        message = (f"Stock: {stock_code}\n"
                   f"Date: {date_str}\n"
                   f"Close: {last_row['close'].values[0]}\n"
                   f"K: {round(last_row['K'].values[0], 2)}\n"
                   f"D: {round(last_row['D'].values[0], 2)}\n"
                   f"J: {round(last_row['J'].values[0], 2)}")
        messages.append(message)  # 將訊息加入列表
        # print(message)  # 輸出訊息到終端檢查

if len(messages) > 0:
    # 將所有訊息合併後發送
    final_message = "\n\n".join(messages)  # 多支股票訊息間加空行
    push_message_api(args.token, args.user_id, final_message)  # 傳送訊息
else:
    print("沒有 J < 0 的項目")