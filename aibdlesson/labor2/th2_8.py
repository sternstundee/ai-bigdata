def write_poem_to_txt():
    # 1. 定义唐诗（每个同学需选择不同诗词，示例：王维《山居秋暝》）
    poem = {
        "title": "山居秋暝",
        "author": "王维",
        "lines": ["空山新雨后，天气晚来秋。", "明月松间照，清泉石上流。", "竹喧归浣女，莲动下渔舟。",
                  "随意春芳歇，王孙自可留。"]
    }

    # 2. 文件名（替换为自己的学号+姓名，如“01-张三思考题2.txt”）
    txt_filename = "2022214736-舒文璨思考题2.txt"

    try:
        # 3. 写入txt文件（with语句自动关闭文件，每行居中）
        with open(txt_filename, "w", encoding="utf-8") as f:
            # 标题、作者、诗句均居中（宽度50字符，空格填充）
            f.write(poem["title"].center(50) + "\n")
            f.write(poem["author"].center(50) + "\n")
            for line in poem["lines"]:
                f.write(line.center(50) + "\n")
        print(f"✅ 唐诗已成功写入 {txt_filename}！")

    except Exception as e:
        print(f"❌ 写入文件失败：{str(e)}")
        return


def read_poem_from_txt():
    # 文件名（与写入时一致）
    txt_filename = "2022214736-舒文璨思考题2.txt"

    try:
        print("\n" + "=" * 50)
        print("1. 用read()函数读取（读取全部内容）：")
        print("=" * 50)
        with open(txt_filename, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)

        print("=" * 50)
        print("2. 用readlines()函数读取（按行读取为列表）：")
        print("=" * 50)
        with open(txt_filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for idx, line in enumerate(lines, 1):
                print(f"第{idx}行：{line.strip()}")  # strip()去除换行符

        print("=" * 50)
        print("3. 用for循环读取（逐行迭代）：")
        print("=" * 50)
        with open(txt_filename, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                print(f"第{idx}行：{line.strip()}")

        # 输出诗的第一句（lines[2]：第1行标题，第2行作者，第3行第一句）
        print("=" * 50)
        with open(txt_filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            first_line = lines[2].strip()  # 第一句诗句
            print(f"📜 诗的第一句：{first_line}")
        print("=" * 50)

    except FileNotFoundError:
        print(f"❌ 未找到文件 {txt_filename}，请先运行写入程序！")
    except Exception as e:
        print(f"❌ 读取文件失败：{str(e)}")


# 先写入唐诗，再读取并输出
write_poem_to_txt()
read_poem_from_txt()