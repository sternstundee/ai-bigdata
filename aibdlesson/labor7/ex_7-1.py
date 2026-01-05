import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
import matplotlib.pyplot as plt
import os
import numpy as np
import warnings

warnings.filterwarnings('ignore')  # 忽略无关警告

# ---------------------- 完全适配你的数据列（age/income/guding/VIP/loan），无需修改！----------------------
file_path = "D:/pythonstudy/aibdlesson/labor7/loan_YN.csv"  # 你的数据路径
target_col = "loan"  # 目标列：贷款状态（loan列）


# ---------------------- 1. 数据读取（自动适配编码，兼容中文）----------------------
def read_data_with_encoding(file_path):
    if file_path.endswith(".csv"):
        try:
            return pd.read_csv(file_path, encoding="gbk")  # Windows中文文件默认编码
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding="utf-8-sig")
    else:
        raise ValueError("仅支持CSV文件（你的文件是.csv，已适配）")


try:
    # 读取数据
    df = read_data_with_encoding(file_path)
    print("=" * 70)
    print(f"✅ 成功读取贷款数据：{df.shape[0]} 条样本，{df.shape[1]} 个特征")
    print("数据列名：", list(df.columns))
    print("\n数据前5行预览：")
    print(df.head())
    print("\n数据类型：")
    print(df.dtypes)
    print("=" * 70)

    # 验证目标列（确保loan列存在）
    if target_col not in df.columns:
        raise ValueError(
            f"数据中不存在loan列！请检查列名：{list(df.columns)}\n"
            f"若目标列名不同，请修改代码中 target_col 为实际列名"
        )

    # 分离特征（X）和目标变量（y）：特征列=age/income/guding/VIP，目标列=loan
    X = df.drop(columns=[target_col])  # 特征列（排除loan）
    y = df[target_col]  # 目标列：loan（贷款状态）
    print(f"📊 特征列（用于预测贷款）：{list(X.columns)}")
    print(f"🎯 目标列（贷款状态）：{target_col}（取值分布：{y.value_counts().to_dict()}）")
    print("=" * 70)

    # ---------------------- 2. One-Hot编码（自动识别分类/数值特征）----------------------
    # 分类特征：guding、VIP（通常是字符串或二分类标签）
    # 数值特征：age（年龄）、income（收入）
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = X.select_dtypes(exclude=["object"]).columns.tolist()
    print(f"🔤 分类特征（One-Hot编码）：{categorical_cols}")
    print(f"🔢 数值特征（直接保留）：{numeric_cols}")

    # One-Hot编码分类特征（适配sklearn 0.24.2版本）
    vec = DictVectorizer(sparse=False)
    X_categorical_encoded = vec.fit_transform(X[categorical_cols].to_dict("records"))
    categorical_feature_names = vec.get_feature_names()

    # 合并数值特征和编码后的分类特征
    if numeric_cols:
        X_numeric = X[numeric_cols].values
        X_encoded = np.hstack([X_numeric, X_categorical_encoded])
        all_feature_names = numeric_cols + categorical_feature_names
    else:
        X_encoded = X_categorical_encoded
        all_feature_names = categorical_feature_names

    print(f"\n🔥 One-Hot编码完成！")
    print(f"编码后特征矩阵形状：{X_encoded.shape}（样本数 × 编码后特征数）")
    print(f"编码后特征名称（共 {len(all_feature_names)} 个）：")
    for i, name in enumerate(all_feature_names, 1):
        print(f"  {i:2d}. {name}")
    print("=" * 70)

    # ---------------------- 3. 训练决策树模型（贷款状态预测）----------------------
    dt_model = DecisionTreeClassifier(
        max_depth=3,  # 限制树深度，避免过拟合，可视化清晰
        random_state=42,  # 固定随机种子，结果可复现
        criterion="gini"  # 基尼系数（适合分类任务）
    )
    dt_model.fit(X_encoded, y)  # 训练模型

    # 模型评估
    train_acc = dt_model.score(X_encoded, y)
    print("🤖 决策树模型训练完成！")
    print(f"训练集准确率：{train_acc:.3f}（越高表示模型拟合效果越好）")
    print("=" * 70)

    # ---------------------- 4. 决策树可视化（保存到labor7目录）----------------------
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 中文支持
    plt.rcParams["axes.unicode_minus"] = False  # 负号显示正常

    # 绘制决策树并保存
    plt.figure(figsize=(18, 10))
    plot_tree(
        dt_model,
        feature_names=all_feature_names,  # 显示特征名称（如age、income、VIP_是）
        class_names=[str(cls) for cls in dt_model.classes_],  # 贷款状态类别（如0/1、是/否）
        filled=True,  # 彩色填充（不同类别不同颜色）
        rounded=True,  # 圆角矩形
        fontsize=10,
        proportion=True  # 显示样本占比
    )
    dt_img_path = "D:/pythonstudy/aibdlesson/labor7/decision_tree_loan_final.png"
    plt.tight_layout()
    plt.savefig(dt_img_path, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"📸 决策树图片已保存到：{dt_img_path}（直接打开查看）")
    print("=" * 70)

    # ---------------------- 5. 导出决策树DOT文件（高清版）----------------------
    dot_path = "D:/pythonstudy/aibdlesson/labor7/decision_tree_loan_final.dot"
    export_graphviz(
        dt_model,
        out_file=dot_path,
        feature_names=all_feature_names,
        class_names=[str(cls) for cls in dt_model.classes_],
        filled=True,
        rounded=True,
        proportion=True
    )
    print(f"📄 决策树DOT文件已保存到：{dot_path}")
    print("💡 高清图片转换（可选）：")
    print("  1. 安装graphviz：https://graphviz.org/download/（Windows选msi，勾选添加到PATH）")
    print("  2. 命令行进入labor7目录，执行：dot -Tpng decision_tree_loan_final.dot -o decision_tree_loan_highres.png")
    print("=" * 70)

    # ---------------------- 6. 核心特征分析（影响贷款的关键因素）----------------------
    feature_importance = pd.DataFrame({
        "特征名称": all_feature_names,
        "重要性": dt_model.feature_importances_
    }).sort_values("重要性", ascending=False)

    print("🏆 影响贷款状态的关键特征排名（按重要性排序）：")
    print(feature_importance.to_string(index=False))

    # 可视化关键特征
    plt.figure(figsize=(12, 6))
    plt.barh(
        feature_importance["特征名称"][::-1],  # 逆序显示，重要性高的在上方
        feature_importance["重要性"][::-1],
        color="#1f77b4"  # 蓝色系，专业美观
    )
    plt.xlabel("特征重要性", fontsize=12)
    plt.title("贷款状态预测 - 决策树特征重要性排名", fontsize=14, fontweight="bold")
    plt.tight_layout()
    importance_img_path = "D:/pythonstudy/aibdlesson/labor7/feature_importance_loan_final.png"
    plt.savefig(importance_img_path, dpi=300)
    plt.show()
    print(f"\n📊 特征重要性图已保存到：{importance_img_path}")
    print("=" * 70)

    # ---------------------- 7. 保存所有实验结果（用于作业提交）----------------------
    # 保存编码后的数据（含目标列）
    encoded_df = pd.DataFrame(X_encoded, columns=all_feature_names)
    encoded_df[target_col] = y.values  # 合并loan列
    result_csv_path = "D:/pythonstudy/aibdlesson/labor7/loan_onehot_dt_final_result.csv"
    encoded_df.to_csv(result_csv_path, index=False, encoding="utf-8-sig")

    # 保存特征重要性数据
    importance_csv_path = "D:/pythonstudy/aibdlesson/labor7/feature_importance_loan_final.csv"
    feature_importance.to_csv(importance_csv_path, index=False, encoding="utf-8-sig")

    print("💾 所有实验结果已保存到 labor7 目录：")
    print(f"  1. 编码后完整数据（含loan列）：{result_csv_path}")
    print(f"  2. 决策树可视化图片：{dt_img_path}")
    print(f"  3. 决策树DOT文件（高清）：{dot_path}")
    print(f"  4. 特征重要性图片：{importance_img_path}")
    print(f"  5. 特征重要性数据：{importance_csv_path}")
    print("=" * 70)
    print("🎉 实验完成！所有文件可直接用于实验报告撰写：")
    print("  - 决策树图片：展示模型决策逻辑")
    print("  - 特征重要性图：分析影响贷款的核心因素")
    print("  - CSV结果：提供编码后的数据和特征重要性数值")

# ---------------------- 错误处理（精准定位问题）----------------------
except FileNotFoundError:
    print(f"❌ 错误：未找到文件！请确认 loan_YN.csv 在以下路径：{file_path}")
except ValueError as e:
    print(f"❌ 错误：{e}")
except Exception as e:
    print(f"❌ 意外错误：{str(e)}")
    print("  排查建议：1. 检查数据是否有空值；2. 确保loan列是分类变量（如0/1、是/否）；3. 确认列名无空格")