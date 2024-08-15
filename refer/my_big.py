from sqlalchemy import create_engine
from datetime import datetime , date
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer,DATE
import pandas as pd
import email.message
import time
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
# 只抓上市的創新版
# https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_TIB?date=20240603&response=html

# 設定float格式為小數點後兩位
pd.set_option("display.float_format",'{:.2f}'.format)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
today = datetime.today().date()
week_day = datetime.isoweekday(today)
# upnewd = datetime.strftime(today, '%Y%m%d')
nowmonth = today.month
# print(nowmonth)
# upnowmonth = nowmonth-1
nowyear = today.year
# print(nowyear)
# quit()
#第一次先執行start_shin.py才能,只要執行一次就好,設定起始日
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
try:
    last_date = pd.read_sql("SELECT Up_date FROM big_index ORDER BY Up_date DESC LIMIT 1",engine)
    last_date = last_date.iloc[0,0]
    lastyear = last_date.year
    # print(lastyear)
    lastmonth = last_date.month
    # print(lastmonth)
    # quit()
except:   
    pass

# 若當天沒有資料往前一直到有資料當天

# 測試用:
# upnewd = "20240501"
date_range = pd.date_range(start=date(lastyear,lastmonth,1),end=date(nowyear,nowmonth,1), freq="M",inclusive="left")
# print(date_range)
# quit()
for dateone in date_range:
    upnewd = datetime.strftime(dateone, '%Y%m%d')
    # print(upnewd)
    # quit()
    url = f"https://www.twse.com.tw/rwd/zh/TAIEX/MI_5MINS_HIST?date={upnewd}&response=html"
    print(url)
    data = pd.read_html(url,
                    na_values ="--",
                    # 不用原本的"--",換成"NaN"
                    keep_default_na = False ,
                    header=1,
                    # skipfooter=6,
                    # usecols=[1,2,6,9,10,11,12],
                    # names=['stockid','stockname','bef','high','low','over','volume'],
                    thousands=",",
                    encoding="utf-8",
                    # parse_dates=["日期"], #需用中掛號包住
                    # date_format="%Y/%m/%d",
                    #  true_values=["yes"], #需用中掛號包住
                    #  false_values=["no"], #需用中掛號包住
                    # engine='python'
                    
                    )
    # print(data)
    df = pd.DataFrame(data[0])
    df.columns=["Up_date","big_open","big_high","big_low","Big"]
    # print(df.info())
    df = df.drop(["big_open","big_high","big_low"],axis=1)
    # dt = datetime.strptime(df['Up_date'][0], '%Y/%m/%d')
    # print(df)
    # quit()
    dt = df['Up_date'].str.split("/",expand=True)
    # print(dt)
    # quit()
    # 先將字串格式改成int才能加1911
    dt = dt.astype("Int16")
    # print(dt.info())
    dt.iloc[:,0] = dt.iloc[:,0]+1911
    # print(dt)
    # 一定要用 [year, month, day] 當column名
    dt.columns = ["year","month","day"]
    # print(dt)
    # quit()

    df["Up_date"] = pd.to_datetime(
        dt[["year","month","day"]]
    ) 



    df = df.query("Up_date > @last_date")
    onedaytype = {
            "Up_date" : DATE,
            "Big":Float
        }
    df.to_sql("big_index",engine,if_exists="append",index=False,dtype=onedaytype)
    print("新增台灣加權指數完成")
    # print(df)
    # quit()




# ---------------------------------------------------------
