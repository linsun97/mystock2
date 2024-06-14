import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
    
# -----偵測創新高的函數--------------------------------------------
# 這樣做h_day1,h_id_day1會變成全域變數
h_day1 = []
h_id_day1=[]
h_day2 = []
h_id_day2=[]
h_day3 = []
h_id_day3=[]

def newhigh(nprice,nstockid,nstockname,nvolume,day1,day2,day3):
    pd.set_option("display.float_format",'{:.2f}'.format)
    try:
        df_list = pd.read_sql(f"SELECT * FROM st_{nstockid} ORDER BY up_date DESC LIMIT 150",engine )
        df_id_nh = pd.DataFrame(df_list)
        print(df_id_nh)
        df_head1 = df_id_nh.head(day1)
        print(df_head1) 
        df_head2 = df_id_nh.head(day2)
        print(df_head2)  
        df_head3 = df_id_nh.head(day3)
        print(df_head3)  

        day1max = df_head1['over'].max()
        print(day1max)
        day2max = df_head2['over'].max()
        print(day2max)
        day3max = df_head3['over'].max()
        print(day3max)

        day1mean = df_head1['volume'].mean()
        print(day1mean)

        if nprice >= day1max:
            print(f"{nstockid},{nstockname}創{day1}天新高")
            # 取到小數點後兩位
            volume_day1 = round(nvolume/day1mean,2)
            print(f"成交量是平均值的{volume_day1}倍")
            h_day1.append(f"{nstockid}({nstockname})")
            h_id_day1.append(f"{nstockid}")
            print(h_id_day1)

        # newh_day2 = []
        if nprice >= day2max:
            print(f"{nstockid},{nstockname}創{day2}天新高")
            h_day2.append(f"{nstockid}({nstockname})")
            h_id_day2.append(f"{nstockid}")
            print(h_id_day2)

        # newh_day3 = []
        if nprice >= day3max:
            print(f"{nstockid},{nstockname}創{day3}天新高")
            h_day3.append(f"{nstockid}({nstockname})")
            h_id_day3.append(f"{nstockid}")
            print(h_id_day3)
    
    except Exception as e:
        print(e)
        pass

     
# --------偵測創新高的函數結束--------------------------------------------------

newhigh(25,1569,"濱川",254130,30,60,90)

print(h_id_day1)      
print(h_id_day2)      
print(h_id_day3) 