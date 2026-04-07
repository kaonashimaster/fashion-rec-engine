import requests
from bs4 import BeautifulSoup

url = "https://zozo.jp/men-category/tops/"

# セッションを開始
session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/", # Googleから来たふりをする
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

try:
    # セッション経由でアクセス
    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    print(f"成功！ステータスコード: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'lxml')
    print(f"ページのタイトル: {soup.title.string}")

except Exception as e:
    print(f"エラー発生: {e}")