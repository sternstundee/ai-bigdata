import random


def guess_number_game():
    # 1. 输入玩家信息
    player_name = input("您的大名是？").strip()
    print(f"您好，{player_name}！我们来玩儿猜数字游戏吧！")

    # 2. 输入数字范围（确保最小值<最大值）
    while True:
        try:
            min_num = int(input("请输入一个最小值："))
            max_num = int(input("再输入一个最大值："))
            if min_num >= max_num:
                print("❌ 最小值必须小于最大值，请重新输入！")
                continue
            break
        except ValueError:
            print("❌ 输入错误！请输入整数。")

    # 3. 生成随机目标数字
    target = random.randint(min_num, max_num)
    max_attempts = 5  # 最大尝试次数
    attempt_count = 0  # 已尝试次数
    print(f"🎮 猜数字游戏开始！（共{max_attempts}次机会，范围：{min_num}~{max_num}）")

    # 4. 猜数字循环
    while attempt_count < max_attempts:
        try:
            guess = int(input("请输入你猜的数字："))
            attempt_count += 1  # 次数+1

            # 判断猜的结果
            if guess == target:
                print(f"🎉 恭喜，您猜对了！这是您第{attempt_count}次尝试！")
                print("游戏结束，再见！")
                return
            elif guess < target:
                print(f"⚠️  您输入的数字小了！这是您第{attempt_count}次尝试！")
            else:
                print(f"⚠️  您输入的数字大了！这是您第{attempt_count}次尝试！")

        except ValueError:
            print("❌ 输入错误！请输入整数。")

    # 5. 次数用尽
    print(f"😢 很遗憾，{max_attempts}次机会已用尽，游戏结束，答案为{target}")


# 启动游戏
guess_number_game()