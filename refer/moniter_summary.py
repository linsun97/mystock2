import datetime
import mysql.connector
from googleapiclient.discovery import build  # 用於 Google Search API
import requests  # 用於呼叫 Google Gemini API 和 Notion API
from langchain_google_genai import ChatGoogleGenerativeAI
from bs4 import BeautifulSoup 
from notion_client import Client
import time 

NOTION_TOKEN = "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"
NOTION_DATABASE_ID = '1535881a43688035a32df5080e57cd3e'
notion = Client(auth=NOTION_TOKEN)
# 檢查是否為指定執行日期
def is_valid_date():
    today = datetime.date.today()
    valid_dates = [(4, 5), (5, 25), (8, 25), (11, 25)]  # 月日
    return (today.month, today.day) in valid_dates

# 取得 MariaDB 資料
def fetch_stock_data():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # 替換為 MariaDB 使用者名稱
        password="nineseve9173",  # 替換為 MariaDB 密碼
        database="stock"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT stockid, stockname FROM moniter")
    stock_data = cursor.fetchall()  # 取得所有資料
    connection.close()
    return stock_data

# Google Search API 查詢
def search_stock_info(stock_list):
    search_results = {}
    # api_key = "your_google_api_key"  # 替換為 Google API 金鑰
    # cse_id = "your_cse_id"  # 替換為 Google Custom Search Engine ID
    googlesearch_api_key = "AIzaSyC60xTfn-SWNSbc17pTzvWs-cfVGsqVZNU"
    googlesearch_engine_id = "500990df209ce4c36"
    # service = build("customsearch", "v1", developerKey=api_key)

    for stock_id, stock_name in stock_list:
        query = f"{stock_id} {stock_name} 新聞 展望"

        # if search_results == None or search_results == {}:

        # 建立 API 請求網址
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={googlesearch_engine_id}&key={googlesearch_api_key}"

        # 發送請求
        response = requests.get(url)

        link_list = []
        # 處理結果
        if response.status_code == 200:
            results = response.json()
            for item in results.get("items", []):
                # print(f"標題: {item['title']}")
                # print(f"連結: {item['link']}")
                link_list.append(item['link'])
                # print(f"摘要: {item['snippet']}")
                # print("="*50)
            # print(results)
            # print(type(results))
            # quit()

            # return results
            # 將link的前三個傳給make_summary
            try:
                # print(link_list)
                # print("*"*50)
                # print(link_list[0:5])
                # print("*"*50)
                search_results[f"{stock_id}{stock_name}"] = link_list[0:5]
                # print(search_results)
                # print("+-"*50)
            except Exception as e:
                print(f"Error:製作股票對應連結失敗-- {e}")

        else:
            print(f"請求google搜尋失敗，狀態碼: {response.status_code}")
    

    return search_results

def fetch_web_content(url):
        """讀取指定網址的網頁內容"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            # return response.text
            # 確保請求成功
            response.encoding = response.apparent_encoding  # 自動檢測編碼
            # print(response.encoding)
            html_content = response.text
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            # 嘗試過濾廣告與非主要內容（可根據網站特性微調）
            for element in soup(["script", "style", "header", "footer", "aside", "nav"]):
                element.extract()  # 移除不需要的元素

            # 提取主要段落文字
            paragraphs = soup.find_all("p")
            main_content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            if not main_content:
                # raise Exception(f"無法提取主要內容: {url}")
                print(f"無法提取主要內容: {url}") # Exception(f"無法提取主要內容: {url}")
                main_content = ""

            return main_content
        
        except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")
                return None

# Google Gemini API 整理摘要
def summarize_links(stock_dict):
    summaries = {}
    # gemini_api_url = "https://gemini.googleapis.com/v1/text-summarize"  # 假設 Google Gemini API URL
    GEMINI_API_KEY = "AIzaSyC93dmru4HZhCTZDJeJS1SYtNeQIAh6KIA"  # 替換為 Google Gemini API 金鑰
    one_content = ""
    for stock, urls in stock_dict.items():
        # print(urls)
        # quit()
        for url in urls:
            # if fetch_web_content(url) == None or fetch_web_content(url) == "":
            #     continue
            # else:
            #     one_content += fetch_web_content(url)
            if fetch_web_content(url):
                one_content += fetch_web_content(url)
                time.sleep(2)

        # print(one_content)
        try:
            llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest", google_api_key=GEMINI_API_KEY)

            # 輸入一個問題
            user_input = f"請將以下的內容做成約500字的繁體中文摘要，請緊扣{stock}，不要寫到其他股票的內容,且資料必須有正確的來源：\n" + one_content
            # print(user_input)
            # print("*"*50)
            # quit()
            response = llm.invoke(user_input)
            summaries[stock] = response.content  # 每檔股票摘要
            # print(":"*50)
            # print(summaries)
            # return response.content
        except requests.RequestException as e:
            print(f"Error summarizing content: {e}")
            return "摘要生成失敗"
    time.sleep(2)    
        
    return summaries
def add_summary_to_notion(summaries):
    one_summary = ""
    for stockname,summary in summaries.items():
        one_summary = f"{stockname}\n{summary}\n\n"
   
    # print("-"*50)
    # print(one_summary)
    # print("*"*50)
    # quit()
        # ""將摘要新增到 Notion 頁面"""
        try:
            # 使用 Notion API 創建頁面
            response = notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "Stockreport": {  # 假設資料庫有一個名稱欄位叫 "Name"
                        "rich_text": [{"text": {"content": one_summary}}]
                        # "rich_text": [{"text": {"content": one_summary}}]
                    }
                },
                children=[  # 可選：為頁面新增內容
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": one_summary}}]
                        }
                    }
                ]
            )
            # print(response)
        except Exception as e:
            print(f"建立頁面時發生錯誤: {e}")
            return None


# 寫入 Notion 資料表
# def write_to_notion(summaries):
#     notion_api_url = "https://api.notion.com/v1/pages"
#     notion_api_key = "your_notion_api_key"  # 替換為 Notion API 金鑰
#     database_id = "your_notion_database_id"  # 替換為 Notion 資料庫 ID
    
#     headers = {
#         "Authorization": f"Bearer {notion_api_key}",
#         "Content-Type": "application/json",
#         "Notion-Version": "2022-06-28"
#     }
    
#     for stock, summary in summaries.items():
#         data = {
#             "parent": {"database_id": database_id},
#             "properties": {
#                 "Name": {"title": [{"text": {"content": stock}}]},
#                 "Summary": {"rich_text": [{"text": {"content": summary}}]}
#             }
#         }
#         response = requests.post(notion_api_url, headers=headers, json=data)
#         if response.status_code != 200:
#             print(f"Failed to write stock {stock} to Notion.")

# 主程式邏輯
if __name__ == "__main__":
    if not is_valid_date():
        print("今天不是指定執行日期，程式結束。")
    else:
        stock_data = fetch_stock_data()
        # print(stock_data)
        # quit()
        stock_list = [(row[0], row[1]) for row in stock_data]
        # print("*"*50)
        # print(stock_list)
        # quit()
        search_results = search_stock_info(stock_list)
        # print("-"*50)
        # print(search_results)
        # quit()
        summaries = summarize_links(search_results)
        # print(summaries)
        # quit()
        add_summary_to_notion(summaries)
        print("資料已成功處理並寫入 Notion。")
