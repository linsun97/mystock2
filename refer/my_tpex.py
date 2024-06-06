from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer,DATE
import pandas as pd
import email.message
import time
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
# 只抓上市的創新版
# https://www.tpex.org.tw/web/stock/aftertrading/index_summary/summary_result.php?l=zh-tw&d=113/06/05&s=0,asc,0&o=htm

# 設定float格式為小數點後兩位
pd.set_option("display.float_format",'{:.2f}'.format)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
today = datetime.today().date()





#第一次先執行start_shin.py才能,只要執行一次就好,設定起始日
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
try:
    last_date = pd.read_sql("SELECT Up_date FROM tpex_index ORDER BY Up_date DESC LIMIT 1",engine)
    last_date = last_date.iloc[0,0]
except:   
    pass

# # 若當天沒有資料往前一直到有資料當天
x = 1
while True:
    
    now_day = last_date + timedelta(days=x)
    week_day = datetime.isoweekday(now_day)
    upyear = datetime.strftime(now_day, '%Y')
    uptyear = int(upyear)-1911
    upmonth = datetime.strftime(now_day, '%m')
    upday = datetime.strftime(now_day, '%d')
    upnewd = str(uptyear)+"/"+upmonth+"/"+upday
    # print(upnewd)

    if now_day > today :
        quit()
    # 測試用:
    # upnewd = "113/05/03"

    url = f"https://www.tpex.org.tw/web/stock/aftertrading/index_summary/summary_result.php?l=zh-tw&d={upnewd}&s=0,asc,0&o=htm"
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
    # print(df)
    print(df.shape[0])
    # 當天為假日
    if int(df.shape[0]) <= 1 :
        print(f"{now_day},星期{week_day}是可能是假日")
        x = x + 1
        # quit()
        continue
    else:
        tpex_index = df.iloc[0,1]
        x = x + 1
        # print(tpex_index)

        df_oneday = pd.DataFrame([[now_day,tpex_index]])
        df_oneday.columns = ["Up_date","Tpex"]
        # print(df_oneday)
        # quit()
        dtypedict = {
            "Up_date" : DATE,
            "Tpex" : Float
        }
        df_oneday.to_sql("tpex_index",engine,if_exists="append",index=False)
        print(f"更新{now_day}的上櫃指數")

        time.sleep(2)       



# df = df.query("Up_date > @last_date")
# onedaytype = {
#         "Up_date" : DATE,
#         "Big":Float
#     }
# df.to_sql("big_index",engine,if_exists="append",index=False,dtype=onedaytype)
# print("新增台灣加權指數完成")
# # print(df)
# # quit()




# # ---------------------------------------------------------
