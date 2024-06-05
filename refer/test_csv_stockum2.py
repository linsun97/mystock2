from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer,DATE
import pandas as pd
import email.message
import twstock
# pip install twstock
# 發現創新版沒有在twstock中

pd.set_option("display.float_format",'{:.2f}'.format)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
today = datetime.today().date()

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
try:
    last_date = pd.read_sql("SELECT Up_date FROM sum_oneday ORDER BY Up_date DESC LIMIT 1",engine)
    last_date = last_date.iloc[0,0]
except:   
    pass

# -----------------------------------------

old_stocks = []
try:
    old_df = pd.read_sql('select stockid from all_id_name_sum',engine)
    old_stocks = old_df['stockid'].tolist() # 把series變成list
    # print(old_stocks)
    # quit()
except:
    pass
#---------------------------------------------------------

# now_day = last_date + timedelta(days=x) 
# weekday : 0-6,sunday為6, isoweekday : 1-7 sunday為7
# week_day = datetime.weekday(now_day)
# week_day = datetime.isoweekday(now_day)
# upnewd = datetime.strftime(now_day, '%Y%m%d')
# if week_day == 5 or week_day == 6: #星期六或星期日
#     continue
# if now_day > today :
#     quit()

url = "https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv"
print(url)
    
try:
    timegap = 0
    data = pd.read_csv(url,
                #  na_values="-"
                header=0,
                # skipfooter=6,
                usecols=[1,3],
                names=['stockid','stockname'],
                thousands=",",
                encoding="utf-8",
                #  parse_dates=["dateone"], #需用中掛號包住
                #  date_format="%Y%m%d",
                #  true_values=["yes"], #需用中掛號包住
                #  false_values=["no"], #需用中掛號包住
                # engine='python'
                
                )
    
except:
    # print(f"{now_day}(星期{week_day})今天可能是假日")
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
    # df_day.to_sql('sum_oneday', engine, if_exists='append', dtype=onedaytype ,index=False  )
    
    # timegap = 1
    # continue
    pass

# print(data)
# quit()
new_id = []
all_id_name = []
try: 
    for i,row in data.iterrows():
        # print(row)
        # 原始資料內有空白,必須先去掉
        if len(str(row["stockid"]).strip()) !=  4 :
            continue
        stock_shin_id_name = [str(row["stockid"]).strip(),str(row["stockname"]).strip()]
        all_id_name.append(stock_shin_id_name)
        new_id.append(int(str(row["stockid"]).strip()))
except:
        pass   

# -------------------------------------------

newup = [x for x in new_id if x not in old_stocks]
# print(old_stocks)
# print(new_id)
# quit()
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
with open("newum_stock.txt","w") as file:
    for new_s in newup :
        file.write(str(new_s)+"\n")
# ----------------------------------------------

df_id_name = pd.DataFrame(all_id_name)

df_id_name.columns = ['stockid','stockname']
# print(df_id_name)
d_id_dtype = {
            'stockid': Integer,
            'stockname': NVARCHAR(length=100)
            }
df_id_name.to_sql('all_id_name_sum', engine, if_exists='replace',dtype=d_id_dtype,index=False)    

# --------------------------------
# quit()

for stock_id in new_id :
    stock = twstock.Stock(str(stock_id))
    stock1 = twstock.realtime.get(str(stock_id))
    # 取得股名
    c_name = stock1["info"]["name"]
    # print(c_name)
    # 會抓從上次更新以來那個月的1號到今日的資料
    stock_mon = stock.fetch_from(last_date.year,last_date.month)
    

    # 測試只有一筆資料會不會變成series,結果不會
    # stock_mon = stock.fetch_from(today.year,today.month)
    # print(stock_oneday) 
    df_stock = pd.DataFrame(stock_mon)
    # 只要最後登記日之後的紀錄
    df_stock = df_stock.query('date > @last_date')
    # print(df_stock)
    # quit()
    # 刪掉不要的欄位
    df_stock = df_stock.drop(["turnover","change","transaction"],axis=1)
    # 重設index,原本為date做index
    df_stock = df_stock.reindex(columns=["close", "open", "high", "low","capacity","date"]) 
    # 插入一個bef欄,設值為0
    df_stock.insert(4,"bef",0)
    # df_stock = df_stock.reset_index()
    # print(df_stock)
    # print(df_stock.info())
    df_stock = df_stock.rename(columns={"close":"over","capacity":"volume","date":"up_date"})
    # print(df_stock)
    # print(df_stock.info())
    df_stock.insert(0,"stockid",str(stock_id))
    df_stock.insert(1,"stockname",c_name)
    df_stock['stockid'].astype("int64")

    dtypedict = {
                'stockid': Integer,
                'stockname': NVARCHAR(length=100),
                'over':Float,
                'open': Float,
                'high': Float,
                'low': Float,
                'bef': Float,
                'volume': Integer,
                'up_date' : DATE,
                }
    
    df_stock = df_stock.astype(
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
    df_stock.to_sql(f'st_{stock_id}', engine, if_exists='append', dtype=dtypedict ,index=False  )
    print(f"新增st_{stock_id}資料表成功,股名:{c_name}")
    # print(df_stock)
    # print(df_stock.info())
    # quit()

    # testday = nowtime.strftime("%Y-%m-%d %H:%M:%S"
    
# --------------------------------------------------------------
# 以後加入創新高個股名單
new_stocks=""
if newup == [] :
    new_stocks = "Today no new stocks"
else:
    for new_one in newup:
        new_stocks = new_stocks+","+str(new_one)

onedaytype = {
    "Up_date" : DATE,
    "New_up" : NVARCHAR(length=1000),
    }

a_day = {
    "Up_date" : today,
    "New_up" : new_stocks
}

# 必須設index
df_day = pd.DataFrame(a_day, index=[0])
print(df_day)
df_day.to_sql('sum_oneday', engine, if_exists='append', dtype=onedaytype ,index=False  )