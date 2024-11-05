import requests
import pandas as pd
import os
from datetime import datetime, timedelta, date
import mariadb
from io import StringIO  # 引入 StringIO

# 連接到MariaDB資料庫
db_connection = mariadb.connect(
    host="localhost",      # 資料庫主機
    user="root",           # 使用者名稱
    password="nineseve9173",  # 密碼
    database="stock"      # 資料庫名稱
)

# 創建一個游標以執行SQL查詢
cursor = db_connection.cursor()

# 查詢up_date欄位的最大日期的後一天作為開始日期
cursor.execute("SELECT DATE_ADD(MAX(up_date), INTERVAL 1 DAY) FROM sum_oneday")
start_date_row = cursor.fetchone()

# 確保 start_date 是 datetime 對象
start_date = start_date_row[0] if start_date_row[0] else datetime.now()

# 如果 start_date 是 date 對象，則轉換為 datetime
if isinstance(start_date, date):
    start_date = datetime.combine(start_date, datetime.min.time())

# 設定結束日期為昨天
end_date = datetime.now() - timedelta(days=1)

# 產生日期範圍
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]


# 設定日期
for date in date_range:
    date_str = date.strftime("%Y%m%d")
    url = f"https://wwwc.twse.com.tw/rwd/zh/afterTrading/STOCK_TIB?date={date_str}&response=csv"

    # 建立資料夾以儲存CSV檔
    os.makedirs("stock_data", exist_ok=True)

    # 發送請求以獲取 CSV 數據
    response = requests.get(url)

    # # 檢查請求是否成功
    # if response.ok:
    #     # 以日期命名儲存為 CSV 檔案
    #     csv_file_path = os.path.join("stock_data", f"{date_str}.csv")
        
    #     # 將響應內容寫入 CSV 檔案
    #     with open(csv_file_path, 'wb') as csv_file:
    #         csv_file.write(response.content)
        
    #     print(f"Downloaded and saved as {csv_file_path}.")
    # else:
    #     print(f"Failed to download data for {date_str}. Status code: {response.status_code}")

# 檢查請求是否成功
if response.ok:
    # 檢查返回的內容是否為 HTML
    if "<html>" in response.text:
        print("獲取到的是 HTML 頁面，而不是 CSV 數據。")
        print(response.text)  # 打印出 HTML 內容以便檢查
    else:
        # 將響應內容寫入 CSV 檔案，使用 Big5 編碼
        csv_file_path = os.path.join("stock_data", f"{date_str}.csv")
        
        with open(csv_file_path, 'wb') as csv_file:
            csv_file.write(response.content)
        
        print(f"Downloaded and saved as {csv_file_path}.")
else:
    print(f"Failed to download data for {date_str}. Status code: {response.status_code}")