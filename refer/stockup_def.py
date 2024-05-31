import  urllib.request,csv
from sqlalchemy import create_engine
from datetime import datetime 
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float, Integer , DATE
import pandas as pd
import email.message

# 設定float格式為小數點後兩位
pd.set_option("display.float_format",'{:.2f}'.format)

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")

# import pytz #設時區
# upnewd = datetime.now("Ymd")
#--會出現-2023-12-08 11:23:57.611618
# upnewd = datetime.timestamp
#--會出現-1549836078
# upnewd = datetime.today().strftime('%Y%m%d')
# upnewd = datetime.today().strftime('%Y%m%d')
#會出現20231208,但要到下午3:46以後才有檔案
# print(pytz.all_timezones)

# print(today)
# yesterday = today - timedelta(days = 1)
# yearnum = datetime.strftime(yesterday, '%Y')
# week_day = datetime.weekday(yesterday)

# if week_day == 5 or week_day == 6: #星期六或星期日
#     yesterday = datetime.now() - timedelta(days = 3)
#     yearnum = datetime.strftime(yesterday, '%Y')
#     week_day = datetime.weekday(yesterday)


# tynum = int(yearnum) - 1911
# print(week_day)
# print(datetime.now())
# print(tynum)
# quit()
# upnewd = datetime.strftime(yesterday, str(tynum)+'/%m/%d')
# print(upnewd)
# quit()