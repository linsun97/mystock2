import os
import requests
from datetime import datetime
# from docx import Document
from duckduckgo_search import DDGS
from duckduckgo_search import exceptions
import mariadb
import time
from summary import make_summary

googlesearch_api_key = "AIzaSyC60xTfn-SWNSbc17pTzvWs-cfVGsqVZNU"
googlesearch_engine_id = "500990df209ce4c36"
# 股票代碼清單
# stock_ids = ['7769', '3616', '7760']  # 股票代碼，不包括 .TW 後綴
youtube_api_key = 'AIzaSyDirDw_Tw2lSp3rano1SLuXBqLgoR2J-zo'  # 替換為您的 YouTube Data API 金鑰

def is_valid_date():
    today = datetime.date.today()
    valid_dates = [(4, 5), (5, 25), (8, 25), (11, 25)]  # 月日
    return (today.month, today.day) in valid_dates
# 連接到 MariaDB 資料庫
def get_stock_names():
    
    connection = mariadb.connect(
        user="root",       # MariaDB 使用者名稱
        password="nineseve9173",   # MariaDB 密碼
        host="localhost",           # 資料庫主機位址，通常是 localhost
        port=3306,                  # 預設 MariaDB 的連接埠
        database="stock"            # 資料庫名稱
    )
    cursor = connection.cursor()
    
    stock_names = {}
    stock_data = []


    try:
        cursor = connection.cursor()
        cursor.execute("SELECT stockid, stockname FROM moniter")
        stock_data = cursor.fetchall()  # 取得所有資料
        connection.close()
    except mariadb.Error as e:
        print(f"Error executing query: {e}")
    
    for stockid, stockname in stock_data:
        stock_names[stockid] = stockname 
    # print(stock_names)
    # quit()
    return stock_names
# 獲取每個資料表最後一筆資料的 New_up 欄位值
def get_last_new_up_values():
    tables = ["shin_oneday", "sum_oneday", "sup_oneday"]
    results = {}
    connection = mariadb.connect(
        user="root",       # MariaDB 使用者名稱
        password="nineseve9173",   # MariaDB 密碼
        host="localhost",           # 資料庫主機位址，通常是 localhost
        port=3306,                  # 預設 MariaDB 的連接埠
        database="stock"            # 資料庫名稱
    )
    cursor = connection.cursor()


    for table in tables:
        cursor.execute(f"SELECT New_up FROM {table} ORDER BY Up_date DESC LIMIT 1")  # 假設 id 是排序依據
        row = cursor.fetchone()
        
        if row:
            new_up_value = row[0]
            if new_up_value:
            #     results[table] = new_up_value.split(",")  # 分割 New_up 欄位值
                # 分割並轉換為整數
                # results[table] = [int(value) for value in new_up_value.split(",") if value.strip() and (value.strip().isdigit() or is_positive_integer(value))]
                results[table] = [int(value) for value in new_up_value.split(",") if value.strip() and (value.strip().isdigit() or isinstance(value,int)) ]
            else:
                results[table] = []
        else:
            results[table] = []

    cursor.close()
    connection.close()
    
    return results

# 定義查詢新聞的功能
def fetch_news(stock_id, stock_name):
    query = f"{stock_id} {stock_name}  新聞 "
    print(query)
    # time.sleep(3)

    results = None
    # retry_count = 5
    # for i in range(retry_count):
    #     try:
    #         # 你的 DuckDuckGo 搜尋程式碼
    #         results = DDGS().text(query, max_results=5)
    #         break  # 如果請求成功則跳出迴圈
    #     except exceptions.RatelimitException as e:
    #         print("速率限制錯誤，嘗試重試...")
    #         time.sleep(5)  # 暫停 10 秒後再重試
    
    
    if results == None or results == []:

        # 建立 API 請求網址
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={googlesearch_engine_id}&key={googlesearch_api_key}"

        # 發送請求
        response = requests.get(url)

        link_list = []
        # 處理結果
        if response.status_code == 200:
            results = response.json()
            for item in results.get("items", []):
                if item['title'] :
                    print(f"標題: {item['title']}")
                if item['link'] :
                    print(f"連結: {item['link']}")
                    link_list.append(item['link'])
                if item['snippet'] :
                    print(f"摘要: {item.get('snippet', '未提供摘要')}")
                print("="*50)
            # print(results)
            # print(type(results))
            # quit()

            # return results
            # 將link的前三個傳給make_summary
            # try:
            #     # print(link_list)
            #     # print("*"*50)
            #     # print(link_list[0:4])
            #     # print("*"*50)

            #     make_summary(link_list[0:4])
            #     print(make_summary)
            # except Exception as e:
            #     print(f"Error:製作摘要失敗-- {e}")

        else:
            print(f"請求google搜尋失敗，狀態碼: {response.status_code}")
    

    
    news_data = []
    
    # for result in results:
    #     news_data.append({
    #         "title": result["title"],
    #         "date": result.get("date", "未知"),
    #         "summary": result["body"],
    #         "link": result["href"]
    #     })
    for item in results.get("items", []):
        news_data.append({
            "title": item["title"],
            "date": item.get("date", "未知"),
            "summary": item.get("snippet", "未知"),
            "link": item["link"]
        })
    
    return news_data

