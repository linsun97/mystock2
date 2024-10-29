import mariadb
import sys

# 刪除上櫃所有股票資料表中某幾筆錯誤資料--用日期

# 連接參數
conn_params = {
    "user": "root", 
    "password": "nineseve9173",
    "host": "localhost",  # 或者你的資料庫主機地址
    "database": "stock"
}

# 建立連接
try:
    conn = mariadb.connect(**conn_params)
except mariadb.Error as e:
    print(f"連接到 MariaDB 伺服器時出錯: {e}")
    sys.exit(1)

# 獲取游標
cur = conn.cursor()

# 執行查詢以獲取 stockid
cur.execute("SELECT stockid FROM all_id_name")

# 將結果存儲為列表
stock_ids = [row[0] for row in cur.fetchall()]

# 輸出結果
print(stock_ids)
# quit()
# 查詢所有以 st_ 開頭的資料表
# cur.execute("SHOW TABLES LIKE 'st_%'")
# tables = cur.fetchall()

# 定義要刪除的日期範圍
start_date = '2024-10-26'
end_date = '2024-10-29'

# 對每個資料表執行刪除操作
for sid in stock_ids:
    delete_query = f"DELETE FROM st_{sid} WHERE up_date BETWEEN '{start_date}' AND '{end_date}'"
    
    try:
        cur.execute(delete_query)
        conn.commit()  # 提交更改
        print(f"從 st_{sid} 刪除了 {cur.rowcount} 筆資料")
    except mariadb.Error as e:
        print(f"在 st_{sid} 刪除資料時出錯: {e}")

# 關閉游標和連接
cur.close()
conn.close()