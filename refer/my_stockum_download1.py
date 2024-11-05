import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# 定義開始與結束日期
start_date = datetime(2024, 9, 13)
end_date = datetime(2024, 11, 4)

# 產生日期範圍
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# 建立一個資料夾來儲存CSV檔
os.makedirs("stock_data", exist_ok=True)

# 下載資料並儲存為CSV檔
for date in date_range:
    date_str = date.strftime("%Y%m%d")
    url = f"https://wwwc.twse.com.tw/rwd/zh/afterTrading/STOCK_TIB?date={date_str}&response=html"
    
    # 發送請求
    response = requests.get(url)
    
    # 檢查是否成功獲取資料
    if response.ok:
        # 讀取資料
        data = response.text
        
        # 處理資料，捨去頭尾的說明文字
        try:
            # 找到資料的起始與結束位置
            start_index = data.index("<table")
            end_index = data.index("</table>") + len("</table>")
            table_html = data[start_index:end_index]

            # 轉換為DataFrame
            df = pd.read_html(table_html)[0]

            # 去掉前兩行和最後一行
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
