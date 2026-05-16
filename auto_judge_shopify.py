import requests
import pandas as pd
import time

# 1. 調査したいセレクトショップのURLリスト（ここに20社のURLを貼ります）
# ※いくつかテスト用に事前に入れています
target_shops = [
    {"name": "O (オー)", "url": "https://store.moc-o.com/"},
    {"name": "NUBIAN", "url": "https://nubiantokyo.com/"},
    {"name": "RESTIR", "url": "https://www.restir.com/"},
    {"name": "MIDWEST", "url": "https://store-midwest.com/"},
    {"name": "KIKUNOBU", "url": "https://kikunobu.jp/"},
    {"name": "1LDK", "url": "https://onlinestore.1ldkshop.com/"},
    {"name": "MAIDENS SHOP", "url": "https://store-maiden.com/"},
    {"name": "BIOTOP", "url": "https://www.junonline.jp/biotop/"},
    {"name": "ARKnets", "url": "https://www.arknets.co.jp/"},
    {"name": "ACRMTSM", "url": "https://www.acrmtsm.jp/"},
    {"name": "HOWDAY", "url": "https://howday.official.ec/"},
    {"name": "DeepInsideInc.", "url": "https://www.deepinsideinc.com/"},
    {"name": "CIENTO", "url": "https://www.cientowebstore.com/"},
    {"name": "Nariwai(業)", "url": "https://nariwai.theshop.jp/"},
    {"name": "ATTIC", "url": "https://attic-sendai.com/"},
    {"name": "rroomm", "url": "https://www.rroomm.jp/"},
    {"name": "sister tokyo", "url": "https://sister-tokyo.com/"}
]

# 2. サイトの裏側を判定する関数
def detect_platform(url):
    headers = {
        # ブラウザからのアクセスに見せかけるための偽装（弾かれにくくする）
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # サイトのHTML（F12のElementsタブで見れる文字の塊）を取得
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text.lower() # 検索しやすいように小文字に変換
        
        # --- キーワード検索（Ctrl+Fの代わり） ---
        if 'cdn.shopify' in html or 'window.shopify' in html:
            return 'Shopify'
        elif 'wp-content' in html or 'wordpress' in html:
            return 'WordPress (WooCommerce等)'
        elif 'makeshop' in html:
            return 'MakeShop'
        elif 'stores.jp' in html:
            return 'STORES'
        elif 'thebase.in' in html or 'base_ec' in html:
            return 'BASE'
        else:
            return '独自CMS / その他'
            
    except requests.exceptions.RequestException as e:
        return 'アクセスブロック/エラー'

# 3. リストを回して全自動チェック
results = []
print("🔍 自動判定をスタートします...\n" + "-"*40)

for shop in target_shops:
    print(f"[{shop['name']}] を調査中...")
    platform = detect_platform(shop["url"])
    
    results.append({
        "ショップ名": shop["name"],
        "URL": shop["url"],
        "プラットフォーム": platform
    })
    
    print(f"  -> 判定結果: {platform}\n")
    time.sleep(2) # 連続アクセスで相手サーバーに負荷をかけないための待機

# 4. 結果をCSVに保存
df = pd.DataFrame(results)
df.to_csv("shop_platform_list.csv", index=False, encoding="utf-8-sig")

print("-" * 40)
print(f"✅ 完了しました！結果を shop_platform_list.csv に保存しました。")