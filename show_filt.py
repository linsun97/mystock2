import requests 
from bs4 import BeautifulSoup 
import time
import random
from datetime import datetime 
from datetime import timedelta
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.types import NVARCHAR, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #瀏覽器等待執行結果後才做動作
from selenium.webdriver.support import expected_conditions as EC #等待執行後捕捉回傳的訊息
from selenium.webdriver.chrome.service import Service
import pandas as pd

def Showfil():
    filter_all = []
    engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
    filter_df = pd.read_sql(f'select * from filter_all',engine)
    record_num = len(filter_df)
    for i in range(record_num):
        filter_one = filter_df.loc[i].tolist()
        rate_one = pd.read_sql(f"select stock_netrate,stock_oprate from netrate_open_{filter_one[0]} order by s_year desc,s_season desc limit 1",engine)
        for j in range(2):
            filter_two = rate_one.loc[0][j]
            filter_one.append(filter_two) 
        rate_two = pd.read_sql(f"select stock_type,facedollar,capital,st_date,up_date from basic_open_all where stock_id={filter_one[0]}",engine)
        for k in range(5):
            filter_three = rate_two.loc[0][k]
            filter_one.append(filter_three) 
        filter_all.append(filter_one)
    td_num = len(filter_one)
    # print(filter_all)
    # print(record_num)
    # print(td_num)
    # filter_df.columns = ['股票代碼','股票名稱','成交價','漲跌','漲跌%','年周','月日','千張%','千張%增減']
    # filter_html = filter_df.to_html(classes='data', header="true")
    return filter_all , td_num

# Showfil()