# from geturl import Geturl #自建的
# from proxynow import Proxynow #自建的
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
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


import pandas as pd



def Get_openbasic(search_market):
    try:
        # opday = datetime.now() - timedelta(days=91)
        # today = datetime.now()
        # upnewd1_y = datetime.strftime(today, '%Y')
        # upnewd1_md = datetime.strftime(today, '%m%d')
        # upnewd2_y = datetime.strftime(opday, '%Y')
        # upnewd2_md = datetime.strftime(opday, '%m%d')

        # if upnewd1_md >= "0331" and upnewd1_md <= "0601" :
        #     input_y = int(upnewd1_y)-1912 
        #     input_q = 4
        # elif upnewd1_md >= "0602" and upnewd1_md <= "0901" :
        #     input_y = int(upnewd2_y)-1911 
        #     input_q = 1
        # elif upnewd1_md >= "0902" and upnewd1_md <= "1201" :
        #     input_y = int(upnewd2_y)-1911 
        #     input_q = 2
        # elif upnewd1_md >= "1202" or upnewd1_md <= "0330" :
        #     input_y = int(upnewd2_y)-1911 
        #     input_q = 3

        # # 上市 1 上櫃 2 興櫃 3
        # search_type = search_market
        # search_season = input_q + 1
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)  #不自動關閉瀏覽器 
        # s = Service(executable_path = "C:/Users/linsu/Documents/goodinfo_s/goodinfo_1/chromedriver.exe")
        driver = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))
        # s = Service(executable_path = "C:/Program Files/Google/Chrome/Application/chrome.exe")
        # driver = webdriver.Chrome(options=options,service=s)

        driver.implicitly_wait(20) #只要設一個底下不用再設 會自動偵測是否須等10秒
        driver.get("https://mops.twse.com.tw/mops/web/t51sb01")
        html = driver.page_source

        # yesterday = datetime.now() - timedelta(days = 1)
        # today = datetime.now()
        # upnewd = datetime.strftime(today, '%Y%m%d')

        # 抓取下拉選單元件
        # select_type = driver.find_element(By.ID, "TYPEK")
        # option[1]上市 option[2]上櫃 option[3]興櫃
        driver.find_element(By.XPATH, f"//select[@name='TYPEK']/option[{search_market}]").click()
        # //*[@id="search"]/table/tbody/tr/td/select[1]/option[1]
        
        # select_type.select_by_index(2)
        time.sleep(2)
        driver.find_element(By.XPATH, f"//select[@name='code']/option[{1}]").click()
        # //*[@id="search"]/table/tbody/tr/td/select[1]/option[1]
        # select_type.select_by_index(2)
        time.sleep(2)

        # select_year = driver.find_element(By.NAME, "year")
        # select_year.send_keys(f"{input_y}")
        # time.sleep(2)
        # select_season = Select(driver.find_element(By.ID, "season"))
        # driver.find_element(By.XPATH, f"//select[@id='season']/option[{search_season}]").click()
        # select_season.select_by_value("01")
        # select_submit = driver.find_element(By.XPATH ,'//[@id="search_bar1"]/div/input').click()
        driver.find_element(By.CSS_SELECTOR ,'#search_bar1 > div > input[type=button]').click()
        time.sleep(2)

        try :
            WebDriverWait(driver,10).until( #等兩秒直到.....
                EC.element_to_be_clickable( #確定element是可以click
                    (By.NAME, "TYPEK") ##search > table > tbody > tr > td > select:nth-child(2) > option:nth-child(1)
                )
            )
            WebDriverWait(driver,10).until( #等兩秒直到.....
                EC.element_to_be_clickable
                ( #確定element是可以click
                    (By.NAME, "code")
                )
            )
            WebDriverWait(driver,10).until( #等兩秒直到.....
                EC.element_to_be_clickable
                ( #確定element是可以click
                    (By.CSS_SELECTOR, "#search_bar1 > div > input[type=button]")
                )
            )
        except:
            pass
        # params = {'TYPEK' : "rotc" , 'year' : "112" , "season" : "01"}
        # r = requests.post("https://mops.twse.com.tw/mops/web/t163sb20" , data=params)
        # time.sleep(5)
        # print(r.text)

        #-----------------------------
        # driver.get("https://mops.twse.com.tw/mops/web/t163sb20")
        # html = driver.page_source

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print("0",soup)
        soup.prettify()
        # response = soup.find("body")
        basic_list = []
        responses = soup.select('table[style="width:100%;"] tr td')
        # print(responses)
        for response in responses :
            # print(response.text.replace(",","").strip())
            # print("-----------")
            basic_list.append(response.text.replace(",","").strip())

        # print("2",basic_list)
        basic_list = basic_list[0:-1]
        # print("2-1",basic_list)
        endnum = len(basic_list)
        # print("endnum",endnum)
        # quit()
        # print(cash_list)
        basic_one_list = []
        for i in range(0,endnum,39):
            # print(cash_list[i],cash_list[i+1],cash_list[i+3])
            # 若不是數字設為0
            #改以億為單位,去掉數字中逗號
            # print(basic_list[i+0])
            # print(basic_list[i+15])
            # print(basic_list[i+16])
            # print(basic_list[i+17])
            # print(basic_list[i+38])
            # quit()

            if basic_list[i+15][-1] == "元" and basic_list[i+15][0] == "新":
                facedollar = basic_list[i+15][:-1] #先去掉後面的"元"
                facedollar = facedollar[3:] #在去掉前面的"新台幣"
                facedollar = round(float(facedollar),2)
            else:
                facedollar = 0.0
            # print('a',facedollar)

            capital = basic_list[i+16].replace(",","")
            capital = round(float(capital)/100000000, 2)    #股本,單位億
            # print('b',capital)

            stocknum = basic_list[i+17].replace(",","")
            stocknum = round(float(stocknum)/1000, 2)    #股張數,單位張
            # print("c",stocknum)
            privnum = basic_list[i+18].replace(",","")
            privnum = round(float(privnum)/1000, 2)    #私募股張數,單位張
            # print("d",privnum)
            # \代表程式碼太長換行
            basic_one_list.append([basic_list[i],\
                                basic_list[i+2],\
                                basic_list[i+3],\
                                basic_list[i+13],\
                                basic_list[i+14],\
                                facedollar,\
                                capital,\
                                stocknum,\
                                privnum,\
                                ])
            
        # print("1",basic_one_list)
        # quit()
        engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock", pool_size=20, max_overflow=40)
        df = pd.DataFrame(basic_one_list)

        for basic_one in basic_one_list :
            print(basic_one)
            df2 = pd.DataFrame(basic_one)
            df2 = df2.T
            dtypedict = {
                'stock_id': Integer,
                'stock_name': NVARCHAR(length=100),
                'stock_type': NVARCHAR(length=100),
                'st_date': NVARCHAR(length=100),
                'up_date': NVARCHAR(length=100),
                'facedollar': Float(),
                'capital': Float(),
                'stocknum': Float(),
                'privnum': Float(),
                }

            # 設定欄位名稱,若沒設定預設是用0,1,2,3....當欄位名稱
            df2.columns = ['stock_id',\
                'stock_name',\
                'stock_type',\
                'st_date',\
                'up_date',\
                'facedollar',\
                'capital',\
                'stocknum',\
                'privnum',\
                ]
            # df.to_sql('cash_6762', engine, if_exists='replace')
            result = df2.to_sql('basic_open_all', engine, if_exists='append',dtype=dtypedict,index=False)
            print(result)
            # quit()
            
        engine.dispose()
        driver.close()
        
            
            
            
            
            
            
            
            
            
            
            # url = "https://mops.twse.com.tw/mops/web/t163sb20"
            # 購買proxy才解決被檔的問題
            # proxy = Proxynow()
            # urlget = Geturl(url_i=url, proxy_i=proxy)
            # response = urlget.get_text()
            # response.encoding='utf-8' 

        # 當測試完畢這一塊要註解掉--------------
        # with open ("opencash.txt","w" , encoding='UTF-8') as file :
        #     file.write(aa)
        #     file.close()

        # with open ("monincome.txt","r") as file :
        #     response = file.read()
        #     file.close()
        # print(response)
        # quit()
        #-------------------------------------
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
