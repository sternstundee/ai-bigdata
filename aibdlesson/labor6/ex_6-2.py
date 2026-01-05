import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os

# ===================== 1. 配置中文显示 =====================
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ===================== 2. 读取本地iris.data文件（适配带表头格式） =====================
iris_file = "iris.data"  # 需放在代码同级目录
if not os.path.exists(iris_file):
    print(f"❌ 未找到文件：{iris_file}，请确认文件在同级目录！")
    exit()

# 读取iris.data（关键修正：有表头，header=0）
try:
    # 表头为：花萼长度,花萼宽度,花瓣长度,花瓣宽度,种类
    col_names = ["花萼长度", "花萼宽度", "花瓣长度", "花瓣宽度", "种类"]
    df_iris = pd.read_csv(
        iris_file,
        encoding="utf-8",
        header=0,  # 第一行是表头，不是数据
        names=col_names,  # 显式指定列名，确保匹配
        sep=","  # 逗号分隔
    )

    # 过滤无效数据
    df_iris = df_iris.dropna()
    # 验证数值列是否为数值型
    numeric_cols = ["花萼长度", "花萼宽度", "花瓣长度", "花瓣宽度"]
    for col in numeric_cols:
        df_iris[col] = pd.to_numeric(df_iris[col], errors="coerce")
    df_iris = df_iris.dropna(subset=numeric_cols)

    print(f"✅ 成功读取{iris_file}：共{len(df_iris)}个有效样本")
    print("\n📊 鸢尾花数据前5行：")
    print(df_iris.head())

    # 映射种类名称为中文（适配你的文件中"种类"列）
    df_iris["类别名称"] = df_iris["种类"].map({
        "Iris-setosa": "山鸢尾",
        "Iris-versicolor": "变色鸢尾",
        "Iris-virginica": "维吉尼亚鸢尾"
    })
    print(f"\n✅ 类别分布：\n{df_iris['类别名称'].value_counts()}")

except Exception as e:
    print(f"❌ 读取iris.data失败：{e}")
    exit()

# ===================== 3. 数据预处理 =====================
# 选择聚类特征（花萼长度+花萼宽度，可改为花瓣特征）
X = df_iris[["花萼长度", "花萼宽度"]].astype(float).values
print(f"\n✅ 特征矩阵形状：{X.shape}")

# ===================== 4. K-means聚类建模 =====================
k = 3  # 鸢尾花真实类别数为3
kmeans = KMeans(n_clusters=k, random_state=42)
cluster_labels = kmeans.fit_predict(X)

# 添加聚类标签
df_iris["聚类标签"] = cluster_labels
print(f"\n✅ 聚类完成，共分为{k}个类别")

# ===================== 5. 聚类结果可视化 =====================
plt.figure(figsize=(10, 6))

# 绘制聚类散点
colors = ["#E74C3C", "#2ECC71", "#3498DB"]
markers = ["o", "s", "^"]

for i in range(k):
    cluster_data = df_iris[df_iris["聚类标签"] == i]
    plt.scatter(
        cluster_data["花萼长度"], cluster_data["花萼宽度"],
        c=colors[i], marker=markers[i], s=80, alpha=0.8, label=f"聚类{i + 1}"
    )

# 图表美化（符合实验报告格式）
plt.title("鸢尾花按花萼特征K-means聚类图--来自136-舒文璨", fontsize=16, pad=20)
plt.xlabel("花萼长度（cm）", fontsize=14)
plt.ylabel("花萼宽度（cm）", fontsize=14)
plt.legend(loc="best", fontsize=12)
plt.grid(True, alpha=0.3, linestyle="--")
plt.tight_layout()

# 保存图表
plt.savefig("136_鸢尾花聚类图.png", dpi=300, bbox_inches="tight")
print("\n✅ 聚类图已保存为：136_鸢尾花聚类图.png")

# 显示图表
plt.show()

# （可选）输出聚类与真实类别的对应关系（实验报告分析用）
print("\n📋 聚类标签与真实类别对应关系：")
cross_tab = pd.crosstab(df_iris["聚类标签"], df_iris["类别名称"])
print(cross_tab)