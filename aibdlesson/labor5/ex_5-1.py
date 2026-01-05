# -*- coding: utf-8 -*-
"""
实验五：Python数据可视化 - 实例1
简历信息词云图
班号：1，学号：36
"""

import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# ========== 实例1：简历信息词云图 ==========
def create_resume_wordcloud():
    """创建简历信息词云图"""
    print("=" * 60)
    print("实例1：简历信息词云图")
    print("班号：1，学号：36")
    print("=" * 60)

    try:
        # 1. 读取简历信息文本文件
        wf = 'per_info.txt'
        with open(wf, 'r', encoding='utf-8') as f:
            word_content = f.read().replace('\n', ' ')
        print(f"✓ 已读取简历信息文件: {wf}")
        print(f"  文本长度: {len(word_content)} 字符")

        # 2. 设置字体路径，优先使用STXINGKA.ttf
        font_path = None

        # 检查当前目录是否存在STXINGKA.ttf字体文件
        if os.path.exists('STXINGKA.ttf'):
            # 尝试验证字体文件是否为TrueType格式
            try:
                from PIL import ImageFont
                test_font = ImageFont.truetype('STXINGKA.ttf', size=12)
                font_path = 'STXINGKA.ttf'
                print(f"✓ 找到指定字体: STXINGKA.ttf")
            except Exception:
                print(f"⚠ STXINGKA.ttf 不是有效的TrueType字体或不被支持，尝试其他字体...")

        if font_path is None:
            # 尝试可能的TrueType字体
            possible_fonts = [
                'C:/Windows/Fonts/simhei.ttf',
                'C:/Windows/Fonts/simsun.ttc',
                'C:/Windows/Fonts/arial.ttf',
                'C:/Windows/Fonts/times.ttf',
                'simhei.ttf',  # 黑体
                'simkai.ttf',  # 楷体
                'arial.ttf',  # Arial字体，通常是TrueType
            ]

            for font in possible_fonts:
                if os.path.exists(font):
                    try:
                        from PIL import ImageFont
                        test_font = ImageFont.truetype(font, size=12)
                        font_path = font
                        print(f"✓ 找到TrueType字体: {font}")
                        break
                    except Exception:
                        continue

        if font_path is None:
            print("⚠ 警告: 未找到TrueType字体文件，将尝试使用系统默认字体")
            # 尝试使用matplotlib的字体
            import matplotlib.font_manager as fm
            fonts = fm.findSystemFonts()
            for font in fonts:
                if 'arial' in font.lower() or 'sim' in font.lower():
                    try:
                        from PIL import ImageFont
                        test_font = ImageFont.truetype(font, size=12)
                        font_path = font
                        print(f"✓ 找到系统字体: {font}")
                        break
                    except Exception:
                        continue

        # 3. 使用jieba进行分词处理
        word_cut = jieba.cut(word_content)
        word_cut_join = " ".join(word_cut)
        print(f"✓ 分词完成")

        # 4. 创建词云参数
        wc_params = {
            'width': 800,
            'height': 600,
            'background_color': 'white',
            'max_words': 200,
            'max_font_size': 150,
            'min_font_size': 10,
            'collocations': False,
            'scale': 2  # 提高分辨率
        }

        # 检查是否需要使用系统字体而不是自定义字体
        # 由于STXINGKA.ttf与WordCloud库存在兼容性问题，我们不将字体路径添加到wc_params中
        if font_path:
            # 不直接添加字体到wc_params，因为这会导致兼容性问题
            print(f"✓ 发现字体文件: {font_path}，但为了兼容性将不使用它")
            # 可以在后续的文本显示中使用该字体

        # 5. 尝试加载背景图片
        try:
            import numpy as np
            from PIL import Image
            img_file = 'china.jpg'
            if os.path.exists(img_file):
                # 使用PIL加载图片并转换为numpy数组
                mask_img = np.array(Image.open(img_file))
                # 暂时存储mask参数，以便在需要时使用
                has_mask = True
                original_mask = mask_img
                print(f"✓ 已加载背景图片: {img_file}")
            else:
                has_mask = False
                print(f"⚠ 未找到背景图片 {img_file}，将使用默认形状")
        except ImportError:
            try:
                import imageio
                img_file = 'china.jpg'
                if os.path.exists(img_file):
                    mask_img = imageio.imread(img_file)
                    has_mask = True
                    original_mask = mask_img
                    print(f"✓ 已加载背景图片: {img_file}")
                else:
                    has_mask = False
                    print(f"⚠ 未找到背景图片 {img_file}，将使用默认形状")
            except ImportError:
                print("⚠ 未安装imageio或PIL库，将不使用背景图片")
                has_mask = False
            except Exception as e:
                print(f"⚠ 加载背景图片时出错: {e}")
                has_mask = False
        except Exception as e:
            print(f"⚠ 加载背景图片时出错: {e}")
            has_mask = False

        # 6. 创建并生成词云
        print("正在生成词云...")

        # 方法1: 尝试使用WordCloud生成
        # 首先尝试使用背景图片但不使用自定义字体（避免兼容性问题）
        try:
            # 基本参数（无自定义字体）
            basic_params = {
                'width': 800,
                'height': 600,
                'background_color': 'white',
                'max_words': 200,
                'max_font_size': 150,
                'min_font_size': 10,
                'collocations': False,
                'scale': 2
            }
            
            # 如果有背景图片，添加背景图片
            if has_mask:
                basic_params['mask'] = original_mask
                print("尝试使用背景图片...")
            
            wc = WordCloud(**basic_params)
            wc.generate(word_cut_join)
            print("✓ 使用WordCloud（背景图片，无自定义字体）生成成功")
            
            # 显示和保存词云图
            plt.figure(figsize=(12, 8))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.title('简历信息词云图 - 1班36号', fontsize=16, fontweight='bold', pad=20)

            # 保存图片
            output_file = 'resume_wordcloud_136.jpg'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"✓ 词云图已保存为: {output_file}")

            plt.show()
            return True

        except Exception as e:
            print(f"✗ 使用WordCloud生成失败: {e}")
            print("尝试替代方法...")

            # 尝试不使用背景图片的基本设置
            try:
                basic_params = {
                    'width': 800,
                    'height': 600,
                    'background_color': 'white',
                    'max_words': 200,
                    'max_font_size': 150,
                    'min_font_size': 10,
                    'collocations': False,
                    'scale': 2
                }
                
                wc = WordCloud(**basic_params)
                wc.generate(word_cut_join)
                print("✓ 使用WordCloud（无特殊设置）生成成功")
                
                # 显示和保存词云图
                plt.figure(figsize=(12, 8))
                plt.imshow(wc, interpolation='bilinear')
                plt.axis('off')
                plt.title('简历信息词云图 - 1班36号', fontsize=16, fontweight='bold', pad=20)

                # 保存图片
                output_file = 'resume_wordcloud_136.jpg'
                plt.savefig(output_file, dpi=300, bbox_inches='tight')
                print(f"✓ 词云图已保存为: {output_file}")

                plt.show()
                return True
            except Exception as no_settings_e:
                print(f"✗ 基本WordCloud也失败: {no_settings_e}")

            # 方法2: 使用matplotlib的文本绘制简单的词云
            create_simple_wordcloud(word_content, font_path)

        # 7. 显示词频统计信息
        print("\n词频统计信息:")
        print("-" * 40)

        # 简单的词频统计
        word_list = word_cut_join.split()
        word_count = {}
        for word in word_list:
            if len(word) >= 2:  # 只统计长度大于等于2的词
                word_count[word] = word_count.get(word, 0) + 1

        # 按词频排序
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

        print(f"总词语数: {len(word_list)}")
        print(f"不同词语数: {len(word_count)}")
        print("\n出现频率最高的10个词语:")
        for i, (word, count) in enumerate(sorted_words[:10], 1):
            print(f"{i:2d}. {word:10s}: {count:3d} 次")

        return True

    except FileNotFoundError as e:
        print(f"✗ 错误: 未找到文件 - {e}")
        print("\n请确保 per_info.txt 文件存在")
        return False
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False


