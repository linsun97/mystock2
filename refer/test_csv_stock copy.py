import  urllib.request,csv
from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer
import pandas as pd
import email.message
import time

# 設定float格式為小數點後兩位
pd.set_option("display.float_format",'{:.2f}'.format)
today = datetime.today().date()
yesterday = datetime.now() - timedelta(days = 1)
upnewd = datetime.strftime(yesterday, '%Y%m%d')
# print(yesd)
#站食用昨天日期來測試20231207
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
old_df = pd.read_sql('select stock_id from all_stocks_shin',engine)
old_stocks = old_df['stock_id'].tolist() # 把series變成list
# print(old_stocks)
# quit()

# 若當天沒有資料往前一直到有資料當天
mykey = 0
while mykey < 1 :
    url = f"http://www.gretai.org.tw/web/emergingstock/historical/daily/EMDaily_dl.php?l=zh-tw&f=EMdes010.{upnewd}-C.csv"
    print(url)
    webpage = urllib.request.urlopen(url)  #開啟網頁
    # data = csv.reader(webpage.read().decode('utf-8').splitlines()) #讀取資料到data陣列中
    data = csv.reader(webpage.read().decode('Big5', errors='ignore').splitlines() ) #讀取資料到data陣列中
    
    if mykey == 1:
        print("over")
        break
    
    for row in data :
        if data.line_num == 1:
            mykey = 1
            break
    
    upnewd = int(upnewd) - 1


all_stocks_shin = []
new_id = []
for i in data:
    if i[0] == "BODY" and i[3] != '':
        # print(i)
        # 去掉前後的空白
        stock_shin = [i[1].strip(),i[2].strip()]
        all_stocks_shin.append(stock_shin)
        new_id.append(i[1].strip())

df = pd.DataFrame(all_stocks_shin)
# print(new_id)
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
with open("newup_stock.txt","w") as file:
    for new_s in newup :
        file.write(new_s+"\n")

# quit()
# print(df)
dtypedict = {
        'stock_id': NVARCHAR(length=25),
        'stock_name': NVARCHAR(length=100)
        }
    
    # 設定欄位名稱,若沒設定預設是用0,1,2,3....當欄位名稱
    # df.columns = ['season','op_cf', 'in_cf', 'fi_cf','else_cf','updown','total_cf']
df.columns = list(dtypedict.keys())
    # df.to_sql('cash_6762', engine, if_exists='replace')
df.to_sql('all_stocks_shin', engine, if_exists='replace',dtype=dtypedict)    

    # sql_df = pd.read_sql('all_stocks_shin', engine)



