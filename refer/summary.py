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
url_list = ['https://udn.com/news/story/7254/8396851', 'https://tw.stock.yahoo.com/news/%E4%B9%85%E6%98%8C12%E6%9C%88%E4%B8%8A%E6%AB%83%E6%8E%9B%E7%89%8C-%E9%9C%8D%E7%88%BEic%E5%B0%8E%E5%85%A5%E7%A3%81%E8%BB%B8%E9%8D%B5%E7%9B%A4%E5%85%A8%E7%90%83%E7%AC%AC-065533859.html', 'https://hk.finance.yahoo.com/quote/6720.TWO/', 'https://tw.stock.yahoo.com/news/%E6%9C%80%E9%AB%98%E6%9C%89%E6%9C%9B35%E8%90%AC%E5%85%A5%E8%A2%8B%EF%BC%81%E4%B9%85%E6%98%8C%E3%80%81%E5%90%89%E8%8C%822%E6%AA%94%E6%96%B0%E8%82%A1%E7%94%B3%E8%B3%BC%E4%BB%8A%E6%97%A5%E9%96%8B%E8%B7%91-020122478.html']

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
                # raise Exception(f"無法提取主要內容: {url}")
                print(f"無法提取主要內容: {url}") # Exception(f"無法提取主要內容: {url}")
                main_content = ""

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
            user_input = "請將以下的內容做成約500字的繁體中文摘要，請緊扣主題，不要寫到不相干的內容：\n" + content

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
        if web_content :
            combined_content += web_content + "\n"
        else:
            print(f"網頁內容為空: {url}")
        # print(combined_content)
        # quit()
    if combined_content:
        summary = summarize_content_with_gemini(combined_content)  # 生成摘要
        # print(f"摘要: {summary}")
        # quit()
        add_summary_to_notion(url, summary)  # 上傳到 Notion

        # print(combined_content)


# 測試
# make_summary(url_list)