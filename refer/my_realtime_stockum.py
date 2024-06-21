from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer,DATE
import pandas as pd
import email.message
import time
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import schedule
# 只抓上市的創新版 html與csv
# https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_TIB?date=20240603&response=html
# https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_TIB?date=20240603&response=csv

# 設定float格式為小數點後兩位
pd.set_option("display.float_format",'{:.2f}'.format)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
today = datetime.today().date()

#第一次先執行start_shin.py才能,只要執行一次就好,設定起始日
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
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
    week_day = datetime.isoweekday(today)
    upnewd = datetime.strftime(today, '%Y%m%d')
    # if week_day == 5 or week_day == 6: #星期六或星期日
    #     continue
    # 測試用:
    # upnewd = "20240519"

    url = f"https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_TIB?date={upnewd}&response=html"
    print(url)
    
    data = pd.read_html(url,
                na_values ="--",
                # 不用原本的"--",換成"NaN"
                keep_default_na = False ,
                header=2,
                # skipfooter=6,
                # usecols=[1,2,6,9,10,11,12],
                # names=['stockid','stockname','bef','high','low','over','volume'],
                thousands=",",
                encoding="utf-8",
                #  parse_dates=["dateone"], #需用中掛號包住
                #  date_format="%Y%m%d",
                #  true_values=["yes"], #需用中掛號包住
                #  false_values=["no"], #需用中掛號包住
                # engine='python'
                
                )
    
    # print(len(data[0]))
    # print(data[0].shape[0])
    # quit()
    # data[0]==0表示0筆資料,代表當天為假日
    if (data[0].shape[0]) == 0:
    # quit()
        print(f"{upnewd}(星期{week_day})今天可能是假日")
        
        pass
    
    else:
        # quit()
        data_s = pd.DataFrame(data[0])
        data_s = data_s.iloc[:-1,[0,1,2,5,6,7,8,11]]
        # data_s = data_s.rename(columns=["stockid","stockname","volume","open","high","low","over","bef"])
        data_s.columns = ["stockid","stockname","volume","open","high","low","over","bef"]
        # 重新排列columns順序
        data_s = data_s.reindex(columns=["stockid","stockname","over", "open", "high", "low","bef","volume"]) 

        data_s = data_s.fillna(0)
        data_s = data_s.astype(
                {
                    'stockid':'int16',
                    'stockname':'category',
                    "volume":"int64",
                    'open':'float32',
                    'high':"float32",
                    'low':"float32",
                    'over':'float32',
                    'bef':"float32",
                }
            )
        # print(data_s)
        # print(data_s.info())
        # print(df_id_name)
        # print(new_id)
        # quit()
        
        # 將值為"-"的內容換成bef的值或0
        data_s.loc[data_s['high']=="0",['high','low','over','open']] = data_s.loc[data_s['high']=="0",'bef']
        def onerow_nh(row):
            # 把row從series變dataframe,取出的row會被當成series但他是直行,先變成list,再變成橫的dataframe
            row_pd = pd.DataFrame([row])
            nowstockid = row_pd.iloc[0,0]
            nowname = row_pd.iloc[0,1]
            nowprice = row_pd.iloc[0,2]
            nowvolume = row_pd.iloc[0,6]
            newhigh(nowprice,nowstockid,nowname,nowvolume,30,60,90)
    
    data_s.apply(onerow_nh,axis = 1)



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




