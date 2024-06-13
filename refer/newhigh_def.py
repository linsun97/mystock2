import pandas as pd
from sqlalchemy import create_engine

    
def newhigh(nowprice,stockid,stockname,day1,day2,day3):
    
    engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")

    pd.set_option("display.float_format",'{:.2f}'.format)
    # 抓最近一次更新日期
    try:
        last_date = pd.read_sql("SELECT Up_date FROM shin_newhigh ORDER BY Up_date DESC LIMIT 1",engine)
        last_date = last_date.iloc[0,0]
    except Exception as e:
        print(e)
        pass
    df_list = pd.read_sql(f"SELECT * FROM st_{stockid} ORDER BY up_date DESC LIMIT 150",engine )
    df_id_nh = pd.DataFrame(df_list)
    # print(df_id_nh)
    # df_id_nh = pd.DataFrame(f"st_{stockid}",index=False)
    df_head1 = df_id_nh.head(day1) 
    df_head2 = df_id_nh.head(day2) 
    df_head3 = df_id_nh.head(day3) 

    day1max = df_head1['over'].max()
    day2max = df_head2['over'].max()
    day3max = df_head3['over'].max()

    # print(df_head1)
    # print(day1max)
    # quit()

    
    
    if nowprice >= day1max:
        print(f"{stockid},{stockname}創{day1}天新高")
        h_day1.append(f"{stockid}({stockname})")
        h_id_day1.append(f"{stockid}")

    # newh_day2 = []
    if nowprice >= day2max:
        print(f"{stockid},{stockname}創{day2}天新高")
        h_day2.append(f"{stockid}({stockname})")
        h_id_day2.append(f"{stockid}")

    # newh_day3 = []
    if nowprice >= day3max:
        print(f"{stockid},{stockname}創{day3}天新高")
        h_day3.append(f"{stockid}({stockname})")
        h_id_day3.append(f"{stockid}")
    
    # return h_day1,h_day2,h_day3
    # return h_day1,h_id_day1

    
    # # 串列變字串的語法"".join(map(str, a))
    # newh_day1_str = "".join(map(str, newh_day1))
    # newh_day2_str = "".join(map(str, newh_day2))
    # newh_day3_str = "".join(map(str, newh_day3))
    # all_newhigh = [now_day,newh_day1_str,newh_day2_str,newh_day3_str]

    # df_day_newh = pd.DataFrame([all_newhigh])
    # dtypedict = {
    #     "Up_date" : DATE,
    #     "day1high" : NVARCHAR(3000),
    #     "day2high" : NVARCHAR(3000),
    #     "day3high" : NVARCHAR(3000),
    # }
    # df_day_newh.to_sql("shin_newhigh",engine,if_exists="append",index=False)
    