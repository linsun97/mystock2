from openai import OpenAI, OpenAIError # 串接 OpenAI API
import yfinance as yf
import pandas as pd # 資料處理套件
import numpy as np
import datetime as dt # 時間套件
import requests
from bs4 import BeautifulSoup

import getpass # 保密輸入套件
api_key = getpass.getpass("請輸入金鑰：")
client = OpenAI(api_key = api_key) # 建立 OpenAI 物件

# 基本面資料
def stock_fundamental(stock_id= "大盤"):
  if stock_id == "大盤":
      return None

  stock = yf.Ticker(stock_id)

  # 營收成長率
  quarterly_revenue_growth = np.round(stock.quarterly_financials.loc["Total Revenue"].pct_change(-1).dropna().tolist(), 2)

  # 每季EPS
  quarterly_eps = np.round(stock.quarterly_financials.loc["Basic EPS"].dropna().tolist(), 2)

  # EPS季增率
  quarterly_eps_growth = np.round(stock.quarterly_financials.loc["Basic EPS"].pct_change(-1).dropna().tolist(), 2)

  # 轉換日期
  dates = [date.strftime('%Y-%m-%d') for date in stock.quarterly_financials.columns]

  data = {
      '季日期': dates[:len(quarterly_revenue_growth)],
      '營收成長率': quarterly_revenue_growth.tolist(),
      'EPS': quarterly_eps[0:3].tolist(),
      'EPS 季增率': quarterly_eps_growth[0:3].tolist()
  }

  return data

print(stock_fundamental("3526.TWO"))


# 新聞資料
def stock_news(stock_name ="大盤"):
  if stock_name == "大盤":
    stock_name="台股 -盤中速報"

  data=[]
  # 取得 Json 格式資料
  json_data = requests.get(f'https://ess.api.cnyes.com/ess/api/v1/news/keyword?q={stock_name}&limit=5&page=1').json()

  # 依照格式擷取資料
  items=json_data['data']['items']
  for item in items:
      # 網址、標題和日期
      news_id = item["newsId"]
      title = item["title"]
      publish_at = item["publishAt"]
      # 使用 UTC 時間格式
      utc_time = dt.datetime.utcfromtimestamp(publish_at)
      formatted_date = utc_time.strftime('%Y-%m-%d')
      # 前往網址擷取內容
      url = requests.get(f'https://news.cnyes.com/'
                        f'news/id/{news_id}').content
      soup = BeautifulSoup(url, 'html.parser')
      p_elements=soup .find_all('p')
      # 提取段落内容
      p=''
      for paragraph in p_elements[4:]:
          p+=paragraph.get_text()
      data.append([stock_name, formatted_date ,title,p])
  return data

print(stock_news("台積電"))