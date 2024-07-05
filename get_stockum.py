
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from fake_useragent import UserAgent
import requests 
from bs4 import BeautifulSoup 
import time
from datetime import date, datetime
from sqlalchemy import create_engine

user_agent = UserAgent()
headers_i = { 'user-agent': user_agent.random }

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock",pool_size=100,pool_recycle=3600, max_overflow=40,echo=False)
pd.set_option("display.float_format",'{:.2f}'.format)

h_day1 = []
h_id_day1=[]
h_day2 = []
h_id_day2=[]
h_day3 = []
h_id_day3=[]
h_vol_day1 = []
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

def get_stockum():
    try:
        merged_df = pd.DataFrame()
        # for dnum,s_link in enumerate(a_link): # a_link:
        url = f"https://tw.stock.yahoo.com/class-quote?sectorId=49&exchange=TAI"
        # response = requests.get(url ,headers=headers_i ,verify=False)
        response = requests.get(url,headers=headers_i)
        response.encoding='utf-8' 
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser") 
            # print(soup)
            stockname = soup.findAll('div', {"class" : "Lh(20px)"})
            stockid = soup.findAll('span', {"class" : "Fz(14px) C(#979ba7) Ell"})
            price = soup.findAll('div', {"class" : "Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(68px)"})
                                                    # Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(68px)
            volume = soup.findAll('div', {"class" : "Fxg(1) Fxs(1) Fxb(0%) Miw($w-table-cell-min-width) Ta(end) Mend($m-table-cell-space) Mend(0):lc"})
                                                    #  Fxg(1) Fxs(1) Fxb(0%) Miw($w-table-cell-min-width) Ta(end) Mend($m-table-cell-space) Mend(0):lc
            volume_list = []
            # print(stockname)
            # print(stockid)
            # print(price)
            # print(volume)
            # quit()
            volume.pop(0)
            for i,y in enumerate(volume):
                if "<" in y.text :
                    y_text = y.text
                    y_1 = y_text.text.replace(",","")
                    if y_1 != "-" :
                        volume_list.append(y_1)
                    else :
                        volume_list.append(0)
                else :
                    if y.text.replace(",","") != "-":
                        volume_list.append(y.text.replace(",",""))
                    else :
                        volume_list.append(0)
                
            price_list = []
            for i,y in enumerate(price):
                if i % 5 == 0:
                        if y.text.replace(",","") != "-":
                            price_list.append(y.text.replace(",",""))
                        else :
                            price_list.append(0)
                    
            price_list.pop(0)
            # quit()
            stockid_list = []
            for i,y in enumerate(stockid):
                if "<" in y.text :
                    y_text = y.text
                    y_1 = y_text.text.replace(".TW","")
                    if y_1 != "-" :
                        stockid_list.append(y_1)
                else :
                    if y.text.replace(",","") != "-":
                        stockid_list.append(y.text.replace(".TW",""))

                stockname_list = []
            for i,y in enumerate(stockname):
                if "<" in y.text :
                    y_text = y.text
                    y_1 = y_text.text.replace(",","")
                    if y_1 != "-" :
                        stockname_list.append(y_1)
                else :
                    if y.text.replace(",","") != "-":
                        stockname_list.append(y.text.replace(",",""))
            # print(stockname_list)
            # print(stockid_list)
            # print(price_list)
            # print(volume_list)
            # quit()
            
            all_stocks = {
                "stock_id" : stockid_list,
                "stock_name" : stockname_list,
                "price" : price_list,
                "volume" : volume_list
            }

            df = pd.DataFrame(all_stocks)
            df = df.astype(
                {
                    "stock_id" : "category",
                    "stock_name" : "category",
                    "price" : "float64",
                    "volume" : "category",
                }
            )


            time.sleep(2)

        # print(df_all.head(5))
        # quit()
        df_real = df.query("stock_id.str.len() == 4 & stock_id.str.isnumeric()") 
        # print(df_real.head(5))
        # return df_real
        def onerow_nh(row):
                # 把row從series變dataframe,取出的row會被當成series但他是直行,先變成list,再變成橫的dataframe
                row_pd = pd.DataFrame([row])
                nowstockid = row_pd.iloc[0,0]
                nowname = row_pd.iloc[0,1]
                nowprice = float(row_pd.iloc[0,2])
                nowvolume = float(row_pd.iloc[0,3])
                newhigh(nowprice,nowstockid,nowname,nowvolume,30,60,90)
                # return h_day1,h_day2,h_day3,h_vol_day1
        
        df_real.apply(onerow_nh,axis = 1)
        return h_day1,h_day2,h_day3,h_vol_day1
        # return h_day1,h_day2,h_day3,h_vol_day1
        # df.apply(newhigh,axis = 1)

    except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    
# h_d1,h_d2,h_d3,h_vol_d1 = get_stockum()
# print(h_d1,h_d2,h_d3,h_vol_d1)