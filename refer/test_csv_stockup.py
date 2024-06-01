import  urllib.request,csv
from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer , DATE
import pandas as pd
import numpy as np
import time
import email.message

# 設定float格式為小數點後兩位
pd.set_option("display.float_format",'{:.2f}'.format)
today = datetime.today().date()

#站食用昨天日期來測試20231207
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
try:
    last_date = pd.read_sql("SELECT Up_date FROM sup_oneday ORDER BY Up_date DESC LIMIT 1",engine)
    last_date = last_date.iloc[0,0]
except:   
    pass
# quit()


x = 1
timegap = 0
while True:
    old_stocks = []
    try:
        old_df = pd.read_sql('select stockid from all_id_name',engine)
        old_stocks = old_df['stockid'].tolist() # 把series變成list
        # print(old_stocks)
        # quit()
    except:
        pass

    x = x+timegap
    now_day = last_date + timedelta(days=x) 
    yearnum = datetime.strftime(now_day, '%Y')

    # weekday : 0-6,sunday為6, isoweekday : 1-7 sunday為7
    # week_day = datetime.weekday(now_day)
    week_day = datetime.isoweekday(now_day)
    if now_day > today :
        quit()
    # if week_day == 5 or week_day == 6: #星期六或星期日
    #     continue
    # 算出民國年
    tynum = int(yearnum) - 1911
    upnewd = datetime.strftime(now_day, str(tynum)+'/%m/%d')

    url = f"https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d={upnewd}&s=0,asc" #上櫃公司-政府公開資料
    print(url)
    try:
        timegap = 0
        data = pd.read_csv(url,usecols=[0,1,2,4,5,6,7,8],thousands=',', encoding='cp950',
                    names=['stockid','stockname','over','open','high','low','bef','volume'],
                    #   index_col='stockid',
                    na_values=["-", " "],skipfooter=8,header=2,
                    engine="python")
        # print(data)
    except:
        print(f"{upnewd}(星期{week_day})今天可能是假日")
        timegap = 1
        continue
    # quit()
    all_id_name = []
    all_stocks_shin = []
    new_id = []
    try: 
        for i,row in data.iterrows():
            if len(row["stockid"]) !=  4 :
                continue
            stock_shin_id_name = [str(row["stockid"]).strip(),str(row["stockname"]).strip()]
            stock_shin = [str(row["stockid"]).strip(),str(row["stockname"]).strip(),row["over"],row["open"],row["high"],row["low"],row["bef"],row["volume"]]
            all_id_name.append(stock_shin_id_name)
            all_stocks_shin.append(stock_shin)
            new_id.append(int(str(row["stockid"]).strip()))
    except:
        pass

    # print("----new_id------")
    # print(new_id)
    df = pd.DataFrame(all_stocks_shin)
    df_id_name = pd.DataFrame(all_id_name)

    df.columns = ["stockid","stockname","over","open","high","low","bef","volume"]
    df_id_name.columns = ["stockid","stockname"]
    df['up_date'] = now_day

# str轉為字串,strip去掉前後的空白
    df['open'] = df['open'].str.strip()
    df['high'] = df['high'].str.strip()
    df['low'] = df['low'].str.strip()
    df['over'] = df['over'].str.strip()


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
                    "up_date":"datetime64[ns]"
                }
            )

    newup = [x for x in new_id if x not in old_stocks]
    # 如果有新股上市寄郵件通知自己
    if newup != []:
        msg=email.message.EmailMessage()
        #利用物件建立基本設定
        from_a = "linsun97@gmail.com"
        to_b = "linsun97@gmail.com"

        msg["From"]=from_a
        msg["To"]=to_b
        msg["Subject"]="上櫃新增股票"
        content = ''
        for new_s in newup :
            content = content + f"<a href='http://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={new_s}&year=&seamon=&mtype=B&'>{new_s}的公開說明書</a><br>" + \
                                f"<a href='https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID={new_s}'>{new_s}的goodinfo</a><br>" + \
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
    else:
        print(f"{upnewd}今日無新股上櫃")
    # print(newup)
    # 將新上興櫃的股票寫入文字檔中
    with open("newup_stockup.txt","w") as file:
        for new_s in newup :
            # int不可和str相加
            file.write(str(new_s)+"\n")

    # print(df)
    # quit()
    dtypedict = {
            'stockid': Integer,
            'stockname': NVARCHAR(length=100),
            'over':Float,
            'open': Float,
            'high': Float,
            'low': Float,
            'bef': Float,
            'volumn': Integer,
            'up_date' : DATE,
            }

    d_id_dtype = {
            'stockid': Integer,
            'stockname': NVARCHAR(length=100)
            }
        
        # 設定欄位名稱,若沒設定預設是用0,1,2,3....當欄位名稱
    df_id_name.to_sql('all_id_name', engine, if_exists='replace',dtype=d_id_dtype,index=False)    

        # sql_df = pd.read_sql('all_stocks_shin', engine)
    def IntoTable(row):
        # 把row從series變dataframe,取出的row會被當成series但他是直行,先變成list,再變成橫的dataframe
        row_pd = pd.DataFrame([row])
        row_pd.to_sql(f'st_{row_pd.iloc[0,0]}', engine, if_exists='append', dtype=dtypedict ,index=False  )
        print(f"新增st_{row_pd.iloc[0,0]}資料表成功,股名:{row_pd.iloc[0,1]}")
    # 可以用df.apply的方法加上axis = 1,就可以把df內每一列當成一個row去執行IntoTable函式
    df.apply(IntoTable,axis = 1)

    # 建立新df做每日報表
    # 以後加入創新高個股名單
    if newup == [] :
        newup = "Today no new stock"
    onedaytype = {
        "Up_date" : DATE,
        "New_up" : NVARCHAR(length=1000),
    }
    new_stocks = "news" 
    for new_one in newup:
        new_stocks = new_stocks+","+new_one
    a_day = {
        "Up_date" : now_day,
        "New_up" : new_stocks
    }

    # 必須設index
    df_day = pd.DataFrame(a_day, index=[0])
    print(df_day)
    df_day.to_sql('sup_oneday', engine, if_exists='append', dtype=onedaytype ,index=False  )

    if now_day == today:
        break
    
    x = x+1
    # 休息五秒進行下一日
    time.sleep(10)
