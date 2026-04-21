import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# 1. ターゲット設定（偵察結果をここに反映！）
shops = [
    {
        "name": "pui", 
        "base_url": "https://puiiup.thebase.in/", 
        "tag": "div", "class": "item part fadeinup"
    },
    {
        "name": "isxnot", 
        "base_url": "https://isxnot.thebase.in/", 
        "tag": "li", "class": "column"
    },
    {
        "name": "amore", 
        "base_url": "https://lilikids7.thebase.in/categories/7179414", 
        "tag": "li", "class": "items-grid_itemListLI_5c97110f"
    }
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
all_data = []

# 2. メインループ（ショップごと ➔ ページごと）
for shop in shops:
    print(f"--- {shop['name']} の取得を開始 ---")
    
    # とりあえず各ショップ 1〜3ページ目まで取ってみる（テスト用）
    for page in range(1, 4):
        # BASEのページネーションURLの法則（?page=N）
        # 元のURLに「?」が含まれているかどうかで連結文字を変える
        connector = "&" if "?" in shop['base_url'] else "?"
        url = f"{shop['base_url']}{connector}page={page}"
        
        print(f"  {page}ページ目を取得中: {url}")
        
        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "lxml")
            items = soup.find_all(shop['tag'], class_=shop['class'])
            
            if not items:
                print(f"    -> このページに商品はありません（終了）。")
                break
                
            for item in items:
                text = item.get_text(separator=" ", strip=True)
                
                # 価格の抽出（正規表現：¥ 1,234 みたいな形式を探す）
                price_match = re.findall(r'¥\s*([\d,]+)', text)
                price = int(price_match[-1].replace(",", "")) if price_match else None
                
                # 商品名（とりあえずテキストの最初の方を抽出。ショップごとに微調整が必要かも）
                name = text.split("¥")[0].strip()
                
                all_data.append({
                    "ショップ名": shop['name'],
                    "商品名": name,
                    "価格": price,
                    "ページ": page
                })
            
            time.sleep(1) # サーバーへの優しさ
            
        except Exception as e:
            print(f"    エラー発生: {e}")

# 3. データの保存
df = pd.DataFrame(all_data)
df.to_csv("combined_base_data.csv", index=False, encoding="utf-8-sig")

print(f"\n✅ 統合完了！ 合計 {len(df)} 件のデータを保存しました。")
print(df.groupby("ショップ名")["価格"].describe()) # 簡易統計を表示