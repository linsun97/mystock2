from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer,DATE
import pandas as pd
import email.message
import time
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

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
    last_date = pd.read_sql("SELECT Up_date FROM shin_oneday ORDER BY Up_date DESC LIMIT 1",engine)
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
        old_df = pd.read_sql('select stockid from all_id_name_shin',engine)
        old_stocks = old_df['stockid'].tolist() # 把series變成list
        # print(old_stocks)
        # quit()
    except:
        pass

    x = x+timegap
    now_day = last_date + timedelta(days=x) 
    # weekday : 0-6,sunday為6, isoweekday : 1-7 sunday為7
    # week_day = datetime.weekday(now_day)
    week_day = datetime.isoweekday(now_day)
    upnewd = datetime.strftime(now_day, '%Y%m%d')
    # if week_day == 5 or week_day == 6: #星期六或星期日
    #     continue
    if now_day > today :
        quit()

    # url = f"https://www.tpex.org.tw/web/emergingstock/historical/daily/EMDaily_dl.php?l=zh-tw&f=EMdes010.{upnewd}-C.csv"
    url = f"https://www.tpex.org.tw/www/zh-tw/emerging/dailyDl?name=EMdes010.{upnewd}-C.csv"
    # 網址已改
    
    print(url)

    
    
    try:
        timegap = 0
        data = pd.read_csv(url,
                    #  na_values="-"
                    header=3,
                    skipfooter=6,
                    usecols=[1,2,6,9,10,11,12],
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
        print(f"{upnewd}(星期{week_day})今天可能是假日")
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
        # df_day.to_sql('shin_oneday', engine, if_exists='append', dtype=onedaytype ,index=False  )
        
        timegap = 1
        continue
    
    # 新增一個open的欄位,只有bef是float,所以open也是float
    data['open'] = data['bef']

    all_id_name = []
    all_stocks_shin = []
    new_id = []
    # print(data)
    # quit()
    try: 
        for i,row in data.iterrows():
            # print(row)
            # 原始資料內有空白,必須先去掉
            if len(str(row["stockid"]).strip()) !=  4 :
                continue
            
            stock_shin_id_name = [str(row["stockid"]).strip(),str(row["stockname"]).strip()]
            stock_shin = [str(row["stockid"]).strip(),str(row["stockname"]).strip(),row["over"],row["open"],row["high"],row["low"],row["bef"],row["volume"]]
            # print(stock_shin)
            all_id_name.append(stock_shin_id_name)
            all_stocks_shin.append(stock_shin)
            # print(all_stocks_shin)
            new_id.append(int(str(row["stockid"]).strip()))
    except:
        pass
    
    # quit()
    # print("----new_id------")
    # print(new_id)
    df = pd.DataFrame(all_stocks_shin)
    # print(df)
    # quit()
    df_id_name = pd.DataFrame(all_id_name)
    
    
    df.columns = ["stockid","stockname","over","open","high","low","bef","volume"]
    df_id_name.columns = ["stockid","stockname"]
    df['up_date'] = now_day

# str轉為字串,strip去掉前後的空白
    if (is_string_dtype(df['open'])):
        df['open'] = df['open'].str.strip()
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
        
    # 將值為"-"的內容換成bef的值或0
    df.loc[df['high']=="-",['high','low','over']] = df.loc[df['high']=="-",'bef']
    # 這兩種寫法,以後的pandas不支援
    if (is_string_dtype(df['bef'])):
        df.loc[df['open']=="-",'open'] = df.loc[df['open']=="-",'over']
        df.loc[df['bef']=="-",'bef'] = df.loc[df['bef']=="-",'over']
    

    df.loc[df['volume']=="-",'volume'] = 0
    
    df['kwave'] = 0.0
    df['rci'] = 0.0
    df['updown'] = 0.0
    df['kwr'] = 0.0
    # 50天相對強度
    df['pc'] = 0.0
    df['rs'] = 0.0
    df['nh'] = ''
    df = df.astype(
                {
                    'stockid':'int16',
                    'stockname':'category',
                    'over':'float32',
                    'open':'float32',
                    'high':"float32",
                    'low':"float32",
                    'bef':"float32",
                    "volume":"float32",
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
    df.loc[df['over'] < df['open'],'kwave'] = abs(df['open']-df['over'])+abs(df['open']-df['high'])+abs(df['high']-df['low'])+abs(df['low']-df['over'])
    df.loc[df['over'] >= df['open'],'kwave'] = abs(df['open']-df['over'])+abs(df['open']-df['low'])+abs(df['low']-df['high'])+abs(df['high']-df['over'])
    df['volume'] = df['volume']/1000
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
        msg["Subject"]="興櫃新增股票"
        content = ''
        for new_s in newup :
            content = content + f"<a href='http://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={new_s}&year=&seamon=&mtype=B&'>{new_s}的公開說明書</a><br>" + \
                                f"<a href='https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID={new_s}'>{new_s}的goodinfo</a><br>" +\
                                f"<a href='https://mops.twse.com.tw/mops/web/t100sb07_1'>法說會簡報下載</a><br>" +\
                                f"<a href='https://www.notion.so/1515881a4368804d8f41d4c7bdf38638'>摘要</a><br><br>"
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
    # with open("newshin_stock.txt","w") as file:
    #     for new_s in newup :
    #         file.write(str(new_s)+"\n")

# -------------------------------------------------------------
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
    df_id_name.to_sql('all_id_name_shin', engine, if_exists='replace',dtype=d_id_dtype,index=False)    
    
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

            # print(h_id_day1)
            # print(row_pd)
            # quit()

            row_pd.to_sql(f'st_{row_pd.iloc[0,0]}', engine, if_exists='append', dtype=dtypedict ,index=False  )
            print(f"新增st_{row_pd.iloc[0,0]}資料表成功,股名:{row_pd.iloc[0,1]}")
        # 可以用df.apply的方法加上axis = 1,就可以把df內每一列當成一個row去執行IntoTable函式
    df.apply(IntoTable,axis = 1)

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
    df_day.to_sql('shin_oneday', engine, if_exists='append', dtype=onedaytype ,index=False  )

    if now_day == today:
        break
    
    x = x+1
    # 休息五秒進行下一日
    time.sleep(2)




