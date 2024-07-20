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
# https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_TIB?date=20240603&response=html

# 設定float格式為小數點後兩位
pd.set_option("display.float_format",'{:.2f}'.format)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
today = datetime.today().date()

#第一次先執行start_shin.py才能,只要執行一次就好,設定起始日
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")

# -----偵測創新高的函數--------------------------------------------
# 這樣做h_day1,h_id_day1會變成全域變數
h_id_day1=[]
h_id_day2=[]
h_id_day3=[]
h_vo_day1=[]

def newhigh(nprice,nstockid,nstockname,nvolume,day1,day2,day3):
    pd.set_option("display.float_format",'{:.2f}'.format)
    try:
        df_list = pd.read_sql(f"SELECT * FROM st_{nstockid} ORDER BY up_date DESC LIMIT 150",engine )
        df_id_nh = pd.DataFrame(df_list)
        df_head1 = df_id_nh.head(day1) 
        df_head2 = df_id_nh.head(day2) 
        df_head3 = df_id_nh.head(day3) 

        day1max = df_head1['over'].max()
        # print("30day high")
        # print(day1max)
        day2max = df_head2['over'].max()
        day3max = df_head3['over'].max()

        day1mean = df_head1['volume'].mean()

        # print("nowprice:")
        # print(nprice)
        
        if nprice >= day1max:
            print(f"{nstockid},{nstockname}創{day1}天新高")
            # 取到小數點後兩位
            volume_day1 = round(nvolume/day1mean,2)
            print(f"成交量是平均值的{volume_day1}倍")
            h_id_day1.append(f"{nstockid}")
            h_vo_day1.append(f"{volume_day1}")
            # print("now high stocks:")
            # print(h_id_day1)

        # newh_day2 = []
        if nprice >= day2max:
            print(f"{nstockid},{nstockname}創{day2}天新高")
            h_id_day2.append(f"{nstockid}")

        # newh_day3 = []
        if nprice >= day3max:
            print(f"{nstockid},{nstockname}創{day3}天新高")
            h_id_day3.append(f"{nstockid}")
    
    except Exception as e:
        print(e)
        pass
    
# --------偵測創新高的函數結束--------------------------------------------------


try:
    last_date = pd.read_sql("SELECT Up_date FROM sum_oneday ORDER BY Up_date DESC LIMIT 1",engine)
    last_date = last_date.iloc[0,0]
except:   
    pass

