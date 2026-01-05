# 实例6：字典操作（国家-首都查询，处理大小写）
# 定义国家-首都字典
dic_country = {
    "China": "Beijing",
    "America": "Washington",
    "Norway": "Oslo",
    "Japan": "Tokyo",
    "Germany": "Berlin",
    "Canada": "Ottawa",
    "France": "Paris",
    "Thailand": "Bangkok"
}

# 输入国家名，处理大小写（如输入“china”自动转为“China”）
country_input = input("请输入国家名（如China、America）：").strip().title()

# 判断是否存在并输出
if country_input in dic_country:
    # 用format()输出首都
    print("首都名：{}".format(dic_country[country_input]))
else:
    print("未查询到该国家名！")