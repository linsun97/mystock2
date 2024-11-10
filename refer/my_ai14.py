import mariadb

# 連接到 MariaDB 資料庫
def connect_db():
    connection = mariadb.connect(
        user="root",       # MariaDB 使用者名稱
        password="nineseve9173",   # MariaDB 密碼
        host="localhost",           # 資料庫主機位址
        port=3306,                  # 預設 MariaDB 的連接埠
        database="stock"    # 替換為您的資料庫名稱
    )
    return connection

# 獲取每個資料表最後一筆資料的 New_up 欄位值
def get_last_new_up_values():
    tables = ["shin_oneday", "sum_oneday", "sup_oneday"]
    results = {}

    connection = connect_db()
    cursor = connection.cursor()

    for table in tables:
        cursor.execute(f"SELECT New_up FROM {table} ORDER BY Up_date DESC LIMIT 1")  # 假設 id 是排序依據
        row = cursor.fetchone()
        
        if row:
            new_up_value = row[0]
            if new_up_value:
            #     results[table] = new_up_value.split(",")  # 分割 New_up 欄位值
                # 分割並轉換為整數
                # results[table] = [int(value) for value in new_up_value.split(",") if value.strip() and (value.strip().isdigit() or is_positive_integer(value))]
                results[table] = [int(value) for value in new_up_value.split(",") if value.strip() and (value.strip().isdigit() or isinstance(value,int))]
            else:
                results[table] = []
        else:
            results[table] = []

    cursor.close()
    connection.close()
    
    return results

# 主程式執行
if __name__ == "__main__":
    last_new_up_values = get_last_new_up_values()
    
    for table, values in last_new_up_values.items():
        print(f"{table} 的最後一筆 New_up 值: {values}")