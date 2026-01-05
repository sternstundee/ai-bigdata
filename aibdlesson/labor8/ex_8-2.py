# 导入依赖库（适配TensorFlow 1.15.0，与实例1保持一致）
import tensorflow as tf
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# ---------------------- 1. 加载测试集数据（与实例1预处理逻辑一致） ----------------------
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 测试集图像预处理：展平为784维（适配模型输入），归一化
x_test_flatten = x_test.reshape(-1, 784).astype('float32') / 255.0


# 标签转为one-hot编码（用于模型加载后验证，不影响预测逻辑）
def to_one_hot(labels, num_classes=10):
    return np.eye(num_classes)[labels]


y_test_onehot = to_one_hot(y_test)

print("测试集加载完成：")
print(f"测试集样本数：{len(x_test)}（序号0-9999）")
print(f"图像原始维度：{x_test.shape[1:]}（28×28）")
print(f"图像输入维度：{x_test_flatten.shape[1]}（展平后）")


# ---------------------- 2. 复用实例1的网络结构（必须完全一致，否则模型加载失败） ----------------------
# 初始化权重函数（与实例1相同）
def init_weights(shape):
    return tf.Variable(tf.random.normal(shape, stddev=0.01))


# 定义网络权重（与实例1完全一致：784→16→16→10）
h1 = init_weights([784, 16])
h2 = init_weights([16, 16])
out = init_weights([16, 10])

# 定义占位符（与实例1相同）
in_x = tf.placeholder(tf.float32, [None, 784], name='x-input')
in_y = tf.placeholder(tf.float32, [None, 10], name='y-input')


# 定义模型（与实例1完全一致）
def model(X, h1, h2, out):
    hidden1 = tf.nn.relu(tf.matmul(X, h1))
    hidden2 = tf.nn.relu(tf.matmul(hidden1, h2))
    return tf.matmul(hidden2, out)


mod = model(in_x, h1, h2, out)  # 初始化模型（仅用于加载参数，不重新训练）

# ---------------------- 3. 加载实例1训练好的模型 ----------------------
saver = tf.train.Saver()
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# 自动查找最新保存的模型（无需手动修改路径）
latest_ckpt = tf.train.latest_checkpoint('./mnist_models/')
if latest_ckpt is None:
    raise FileNotFoundError("未找到训练好的模型！请先运行实例1完成训练，确保mnist_models目录下有.ckpt文件")

saver.restore(sess, latest_ckpt)
print(f"\n✅ 模型加载成功：{latest_ckpt}")

# ---------------------- 4. 定义可视化函数（按实验要求实现） ----------------------
# 设置中文显示（解决乱码问题）
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def display_compare(num):
    """
    展示指定序号的测试图片、预测值和真实标签
    num：图片序号（0-9999，对应测试集所有样本）
    """
    # 1. 获取指定序号的测试数据
    x_single = x_test_flatten[num:num + 1]  # 取单个样本，维度：[1, 784]
    true_label = y_test[num]  # 真实标签（数字形式，0-9）

    # 2. 模型预测
    pred_logits = sess.run(mod, feed_dict={in_x: x_single})
    pred_label = np.argmax(pred_logits)  # 取概率最大的数字作为预测值

    # 3. 判断预测结果
    if pred_label == true_label:
        title = f"预测值: {pred_label}, 标签: {true_label}, 预测正确！"
        color = 'green'  # 正确用绿色标题
    else:
        title = f"预测值: {pred_label}, 标签: {true_label}, 预测错误！"
        color = 'red'  # 错误用红色标题

    # 4. 可视化图片（重构为28×28灰度图）
    plt.figure(figsize=(5, 5))
    plt.title(title, fontsize=14, color=color)
    # 显示原始图片（x_test[num]是28×28维度，gray_r：黑字白底）
    plt.imshow(x_test[num], cmap=plt.get_cmap('gray_r'))
    plt.axis('off')  # 隐藏坐标轴，更清晰
    plt.tight_layout()
    plt.show()


# ---------------------- 5. 交互测试（支持键盘输入图片序号） ----------------------
print("\n📌 支持输入图片序号范围：0-9999（输入-1退出程序）")
while True:
    try:
        num_input = input("\n请输入需要预测的图片序号：")
        num = int(num_input)
        if num == -1:
            print("👋 退出程序，感谢使用！")
            break
        if 0 <= num <= 9999:
            display_compare(num)
        else:
            print("❌ 序号超出范围！请输入0-9999之间的整数。")
    except ValueError:
        print("❌ 输入错误！请输入有效的整数（0-9999或-1）。")

# 关闭会话，释放资源
sess.close()