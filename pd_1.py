import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer , DATE
import numpy as np
import datetime 

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/testdb")
to_day = datetime.date.today()
# print(to_day) #2024-5-23
# quit()
pd.set_option('display.max_columns', 500)
df = pd.read_csv('e2.csv',
                #  na_values="-"
                 header=4,
                 skipfooter=6,
                 usecols=[1,2,6,9,10,11,12],
                 thousands=",",
                 encoding="cp950",
                #  parse_dates=["dateone"], #需用中掛號包住
                #  date_format="%Y%m%d",
                #  true_values=["yes"], #需用中掛號包住
                #  false_values=["no"], #需用中掛號包住
                 engine='python'
                 
                 )

df.columns = ['stockid','stockname','bef','high','low','over','volumn']

# 去掉前後空白
df['high'] = df['high'].str.strip()
df['low'] = df['low'].str.strip()
df['over'] = df['over'].str.strip()
df['volumn'] = df['volumn'].str.strip() 
# 將值為"-"的內容換成bef的值或0
df.loc[df['high']=="-",['high','low','over']] = df.loc[df['high']=="-",'bef']
df.loc[df['volumn']=="-",'volumn'] = 0
df['up_date'] = to_day


# tdict = {
#         'stockid': "int8",
#         'stockname': "string",
#         'bef':"float32",
#         'high': "float32",
#         'low': "float32",
#         'over': "float32",
#         'volumn': "int64",
#         'up_date' : "str",
#         }

# df = df.astype(tdict)
# print(df.info())
# print(df[df.high > 50])
# print(df.loc[df.high > 50])
# # 以上兩個顯示的東西相同
# quit()

# print(df.head())
# quit()
# 設定欄位型態,這是sqlalchemy的格式不是astype的格式
dtypedict = {
        'stockid': Integer,
        'stockname': NVARCHAR(length=100),
        'bef': Float,
        'high': Float,
        'low': Float,
        'over': Float,
        'volumn': Integer,
        'up_date' : DATE,
        }

# print(df)

# 將每一筆資料分別存入不同資料表的第一種方法
def IntoTable(row):
    row_pd = pd.DataFrame([row])
    row_pd.to_sql(f'p{row_pd.iloc[0,0]}', engine, if_exists='append', dtype=dtypedict ,index=False)

# 可以用df.apply的方法加上axis = 1,就可以把df內每一列當成一個row去執行IntoTable函式
df.apply(IntoTable,axis = 1)

# 將每一筆資料分別存入不同資料表的第二種方法
# for i in range(len(df)):
#     try:
#         df.iloc[i:i+1].to_sql(name=f'k{df.iloc[i,0]}',if_exists='append',con = engine, dtype=dtypedict ,index=False)
#     except IntegrityError:
#         pass #or any other action

print(df.info())
quit()

