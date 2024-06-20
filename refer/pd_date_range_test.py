import pandas as pd
from datetime import datetime,time,date
import time

# date_range = pd.date_range(date(2024,1,1),date(2024,6,17),freq="1D")
start_day = "2024-06-01"
end_day = date.today()
# inclusive 有 left,right,both三種選擇,left:包含start_day不包含end_day,以此類推
date_range = pd.date_range(start_day,end_day, inclusive='right',freq="D")

for i in date_range:
    # print(i.year)
    x = date(i.year,i.month,i.day)
    print(x)


# B

# 工作日頻率

# C

# 自訂工作日頻率

# D

# 日曆日頻率

# W

# 每週頻率

# ME

# 月末頻率

# SME

# 半月結束頻率（15 日和月底）

# BME

# 營業月結束頻率

# CBME

# custom business month end frequency

# MS

# month start frequency

# SMS

# semi-month start frequency (1st and 15th)

# BMS

# business month start frequency

# CBMS

# custom business month start frequency

# QE

# quarter end frequency

# BQE

# business quarter end frequency

# QS

# quarter start frequency

# BQS

# business quarter start frequency

# YE

# year end frequency

# BYE

# business year end frequency

# YS

# year start frequency

# BYS

# business year start frequency

# h

# hourly frequency

# bh

# business hour frequency

# cbh

# custom business hour frequency

# min

# minutely frequency

# s

# secondly frequency

# ms

# milliseconds

# us

# microseconds

# ns

# nanoseconds