# 若當天沒有資料往前一直到有資料當天
x = 1
timegap = 0
while True:
    h_id_day1=[]
    h_id_day2=[]
    h_id_day3=[]
    h_vo_day1=[]
    old_stocks = []
    try:
        old_df = pd.read_sql('select stockid from all_id_name_sum',engine)
        old_stocks = old_df['stockid'].tolist() # 把series變成list
        # print(old_stocks)
        # quit()
    except Exception as e:
        print(e)
        pass

    x = x+timegap
    now_day = last_date + timedelta(days=x) 
    # weekday : 0-6,sunday為6, isoweekday : 1-7 sunday為7
    # week_day = datetime.weekday(now_day)
    week_day = datetime.isoweekday(now_day)
    upnewd = datetime.strftime(now_day, '%Y%m%d')
    # if week_day == 5 or week_day == 6: #星期六或星期日
    #     continue
    # 測試用:
    # upnewd = "20240519"
    if now_day > today :
        quit()

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
        time.sleep(5)
        
        # onedaytype = {
        # "Up_date" : DATE,
        # "New_up" : NVARCHAR(length=1000),
        # "day1_high" : NVARCHAR(length=2000),
        # "day2_high" : NVARCHAR(length=2000),
        # "day3_high" : NVARCHAR(length=2000)
        # }
        # a_day = {
        #     "Up_date" : now_day,
        #     "New_up" : "holiday"
        # }
        # # 必須設index
        # df_day = pd.DataFrame(a_day, index=[0])
        # print(df_day)
        # df_day.to_sql('sum_oneday', engine, if_exists='append', dtype=onedaytype ,index=False  )
        timegap = 1
        time.sleep(1)
        continue
    
    else:
        # quit()
        data_s = pd.DataFrame(data[0])
        data_s = data_s.iloc[:-1,[0,1,2,5,6,7,8,11]]
        # data_s = data_s.rename(columns=["stockid","stockname","volume","open","high","low","over","bef"])
        data_s.columns = ["stockid","stockname","volume","open","high","low","over","bef"]
        # 重新排列columns順序
        data_s = data_s.reindex(columns=["stockid","stockname","over", "open", "high", "low","bef","volume"]) 

        data_s = data_s.fillna(0)
        data_s["up_date"] = now_day
        data_s['kwave'] = 0.0
        data_s['rci'] = 0.0
        data_s['updown'] = 0.0
        data_s['kwr'] = 0.0
        # 50天相對強度
        data_s['pc'] = 0.0
        data_s['rs'] = 0.0
        data_s['nh'] = ''
        
        data_s = data_s.astype(
                {
                    'stockid':'int16',
                    'stockname':'category',
                    "volume":"float32",
                    'open':'float32',
                    'high':"float32",
                    'low':"float32",
                    'over':'float32',
                    'bef':"float32",
                    "up_date":"datetime64[ns]",
                    "kwave" : "float32",
                    "rci" : "float32",
                    "updown" : "float32",
                    "kwr" : "float32",
                    "pc" : "float32",
                    "rs" : "float32",
                    "nh" : 'category'
                }
            )
        
        data_s.loc[data_s['over'] < data_s['open'],'kwave'] = abs(data_s['open']-data_s['over'])+abs(data_s['open']-data_s['high'])+abs(data_s['high']-data_s['low'])+abs(data_s['low']-data_s['over'])
        data_s.loc[data_s['over'] >= data_s['open'],'kwave'] = abs(data_s['open']-data_s['over'])+abs(data_s['open']-data_s['low'])+abs(data_s['low']-data_s['high'])+abs(data_s['high']-data_s['over'])

        data_s['volume'] = data_s['volume']/1000

        df_id_name = data_s.iloc[:,[0,1]]
        # 用兩層中掛號,從series變成dataframe
        new_id = data_s["stockid"].tolist()
        # print(data_s)
        # print(data_s.info())
        # print(df_id_name)
        # print(new_id)
        # quit()
        
        # 將值為"-"的內容換成bef的值或0
        data_s.loc[data_s['high']=="0",['high','low','over','open']] = data_s.loc[data_s['high']=="0",'bef']

# -------------------------------------------------------------------
        newup = [x for x in new_id if x not in old_stocks]
        # 如果有新股上市寄郵件通知自己
        if newup != []:
            msg=email.message.EmailMessage()
            #利用物件建立基本設定
            from_a = "linsun97@gmail.com"
            to_b = "linsun97@gmail.com"

            msg["From"]=from_a
            msg["To"]=to_b
            msg["Subject"]="上市創新版新增股票"
            content = ''
            for new_s in newup :
                content = content + f"<a href='http://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={new_s}&year=&seamon=&mtype=B&'>{new_s}的公開說明書</a><br>" + \
                                    f"<a href='https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID={new_s}'>{new_s}的goodinfo</a><br>" +\
                                    f"<a href='https://mops.twse.com.tw/mops/web/t100sb07_1'>法說會簡報下載</a><br><br>"
            #寄送郵件主要內容
            msg.add_alternative(content,subtype="html") #HTML信件內容
            acc = "linsun97"
            password = "eajzbxiterroviom"

            #連線到SMTP Sevver
            import smtplib
            #可以從網路上找到主機名稱和連線埠
            server=smtplib.SMTP_SSL("smtp.gmail.com",465) #建立gmail連驗
            server.login(acc,password)
            server.send_message(msg)
            server.close() #發送完成後關閉連線
        # print(newup)
        # 將新上興櫃的股票寫入文字檔中
        # with open("newum_stock.txt","w") as file:
        #     for new_s in newup :
        #         file.write(str(new_s)+"\n")