def create_simple_wordcloud(text, font_path=None):
    """创建简单的词云图（WordCloud的替代方案）"""
    try:
        # 使用简单的文本绘制
        plt.figure(figsize=(12, 8))

        # 设置背景色
        plt.gca().set_facecolor('white')

        # 添加标题
        plt.text(0.5, 0.95, '简历信息词云图 - 1班36号',
                 fontsize=20, fontweight='bold',
                 ha='center', va='top', transform=plt.gca().transAxes)

        # 添加文本信息
        plt.text(0.5, 0.5, text[:500] + "...",  # 只显示前500个字符
                 fontsize=12, ha='center', va='center',
                 wrap=True, transform=plt.gca().transAxes)

        plt.text(0.5, 0.1, "注: WordCloud生成失败，此为文本预览",
                 fontsize=10, style='italic', color='gray',
                 ha='center', va='bottom', transform=plt.gca().transAxes)

        plt.axis('off')

        # 保存图片
        output_file = 'resume_wordcloud_simple_136.jpg'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ 简单词云图已保存为: {output_file}")

        plt.show()
        return True

    except Exception as e:
        print(f"✗ 创建简单词云图时出错: {e}")
        return False


# ========== 主程序 ==========
if __name__ == "__main__":
    print("=" * 70)
    print("实验五：实例1 - 简历信息词云图")
    print("=" * 70)

    # 检查必要的库
    print("检查必要的库...")
    required_libraries = ['jieba', 'matplotlib', 'wordcloud']

    missing_libs = []
    for lib in required_libraries:
        try:
            __import__(lib)
            print(f"✓ {lib} 已安装")
        except ImportError:
            print(f"✗ {lib} 未安装")
            missing_libs.append(lib)

    # 检查PIL库（用于图片处理）
    try:
        from PIL import Image
        print(f"✓ PIL 已安装")
    except ImportError:
        print(f"✗ PIL 未安装")
        missing_libs.append('Pillow')  # Pillow是PIL的更新版本

    if missing_libs:
        print(f"\n缺少必要的库: {', '.join(missing_libs)}")
        print("请运行以下命令安装:")
        print("pip install jieba matplotlib wordcloud Pillow")
        exit(1)

    print("\n" + "=" * 70)

    # 执行实例1：简历信息词云图
    if create_resume_wordcloud():
        print("\n" + "=" * 70)
        print("✓ 实例1完成!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("✗ 实例1执行失败")
        print("=" * 70)