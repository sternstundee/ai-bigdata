# 实例5：列表操作（5个城市，第一个为家乡）
# 1. 输入5个城市（第一个为家乡，用空格分隔，如“北京 上海 广州 深圳 成都”）
while True:
    cities_input = input("请输入5个城市的名字，用空格分隔（第一个为家乡）：")
    cities = cities_input.split()
    if len(cities) == 5:
        break
    print("❌ 城市数量不是5个，请重新输入！")
hometown = cities[0]  # 家乡（第一个元素）
print(f"\n1. 原始城市列表：{cities}")

# 2. for循环遍历输出
print("\n2. 遍历输出城市：")
for idx, city in enumerate(cities, 1):
    print(f"   第{idx}个城市：{city}")

# 3. 索引输出家乡，切片输出其他城市
print(f"\n3. 家乡城市（索引0）：{cities[0]}")
print(f"   其他城市（切片1:）：{cities[1:]}")

# 4. 逆序输出（两种方法，不改变原列表）
# 方法一：切片法
reverse1 = cities[::-1]
# 方法二：copy后用reverse()
reverse2 = cities.copy()
reverse2.reverse()
print(f"\n4. 逆序方法一（切片）：{reverse1}")
print(f"   逆序方法二（reverse()）：{reverse2}")

# 5. 降序排序（两种方法）
# 方法一：sorted()（不改变原列表）
sorted1 = sorted(cities, reverse=True)
# 方法二：copy后用sort()（改变复制后的列表）
sorted2 = cities.copy()
sorted2.sort(reverse=True)
print(f"\n5. 降序方法一（sorted()）：{sorted1}")
print(f"   降序方法二（sort()）：{sorted2}")

# 6. 输出家乡在排序后列表的前后城市（用index()找索引）
hometown_idx = sorted1.index(hometown)
print(f"\n6. 排序后家乡「{hometown}」的位置索引：{hometown_idx}")
if hometown_idx > 0:
    print(f"   家乡前面的城市：{sorted1[hometown_idx-1]}")
else:
    print("   家乡前面没有城市（位于第一个）")
if hometown_idx < 4:
    print(f"   家乡后面的城市：{sorted1[hometown_idx+1]}")
else:
    print("   家乡后面没有城市（位于最后一个）")

# 7. 修改家乡前后的城市（用index()定位）
sorted_modify = sorted1.copy()  # 复制排序后的列表，避免修改原列表
if hometown_idx > 0:
    sorted_modify[hometown_idx-1] = "天津"  # 修改前面的城市（自定义）
if hometown_idx < 4:
    sorted_modify[hometown_idx+1] = "杭州"  # 修改后面的城市（自定义）
print(f"\n7. 修改后的列表：{sorted_modify}")

# 8. 删除修改后的城市（先删后面，避免索引混乱）
sorted_delete = sorted_modify.copy()
# 先删后面的城市（索引大，删除后不影响前面）
if hometown_idx < len(sorted_delete)-1:
    deleted_back = sorted_delete.pop(hometown_idx+1)
    print(f"   删除的后面城市：{deleted_back}")
# 再删前面的城市
if hometown_idx > 0:
    deleted_front = sorted_delete.pop(hometown_idx-1)
    print(f"   删除的前面城市：{deleted_front}")
print(f"8. 最终剩余城市：{sorted_delete}")