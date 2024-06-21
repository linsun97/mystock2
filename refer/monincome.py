import  urllib.request,csv
import time
from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer
import pandas as pd

# upnewd = datetime.now("Ymd")
#--會出現-2023-12-08 11:23:57.611618
# upnewd = datetime.timestamp
#--會出現-1549836078
# upnewd = datetime.today().strftime('%Y%m%d')
# upnewd = datetime.today().strftime('%Y%m%d')
#會出現20231208,但要到下午3:46以後才有檔案

def Monincome(yearlist,monlist):
    markte_list = ["rotc","otc","sii"]
    # markte_list = ["rotc"]
    # year_list = ["113"]
    # mon_list = ["3"]
    try:
        
        for down_y in yearlist:
            for down_m in monlist:
                for market in markte_list:
                    # today = datetime.now() 
                    # upnewd_y = datetime.strftime(today, '%Y')
                    # upnewd_m = datetime.strftime(today, '%m')
                    # down_y = int(upnewd_y) - 1911
                    # down_m = int(upnewd_m) - 1
                    # print(yesd)
                    #站食用昨天日期來測試20231207
                    print(market,down_y,down_m)
                    time.sleep(5)
                    engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
                    url = f"https://mops.twse.com.tw/nas/t21/{market}/t21sc03_{down_y}_{down_m}.csv"
                    print(url)
                    webpage = urllib.request.urlopen(url)  #開啟網頁
                    # data = csv.reader(webpage.read().decode('utf-8').splitlines()) #讀取資料到data陣列中
                    data = csv.reader(webpage.read().decode('utf-8', errors='ignore').splitlines() ) #讀取資料到data陣列中
                    # print(data)
                    # quit()
                    next(data,None)
                    
                    for i in data:
                        # print(type(i[5]))
                        # quit()
                        stockid = i[2].strip()
                        if i[5].strip() != ""  :
                            income = round(float(i[5].strip())/100000 ,2)
                        else:
                            income = 0.0

                        if i[8].strip() != "" :
                            lastmon = round(float(i[8].strip()),2)
                        else:
                            lastmon = 0.0

                        if i[9].strip() != "" :
                            lastyea = round(float(i[9].strip()),2)
                        else:
                            lastyea = 0.0

                        if i[10].strip() != "" :
                            allincome = round(float(i[10].strip())/100000,2)
                        else:
                            allincome = 0.0

                        if i[12].strip() != "" :
                            alllastyea = round(float(i[12].strip()),2)
                        else:
                            alllastyea = 0.0

                            # 去掉前後的空白
                        stock_shin = [i[1].strip(),stockid,i[3].strip(),income,lastyea,allincome,alllastyea]
                        all_stocks_shin.append(stock_shin)

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        pass



# ----------------------------------------
today = datetime.today().date()
yearnum = datetime.strftime(today, '%Y')
monthnum = datetime.strftime(today, '%m')
daynum = datetime.strftime(today, '%d')
tynum = int(yearnum) - 1911
tmnum = int(monthnum) - 1

yearlist = [str(tynum)]
monlist = [str(tmnum)]
# monlist = ["1","2","3","4","5"]

# -----將Monincome資料寫入資料庫--------------------------------------
def intomontable(all_stocks_shin,today,tynum,tmnum):
    df = pd.DataFrame(all_stocks_shin)
    df.columns = ["up_date","stockid","stockname","income","lastyea","allincome","alllastyea"]
    df_select = df.query("lastyea > 30 and alllastyea > 20")
    df_slist = df_select['stockid'].to_list()
    all_select = ",".join(df_slist)
    # all_list = all_select.split(",")
    # print(all_list)
    
    df_incomedict = {
        'up_date' : today,
        'allstockid' : all_select,
        'upym' : str(tynum) + "/" + str(tmnum)
    }
    df_income = pd.DataFrame(df_incomedict ,index=[0])
    df_income = df_income.astype(
                                {
                                    "up_date" : "datetime64[ns]",
                                    "allstockid" : "category",
                                    "upym" : "category"
                                }
                                )

    engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
    df_income.to_sql('monincome', engine, if_exists='append', index=False )
    print(df_income)
    # quit()
# -------------------------------------------

for mon in monlist:
    all_stocks_shin = []
    if (monthnum =="2") and (daynum == "20"):
        Monincome(yearlist,monlist)
        intomontable(all_stocks_shin,today,tynum,tmnum)
    else:
        if daynum == "13":    #如果是13號
            Monincome(yearlist,monlist)
            intomontable(all_stocks_shin,today,tynum,tmnum)
        
        # Monincome(yearlist,[mon])
        # intomontable(all_stocks_shin,today,tynum,tmnum)

