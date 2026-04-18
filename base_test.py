import requests
from bs4 import BeautifulSoup

url = "https://www.bloomlatte.jp/categories/2646842"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

response = requests.get(url, headers=headers)

# 1. 念のため、より強力な解析エンジン 'lxml' を使う（すでにインストール済みのはず）
soup = BeautifulSoup(response.text, "lxml")

# 2. 「ドット柄」という文字を含んでいる要素を直接探す
target_text = soup.find(string=lambda t: "ドット柄" in t if t else False)

if target_text:
    print("【発見！】『ドット柄』という文字を見つけました。")
    # その文字の「親の親の親」くらいまでのタグとクラス名を表示して正体を探る
    parent = target_text.parent
    print(f"直接のタグ: <{parent.name}> class={parent.get('class')}")
    print(f"その親のタグ: <{parent.parent.name}> class={parent.parent.get('class')}")
    print(f"さらにその親: <{parent.parent.parent.name}> class={parent.parent.parent.get('class')}")
else:
    print("BeautifulSoupの解析結果からは見つかりませんでした。")

# 3. CSSセレクタという別の方法で item クラスを探してみる
items_by_selector = soup.select(".item")
print(f"CSSセレクタで見つかった件数: {len(items_by_selector)}")