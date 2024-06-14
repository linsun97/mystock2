from sqlalchemy import create_engine
import datetime  
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer , DATE
import pandas as pd
import numpy as np
import time
import email.message
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")

onedaytype = {
        "Up_date" : DATE,
        "New_up" : NVARCHAR(length=8000),
        "day1_high" : NVARCHAR(length=2000),
        "day2_high" : NVARCHAR(length=2000),
        "day3_high" : NVARCHAR(length=2000)
    }
a_day = {
        "Up_date" : datetime.date(2024,5,1),
        "New_up" : "nothing"
    }

    # 必須設index
df_day = pd.DataFrame(a_day, index=[0])
print(df_day)
df_day.to_sql('shin_oneday', engine, if_exists='append', dtype=onedaytype ,index=False  )

# data = csv.reader(webpage.read().decode('utf-8').splitlines()) #讀取資料到data陣列中
# data = csv.reader(webpage.read().decode('Big5', errors='ignore').splitlines() ) #讀取資料到data陣列中
    