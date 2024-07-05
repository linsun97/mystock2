import  urllib.request,csv
from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer , DATE
import pandas as pd
import numpy as np
import time
import email.message
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import schedule

# 上櫃即時創新高 csv版與html版
# https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d=113/06/07&s=0,asc,0
# https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=htm&d=113/06/07&s=0,asc,0
# 設定float格式為小數點後兩位
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock",pool_size=100,pool_recycle=3600, max_overflow=40,echo=False)
pd.set_option("display.float_format",'{:.2f}'.format)
today = datetime.today().date()

def get_sup_newhigh():
# -----偵測創新高的函數--------------------------------------------
    def newhigh(nprice,nstockid,nstockname,nvolume,day1,day2,day3):
        pd.set_option("display.float_format",'{:.2f}'.format)
        try:
            df_list = pd.read_sql(f"SELECT * FROM st_{nstockid} ORDER BY up_date DESC LIMIT 150",engine )
            df_id_nh = pd.DataFrame(df_list)
            df_head1 = df_id_nh.head(day1) 
            df_head2 = df_id_nh.head(day2) 
            df_head3 = df_id_nh.head(day3) 

            day1max = df_head1['over'].max()
            day2max = df_head2['over'].max()
            day3max = df_head3['over'].max()

            day1mean = df_head1['volume'].mean()
            
            if nprice >= day1max:
                print(f"{nstockid},{nstockname}創{day1}天新高")
                # 取到小數點後兩位
                volume_day1 = round(nvolume/day1mean,2)
                print(f"成交量是平均值的{volume_day1}倍")
                h_day1.append(f"{nstockid}({nstockname})")
                h_id_day1.append(f"{nstockid}")
                h_vol_day1.append(f"{volume_day1}")

            # newh_day2 = []
            if nprice >= day2max:
                print(f"{nstockid},{nstockname}創{day2}天新高")
                h_day2.append(f"{nstockid}({nstockname})")
                h_id_day2.append(f"{nstockid}")

            # newh_day3 = []
            if nprice >= day3max:
                print(f"{nstockid},{nstockname}創{day3}天新高")
                h_day3.append(f"{nstockid}({nstockname})")
                h_id_day3.append(f"{nstockid}")
        
        except Exception as e:
            print(e)
            pass
        
    # --------偵測創新高的函數結束--------------------------------------------------

    import twstock

    def detect_new_highs():
        def process_row(row):
            stock_id = row["stockid"]
            # print(f"Processing stock_id: {stock_id}")
            realtime_stock = twstock.realtime.get(stock_id)
            if realtime_stock:
                # print(f"Found data for stock_id: {stock_id}")
                # print(realtime_stock)
                name = realtime_stock['info']["name"]
                if realtime_stock['realtime']["high"] == "-":
                    price = 0.0
                else:
                    price  = float(realtime_stock['realtime']["high"])
                # print(f"Latest trade price: {price}")
                volume = int(realtime_stock['realtime']["accumulate_trade_volume"])
                # print(f"Accumulated trade volume: {volume}")
                print(f"Processing newhigh for stock_id: {stock_id}")
                newhigh(price, stock_id, name, volume, 60, 90, 120)
                # quit()
            else:
                print(f"Data not found for stock_id: {stock_id}")

        df_stock_ids = pd.read_sql("SELECT stockid FROM all_id_name", engine)
        print(f"Total number of stocks: {len(df_stock_ids)}")
        df_stock_ids.apply(process_row, axis=1)
        return h_day1,h_day2,h_day3,h_vol_day1



    # 這樣做h_day1,h_id_day1會變成全域變數
    h_day1 = []
    h_id_day1=[]
    h_day2 = []
    h_id_day2=[]
    h_day3 = []
    h_id_day3=[]
    h_vol_day1 = []
    h_day1,h_day2,h_day3,h_vol_day1 = detect_new_highs()

    return h_day1,h_day2,h_day3,h_vol_day1

    # ----自動執行-----------------------------------------
        
    # schedule.every(5).minutes.do(detect_new_highs)
    # schedule.every().day.at("09:00").do(detect_new_highs)

    # def job_cancel():
    #     global running
    #     running = False
    #     print("Stopped")
    #     return schedule.clear()

    # schedule.every().day.at('17:00').do(job_cancel)

    # while True:

    #     schedule.run_pending()
    #     if not schedule.jobs:
    #         break
    #     time.sleep(1)

    # print("Today is end!!")



    # detect_nh()
    # print(h_id_day1)
    # 串列轉為字串,用","分隔
    # newh_day1_str = ",".join(map(str, h_id_day1))
    # print(newh_day1_str)
    # quit()