# -------------------------------------------------------------------

        dtypedict = {
                    'stockid': Integer,
                    'stockname': NVARCHAR(length=100),
                    'over':Float,
                    'open': Float,
                    'high': Float,
                    'low': Float,
                    'bef': Float,
                    'volume': Float,
                    'up_date' : DATE,
                    'kwave': Float,
                    "rci" : Float,
                    "updown" : Float,
                    "kwr" : Float,
                    "pc" : Float,
                    "rs" : Float,
                    "nh" : NVARCHAR(length=100),
                    }

        d_id_dtype = {
                'stockid': Integer,
                'stockname': NVARCHAR(length=100)
                }
        # 設定欄位名稱,若沒設定預設是用0,1,2,3....當欄位名稱
        df_id_name.to_sql('all_id_name_sum', engine, if_exists='replace',dtype=d_id_dtype,index=False)    
        
        def IntoTable(row):
                # 把row從series變dataframe,取出的row會被當成series但他是直行,先變成list,再變成橫的dataframe
                row_pd = pd.DataFrame([row])
                # --------------------------
                nowstockid = row_pd.iloc[0,0]
                # print(nowstockid) 
                nowname = row_pd.iloc[0,1]
                # print(nowname) 
                nowprice = row_pd.iloc[0,2]
                # print(nowprice)
                nowvolume = row_pd.iloc[0,7]
                # print(nowvolume)
                newhigh(nowprice,nowstockid,nowname,nowvolume,30,60,90)
                # -------------------------------------
                if str(row_pd.iloc[0,0]) in h_id_day1:
                    row_pd['nh'] = '30up'
                if str(row_pd.iloc[0,0]) in h_id_day2:
                    row_pd['nh'] = '3060up'
                if str(row_pd.iloc[0,0]) in h_id_day3:
                    row_pd['nh'] = '306090up'
                row_pd.to_sql(f'st_{row_pd.iloc[0,0]}', engine, if_exists='append', dtype=dtypedict ,index=False  )
                print(f"新增st_{row_pd.iloc[0,0]}資料表成功,股名:{row_pd.iloc[0,1]}")
            # 可以用df.apply的方法加上axis = 1,就可以把df內每一列當成一個row去執行IntoTable函式
        data_s.apply(IntoTable,axis = 1)

        # ------------------------------------------------
        newh_day1_str = ",".join(map(str, h_id_day1))
        newh_day2_str = ",".join(map(str, h_id_day2))
        newh_day3_str = ",".join(map(str, h_id_day3))
        newv_day1_str = ",".join(map(str, h_vo_day1))


        # 建立新df做每日報表
        # 以後加入創新高個股名單
        new_stocks=""
        if newup == [] :
            new_stocks = "Today no new stocks"
        else:
            # for new_one in newup:
            #     new_stocks = new_stocks+","+str(new_one)
            new_stocks = ",".join(map(str, newup))

        onedaytype = {
            "Up_date" : DATE,
            "New_up" : NVARCHAR(length=1000),
            "day1_high" : NVARCHAR(length=10000),
            "day2_high" : NVARCHAR(length=10000),
            "day3_high" : NVARCHAR(length=10000),
            "d1vo_high" : NVARCHAR(length=10000),
            }
        
        a_day = {
            "Up_date" : now_day,
            "New_up" : new_stocks,
            "day1_high" : newh_day1_str,
            "day2_high" : newh_day2_str,
            "day3_high" : newh_day3_str,
            "d1vo_high" : newv_day1_str
        }

        # 必須設index
        df_day = pd.DataFrame(a_day, index=[0])
        print(df_day)
        df_day.to_sql('sum_oneday', engine, if_exists='append', dtype=onedaytype ,index=False  )

        if now_day == today:
            break
        
        x = x+1
        timegap = 0
        # 休息五秒進行下一日
        time.sleep(2)




