import  urllib.request,csv
import time
from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer
import pandas as pd

pd.set_option("display.float_format",'{:.2f}'.format)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)  

def Monincome(yearlist,monlist):
    markte_list = ["rotc","otc","sii"]
    df_combi = pd.DataFrame()
    # markte_list = ["rotc"]
    # year_list = ["113"]
    # mon_list = ["3"]
    try:
        
        for down_y in yearlist:
            for down_m in monlist:
                for market in markte_list:
                    #站食用昨天日期來測試20231207
                    print(market,down_y,down_m)
                    time.sleep(5)
                    engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
                    url = f"https://mops.twse.com.tw/nas/t21/{market}/t21sc03_{down_y}_{down_m}.csv"
                    print(url)
                    df = pd.read_csv(url,
                                     usecols=[1,2,3,5,9,10,12],
                                     names=['upym','stockid','stockname','income','rate1','allincome','rate2'],
                                     thousands=",",
                                     na_values="",
                                     header=1,
                                    #  date_format='%Y/%m/%d',
                                    #  parse_dates=['up_date'],
                                     )
                    
                    df['income'] = df["income"]/100000
                    # df['lastyearmon'] = df["lastyearmon"]/100000
                    df['allincome'] = df["allincome"]/100000
                    # df['alllastmon'] = df["alllastmon"]/100000
                    df_combi = pd.concat([df_combi,df],axis=0) 
                    

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        pass

    return df_combi 

# -----將Monincome資料寫入資料庫--------------------------------------
def intomontable(df_all,today,tynum,tmnum):
    df = df_all
    df.columns = ["up_date","stockid","stockname","income","lastyea","allincome","alllastyea"]
    df_select = df.query("lastyea > 30 and alllastyea > 20")
    df_slist = df_select['stockid'].to_list()
    df_slist = list(map(str, df_slist))
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


today = datetime.today().date()
yearnum = datetime.strftime(today, '%Y')
monthnum = datetime.strftime(today, '%m')
daynum = datetime.strftime(today, '%d')
tynum = int(yearnum) - 1911
tmnum = int(monthnum) - 1

yearlist = [str(tynum)]
monlist = [str(tmnum)]
# ----------------------------------------
for mon in monlist:
    if (monthnum =="2") and (daynum == "20"):
        df_all = Monincome(yearlist,monlist)
        intomontable(df_all,today,tynum,tmnum)
    else:
        if (monthnum !="2") and (daynum == "16"):    #如果是13號
            
            df_all = Monincome(yearlist,monlist)
            # print(df_all)
            # quit()
            intomontable(df_all,today,tynum,tmnum)
        

