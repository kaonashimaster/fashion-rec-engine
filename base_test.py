import requests
from bs4 import BeautifulSoup

url = "https://www.bloomlatte.jp/categories/2646842"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 【修正ポイント】 li ではなく div で探す
items = soup.find_all("div", class_="item")
print(f"取得した商品数: {len(items)}")

# 商品名の一部が、生のHTMLコードの中に含まれているかチェック
print(f"『ドット柄』という文字はHTMLにあるか: {'ドット柄' in response.text}")

for item in items:
    # 商品名は img タグの alt 属性に書かれていることを確認
    img_tag = item.find("img")
    if img_tag and img_tag.get("alt"):
        name = img_tag.get("alt")
        # 価格などの他の要素も、同じように div.item の中から探せます
        print(f"商品名: {name}")

# もし価格も取りたいなら、ブラウザで価格の数字を右クリックして
# どのクラス（例: itemPrice など）に入っているか教えてください！