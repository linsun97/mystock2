import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import mariadb
from datetime import date

pd.set_option("display.float_format",'{:.2f}'.format)
# 不設下列對切片做運算時會出錯
pd.set_option("copy_on_write",True)

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")

mydb = mariadb.connect(
  host="localhost",
  user="root",
  password="nineseve9173",
  database="stock"
)

mycursor = mydb.cursor()
df_tpex = pd.read_sql("all_id_name",engine)
# 用5筆測試
# df_tpex = df_tpex.head(20) 



# ---計算出每隻股的rs--------------------------------------
rs = []
def cal_ratio(row):
    row_pd = pd.DataFrame([row])
    # --------------------------
    nowstockid = row_pd.iloc[0,0]
    # print(nowstockid) 
    nowname = row_pd.iloc[0,1]
    # print(nowname) 
    df = pd.read_sql(f"st_{nowstockid}",engine)
    # print(df)
    # 算出最後一次更新日期
    df_l = df.loc[df['rci'] != 0]
    # print(df_l)
    # print(df_l.iloc[-1,:].up_date)
    # 最後更新rci的日期
    l_rci_d = df_l.iloc[-1,:].up_date
    start_d = date(l_rci_d.year,l_rci_d.month,l_rci_d.day)
    # print(start_d)
    # 目前資料最後一筆的日期
    n_rci_d = df.iloc[-1,:].up_date
    end_d = date(n_rci_d.year,n_rci_d.month,n_rci_d.day)
    # print(end_d)
    # quit()
    # if start_d != end_d :

    date_range = pd.date_range(start_d,end_d,inclusive="right",freq="D")
    # print(date_range)
    # quit()

    for one_d in date_range :
        try:
        # 計算RCI---------------------------------
        # print(df)
            # df_copy = df.copy()
            df_copy = df.tail(60).copy()
            df_xday = df_copy.iloc[-20:]
            # print(df_xday)
            df_xday['date_rank'] = df_xday['up_date'].rank(method='min',ascending=False)
            # print(df_xday)
            df_xday['price_rank'] = df_xday['over'].rank(method='min',ascending=False)
            # print(df_xday)
            df_xday['d1day'] = (df_xday['date_rank']-df_xday['price_rank'])**2
            D = df_xday['d1day'].sum()
            # print(df_xday) 
            # print(D)
            rci = round((1-6*D/(20*(400-1)))*100,2)
            # print(rci)
            # print(last_d)

            # 計算kwr---k線波動率20日------------------------------
            # print(df_xday)
            # quit()
            kw_mean = df_xday['kwave'].mean()
            over_mean = df_xday['over'].mean()
            kw_ratio = round((kw_mean/over_mean)*100,2)
            # print(df_xday)
            # quit()

            # 計算updown 一段時間的波動率範圍-預設為50天--------------------------------
            df_xday = df_copy.iloc[-50:]
            max_value = df_xday['over'].max()
            min_value = df_xday['over'].min()
            mean_value = df_xday['over'].mean()

            updown = round((max_value-min_value)/mean_value*100,2)
            # print(updown)
            # quit()

            # 計算rs(beta) 一段時間的對大盤相對強度-預設為50天--------------------------------
            df_long = df_xday.iloc[0]
            # print(df_long)
            df_long1 = df_long['over']
            # 最新over價
            df_newest = df_xday.iloc[-1,2]
            df_mean1 = round(df_xday.over.mean(),2)
            # 計算漲跌除平均乘100後取小數點2位
            bewt = ((df_newest-df_long1)/df_mean1)*100
            pc = round(bewt,2)
            # print(df_long1)
            # print(df_newest)
            # print(df_mean1)
            # print(pc)
            
            pc_dict = {
                "stockid" : nowstockid,
                "pc" : pc,
                "up_date" : one_d
                }
            rs.append(pc_dict)

          # 將數值更新到資料表--------------------------------
            sql = f"UPDATE st_{nowstockid} SET rci = {rci} ,updown ={updown} ,kwr = {kw_ratio} ,pc = {pc} WHERE up_date = '{one_d}'"
            print(sql)
            mycursor.execute(sql)
            mydb.commit()
            # print(f"更新{nowstockid},{nowname}的rci,updown,kwr,pc成功")
        except Exception as e :
            print(e)
            pass
    

# ----------將rs放入資料表中-----------------------------
def cal_rd(row):
    row_pd = pd.DataFrame([row])
    stockid = row_pd.iloc[0,0]
    sql = f"UPDATE st_{stockid} SET rs = {row_pd['rs'].iloc[0]} WHERE up_date = '{row_pd['up_date'].iloc[0]}'"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()
    # print(f"更新{stockid}的rs成功")   


df_tpex.apply(cal_ratio,axis=1)
df_rs = pd.DataFrame(rs)
df_rs['rank'] = df_rs['pc'].rank(method="min")
df_rs['rs'] = round((df_rs['rank']/len(df_rs))*100,2)
df_rs.apply(cal_rd,axis=1)

mydb.close()