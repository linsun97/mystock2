import requests

def google_search(api_key, query):
    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx=YOUR_SEARCH_ENGINE_ID&q={query}'
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    api_key = 'AIzaSyDtfIUwCr5umTvtoCu_iRqhaIHl11rr-Sc'  # 替換為您的 Google Search API 金鑰
    search_engine_id = 'YOUR_SEARCH_ENGINE_ID'  # 替換為您的自訂搜尋引擎 ID
    query = '台股 達亞'
    
    search_results = google_search(api_key, query)
    
    for item in search_results.get('items', []):
        print(f"標題: {item['title']}, 連結: {item['link']}")