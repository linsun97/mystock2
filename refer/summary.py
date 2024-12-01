import requests
from notion_client import Client
import json
from bs4 import BeautifulSoup 
from langchain_google_genai import ChatGoogleGenerativeAI

# 設定 Google Gemini API 和 Notion Token
GEMINI_API_KEY = "AIzaSyC93dmru4HZhCTZDJeJS1SYtNeQIAh6KIA"  # 替換為你的 Google Gemini API Key
NOTION_TOKEN = "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"  # 替換為你的 Notion 整合 Token
# NOTION_PAGE_ID = "your_notion_page_id"  # 替換為你的 Notion 頁面 ID
# 設定您的 API 金鑰和資料庫 ID
# api_key = 'YOUR_NOTION_API_KEY'
NOTION_DATABASE_ID = '14d5881a436880cc8dd3fc49c05ef4f6'

# 網址列表
url_list = [ "http://www.investor.com.tw/Mobile/content.asp?articleNo=14202411290064","https://tw.stock.yahoo.com/news/%E5%AE%8F%E7%A2%81%E6%97%97%E4%B8%8B%E5%94%AF-%E9%9D%9E%E9%9B%BB%E5%AD%90%E5%B0%8F%E9%87%91%E8%99%8E-%E5%8D%9A%E7%91%9E%E9%81%94%E6%87%89%E6%9D%90%E4%BB%8A%E7%99%BB%E8%88%88%E6%AB%83-012421400.html"]

# 初始化 Notion 客戶端
notion = Client(auth=NOTION_TOKEN)

def make_summary(url_list):

    def fetch_web_content(url):
        """讀取指定網址的網頁內容"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            # return response.text
            # 確保請求成功
            response.encoding = response.apparent_encoding  # 自動檢測編碼
            print(response.encoding)
            
            
            html_content = response.text

            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # # 去除不必要的內容（例如 script, style 等）
            # for tag in soup(['script', 'style']):
            #     tag.decompose()

            # # 提取主要文字內容
            # main_text = soup.get_text(separator='\n')  # 使用換行符分隔段落

            # # 清理額外的空白
            # clean_text = '\n'.join(line.strip() for line in main_text.splitlines() if line.strip())

            # return clean_text

            # 嘗試過濾廣告與非主要內容（可根據網站特性微調）
            for element in soup(["script", "style", "header", "footer", "aside", "nav"]):
                element.extract()  # 移除不需要的元素

            # 提取主要段落文字
            paragraphs = soup.find_all("p")
            main_content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            if not main_content:
                raise Exception(f"無法提取主要內容: {url}")

            return main_content
        
        except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")
                return None

    def summarize_content_with_gemini(content):
        """透過 Google Gemini API 生成內容摘要"""

        
        try:
            llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest", google_api_key=GEMINI_API_KEY)

            # 輸入一個問題
            user_input = "請將下面的內容做成約500字的繁體中文摘要：\n" + content

            response = llm.invoke(user_input)

            return response.content
        except requests.RequestException as e:
            print(f"Error summarizing content: {e}")
            return "摘要生成失敗"

    def add_summary_to_notion(url, summary):
        """將摘要新增到 Notion 頁面"""
        try:
            # 使用 Notion API 創建頁面
            response = notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "Name": {  # 假設資料庫有一個名稱欄位叫 "Name"
                        "title": [{"text": {"content": summary}}]
                    }
                },
                children=[  # 可選：為頁面新增內容
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": summary}}]
                        }
                    }
                ]
            )

            # new_page_id = "14d5881a436880a2ad18d1858a90b960"
            # notion.pages.update(
            #     **{
            #         "page_id": new_page_id,
            #         "properties": {
            #             "title": {
            #                 "type": "title",
            #                 "title": [{"type": "text", "text": {"content": "股票新聞摘要"}}],
            #             },
            #         },
            #         "children": [
            #             {
            #                 "object": "block",
            #                 "type": "paragraph",
            #                 "paragraph": {"text": [{"type": "text", "text": {"content": summary}}]},
            #             }
            #         ],
            #     }
            # )

            # 返回新頁面的 ID
            # new_page_id = response["id"]
            
            # print(f"新頁面已建立，Page ID: {new_page_id}")
            # return new_page_id
        except Exception as e:
            print(f"建立頁面時發生錯誤: {e}")
            return None

    # 主程式
    combined_content = ""
    for url in url_list:
        web_content = fetch_web_content(url)  # 獲取網頁內容
        # web_content = "股票代碼: 6972 (博瑞達應材)"
        combined_content += web_content + "\n"
        # print(combined_content)
        # quit()
    if combined_content:
        summary = summarize_content_with_gemini(combined_content)  # 生成摘要
        # print(f"摘要: {summary}")
        # quit()
        add_summary_to_notion(url, summary)  # 上傳到 Notion

        # print(combined_content)
