import requests
import os
import json
from googleapiclient.discovery import build

import os

# 添加 GTK 的 DLL 路徑
os.add_dll_directory(r'C:\Program Files\GTK3-Runtime Win64\bin')

# 然後再導入 WeasyPrint 或其他依賴於 Pango 的庫
from weasyprint import HTML
# from weasyprint import HTML

# Google Search API 設定
def google_search(api_key, query):
    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx=500990df209ce4c36&q={query}'
    response = requests.get(url)
    return response.json()

# YouTube Data API 設定
def youtube_search(api_key, query):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(part='snippet', q=query, type='video', maxResults=5)
    response = request.execute()
    return response

# 整理資料並生成 Markdown 格式報告
def generate_report(news_data, video_data):
    report_content = "# 台灣股票達亞（6762）相關報告\n\n"
    
    report_content += "## 新聞\n"
    for item in news_data.get('items', []):
        report_content += f"- **標題**: {item['title']}\n"
        report_content += f"  **連結**: {item['link']}\n\n"

    report_content += "## 影片\n"
    for item in video_data.get('items', []):
        report_content += f"- **標題**: {item['snippet']['title']}\n"
        report_content += f"  **連結**: https://www.youtube.com/watch?v={item['id']['videoId']}\n\n"

    return report_content

# 將 Markdown 轉換為 PDF
def save_pdf(markdown_content, output_file):
    html_content = HTML(string=markdown2.markdown(markdown_content))
    html_content.write_pdf(output_file)

if __name__ == "__main__":
    # 替換為您的 API 金鑰和搜尋引擎 ID
    google_api_key = 'AIzaSyDtfIUwCr5umTvtoCu_iRqhaIHl11rr-Sc'
    youtube_api_key = 'Ye0819310a4cf6a94f5071be1c9f017281ca2383bcfc8db73a58e4f902c13eb6'
    
    query = '台股 達亞 股票代號6762'
    
    # 獲取新聞和影片資料
    news_data = google_search(google_api_key, query)
    video_data = youtube_search(youtube_api_key, query)

    # 生成報告
    report_markdown = generate_report(news_data, video_data)

    # 儲存為 PDF 檔案
    pdf_file_name = '台灣股票達亞報告.pdf'
    save_pdf(report_markdown, pdf_file_name)

    print(f"報告已儲存為 {pdf_file_name}")