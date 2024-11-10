from googlesearch import search
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import youtube_dl

def search_news(query, num_results=5):
    news_results = list(search(query + " 新聞", num_results=num_results, lang="zh-TW"))
    return news_results

def search_videos(query, num_results=3):
    video_results = []
    for url in search(query + " 影片", num_results=num_results, lang="zh-TW"):
        if "youtube.com" in url:
            video_results.append(url)
    return video_results

def get_video_info(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info['title'], info['description']
        except Exception as e:
            print(f"無法獲取影片信息: {str(e)}")
            return "無標題", "無描述"

def create_pdf_report(stock_name, news_results, video_results):
    doc = SimpleDocTemplate(f"{stock_name}股票報告.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # 添加標題
    story.append(Paragraph(f"{stock_name}股票相關資訊報告", styles['Title']))
    story.append(Spacer(1, 12))

    # 添加新聞部分
    story.append(Paragraph("相關新聞：", styles['Heading2']))
    for i, url in enumerate(news_results, 1):
        story.append(Paragraph(f"{i}. {url}", styles['BodyText']))
        story.append(Spacer(1, 6))

    # 添加影片部分
    story.append(Paragraph("相關影片：", styles['Heading2']))
    for i, url in enumerate(video_results, 1):
        title, description = get_video_info(url)
        story.append(Paragraph(f"{i}. {title}", styles['Heading3']))
        story.append(Paragraph(f"   連結：{url}", styles['BodyText']))
        story.append(Paragraph(f"   描述：{description}", styles['BodyText']))
        story.append(Spacer(1, 6))

    doc.build(story)

def main():
    stock_name = "達亞"
    news_results = search_news(stock_name + " 股票")
    video_results = search_videos(stock_name + " 股票")
    create_pdf_report(stock_name, news_results, video_results)
    print(f"PDF報告已生成：{stock_name}股票報告.pdf")

if __name__ == "__main__":
    main()
