# 实例4：计算三角形面积（输入三边，先判断是否为有效三角形）
import math  # 导入数学模块，用于开平方

try:
    # 输入三边（替换为自己的数值，如3、4、5）
    a = float(input("请输入三角形第一条边长："))
    b = float(input("请输入三角形第二条边长："))
    c = float(input("请输入三角形第三条边长："))
except ValueError:
    print("❌ 输入错误！请输入有效的数字。")
else:
    # 判断是否能构成三角形（两边之和>第三边，且边长>0）
    if a > 0 and b > 0 and c > 0 and (a+b > c) and (a+c > b) and (b+c > a):
        p = (a + b + c) / 2  # 半周长
        area = math.sqrt(p * (p - a) * (p - b) * (p - c))  # 海伦公式
        print(f"\n✅ 三角形面积为：{area:.2f}（单位：平方单位）")
    else:
        print("\n❌ 输入的三边无法构成有效三角形！")