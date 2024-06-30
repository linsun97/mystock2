import pandas as pd
import sqlite3
from sqlalchemy import create_engine

pd.set_option("display.max_columns", 100)
# 假設有兩個表A和B
# conn = sqlite3.connect('database.db')
engine = create_engine('mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock')

def get_cashgood():
    
# 使用SQL語法進行左連接
    sql_query = """
    SELECT *
    FROM goodstocks
    LEFT JOIN basic_open_all
    ON goodstocks.stockid = basic_open_all.stock_id
    ORDER BY upyear DESC,season DESC,inv_cap DESC;
    """

    # 將查詢結果轉換為pandas DataFrame
    merged_df = pd.read_sql_query(sql_query, engine)

    # 關閉數據庫連接
    # conn.close()
    # print(merged_df.sort_values(by='inv_cap',ascending=False))
    # print(merged_df)
    # print(merged_df.groupby('upyear')['stockid'].count())
    return merged_df