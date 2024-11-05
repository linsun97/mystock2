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

# 建立一個資料夾來儲存CSV檔
os.makedirs("stock_data", exist_ok=True)

# 下載資料並儲存為CSV檔
for date in date_range:
    date_str = date.strftime("%Y%m%d")
    url = f"https://wwwc.twse.com.tw/rwd/zh/afterTrading/STOCK_TIB?date={date_str}&response=html"
    print(url)
    
    # 發送請求
    response = requests.get(url)
    
    # 檢查是否成功獲取資料
    if response.ok:
        # 使用 StringIO 包裝 HTML 字符串以避免 FutureWarning
        table_io = StringIO(response.text)
        print(table_io)

        try:
            # 直接從 HTML 中讀取所有表格，並檢查是否有任何 DataFrame 被讀取
            dfs = pd.read_html(table_io)
            
            if not dfs:  # 如果沒有 DataFrame 被讀取，則跳過此日期的 CSV 創建
                print(f"No data available for {date_str}, skipping CSV creation.")
                continue
            
            df = dfs[0]  # 獲取第一個 DataFrame

            # 去掉前兩行和最後一行（如果需要）
            df = df.iloc[2:-1]

            # 檢查是否有任何欄位沒有資料
            if df.isnull().values.any():
                print(f"No data available for {date_str}, skipping CSV creation.")
                continue  # 跳過此日期的CSV檔案創建

            # 儲存為CSV檔
            csv_file_path = f"stock_data/{date_str}.csv"
            df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
            print(f"Created CSV for {date_str}.")
            
        except Exception as e:
            print(f"Error processing data for {date_str}: {e}")

# 關閉游標和資料庫連接
cursor.close()
db_connection.close()