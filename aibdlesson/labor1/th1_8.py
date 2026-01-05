1# 思考题实例2：成绩统计（基于给定字典）
# 原始成绩字典
dic_score = {
    "张三": [88,  90,  98,  95],
    "李四": [85,  92,  95,  98],
    "王五": [89,  89,  90,  92],
    "丁六": [82,  86,  89,  90]
}

# 1. 统计每名学生的平均分和最高分，添加到列表中
print("1. 添加平均分和最高分后的字典：")
for name, scores in dic_score.items():
    avg = sum(scores) / len(scores)  # 平均分
    max_s = max(scores)             # 最高分
    scores.append(round(avg, 2))    # 保留2位小数添加到列表
    scores.append(max_s)
    print(f"   {name}：{scores}")

# 2. 转化为嵌套列表（含表头）
nested_score = [["姓名", "语文", "数学", "英语", "计算机", "平均分", "最高分"]]
for name, scores in dic_score.items():
    nested_score.append([name] + scores)  # 姓名+成绩拼接
print(f"\n2. 嵌套列表：")
for row in nested_score:
    print(f"   {row}")

# 3. 计算每门课的最高分，添加到列表并格式化输出表格
# 提取每门课的成绩（语文：索引1，数学：2，英语：3，计算机：4，平均分：5，最高分：6）
chinese = [row[1] for row in nested_score[1:]]  # 跳过表头
math = [row[2] for row in nested_score[1:]]
english = [row[3] for row in nested_score[1:]]
computer = [row[4] for row in nested_score[1:]]
avg_all = [row[5] for row in nested_score[1:]]
max_all = [row[6] for row in nested_score[1:]]

# 计算每门课的最高分
max_row = [
    "最高分",
    max(chinese),
    max(math),
    max(english),
    max(computer),
    max(avg_all),
    max(max_all)
]
nested_score.append(max_row)  # 添加最高分一行

# 格式化输出表格（左对齐，固定宽度）
print(f"\n3. 成绩统计表格：")
# 设置每列的宽度，使表头和数据对齐
format_line = "{:<8} {:<6} {:<6} {:<6} {:<8} {:<8} {:<6}"
print(format_line.format(*nested_score[0]))  # 表头
for row in nested_score[1:]:
    # 格式化数据（整数转int，平均分保留2位）
    formatted = [
        row[0],
        int(row[1]),
        int(row[2]),
        int(row[3]),
        int(row[4]),
        row[5],
        int(row[6])
    ]
    print(format_line.format(*formatted))