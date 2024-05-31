import  urllib.request
import csv
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer , DATE
import pandas as pd
import numpy as np
import datetime 

nowdate = datetime.date.today()
# print(nowdate)
# quit()

'''
用sqlalchemy須解決幾個問題:
1.欄位名稱有可能是Big5的中文,最好改欄位名稱為英文
2.為方便查詢,有些資料格式必須為float,需要設定
3.去掉空值或不符合資料格式的值,並用其他如0.0代替
'''

#站食用昨天日期來測試20231207
# upnewd = "20231207"
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/testdb")
# url = f"http://www.gretai.org.tw/web/emergingstock/historical/daily/EMDaily_dl.php?l=zh-tw&f=EMdes010.{upnewd}-C.csv"
# print(url)

# 有空試試看
# df1 = pd.read_csv("E20231207.csv",thousands=',' ,index_col='證劵代號',
#                   na_values=["-", " "],skiprows=1,
#                   keep_default_na=True, #空值會變成null
#                   skipfooter=1,header=3,
#                     可以在读取的时候对列数据进行变换：id的值全部加10
#                     converters={"id": lambda x: int(x) + 10})
#                   names=["编号", "姓名", "地址", "日期"],sep='/t',
#                   delim_whitespace=True,
#                   usecols=["name", "address"],usecols=[1, 2],
#                   dtype={"id": str},true_values=["Yes"],
#                     false_values=["No"],nrows=100,
#                     parse_dates='Date',date_format='%Y%m%d %I',
#                       encoding="utf-8", engine="python")



df = pd.read_csv("E20231207.csv",usecols=[1,2,6,9,10,11,12],thousands=',', encoding='cp950',
                  names=['stockid','stockname','avaragep','high','low','overprice','totals'],
                #   index_col='stockid',
                  na_values=["-", " "],skipfooter=6,header=4,
                  engine="python")
# print(df)
# print(df.dtypes)
# quit()

'''
to_numeric 方法將列轉換為 Pandas 中的數值
to_numeric() 是將 dataFrame 的一列或多列轉換為數值的最佳方法。它還會嘗試將非數字物件（例如字串）適當地更改為整數或浮點數。to_numeric() 輸入可以是 Series 或 DataFrame 的列。如果某些值不能轉換為數字型別，則 to_numeric() 允許我們將非數字值強制為 NaN。

# python 3.x
import pandas as pd

s = pd.Series([-3, 1, -5])
print(s)
print(pd.to_numeric(s, downcast="integer"))
'''
'''
header 證券代號	證券名稱	最後最佳報買價	最後最佳報賣價	
日均價	前日均價	漲跌	漲跌幅	最高	最低	最後	
成交量	成交金額	筆數	發行股數	上市櫃進度日期	上市櫃進度

'''



# 將totals欄位資料格式改為integer, errors='coerce'會將有問題的值用NULL取代
# df['totals']是一個series所以不用加入axis=1
df['totals']=pd.to_numeric(df['totals'], errors='coerce', downcast="integer")

# 將有缺失的資料(NULL)用0取代
df['totals']=df['totals'].fillna(0)
# print(df)
# quit()
# 這個方法無法改資料型態
# df1['overprice'] = df1['overprice'].astype(float,copy=True)
# 改overprice欄位資料為float
# df1['overprice'] = pd.to_numeric(df1['overprice'], downcast='float')

'''
若要刪掉多個欄位
cols = ['col1', 'col2', 'col3']
data[cols] = data[cols].apply(pd.to_numeric, errors='coerce', axis=1)
'''
# 一次更改多個欄位的資料格式為float,用apply搭配pd.to_numeric
cols = ['avaragep','high','low','overprice']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1 , downcast='float')
df[cols] = df[cols].fillna(0.0)

df['up_date'] = nowdate


# 設定欄位型態
dtypedict = {
        'stockid': Integer,
        'stockname': NVARCHAR(length=100),
        'avaragep': Float,
        'high': Float,
        'low': Float,
        'overprice': Float,
        'totals': Integer,
        'up_date' : DATE,
        }
    

# df.to_sql('s1', engine, if_exists='replace',dtype=dtypedict) 

def IntoTable(row):
    # [row]直接把每個row變成list 物件但與row.to_list的list物件不同,並做成一個datafrme
    # print([row])
    # [stockid                    9957
      # stockname    燁聯
      # avaragep                   6.98
      # high                        7.0
      # low                        6.92
      # overprice                   7.0
      # totals                 128488.0
      # up_date              2024-04-21
      # Name: 307, dtype: object]
    # print(row.to_list()) 
    # 這個做出來的datafrme還需要用T反轉,直接用[row]不用
    # [9957, '燁聯                ', 6.980000019073486, 7.0, 6.920000076293945, 7.0, 128488.0, datetime.date(2024, 4, 21)]
    row_pd = pd.DataFrame([row])

    # 被上方的作法取代
    # # series先轉成list
    # row_l = row.to_list()
    # # 再把list變成DataFrame並反轉行與列
    # row_pd=pd.DataFrame(row_l).T
    
    # # 幫這個小dataframe放入columns名稱
    # row_pd.columns = list(dtypedict.keys())
    
    # print(row_pd)
    # print(row_pd.iloc[0,0])
    # quit()

    row_pd.to_sql(f't{row_pd.iloc[0,0]}', engine, if_exists='append', dtype=dtypedict)
    # print(row2.T)
    # print(row2.T.shape)

# 可以用df.apply的方法加上axis = 1,就可以把df內每一列當成一個row去執行IntoTable函式
df.apply(IntoTable,axis = 1)

