import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

print("测试 WordCloud 与背景图片的兼容性...")

try:
    # 读取背景图片
    mask_img = np.array(Image.open('china.jpg'))
    print('✓ 背景图片加载成功，形状:', mask_img.shape)

    # 尝试创建一个简单的词云（无字体）
    text = 'test word cloud hello world'
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
    plt.savefig('test_wordcloud_with_mask.jpg', dpi=300, bbox_inches='tight')
    print('✓ 词云图已保存为 test_wordcloud_with_mask.jpg')
    plt.show()

except Exception as e:
    print(f'✗ 使用背景图片失败: {e}')
    
    # 尝试不使用背景图片
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
        plt.savefig('test_wordcloud_without_mask.jpg', dpi=300, bbox_inches='tight')
        print('✓ 词云图已保存为 test_wordcloud_without_mask.jpg')
        plt.show()
        
    except Exception as e2:
        print(f'✗ 基本词云也失败: {e2}')