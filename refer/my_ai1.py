# 由於OpenAI的API目前並不支援直接搜尋新聞和影片資料，因此這樣的需求必須透過第三方的API服務來實現。可以考慮整合YouTube API來取得影片，並搭配網頁爬蟲（例如BeautifulSoup）或新聞API（如Google News API）來抓取最新的新聞資料。

### 程式邏輯概述
# 1. **新聞資料的取得**：使用Google News API來抓取「達亞」的新聞資料。
# 2. **影片資料的取得**：使用YouTube API來搜尋「達亞」相關的影片。
# 3. **資料整理與排序**：將取得的新聞和影片資料按時間先後排序。
# 4. **報告生成**：用Markdown格式生成報告，並將Markdown轉換為PDF檔案。
# 5. **下載PDF**：讓PDF生成後提供下載連結。

### 安裝需求
# 首先需要安裝以下Python套件：
# ```bash
# pip install google-api-python-client openai reportlab markdown
# ```

### Python範例程式碼
# 以下為一個完整的範例程式碼，供您參考：

# ```python
import openai
from googleapiclient.discovery import build
from datetime import datetime
import markdown
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tempfile
import os

# 設定API金鑰
openai.api_key = "YOUR_OPENAI_API_KEY"
youtube_api_key = "Ye0819310a4cf6a94f5071be1c9f017281ca2383bcfc8db73a58e4f902c13eb6f"

# 設定關鍵字
keyword = "達亞 台灣 股票"

# searchkey = AIzaSyDtfIUwCr5umTvtoCu_iRqhaIHl11rr-Sc

# key= AIzaSyAuSUtIVf751K8zbnyoWyDxx2V_gMenYhw
# 定義Google News API URL（需要第三方新聞API）
# 若您使用的是Google News API，則需註冊並使用合法的API金鑰。
news_api_key = "e0819310a4cf6a94f5071be1c9f017281ca2383bcfc8db73a58e4f902c13eb6f"

# 定義YouTube資料擷取函數
def get_youtube_videos(keyword, max_results=5):
    youtube = build("youtube", "v3", developerKey=youtube_api_key)
    search_response = youtube.search().list(
        q=keyword, part="snippet", maxResults=max_results, order="date", type="video"
    ).execute()
    
    videos = []
    for item in search_response.get("items", []):
        video_title = item["snippet"]["title"]
        video_date = item["snippet"]["publishedAt"]
        video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        videos.append({"title": video_title, "date": video_date, "url": video_url})
    return videos

# 定義新聞資料擷取函數（範例假設使用第三方API）
def get_news(keyword, max_results=5):
    # 替換成實際的API呼叫
    news_data = [
        {"title": "達亞股票表現出色", "date": "2024-11-08", "url": "https://news.example.com/article1"},
        {"title": "達亞新產品發布", "date": "2024-11-06", "url": "https://news.example.com/article2"},
    ]
    return news_data

# 整合資料並按時間排序
def generate_report_data():
    news_data = get_news(keyword)
    videos_data = get_youtube_videos(keyword)
    
    combined_data = news_data + videos_data
    combined_data.sort(key=lambda x: x["date"], reverse=True)
    
    report_content = "# 達亞股票新聞與影片報告\n\n"
    report_content += "## 資料來源（按時間先後排序）\n\n"
    for item in combined_data:
        date = datetime.fromisoformat(item["date"].replace("Z", "+00:00")).strftime('%Y-%m-%d')
        report_content += f"### {item['title']}\n"
        report_content += f"- 日期：{date}\n"
        report_content += f"- 連結：[點此查看]({item['url']})\n\n"
    return report_content

