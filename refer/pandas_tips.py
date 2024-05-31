import pandas as pd
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer , DATE

to_day = date.today()
# print(to_day)
# quit()
# 顯示500個以下的所有col
pd.set_option('display.max_columns', 500) 
pd.set_option("display.float_format",'{:.2f}'.format)

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/testdb")
df = pd.read_csv('e2.csv',
                #  na_values="-"
                 header=4,
                 skipfooter=6,
                 usecols=[1,2,6,9,10,11,12],
                 thousands=",",
                 encoding="cp950",
                #  parse_dates=["up_date"], #需用中掛號包住
                #  date_format="%Y%m%d",
                 true_values=["yes"], #需用中掛號包住
                 false_values=["no"], #需用中掛號包住
                 engine='python' #python的engine預設是"c",但不支持skipfooter
                 
                 )

df.columns = ['stockid','stockname','bef','high','low','over','volume']
df['up_date'] = to_day
# print(df.info())
# quit()
# 應改df的資料屬性
# str轉為字串,strip去掉前後的空白
df['high'] = df['high'].str.strip()
df['low'] = df['low'].str.strip()
df['over'] = df['over'].str.strip()
df['volume'] = df['volume'].str.strip()


# df1 = df.loc[df['high']=="-",["high","low","over"]] 
# print(df1)
# quit()
df.loc[df['high']=="-",["high","low","over"]] = df.loc[df["high"]=="-","bef"]
df.loc[df['volume']=="-","volume"] = 0
# print(df)
# quit()

# df的格式
df = df.astype(
            {
                'stockid':'int16',
                'stockname':'category',
                'bef':'float32',
                'high':'float32',
                'low':"float32",
                'over':"float32",
                "volume":"int64",
                "up_date":"datetime64[ns]"
            }
        )

# df.style.format().highlight_max("over",color="red")
# print(df.head())
# print(df.info())
# quit()
# 資料庫用的格式
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

def IntoTable(row):
    # 把row從series變dataframe,取出的row會被當成series但他是直行,先變成list,再變成橫的dataframe
    row_pd = pd.DataFrame([row])
    row_pd.to_sql(f'p_{row_pd.iloc[0,0]}', engine, if_exists='append', dtype=dtypedict ,index=False)

# 可以用df.apply的方法加上axis = 1,就可以把df內每一列當成一個row去執行IntoTable函式
df.apply(IntoTable,axis = 1)

# print("---------")
# print(df['high'].value_counts())

# df.to_csv("e1.csv")