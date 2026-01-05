# 实例2：四则运算（输入两个不同浮点数，处理除数为0和输入错误）
try:
    # 输入两个浮点数（替换为自己的数值，如3.5和2.2）
    num1 = float(input("请输入第一个浮点型运算数："))
    num2 = float(input("请输入第二个浮点型运算数："))
except ValueError:
    print("❌ 输入错误！请输入有效的数字（如5.0、3.2）。")
else:
    # 1. 和：%f占位符（保留2位小数）
    sum_result = num1 + num2
    print(f"\n1. {num1:.2f}与{num2:.2f}的和为：%.2f" % sum_result)

    # 2. 差：%d占位符（自动转为整数）
    diff_result = num1 - num2
    print(f"2. {num1:.0f}与{num2:.0f}的差为：%d" % int(diff_result))

    # 3. 积：format()方法
    product_result = num1 * num2
    print(f"3. {num1:.2f}与{num2:.2f}的积为：{product_result:.2f}".format())

    # 4. 商：f-strings（处理除数为0）
    if num2 != 0:
        quotient_result = num1 / num2
        print(f"4. {num1:.2f}与{num2:.2f}的商为：{quotient_result:.2f}")
    else:
        print("4. ❌ 除数不能为0，无法计算商！")