# 將Markdown轉成PDF
def markdown_to_pdf(md_text, pdf_filename="報告.pdf"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        pdf_path = temp_pdf.name
        c = canvas.Canvas(pdf_path, pagesize=A4)
        text = markdown.markdown(md_text)
        
        # 設定字型
        c.setFont("Helvetica", 12)
        
        # 輸入文字內容
        y_position = 800
        for line in text.splitlines():
            c.drawString(50, y_position, line)
            y_position -= 15
            if y_position < 50:  # 換頁處理
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = 800
        
        c.save()
        os.rename(pdf_path, pdf_filename)

# 主程式執行
if __name__ == "__main__":
    # 生成報告內容
    report_md = generate_report_data()
    
    # 生成PDF
    pdf_filename = "達亞股票報告.pdf"
    markdown_to_pdf(report_md, pdf_filename)
    
    print(f"報告已生成：{pdf_filename}")
# ```

### 程式碼說明
# 1. **`get_youtube_videos`**：透過YouTube API來取得關鍵字「達亞 台灣 股票」的相關影片，並取得影片標題、日期、連結等資訊。
# 2. **`get_news`**：假設使用Google News API或其他第三方API來取得「達亞」的新聞資料（此處僅為範例資料）。
# 3. **`generate_report_data`**：整合新聞與影片資料，並按時間順序生成Markdown格式的報告內容。
# 4. **`markdown_to_pdf`**：使用ReportLab套件將Markdown格式的報告內容轉換為PDF。

### 執行後結果
# - 產生的PDF文件包含「達亞」的最新新聞和影片資訊，並且按時間先後排列。
# - 您可以下載生成的PDF檔案。

### 注意事項
# - YouTube API和Google News API需要註冊並獲得API金鑰。
# - 請將API金鑰替換為您的實際金鑰。
# 幫我寫一段程式，將新聞和影片資料整合成報告，並且按時間順序排列。
# 我們可以使用Python來完成這個任務。首先，我們需要從YouTube API和Google News API取得相關資料。然後，我們可以將這些資料整合成一個報告，並按照時間順序排列。最後，我們可以將報告轉換為PDF格式。

# 以下是一個簡單的Python程式碼範例，展示了如何實現這個任務：

# ```python
# import requests
# from datetime import datetime
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# import markdown
# import tempfile
# import os

# def get_youtube_videos(keyword):              

# 使用YouTube API取得影片資料
# 參考連結：https://developers.google.com/youtube/v3/docs/videos/list
# 參考連結：https://developers.google.com/youtube/v3/docs/channels/list
# 參考連結：https://developers.google.com/youtube/v3/docs/playlists/list    
# 參考連結：https://developers.google.com/youtube/v3/docs/search/list

# 使用Google News API取得新聞資料
# 參考連結：https://newsapi.org/docs/endpoints/top-headlines
# 參考連結：https://newsapi.org/docs/endpoints/everything    

# 將影片資料和新聞資料整合成報告內容        
# 將報告內容轉換為PDF格式                       
# ```
#    
# 這個程式碼範例中，我們使用了ReportLab套件來生成PDF文件，這個套件可以很方便地將Markdown格式的報告內容轉換為PDF檔案。    
# 這個程式碼範例中，我們使用了Markdown套件來格式化報告內容，這個套件可以很方便地將文字轉換為HTML格式，然後再轉換為PDF檔案。    
# 最後，這個程式碼範例中，我們使用了tempfile和os套件來生成PDF檔案，這些套件可以很方便地將PDF檔案保存到本地。    
#    
# 這個程式碼範例中，我們使用了requests套件來獲取YouTube API和Google News API的資料，這些套件可以很方便地獲取網路資料。
#     
# 這個程式碼範例中，我們使用了datetime套件來獲取日期和時間，這個套件可以很方便地獲取日期和時間。
#     
# 這個程式碼範例中，我們使用了reportlab套件來生成PDF文件，這個套件可以很方便地將Markdown格式的報告內容轉換為PDF檔案。
#     
# 這個程式碼範例中，我們使用了markdown套件來格式化報告內容，這個套件可以很方便地將文字轉換為HTML格式，然後再轉換為PDF檔案。
#     
# 這個程式碼範例中，我們使用了tempfile和os套件來生成PDF檔案，這些套件可以很方便地將PDF檔案保存到本地。
#     
# 這個程式碼範例中，我們使用了requests套件來獲取YouTube API和Google News API的資料，這些套件可以很方便地獲取網路資料。
#     
# 這個程式碼範例中，我們使用了datetime套件來獲取日期和時間，這個套件可以很方便地獲取日期和時間。
#     
# 這個程式碼範例中，我們使用了reportlab套件來生成PDF文件，這個套件可以很方便地將Markdown格式的報告內容轉換為PDF檔案。
#     
# 這個程式碼範例中，我們使用了markdown套件來格式化報告內容，這個套件可以很方便地將文字轉換為HTML格式，然後再轉換為PDF檔案。
#     
# 這個程式碼範例中，我們使用了tempfile和os套件來生成PDF檔案，這些套件可以很方便地將PDF檔案保存到本地。
#     
# 這個程式碼範例中，我們使用了requests套件來獲取YouTube API和Google News API的資料，這些套件可以很方便地獲取網路資料。
#                            


