# 导入所需库
import jieba  # 分词模块
import matplotlib.pyplot as plt  # 画图模块
from wordcloud import WordCloud  # 文字云模块
import imageio  # 处理图像的函数，读取背景图片
import os

# 检查文件是否存在
print("检查文件是否存在...")
print("当前目录:", os.getcwd())
print("文件列表:", os.listdir('.'))

# 1. 读取个人信息文本文件
try:
    wf = 'per_info.txt'
    word_content = open(wf, 'r', encoding='utf-8').read().replace('\n', '')
    print(f"成功读取个人信息文件: {wf}")
    print(f"文本内容预览: {word_content[:50]}...")
except FileNotFoundError:
    print(f"错误: 找不到文件 {wf}")
    print("请创建 per_info.txt 文件，内容格式如下：")
    print("张三 Python编程 篮球 旅游 电影 音乐 北京 清华大学 软件工程")
    # 创建示例文件
    with open('per_info.txt', 'w', encoding='utf-8') as f:
        f.write("张三 Python编程 篮球 旅游 电影 音乐 北京 清华大学 软件工程")
    word_content = "张三 Python编程 篮球 旅游 电影 音乐 北京 清华大学 软件工程"

# 2. 设置背景图片（实验要求使用 china.jpg）
img_file = 'china.jpg'  # 设置背景图片
try:
    mask_img = imageio.imread(img_file)  # 解析背景图片
    print(f"成功读取背景图片: {img_file}")
    print(f"图片尺寸: {mask_img.shape}")
except FileNotFoundError:
    print(f"错误: 找不到背景图片 {img_file}")
    print("请确保 'china.jpg' 图片在当前目录中")
    print("可以从网上下载一张中国地图的图片，命名为 china.jpg")
    exit(1)  # 退出程序，因为没有背景图片无法完成实验

# 3. 进行分词处理
print("开始分词处理...")
word_cut = jieba.cut(word_content)  # 进行分词
word_cut_join = " ".join(word_cut)  # 把分词用空格连起来（实验要求）
print(f"分词结果: {word_cut_join}")

# 4. 设置中文字体路径
font_path = None
# 尝试常见的中文字体路径
possible_fonts = [
    'C:/Windows/Fonts/simhei.ttf',  # Windows 黑体
    'C:/Windows/Fonts/msyh.ttc',    # Windows 微软雅黑
    'STXINGKA.ttf',                 # 当前目录字体
    '/System/Library/Fonts/PingFang.ttc',  # Mac 苹方字体
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'  # Linux 文泉驿
]

for font in possible_fonts:
    if os.path.exists(font):
        font_path = font
        print(f"使用字体: {font}")
        break

if font_path is None:
    print("警告: 未找到中文字体，可能显示乱码")
    font_path = 'simhei.ttf'  # 使用一个可能不存在的字体名

# 5. 创建词云对象（按照实验要求配置）
print("正在生成词云...")
wc = WordCloud(
    font_path=font_path,      # 设置中文字体
    mask=mask_img,           # 使用的背景图片（必须要有）
    width=800,               # 宽度
    height=600,              # 高度
    background_color='white', # 背景颜色
    max_words=200,           # 最大词数
    max_font_size=100,       # 最大字体大小
    min_font_size=10,        # 最小字体大小
    contour_width=1,         # 轮廓宽度
    contour_color='steelblue' # 轮廓颜色
)

# 6. 生成词云（修正实验示例中的错误：应该是generate，不是wc_generate）
wc.generate(word_cut_join)

# 7. 显示和保存词云图
plt.figure(figsize=(12, 8))  # 设置画布大小
plt.imshow(wc, interpolation='bilinear')  # 显示图片
plt.axis('off')  # 去掉坐标轴

# 设置标题（使用中文字体）
plt.title('个人简历信息词云图', fontsize=16, fontproperties='SimHei')

# 保存图片（按照实验要求格式）
output_file = 'resume_wordcloud.jpg'  # 可以改为实验示例中的 '09-你的名字.jpg'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"词云图已保存为: {output_file}")

# 显示图片
plt.show()

print("词云生成完成！")