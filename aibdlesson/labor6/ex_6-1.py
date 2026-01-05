import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os

# ===================== 1. 配置中文显示 =====================
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 黑体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示

# ===================== 2. 读取本地China_cities.csv文件 =====================
csv_file = "China_cities.csv"  # 需放在代码同级目录
# 验证文件是否存在
if not os.path.exists(csv_file):
    print(f"❌ 未找到文件：{csv_file}，请确认文件在同级目录！")
    exit()

# 读取CSV（自动适配常见列名，兼容不同格式）
try:
    # 尝试常见列名组合（纬度/北纬/lat，经度/东经/lng）
    df_cities = pd.read_csv(csv_file, encoding="utf-8-sig")
    # 统一列名（适配不同CSV格式）
    col_mapping = {
        "纬度": "北纬", "lat": "北纬", "Latitude": "北纬",
        "经度": "东经", "lng": "东经", "Longitude": "东经",
        "城市名": "城市", "name": "城市"
    }
    df_cities.rename(columns=col_mapping, inplace=True)

    # 检查核心列是否存在
    required_cols = ["城市", "北纬", "东经"]
    missing_cols = [col for col in required_cols if col not in df_cities.columns]
    if missing_cols:
        print(f"❌ CSV文件缺少核心列：{missing_cols}")
        print(f"当前文件列名：{df_cities.columns.tolist()}")
        exit()

    # 过滤无效数据（去除空值、非数值经纬度）
    df_cities = df_cities.dropna(subset=["北纬", "东经"])
    df_cities = df_cities[pd.to_numeric(df_cities["北纬"], errors="coerce").notna()]
    df_cities = df_cities[pd.to_numeric(df_cities["东经"], errors="coerce").notna()]

    print(f"✅ 成功读取{csv_file}：共{len(df_cities)}个有效城市数据")
    print("\n📊 城市数据前5行：")
    print(df_cities[["城市", "北纬", "东经"]].head())

except Exception as e:
    print(f"❌ 读取CSV失败：{e}")
    exit()

# ===================== 3. 数据预处理 =====================
# 提取聚类特征（北纬、东经转为数值型）
X = df_cities[["北纬", "东经"]].astype(float).values
print(f"\n✅ 特征矩阵形状：{X.shape}（{X.shape[0]}个样本，{X.shape[1]}个特征）")

# ===================== 4. K-means聚类建模 =====================
k = 4  # 按中国地理分区聚类（可根据需求调整）
kmeans = KMeans(n_clusters=k, random_state=42)  # random_state确保结果可复现
cluster_labels = kmeans.fit_predict(X)

# 添加聚类标签到数据框
df_cities["聚类标签"] = cluster_labels
print(f"\n✅ 聚类完成，共分为{k}个类别")

# 输出各聚类包含的城市（便于实验报告分析）
print("\n📋 各聚类包含的城市：")
for i in range(k):
    cluster_cities = df_cities[df_cities["聚类标签"] == i]["城市"].tolist()
    # 最多显示10个城市，避免输出过长
    show_cities = cluster_cities[:10] if len(cluster_cities) > 10 else cluster_cities
    print(f"类别{i + 1}（共{len(cluster_cities)}个）：{', '.join(show_cities)}{'...' if len(cluster_cities) > 10 else ''}")

# ===================== 5. 聚类结果可视化 =====================
plt.figure(figsize=(12, 8))

# 绘制不同聚类的散点（4种颜色/标记）
colors = ["#E74C3C", "#2ECC71", "#3498DB", "#F39C12"]
markers = ["o", "s", "^", "D"]

for i in range(k):
    cluster_data = df_cities[df_cities["聚类标签"] == i]
    plt.scatter(
        cluster_data["东经"], cluster_data["北纬"],
        c=colors[i], marker=markers[i], s=80, alpha=0.8, label=f"聚类{i + 1}"
    )

# 标注主要城市（前20个，避免重叠）
top_cities = df_cities.head(20)
for idx, row in top_cities.iterrows():
    plt.annotate(
        row["城市"], xy=(row["东经"], row["北纬"]),
        xytext=(5, 5), textcoords="offset points",
        fontsize=9, alpha=0.9
    )

# 图表美化
plt.title("中国城市经纬度K-means聚类图", fontsize=16, pad=20)
plt.xlabel("东经（°）", fontsize=14)
plt.ylabel("北纬（°）", fontsize=14)
plt.legend(loc="best", fontsize=12)
plt.grid(True, alpha=0.3, linestyle="--")
plt.tight_layout()

# 保存图表（可选，便于实验报告提交）
plt.savefig("136_城市聚类图.png", dpi=300, bbox_inches="tight")
print("\n✅ 聚类图已保存为：136_城市聚类图.png")

# 显示图表
plt.show()