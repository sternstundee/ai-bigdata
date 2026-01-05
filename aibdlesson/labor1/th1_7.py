# 思考题实例1：嵌套列表（替换X=班号，YY=学号，如班号2、学号18→X=2，YY=18）
# 1. 定义嵌套列表（规则：以学号为中心，前后各4个数字，分3行）
# 示例：班号1（X=1），学号36（YY=36）→ 中心18，前后4个：14,15,16,17,18,19,20,21,22
# 第一行（最小3个）：14,15,16（顺序随意）；第二行（中间3个）：17,18,19；第三行（最大3个）：20,21,22
nested_list_136 = [[16, 14, 15], [19, 17, 18], [22, 20, 21]]  # 替换为自己的班号学号
print(f"1. 原始嵌套列表（nested_list_218）：{nested_list_136}")

# 2. 每行升序排序
sorted_nested = [sorted(row) for row in nested_list_136]
print(f"2. 每行升序排序后：{sorted_nested}")

# 3. 压平为非嵌套列表，遍历输出
list_218 = [num for row in sorted_nested for num in row]  # 列表推导式压平
print(f"3. 压平后的列表（list_218）：{list_218}")
print("   遍历输出压平列表：", end="")
for num in list_218:
    print(f" {num}", end="")