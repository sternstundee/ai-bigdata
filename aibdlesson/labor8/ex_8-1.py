# 导入依赖库（适配TensorFlow 1.15.0，修复所有兼容问题）
import tensorflow as tf
from tensorflow.keras.datasets import mnist
import numpy as np
import warnings

warnings.filterwarnings('ignore')  # 忽略废弃API警告

# ---------------------- 1. 读取并预处理MNIST数据集 ----------------------
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 图像展平+归一化：(样本数, 28, 28) → (样本数, 784)，值映射到0-1
x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0


# 标签转为one-hot编码（实验要求格式）
def to_one_hot(labels, num_classes=10):
    return np.eye(num_classes)[labels]


y_train = to_one_hot(y_train)
y_test = to_one_hot(y_test)


# 封装数据集类，保持batch读取逻辑
class MNIST_Dataset:
    def __init__(self, images, labels):
        self.images = images
        self.labels = labels
        self.num_examples = len(images)
        self.index = 0

    def next_batch(self, batch_size):
        start = self.index
        self.index += batch_size
        if self.index > self.num_examples:
            # 打乱数据重新开始
            perm = np.arange(self.num_examples)
            np.random.shuffle(perm)
            self.images = self.images[perm]
            self.labels = self.labels[perm]
            start = 0
            self.index = batch_size
        end = self.index
        return self.images[start:end], self.labels[start:end]


# 初始化数据集对象
mnist = type('obj', (object,), {})()
mnist.train = MNIST_Dataset(x_train, y_train)
mnist.test = MNIST_Dataset(x_test, y_test)

print("数据集加载完成：")
print(f"训练集样本数：{mnist.train.num_examples}")
print(f"测试集样本数：{mnist.test.num_examples}")
print(f"图像维度：{x_train.shape[1]}（28×28展平后）")
print(f"标签维度：{y_train.shape[1]}（one-hot编码）")


# ---------------------- 2. 初始化参数矩阵（修复tf.random_normal问题） ----------------------
def init_weights(shape):
    """生成标准差为0.01的正态分布随机张量（兼容TF 1.15.0）"""
    return tf.Variable(tf.random.normal(shape, stddev=0.01))  # 改为tf.random.normal


# 定义三层网络权重（按实验要求：784→16→16→10）
h1 = init_weights([784, 16])  # 隐藏层1：输入784维，输出16维
h2 = init_weights([16, 16])  # 隐藏层2：输入16维，输出16维
out = init_weights([16, 10])  # 输出层：输入16维，输出10维（0-9分类）

# ---------------------- 3. 定义神经网络模型（按实验要求实现） ----------------------
in_x = tf.placeholder(tf.float32, [None, 784], name='x-input')  # 输入占位符
in_y = tf.placeholder(tf.float32, [None, 10], name='y-input')  # 标签占位符


def model(X, h1, h2, out):
    """前向传播：输入→隐藏层1（ReLU）→隐藏层2（ReLU）→输出层"""
    hidden1 = tf.nn.relu(tf.matmul(X, h1))
    hidden2 = tf.nn.relu(tf.matmul(hidden1, h2))
    return tf.matmul(hidden2, out)


mod = model(in_x, h1, h2, out)  # 初始化模型

# ---------------------- 4. 损失函数与优化器 ----------------------
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=mod, labels=in_y))
train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cost)  # 按实验要求设置优化器

# 准确率计算
predict_acc = tf.reduce_mean(tf.cast(
    tf.equal(tf.argmax(mod, 1), tf.argmax(in_y, 1)),
    tf.float32
))

# ---------------------- 5. 模型训练（支持键盘输入训练次数） ----------------------
saver = tf.train.Saver()  # 模型保存器
sess = tf.Session()
sess.run(tf.global_variables_initializer())  # 初始化所有变量

# 键盘输入训练次数
train_num = int(input('\n请输入需要训练的次数:'))
batch_size = 64  # 每批次64张图片（实验默认）

print("\n开始训练...")
for step in range(1, train_num + 1):
    batch_x, batch_y = mnist.train.next_batch(batch_size)
    sess.run(train_op, feed_dict={in_x: batch_x, in_y: batch_y})

    # 每隔1000批次输出损失值和准确率（按实验要求格式）
    if step % 1000 == 0:
        loss, acc = sess.run([cost, predict_acc], feed_dict={in_x: batch_x, in_y: batch_y})
        print(f"第{step:5d}次训练  损失值:{loss:.6f}  训练准确率:{acc * 100:.3f}%")
        # 保存模型到mnist_models目录
        saver.save(sess, './mnist_models/model.ckpt', global_step=step)

# ---------------------- 6. 计算并输出测试准确率 ----------------------
test_batch_size = 1000
test_acc_total = 0.0
test_batches = mnist.test.num_examples // test_batch_size

for i in range(test_batches):
    start = i * test_batch_size
    end = start + test_batch_size
    test_x = mnist.test.images[start:end]
    test_y = mnist.test.labels[start:end]
    batch_acc = sess.run(predict_acc, feed_dict={in_x: test_x, in_y: test_y})
    test_acc_total += batch_acc

test_acc = test_acc_total / test_batches
print(f"\n测试准确率:{test_acc * 100:.3f}%")

# 关闭会话
sess.close()