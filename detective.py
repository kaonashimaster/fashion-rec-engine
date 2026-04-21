import requests
from bs4 import BeautifulSoup
import time

# ターゲット3社のURL（商品一覧ページ）
target_shops = {
    "pui": "https://puiiup.thebase.in/",
    "isxnot": "https://isxnot.thebase.in/",
    "amore": "https://lilikids7.thebase.in/categories/7179414"
}

headers = {"User-Agent": "Mozilla/5.0"}

for shop_name, url in target_shops.items():
    print(f"【偵察中】{shop_name} ... ", end="")
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        
        # 先週 bloomlatte で成功したクラス名で探してみる
        items = soup.find_all("a", class_="list")
        
        if len(items) > 0:
            print(f"成功！ ({len(items)}件発見) -> 先週のコードがそのまま使えます！")
        else:
            print(f"失敗 (0件) -> デザインテーマが違うため、クラス名の特定（デバッグ）が必要です。")
            
    except Exception as e:
        print(f"通信エラー: {e}")
        
    time.sleep(2) # 相手サーバーに負荷をかけないよう2秒待つ（礼儀）