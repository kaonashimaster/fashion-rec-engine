import pandas as pd
import matplotlib.pyplot as plt

# Windowsでグラフの日本語が文字化けしないための設定
plt.rcParams['font.family'] = 'Meiryo'

# 1. データの読み込み
df = pd.read_csv("base_items_tops.csv")

# 2. グラフの設定（ヒストグラム）
plt.figure(figsize=(10, 6)) # グラフのサイズ
plt.hist(df['価格'], bins=8, color='royalblue', edgecolor='black', alpha=0.7)

# 3. タイトルとラベルの追加
plt.title("BASE某ショップ：トップスの価格帯分布", fontsize=16, fontweight='bold')
plt.xlabel("価格 (円)", fontsize=14)
plt.ylabel("商品数", fontsize=14)

# 4. 平均値の線を引く（統計学徒らしいワンポイント！）
mean_price = df['価格'].mean()
plt.axvline(mean_price, color='red', linestyle='dashed', linewidth=2, label=f'平均価格: ¥{mean_price:.0f}')
plt.legend()

# 見やすくするためのグリッド線
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 5. 画像として保存して画面に表示
plt.savefig("price_histogram.png", dpi=300, bbox_inches='tight')
print("グラフを 'price_histogram.png' として保存しました！")
plt.show() # 画面にもポップアップで表示されます