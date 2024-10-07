import requests 
from bs4 import BeautifulSoup 
import time
import random
from datetime import date, datetime
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.types import NVARCHAR, Float, Integer,DATE,TEXT
from sqlalchemy.ext.declarative import declarative_base
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #瀏覽器等待執行結果後才做動作
from selenium.webdriver.support import expected_conditions as EC #等待執行後捕捉回傳的訊息
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.chrome.service import Service as ChromiumService
# from webdriver_manager.core.os_manager import ChromeType
# driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
# quit()

# 因新版本出現暫時起用
from selenium.webdriver.chrome.service import Service

import pandas as pd
engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock", pool_size=20, max_overflow=40)
def Get_good_big():
    try:
        # 因新版本出現暫時不用
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)  #不自動關閉瀏覽器 
        # driver = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))

        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(options=options,service=service)


        driver.implicitly_wait(20) #只要設一個底下不用再設 會自動偵測是否須等10秒
        # driver.get("https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%E6%9C%88%E5%A2%9E%E6%B8%9B%E6%95%B8%E2%80%93%EF%BC%9E1000%E5%BC%B5&FL_VAL_S0=0.2&FL_VAL_E0=100&FL_ITEM1=&FL_VAL_S1=&FL_VAL_E1=&FL_ITEM2=&FL_VAL_S2=&FL_VAL_E2=&FL_ITEM3=&FL_VAL_S3=&FL_VAL_E3=&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=&FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E8%82%A1%E6%9D%B1%E6%8C%81%E8%82%A1%E5%88%86%E7%B4%9A_%E8%BF%91N%E5%80%8B%E6%9C%88%E4%B8%80%E8%A6%BD&FL_SHEET2=%E6%8C%81%E6%9C%89%E5%BC%B5%E6%95%B8%28%E8%90%AC%E5%BC%B5%29%E2%80%93%EF%BC%9E1000%E5%BC%B5&FL_MARKET=%E5%8F%AA%E6%9C%89%E8%88%88%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2")
        driver.get("https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%E6%9C%88%E5%A2%9E%E6%B8%9B%E6%95%B8%E2%80%93%EF%BC%9E1000%E5%BC%B5&FL_VAL_S0=0.2&FL_VAL_E0=100&FL_ITEM1=&FL_VAL_S1=&FL_VAL_E1=&FL_ITEM2=&FL_VAL_S2=&FL_VAL_E2=&FL_ITEM3=&FL_VAL_S3=&FL_VAL_E3=&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=&FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E8%82%A1%E6%9D%B1%E6%8C%81%E8%82%A1%E5%88%86%E7%B4%9A_%E8%BF%91N%E5%80%8B%E6%9C%88%E4%B8%80%E8%A6%BD&FL_SHEET2=%E6%8C%81%E6%9C%89%E5%BC%B5%E6%95%B8%28%E8%90%AC%E5%BC%B5%29%E2%80%93%EF%BC%9E1000%E5%BC%B5&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83%2F%E8%88%88%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2")
        html = driver.page_source
        time.sleep(10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print("0",soup)
        soup.prettify()
        # response = soup.find("body")
        basic_list = []
        # responses = soup.select('table[style="width:100%;"] tr td')
        # responses = soup.select('table[id="tblStockList"] tr td')
        responses = soup.select('table[id="tblStockList"] tr th')
        # print(responses)
        # quit()
        for response in responses :
            basic_list.append(response.text.replace(",","").strip())

        # print(basic_list)
        # quit()
        stockid_list = []
        def is_chinese(string):
            for char in string:
                if '\u4e00' <= char <= '\u9fa5':
                    return True
            return False
        def is_number(string):
            try:
                int(string)
                return True
            except ValueError:
                return False
            
        for id in basic_list:
            if len(id) == 4:
                if not is_chinese(id) :
                    if is_number(id) :
                        stockid_list.append(id)
        
        # print(stockid_list)
        big_increase = ",".join(map(str, stockid_list))
        big = {
            "stockid" : big_increase,
            "up_date" : date.today()
        }
        dtypedict = {
                'stockid': TEXT,
                'up_date': DATE,
                }
        df = pd.DataFrame(big,index=[0])
        # print(df)
        # quit()
        df.to_sql("big_increase", engine, if_exists='replace', index=False ,dtype=dtypedict)
        print("新增大戶持股增加股票名單")
        engine.dispose()
        driver.close()
        
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


# ------------------------------------------
today = datetime.today().date()
daynum = datetime.strftime(today, '%d')
weeknum = datetime.strftime(today, '%w')
# daynum = today.day 結果會是數字1
# print(daynum)
# quit()

if  daynum == "08" or daynum == "18" :
    Get_good_big()
else:
    pass