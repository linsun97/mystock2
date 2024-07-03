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
import pandas as pd



def Get_filteropen():
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    # 千張以上比例
    thousand_rate_low = 40 
    thousand_rate_high = 90
    # 掛牌年數
    up_years_low = 0
    up_years_high = 15
    # 毛利率區間
    netrate_low = 40
    netrate_high = 90
    # 進四季每股投資現金流
    cash_1 = -50
    cash_2 = -10

    # url = "https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%EF%BC%9E1000%E5%BC%B5&FL_VAL_S0=40&FL_VAL_E0=80&FL_ITEM1=%E5%85%AC%E5%8F%B8%E6%8E%9B%E7%89%8C%E5%B9%B4%E6%95%B8+%28%E5%B9%B4%29&FL_VAL_S1=0&FL_VAL_E1=10&FL_ITEM2=%E7%B4%AF%E5%AD%A3%E2%80%93%E6%AF%9B%E5%88%A9%E7%8E%87%28%25%29%E2%80%93%E6%9C%AC%E5%AD%A3%E5%BA%A6&FL_VAL_S2=30&FL_VAL_E2=100&FL_ITEM3=%E8%91%A3%E7%9B%A3%E6%8C%81%E8%82%A1%28%25%29%E2%80%93%E9%9D%9E%E7%8D%A8%E7%AB%8B%E2%80%93%E7%95%B6%E6%9C%88&FL_VAL_S3=30&FL_VAL_E3=80&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=%E7%8F%BE%E9%87%91%E6%B5%81%E9%87%8F%7C%7C%E8%BF%91%E5%9B%9B%E5%AD%A3%E6%8A%95%E8%B3%87%E6%B4%BB%E5%8B%95%E9%87%91%E6%B5%81%E5%89%B5%E6%AD%B7%E5%AD%A3%E5%89%8D%E4%B8%89%E4%BD%8E%40%40%E6%8A%95%E8%B3%87%E6%B4%BB%E5%8B%95%E9%87%91%E6%B5%81%E5%89%B5%E6%96%B0%E9%AB%98%2F%E4%BD%8E%40%40%E8%BF%91%E5%9B%9B%E5%AD%A3%E6%8A%95%E8%B3%87%E6%B4%BB%E5%8B%95%E9%87%91%E6%B5%81%E5%89%B5%E6%AD%B7%E5%AD%A3%E5%89%8D%E4%B8%89%E4%BD%8E&FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%E8%B6%85%E9%81%8E1000%E5%BC%B5%E2%80%93%E7%95%B6%E6%9C%88%7C%7C1%7C%7C0%7C%7C%3E%3D%7C%7C%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%E8%B6%85%E9%81%8E1000%E5%BC%B5%E2%80%93%E5%89%8D1%E6%9C%88%7C%7C1%7C%7C0&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E8%82%A1%E6%9D%B1%E6%8C%81%E8%82%A1%E5%88%86%E7%B4%9A_%E6%9C%88%E7%B5%B1%E8%A8%88&FL_SHEET2=%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%E9%81%9E%E5%A2%9E%E5%88%86%E7%B4%9A%E4%B8%80%E8%A6%BD&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83%2F%E8%88%88%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2"
    # url = f"https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%EF%BC%9E1000%E5%BC%B5&FL_VAL_S0={thousand_rate_low}&FL_VAL_E0={thousand_rate_high}&FL_ITEM1=%E5%85%AC%E5%8F%B8%E6%8E%9B%E7%89%8C%E5%B9%B4%E6%95%B8+%28%E5%B9%B4%29&FL_VAL_S1={up_years_low}&FL_VAL_E1={up_years_high}&FL_ITEM2=%E7%B4%AF%E5%AD%A3%E2%80%93%E6%AF%9B%E5%88%A9%E7%8E%87%28%25%29%E2%80%93%E6%9C%AC%E5%AD%A3%E5%BA%A6&FL_VAL_S2={netrate_low}&FL_VAL_E2={netrate_high}&FL_ITEM3=%E8%91%A3%E7%9B%A3%E6%8C%81%E8%82%A1%28%25%29%E2%80%93%E9%9D%9E%E7%8D%A8%E7%AB%8B%E2%80%93%E7%95%B6%E6%9C%88&FL_VAL_S3={notdepend_low}&FL_VAL_E3={notdepend_high}&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=%E7%8F%BE%E9%87%91%E6%B5%81%E9%87%8F%7C%7C%E8%BF%91%E5%9B%9B%E5%AD%A3%E6%8A%95%E8%B3%87%E6%B4%BB%E5%8B%95%E9%87%91%E6%B5%81%E5%89%B5%E6%AD%B7%E5%AD%A3%E5%89%8D%E4%B8%89%E4%BD%8E%40%40%E6%8A%95%E8%B3%87%E6%B4%BB%E5%8B%95%E9%87%91%E6%B5%81%E5%89%B5%E6%96%B0%E9%AB%98%2F%E4%BD%8E%40%40%E8%BF%91%E5%9B%9B%E5%AD%A3%E6%8A%95%E8%B3%87%E6%B4%BB%E5%8B%95%E9%87%91%E6%B5%81%E5%89%B5%E6%AD%B7%E5%AD%A3%E5%89%8D%E4%B8%89%E4%BD%8E&FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%E8%B6%85%E9%81%8E1000%E5%BC%B5%E2%80%93%E7%95%B6%E6%9C%88%7C%7C1%7C%7C0%7C%7C%3E%3D%7C%7C%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%E8%B6%85%E9%81%8E1000%E5%BC%B5%E2%80%93%E5%89%8D1%E6%9C%88%7C%7C1%7C%7C0&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E8%82%A1%E6%9D%B1%E6%8C%81%E8%82%A1%E5%88%86%E7%B4%9A_%E6%9C%88%E7%B5%B1%E8%A8%88&FL_SHEET2=%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%E9%81%9E%E5%A2%9E%E5%88%86%E7%B4%9A%E4%B8%80%E8%A6%BD&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83%2F%E8%88%88%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2"
    
    # 最新的query如下
    # https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E8%BF%91%E5%9B%9B%E5%AD%A3%E2%80%93%E6%AF%8F%E8%82%A1%E6%8A%95%E8%B3%87%E9%87%91%E6%B5%81%28%E5%85%83%29&FL_VAL_S0=-50&FL_VAL_E0=-10&FL_ITEM1=%E5%96%AE%E5%AD%A3%E2%80%93%E6%AF%9B%E5%88%A9%E7%8E%87%28%25%29&FL_VAL_S1=40&FL_VAL_E1=90&FL_ITEM2=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%EF%BC%9E1000%E5%BC%B5&FL_VAL_S2=40&FL_VAL_E2=90&FL_ITEM3=%E5%85%AC%E5%8F%B8%E6%8E%9B%E7%89%8C%E5%B9%B4%E6%95%B8+%28%E5%B9%B4%29&FL_VAL_S3=0&FL_VAL_E3=15&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=&FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%EF%BC%9E1000%E5%BC%B5%E2%80%93%E5%89%8D1%E6%9C%88%7C%7C1%7C%7C0%7C%7C%3C%3D%7C%7C%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%EF%BC%9E1000%E5%BC%B5%E2%80%93%E7%95%B6%E6%9C%88%7C%7C1%7C%7C0&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E5%85%AC%E5%8F%B8%E5%9F%BA%E6%9C%AC%E8%B3%87%E6%96%99&FL_SHEET2=&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83%2F%E8%88%88%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2
    url = f"https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E8%BF%91%E5%9B%9B%E5%AD%A3%E2%80%93%E6%AF%8F%E8%82%A1%E6%8A%95%E8%B3%87%E9%87%91%E6%B5%81%28%E5%85%83%29&FL_VAL_S0=-{cash_1}&FL_VAL_E0={cash_2}&FL_ITEM1=%E5%96%AE%E5%AD%A3%E2%80%93%E6%AF%9B%E5%88%A9%E7%8E%87%28%25%29&FL_VAL_S1={netrate_low}&FL_VAL_E1={netrate_high}&FL_ITEM2=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%EF%BC%9E1000%E5%BC%B5&FL_VAL_S2={thousand_rate_low}&FL_VAL_E2={thousand_rate_high}&FL_ITEM3=%E5%85%AC%E5%8F%B8%E6%8E%9B%E7%89%8C%E5%B9%B4%E6%95%B8+%28%E5%B9%B4%29&FL_VAL_S3={up_years_low}&FL_VAL_E3={up_years_high}&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=&FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%EF%BC%9E1000%E5%BC%B5%E2%80%93%E5%89%8D1%E6%9C%88%7C%7C1%7C%7C0%7C%7C%3C%3D%7C%7C%E5%88%86%E7%B4%9A%E6%8C%81%E6%9C%89%E6%AF%94%E4%BE%8B%28%25%29%E2%80%93%EF%BC%9E1000%E5%BC%B5%E2%80%93%E7%95%B6%E6%9C%88%7C%7C1%7C%7C0&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E5%85%AC%E5%8F%B8%E5%9F%BA%E6%9C%AC%E8%B3%87%E6%96%99&FL_SHEET2=&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83%2F%E8%88%88%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2"
    # #            """
    #     # 原始意思: https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=自訂篩選&INDUSTRY_CAT=我的條件
    #     # &FL_ITEM0=分級持有比例(%)–＞1000張&FL_VAL_S0=40&FL_VAL_E0=80
    #     # &FL_ITEM1=公司掛牌年數+(年)&FL_VAL_S1=0&FL_VAL_E1=10
    #     # &FL_ITEM2=累季–毛利率(%)–本季度&FL_VAL_S2=30&FL_VAL_E2=100
    #     # &FL_ITEM3=董監持股(%)–非獨立–當月&FL_VAL_S3=30&FL_VAL_E3=80
    #     # &FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=
    #     # &FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=
    #     # &FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=
    #     # &FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=
    #     # &FL_RULE0=現金流量||近四季投資活動金流創歷季前三低@@投資活動金流創新高/低@@近四季投資活動金流創歷季前三低
    #     # &FL_RULE1=&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=
    #     # &FL_FD0=分級持有比例(%)–超過1000張–當月||1||0||>=||分級持有比例(%)–超過1000張–前1月||1||0
    #     # &FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=
    #     # &FL_SHEET=股東持股分級_月統計&FL_SHEET2=持有比例(%)–遞增分級一覽
    #     # &FL_MARKET=上市/上櫃/興櫃&FL_QRY=查++詢
    response = requests.get(url, headers=headers)
    response.encoding='utf-8' 

    time.sleep(20)
    # # print(response.text)
    
    # with open("test_filter.txt","w") as file:
    #     file.write(response.text)
    # #-----------------------------
    # # html = driver.page_source
    if response.status_code == 200:
    # with open("test_filter.txt","r") as file:
    #     responses = file.read()
    # if responses :
        soup = BeautifulSoup(response.text,"lxml")
        # time.sleep(10)
        soup.prettify()
        # response = soup.find("body")
        # 不抓標題,只抓class為even與odd的tr內的td資料
        
        responses1 = soup.select('table[id="tblStockList"]   tr  ')
        tr_num = len(responses1)
        # print(tr_num)
        tr_num = int(tr_num)-1
        # print(responses1)
        
        
        stock_list = []
        for i in range(tr_num):
            r2=soup.select(f'tr[id="row{i}"]  td')
            for r3 in r2 :
                stock_list.append(r3.text.replace(",","").strip())
                # print(r3.text.replace(",","").strip())
                    # quit()
            # print(r2)
        # print(stock_list)
        endnum = len(stock_list)
    # print("endnum",endnum)
    # quit()
    # print(cash_list)
        stock_one_list = []
        # 共22個欄位
        for i in range(0,endnum,22):
            stock_one_list.append([stock_list[i],\
                               stock_list[i+1],\
                               stock_list[i+2],\
                               stock_list[i+4],\
                               stock_list[i+7],\
                               stock_list[i+8],\
                               stock_list[i+9],\
                               stock_list[i+11],\
                               stock_list[i+12],\
            ])
        print(stock_one_list)


        engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")
        df = pd.DataFrame(stock_one_list)

        
        dtypedict = {
            'stock_id': NVARCHAR(length=25),
            'stock_name': NVARCHAR(length=100),
            'stock_market': NVARCHAR(length=100),
            'stock_price': NVARCHAR(length=25),
            'stock_10': NVARCHAR(length=25),
            'stock_cap': NVARCHAR(length=25),
            'stock_total': NVARCHAR(length=25),
            'stock_estyear': NVARCHAR(length=25),
            'stock_upyear': NVARCHAR(length=25)
            
            }

        #     # 設定欄位名稱,若沒設定預設是用0,1,2,3....當欄位名稱
        df.columns = ['stock_id', 'stock_name', 'stock_market','stock_price','stock_10','stock_cap','stock_t0tal','stock_estyear', 'stock_upyear']
        df.to_sql('filter_all', engine, if_exists='replace',dtype=dtypedict,index=False)
        #     df2.to_sql(f'netrate_open_{stock_one[0]}', engine, if_exists='append',dtype=dtypedict,index=False)
            
        #     # quit()
            

        # driver.close()
        
        
        
Get_filteropen()
        
        
        
        
        
        
     