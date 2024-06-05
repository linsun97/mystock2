import  urllib.request,csv
from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer
import pandas as pd
import email.message
# upnewd = datetime.now("Ymd")
#--會出現-2023-12-08 11:23:57.611618
# upnewd = datetime.timestamp
#--會出現-1549836078
# upnewd = datetime.today().strftime('%Y%m%d')
# upnewd = datetime.today().strftime('%Y%m%d')
#會出現20231208,但要到下午3:46以後才有檔案
yesterday = datetime.now() - timedelta(days = 1)
upnewd = datetime.strftime(yesterday, '%Y%m%d')
# print(yesd)
#站食用昨天日期來測試20231207
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
old_df = pd.read_sql('select stock_id from all_stockums_shin',engine)
old_stocks = old_df['stock_id'].tolist() # 把series變成list
# url = f"http://www.gretai.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_download.php?l=zh-tw&d=112/12/14&se=AL"
# url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG_ALL?response=open_data" #上市-政府公開資料
# url = "https://mopsfin.twse.com.tw/opendata/t187ap35_L.csv" #上市公司-政府公開資料
url = "https://mopsfin.twse.com.tw/opendata/t187ap05_L.csv" #上市公司-政府公開資料
# print(url)

webpage = urllib.request.urlopen(url)  #開啟網頁
webpage
# print(webpage)
data = csv.reader(webpage.read().decode('utf-8', errors='ignore').splitlines()) #讀取資料到data陣列中
# 去掉第一筆標頭不抓入資料庫
next(data,None)
# data = csv.reader(webpage.read().decode('Big5', errors='ignore').splitlines() ) #讀取資料到data陣列中
# print(data)

# quit()
all_stocks_shin = []
new_id = []
for i in data:
    # if i[0] == "BODY" and i[3] != '':
        # print(i)
        # 去掉前後的空白
    stock_shin = [i[2].strip(),i[3].strip()]
    all_stocks_shin.append(stock_shin)
    new_id.append(i[2].strip())
    

df = pd.DataFrame(all_stocks_shin)

newup = [x for x in new_id if x not in old_stocks]
# print(newup)
# quit()
# 如果有新股上市寄郵件通知自己
if newup != []:
    msg=email.message.EmailMessage()
    #利用物件建立基本設定
    from_a = "linsun97@gmail.com"
    to_b = "linsun97@gmail.com"

    msg["From"]=from_a
    msg["To"]=to_b
    msg["Subject"]="上市新增股票"
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

# print(newup)
# 將新上興櫃的股票寫入文字檔中
with open("newup_stockum.txt","w") as file:
    for new_s in newup :
        file.write(new_s+"\n")

# print(df)
# quit()
dtypedict = {
        'stock_id': NVARCHAR(length=25),
        'stock_name': NVARCHAR(length=100)
        }
    
    # 設定欄位名稱,若沒設定預設是用0,1,2,3....當欄位名稱
    # df.columns = ['season','op_cf', 'in_cf', 'fi_cf','else_cf','updown','total_cf']
df.columns = list(dtypedict.keys())
    # df.to_sql('cash_6762', engine, if_exists='replace')
df.to_sql('all_stockums_shin', engine, if_exists='replace',dtype=dtypedict)    

    # sql_df = pd.read_sql('all_stocks_shin', engine)



