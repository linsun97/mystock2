import twstock
import pandas as pd

stock = twstock.Stock("2254")
stock1 = twstock.realtime.get("2254")
# 取得股名
c_name = stock1["info"]["name"]
# print(c_name)
# 會抓從上次更新以來那個月的1號到今日的資料
stock_mon = stock.fetch_from(2024,6)


# 測試只有一筆資料會不會變成series,結果不會
# stock_mon = stock.fetch_from(today.year,today.month)
# print(stock_oneday) 
df_stock = pd.DataFrame(stock_mon)
print(df_stock)

# 創新板目前沒有
# 創新版html行情