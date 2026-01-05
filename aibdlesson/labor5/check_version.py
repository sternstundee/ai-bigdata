import wordcloud
print('WordCloud 版本:', wordcloud.__version__)

# 检查系统中是否设置了默认字体
import matplotlib
print('Matplotlib 默认字体:', matplotlib.rcParams.get('font.family', 'Unknown'))

# 尝试重置matplotlib字体设置
import matplotlib.pyplot as plt
plt.rcParams.update(plt.rcParamsDefault)
print('已重置matplotlib配置')