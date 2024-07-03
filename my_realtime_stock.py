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
# from newhigh_def import newhigh
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock",pool_size=100,pool_recycle=3600, max_overflow=40,echo=False)
pd.set_option("display.float_format",'{:.2f}'.format)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 500)
today = datetime.today().date()



def get_shin_newhigh():
    
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


# 興櫃即時偵測創新高 無html版
# https://www.tpex.org.tw/storage/emgstk/ch/new.csv
# 設定float格式為小數點後兩位


    def detect_nh():
        url = "https://www.tpex.org.tw/storage/emgstk/ch/new.csv"
        print(url)
        try:
            # timegap = 0
            data = pd.read_csv(url,
                        #  na_values="-"
                        # 前2列不要,第3列當column
                        header=2,
                        # 後四列不要
                        skipfooter=4,
                        usecols=[0,1,3,7,8,10,13],
                        names=['stockid','stockname','bef','high','low','over','volume'],
                        thousands=",",
                        encoding="cp950",
                        #  parse_dates=["dateone"], #需用中掛號包住
                        #  date_format="%Y%m%d",
                        #  true_values=["yes"], #需用中掛號包住
                        #  false_values=["no"], #需用中掛號包住
                        engine='python'
                        
                        )
        except:
            pass
        
        all_stocks_shin = []
        try: 
            for i,row in data.iterrows():
                # print(row)
                # 原始資料內有空白,必須先去掉
                if len(str(row["stockid"]).strip()) !=  4 :
                    continue
                
                stock_shin = [str(row["stockid"]).strip(),str(row["stockname"]).strip(),row["over"],row["high"],row["low"],row["bef"],row["volume"]]
                all_stocks_shin.append(stock_shin)
        except:
            pass
    
        df = pd.DataFrame(all_stocks_shin)
    # print(df)
        # return df
    # quit()
    
        df.columns = ["stockid","stockname","over","high","low","bef","volume"]

# str轉為字串,strip去掉前後的空白
    # if (is_string_dtype(df['open'])):
    #     df['open'] = df['open'].str.strip()
        if (is_string_dtype(df['high'])):
            df['high'] = df['high'].str.strip()
        if (is_string_dtype(df['low'])):
            df['low'] = df['low'].str.strip()
        if (is_string_dtype(df['over'])):
            df['over'] = df['over'].str.strip()
        if (is_string_dtype(df['bef'])):
            df['bef'] = df['bef'].str.strip()
        if (is_string_dtype(df['volume'])):
            df['volume'] = df['volume'].str.strip()

        df.loc[df['bef']=="-",'bef'] = 0
            
        # 將值為"-"的內容換成bef的值或0
        df.loc[df['high']=="-",['high','low','over']] = df.loc[df['high']=="-",'bef']
        # 這兩種寫法,以後的pandas不支援
        if (is_string_dtype(df['bef'])):
            df.loc[df['bef']=="-",'bef'] = df.loc[df['bef']=="-",'over']
        

        df.loc[df['volume']=="-",'volume'] = 0
        
        # print(df)
        # print(df.info())
        # quit()
        df = df.astype(
                    {
                        'stockid':'int16',
                        'stockname':'category',
                        'over':"float32",
                        'high':"float32",
                        'low':"float32",
                        'bef':'float32',
                        "volume":"float32"
                    }
                )
        df['volume'] = df['volume']/1000
        # print(df)
        # print(df.info())
        # return df
        # quit()


        def onerow_nh(row):
                # 把row從series變dataframe,取出的row會被當成series但他是直行,先變成list,再變成橫的dataframe
                row_pd = pd.DataFrame([row])
                nowstockid = row_pd.iloc[0,0]
                nowname = row_pd.iloc[0,1]
                nowprice = row_pd.iloc[0,2]
                nowvolume = row_pd.iloc[0,6]
                newhigh(nowprice,nowstockid,nowname,nowvolume,30,60,90)
        
        df.apply(onerow_nh,axis = 1)
        return h_day1,h_day2,h_day3,h_vol_day1




# 這樣做h_day1,h_id_day1會變成全域變數
    h_day1 = []
    h_id_day1=[]
    h_day2 = []
    h_id_day2=[]
    h_day3 = []
    h_id_day3=[]
    h_vol_day1 = []

    h_day1,h_day2,h_day3,h_vol_day1 = detect_nh()
    # df1 =detect_nh()
    # return df1
    
    return h_day1,h_day2,h_day3,h_vol_day1

# ----自動執行-----------------------------------------
    
# schedule.every(5).minutes.do(detect_nh)
# schedule.every().day.at("09:00").do(detect_nh)

# def job_cancel():
#     global running
#     running = False
#     print("Stopped")
#     return schedule.clear()

# schedule.every().day.at('15:00').do(job_cancel)

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




