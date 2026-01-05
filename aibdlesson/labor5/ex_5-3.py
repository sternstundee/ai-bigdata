import jieba
import matplotlib.pyplot as plt

# ===================== 1. 配置参数 =====================
# 政府工作报告文本文件
report_file = "govreport-2022.txt"
# 需过滤的标点符号（根据文本实际情况补充）
punctuations = [",", "!", "“", "”", "。", "?", ":", "...", "、", ";", "（", "）", "【", "】"]

# ===================== 2. 读取并处理文本 =====================
try:
    # 读取文本，去除换行符
    with open(report_file, "r", encoding="utf-8") as f:
        word_content = f.read().replace("\n", "").strip()
    print(f"✅ 成功读取政府工作报告：{report_file}")
except FileNotFoundError:
    print(f"❌ 未找到文本文件 {report_file}，请检查路径！")
    exit()

# 分词处理
word_cut = jieba.cut(word_content)

# ===================== 3. 统计词频（过滤标点和单字）=====================
word_counts = {}
for word in word_cut:
    # 去除标点符号
    for p in punctuations:
        word = word.replace(p, "").strip()
    # 过滤单字和空字符串（无实际意义）
    if len(word) == 1 or word == "":
        continue
    # 统计词频（不存在则初始为0，存在则+1）
    word_counts[word] = word_counts.get(word, 0) + 1

# ===================== 4. 筛选前5高频词 =====================
# 按词频降序排序（items()转换为元组列表，key取词频，reverse=True降序）
sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
top5_words = sorted_words[:5]  # 取前5个

# 分离词语和对应次数（用于柱状图x/y轴）
words = [item[0] for item in top5_words]
counts = [item[1] for item in top5_words]

print("\n📊 2022年政府工作报告前5高频词：")
for idx, (word, count) in enumerate(top5_words, 1):
    print(f"{idx}. {word}：{count}次")

# ===================== 5. 绘制柱状图 =====================
# 中文显示配置
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 创建图表（宽10，高6，适合展示5个类别）
plt.figure(figsize=(10, 6))

# 绘制柱状图（蓝色，宽度0.6）
bars = plt.bar(words, counts, width=0.6, color="#2E86AB")

# 图表美化
plt.title("WordCount(词频统计)", fontsize=18, pad=20)
plt.xlabel("单词名称", fontsize=14)
plt.ylabel("出现次数", fontsize=14)
plt.tick_params(labelsize=12)  # 刻度字号

# 在柱子顶部显示具体次数（增强可读性）
for bar, count in zip(bars, counts):
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2., height + 1,
        str(count), ha="center", va="bottom", fontsize=12
    )

# 自动调整布局
plt.tight_layout()

# 显示图表
plt.show()