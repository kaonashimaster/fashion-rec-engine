import requests
from bs4 import BeautifulSoup

url = "https://www.bloomlatte.jp/categories/2646842"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# 1. デバッグで特定した「本当の商品の箱（aタグのlistクラス）」を全て取得
items = soup.find_all("a", class_="list")

print(f"【大成功】取得した商品数: {len(items)}件\n" + "="*30)

# 2. 上位5件だけ、中身を細かく見てみる
for i, item in enumerate(items[:5], 1):
    # 商品名（先ほど特定した pタグの text1クラス）
    name_tag = item.find("p", class_="text1")
    name = name_tag.text.strip() if name_tag else "名前なし"
    
    # リンクのURL
    link = item.get("href")
    
    # ★価格を探すために、箱の中の文字を全部繋げて表示してみる
    all_text = item.get_text(separator=" | ", strip=True)

    print(f"[{i}件目]")
    print(f"商品名: {name}")
    print(f"箱の中身全て: {all_text}")
    print(f"URL: {link}")
    print("-" * 30)