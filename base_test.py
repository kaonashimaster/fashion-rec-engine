import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://www.bloomlatte.jp/categories/2646842"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

print("データ取得を開始します...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

items = soup.find_all("a", class_="list")
print(f"取得した商品数: {len(items)}件\n")

# 抽出したデータを貯めるための空のリスト
data_list = []

for item in items:
    # 1. 商品名の取得
    name_tag = item.find("p", class_="text1")
    name = name_tag.text.strip() if name_tag else "名前なし"
    
    # 2. URLの取得
    link = item.get("href")
    
    # 3. 価格の取得（正規表現で ¥ とカンマを取り除いて数字だけにする）
    all_text = item.get_text(separator=" ", strip=True)
    
    # "¥1,234" や "¥ 1,234" のようなパターンを探す
    price_match = re.findall(r'¥\s*([\d,]+)', all_text)
    
    price = None
    if price_match:
        # セール品などで複数価格がある場合は、一番最後の価格（現在価格）を正とする
        raw_price = price_match[-1].replace(",", "")
        try:
            price = int(raw_price)
        except ValueError:
            price = None

    # リストに追加
    data_list.append({
        "商品名": name,
        "価格": price,
        "URL": link
    })

# --- ここからPandasの出番 ---
# リストをデータフレーム（表形式）に変換
df = pd.DataFrame(data_list)

# 価格が取れなかったデータ（None）を除外
df = df.dropna(subset=['価格'])

print(df.head()) # 上位5件を表形式で表示

# CSVファイルとして保存（エクセルで開けます）
csv_filename = "base_items_tops.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print(f"\n【完了】データを {csv_filename} に保存しました！")
print(f"平均価格: ¥{df['価格'].mean():.0f}")
print(f"最高価格: ¥{df['価格'].max()}")