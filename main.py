import os
import sys
import argparse
from datetime import datetime, timedelta, timezone
from calculate_KDJ import get_twstockData
from line_message import broadcast_message_api, push_message_api

# 從檔案中讀取股票代碼
def read_stock_list(file_path):
    with open(file_path, 'r') as file:
        stock_list = [line.strip() for line in file if line.strip()]
    return stock_list


def main():
    # 使用 argparse 解析命令列參數（優先使用 --token，未提供時由 CHANNEL_ACCESS_TOKEN 環境變數讀取）
    parser = argparse.ArgumentParser(description="LINE Bot Message Sender")
    parser.add_argument(
        "--token",
        default=os.getenv("CHANNEL_ACCESS_TOKEN"),
        help="LINE Channel Access Token (可由環境變數 CHANNEL_ACCESS_TOKEN 或此參數提供)"
    )
    # parser.add_argument("--user_id", required=True, help="LINE User ID")

    args = parser.parse_args()

    if not args.token:
        parser.error("缺少 LINE Channel Access Token，請設定 CHANNEL_ACCESS_TOKEN 環境變數或使用 --token 參數。")

    # 設定檔案路徑
    stock_file = 'stockList.txt'  # 儲存股票代碼的檔案
    stock_list = read_stock_list(stock_file)

    # 儲存所有訊息
    messages = []

    # 取得台灣時間 (UTC+8)
    tw_tz = timezone(timedelta(hours=8))
    today_tw = datetime.now(tw_tz).date()
    tw_weekday = today_tw.weekday()

    for stock_code in stock_list:
        last_row = get_twstockData(stock_code)  # 獲取股票資料
        if last_row is None or last_row.empty:
            continue

        date_str = str(last_row['Date'].values[0])[:10]
        row_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # 避免重複發送訊息 (例如沒開盤時重複推送舊資訊)
        if ".TW" in stock_code:
            # 台股：最新資料日期必須為今日
            if row_date != today_tw:
                print(f"[{stock_code}] 最新資料日期 ({date_str}) 非今日 ({today_tw})，跳過。")
                continue
        else:
            # 美股：若開盤前執行為前一交易日 (週一為前3天週五，其餘平日為前1天)；若開盤後執行則為今日
            expected_prev = today_tw - timedelta(days=3 if tw_weekday == 0 else 1)
            # 容許為今日、預期前一交易日，或 4 天內之有效交易日 (涵蓋連假)
            if row_date != today_tw and row_date != expected_prev and (today_tw - row_date).days > 4:
                print(f"[{stock_code}] 最新資料日期 ({date_str}) 過舊，跳過。")
                continue
        
        if last_row['J'].values[0] < 0:
            # 格式化資料，加入股票代號
            message = (f"Stock: {stock_code}\n"
                       f"Date: {date_str}\n"
                       f"Close: {last_row['Close'].values[0]}\n"
                       f"K: {round(last_row['K'].values[0], 2)}\n"
                       f"D: {round(last_row['D'].values[0], 2)}\n"
                       f"J: {round(last_row['J'].values[0], 2)}")
            messages.append(message)  # 將訊息加入列表
            # print(message)  # 輸出訊息到終端檢查

    if len(messages) > 0:
        # 將所有訊息合併後發送
        final_message = "\n\n".join(messages)  # 多支股票訊息間加空行
        ## 只傳給一個人
        # push_message_api(args.token, args.user_id, final_message)
        ## 傳給所有好友
        broadcast_message_api(args.token, final_message)
    else:
        print("沒有 J < 0 的項目")


if __name__ == "__main__":
    main()