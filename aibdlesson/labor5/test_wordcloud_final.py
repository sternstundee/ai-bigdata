import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

print("测试 WordCloud 与背景图片的兼容性（完全隔离环境）...")

# 重置matplotlib配置
plt.rcParams.update(plt.rcParamsDefault)

try:
    # 读取背景图片
    mask_img = np.array(Image.open('china.jpg'))
    print('✓ 背景图片加载成功，形状:', mask_img.shape)

    # 创建一个简单的测试文本
    text = 'Hello World Python WordCloud Test'
    
    # 创建WordCloud对象，不指定任何字体
    print("尝试创建带背景图片的词云（无字体）...")
    wc = WordCloud(
        width=800,
        height=600,
        background_color='white',
        max_words=200,
        max_font_size=150,
        min_font_size=10,
        collocations=False,
        scale=2,
        mask=mask_img
    )
    wc.generate(text)

    print('✓ 词云生成成功！')
    
    # 显示和保存词云图
    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('测试词云 - 带背景图片')
    plt.savefig('test_final_wordcloud.jpg', dpi=300, bbox_inches='tight')
    print('✓ 词云图已保存为 test_final_wordcloud.jpg')
    plt.show()

except Exception as e:
    print(f'✗ 使用背景图片失败: {e}')
    
    # 尝试创建没有mask的词云
    try:
        print("尝试创建不带背景图片的词云...")
        wc = WordCloud(
            width=800,
            height=600,
            background_color='white',
            max_words=200,
            max_font_size=150,
            min_font_size=10,
            collocations=False,
            scale=2
        )
        wc.generate(text)

        print('✓ 无背景图片的词云生成成功！')
        
        # 显示和保存词云图
        plt.figure(figsize=(12, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title('测试词云 - 无背景图片')
        plt.savefig('test_final_wordcloud_no_mask.jpg', dpi=300, bbox_inches='tight')
        print('✓ 词云图已保存为 test_final_wordcloud_no_mask.jpg')
        plt.show()
        
    except Exception as e2:
        print(f'✗ 基本词云也失败: {e2}')
        print("WordCloud库可能存在严重兼容性问题")