# 定義查詢影片的功能
def fetch_videos(stock_id, stock_name):
    query = f"{stock_id} {stock_name}"
    print(query)
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={youtube_api_key}&maxResults=5&regionCode=TW&type=video"
    response = requests.get(url)
    video_data = []
    
    if response.status_code == 200:
        video_items = response.json().get('items', [])
        for item in video_items:
            video_data.append({
                "title": item["snippet"]["title"],
                "date": item["snippet"]["publishedAt"],
                "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            })
    else:
        print(f"Failed to fetch videos for {stock_id} {stock_name}. Status code: {response.status_code}")
    return video_data

# 統整每支股票的報告內容
def compile_report(stock_id, stock_name):
    news = fetch_news(stock_id, stock_name)
    videos = fetch_videos(stock_id, stock_name)
    
    goodinfo_link = f"https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID={stock_id}&INIT=T"
    
    report_content = f"## 股票代碼: {stock_id} ({stock_name})\n"
    print(report_content)
    report_content += f"### Goodinfo連結:\n"
    report_content += f'<a href="{goodinfo_link}" target="_blank">{goodinfo_link}</a><br>\n\n'
    
    report_content += "### 新聞分析:\n"
    
    if news:
        for n in news:
            report_content += f"- **{n['date']}**: {n['title']}<br>  {n['summary']}<br>  <a href='{n['link']}' target='_blank'>來源</a><br><br>\n"
            # time.sleep(3)  # 暫停 3 秒，避免過快請求

    else:
        report_content += "- 無相關新聞資料\n\n"

    report_content += "### 影片分析:\n"
    
    if videos:
        for v in videos:
            report_content += f"- **{v['date']}**: {v['title']}<br>  <a href='{v['link']}' target='_blank'>來源</a><br><br>\n"
            # time.sleep(3)  # 暫停 3 秒，避免過快請求


    else:
        report_content += "- 無相關影片資料\n\n"

    return report_content  # 限制字數在3000以內

# 生成 HTML 報告
def generate_html(reports):
    os.makedirs("report_moniter", exist_ok=True)
    html_name = datetime.now().strftime("%Y%m%d") + f"_new.html"
    html_path = os.path.join("report_moniter", html_name)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write("<html><head><meta charset='utf-8'><title>股票報告</title></head><body>")
        
        for report in reports:
            f.write("<div style='page-break-after: always;'>")  # 每個報告之間插入分頁
            for line in report.split('\n'):
                if line.startswith("##"):
                    f.write(f"<h2>{line[3:]}</h2>")  # 添加二級標題
                elif line.startswith("###"):
                    f.write(f"<h3>{line[4:]}</h3>")  # 添加三級標題
                elif line.startswith("-"):
                    f.write(f"<li>{line[2:]}</li>")  # 添加項目符號列表
                else:
                    f.write(f"<p>{line}</p>")  # 添加普通段落
            
            f.write("</div>")
        
        f.write("</body></html>")
    
    print(f"報告已生成: {html_path}")

# 主程式執行
if __name__ == "__main__":
    # tables = ["shin_oneday", "sum_oneday", "sup_oneday"]
    # stock_names_dict = get_stock_names()
    # print(stock_names_dict)

    # last_new_up_values = get_last_new_up_values()
    # print(last_new_up_values)
    # quit()
    
    # for table, values in last_new_up_values.items():
    #     print(f"{table} 的最後一筆 New_up 值: {values}")

    #     if values == []:  # 檢查 stock_ids 是否為空
    #         print(f"股票代碼列表為空，今日{table}無新上市櫃股票。")
    #         # quit()
    #         continue
    if not is_valid_date():
        print("今天不是指定執行日期，程式結束。")
    else:    
        stock_names_dict = get_stock_names()
        # print(stock_names_dict)
        
        reports = []

        for stock_id, stock_name in stock_names_dict.items():
            report_content = compile_report(stock_id, stock_name)
            reports.append(report_content)

        generate_html(reports)  # 呼叫生成 HTML 報告的函數