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
def detect_nh():
    yearnum = datetime.strftime(today, '%Y')
    week_day = datetime.isoweekday(today)
    # if week_day == 5 or week_day == 6: #星期六或星期日
    #     continue
    # 算出民國年
    tynum = int(yearnum) - 1911
    upnewd = datetime.strftime(today, str(tynum)+'/%m/%d')

    url = f"https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d={upnewd}&s=0,asc" #上櫃公司-政府公開資料
    print(url)
    try:
        data = pd.read_csv(url,usecols=[0,1,2,4,5,6,7,8],thousands=',', encoding='cp950',
                    names=['stockid','stockname','over','open','high','low','bef','volume'],
                    #   index_col='stockid',
                    na_values=["-", " "],skipfooter=8,header=2,
                    engine="python")
        # print(data)
    except:
        print(f"{upnewd}(星期{week_day})今天可能是假日")
        # onedaytype = {
        # "Up_date" : DATE,
        # "New_up" : NVARCHAR(length=1000),
        # }
        # a_day = {
        #     "Up_date" : now_day,
        #     "New_up" : "holiday"
        # }

        # # 必須設index
        # df_day = pd.DataFrame(a_day, index=[0])
        # print(df_day)
        # df_day.to_sql('sup_oneday', engine, if_exists='append', dtype=onedaytype ,index=False  )
        
        pass
    # quit()
    all_stocks_shin = []
    try: 
        for i,row in data.iterrows():
            if len(row["stockid"]) !=  4 :
                continue
            stock_shin = [str(row["stockid"]).strip(),str(row["stockname"]).strip(),row["over"],row["open"],row["high"],row["low"],row["bef"],row["volume"]]
            all_stocks_shin.append(stock_shin)
    except:
        pass

    # print("----new_id------")
    # print(new_id)
    df = pd.DataFrame(all_stocks_shin)

    df.columns = ["stockid","stockname","over","open","high","low","bef","volume"]

# str轉為字串,strip去掉前後的空白
    if (is_string_dtype(df['open'])):
        df['open'] = df['open'].str.strip()
    if (is_string_dtype(df['high'])):
        df['high'] = df['high'].str.strip()
    if (is_string_dtype(df['low'])):
        df['low'] = df['low'].str.strip()
    if (is_string_dtype(df['over'])):
        df['over'] = df['over'].str.strip()
    if (is_string_dtype(df['volume'])):
        df['volume'] = df['volume'].str.strip()


    df.loc[df['high']=="---",["open","high","low","over"]] = df.loc[df["high"]=="---","bef"]
    
    df = df.astype(
                {
                    'stockid':'int16',
                    'stockname':'category',
                    'over':'float32',
                    'open':'float32',
                    'high':"float32",
                    'low':"float32",
                    'bef':"float32",
                    "volume":"int64",
                }
            )



        # sql_df = pd.read_sql('all_stocks_shin', engine)
    def onerow_nh(row):
            # 把row從series變dataframe,取出的row會被當成series但他是直行,先變成list,再變成橫的dataframe
            row_pd = pd.DataFrame([row])
            nowstockid = row_pd.iloc[0,0]
            nowname = row_pd.iloc[0,1]
            nowprice = row_pd.iloc[0,2]
            nowvolume = row_pd.iloc[0,6]
            newhigh(nowprice,nowstockid,nowname,nowvolume,30,60,90)
    
    df.apply(onerow_nh,axis = 1)



# 這樣做h_day1,h_id_day1會變成全域變數
h_day1 = []
h_id_day1=[]
h_day2 = []
h_id_day2=[]
h_day3 = []
h_id_day3=[]

# ----自動執行-----------------------------------------
    
schedule.every(5).minutes.do(detect_nh)
schedule.every().day.at("09:00").do(detect_nh)

def job_cancel():
    global running
    running = False
    print("Stopped")
    return schedule.clear()

schedule.every().day.at('15:00').do(job_cancel)

while True:

    schedule.run_pending()
    if not schedule.jobs:
        break
    time.sleep(1)

print("Today is end!!")



# detect_nh()
# print(h_id_day1)
# 串列轉為字串,用","分隔
# newh_day1_str = ",".join(map(str, h_id_day1))
# print(newh_day1_str)
# quit()




