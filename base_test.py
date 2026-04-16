import requests
from bs4 import BeautifulSoup

url = "https://www.bloomlatte.jp/categories/2646842"  # BASEで動いているセレクトショップ
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
print(f"ステータスコード: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# BASEの商品要素を探す
items = soup.find_all("li", class_="item")
print(f"取得した商品数: {len(items)}")

if items:
    for item in items[:3]:
        print(item.text.strip()[:100])
else:
    # 構造確認用
    print(response.text[:2000])