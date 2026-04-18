import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

url = "https://www.bloomlatte.jp/categories/2646842"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

items = soup.find_all("a", class_="list")
data_list = []

for item in items:
    name_tag = item.find("p", class_="text1")
    name = name_tag.text.strip() if name_tag else "名前なし"
    all_text = item.get_text(separator=" ", strip=True)
    price_match = re.findall(r'¥\s*([\d,]+)', all_text)
    
    price = None
    if price_match:
        price = int(price_match[-1].replace(",", ""))

    data_list.append({
        "商品名": name,
        "生のテキスト": all_text, # 原因を探るために生データも残す
        "価格": price
    })

df = pd.DataFrame(data_list)

# ★ 今回の主役：価格が取れなかった（NaN）データだけを抽出する
missing_price_df = df[df['価格'].isna()]

print(f"価格が取れなかった商品数: {len(missing_price_df)}件\n")
for index, row in missing_price_df.iterrows():
    print(f"商品名: {row['商品名']}")
    print(f"生テキスト: {row['生のテキスト']}")
    print("-" * 30)