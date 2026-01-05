import pymysql
import pandas as pd

# ===================== 1. 配置MySQL连接信息 =====================
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",  # 替换为你的MySQL密码
    "port": 3306,
    "database": "test01",  # 班号1+学号36
    "charset": "utf8mb4"
}

# ===================== 2. 连接MySQL，用Pandas读取成绩数据 =====================
try:
    # 步骤1：连接数据库，读取score表数据
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    query_sql = "SELECT * FROM score;"
    df = pd.read_sql(query_sql, conn)  # Pandas读取SQL结果
    print("✅ 原始成绩数据：")
    print(df)

    # ===================== 3. 计算学生平均分和最高分 =====================
    df["平均分"] = df[["chinese", "math", "english", "computer"]].mean(axis=1).round(2)
    df["最高分"] = df[["chinese", "math", "english", "computer"]].max(axis=1)
    print("\n📈 计算学生平均分和最高分后：")
    print(df)

    # ===================== 4. 计算每门课程的最高分（新增“最高分”行）=====================
    course_max = {
        "name": "最高分",
        "chinese": df["chinese"].max(),
        "math": df["math"].max(),
        "english": df["english"].max(),
        "computer": df["computer"].max(),
        "平均分": df["平均分"].max(),
        "最高分": df["最高分"].max()
    }
    df = pd.concat([df, pd.DataFrame([course_max])], ignore_index=True)
    print("\n📊 添加课程最高分后的数据：")
    print(df)

    # ===================== 5. 兼容版：给score表添加字段（支持MySQL 5.x）=====================
    def add_column_if_not_exists(table, column, dtype):
        """
        兼容MySQL 5.x：先查询字段是否存在，不存在则添加
        table: 表名, column: 字段名, dtype: 字段类型（如FLOAT、VARCHAR(50)）
        """
        # 查询字段是否存在
        cursor.execute(f"""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{mysql_config["database"]}' 
              AND TABLE_NAME = '{table}' 
              AND COLUMN_NAME = '{column}';
        """)
        exists = cursor.fetchone()  # 存在返回字段信息，不存在返回None
        if not exists:
            # 字段不存在，执行添加
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {dtype};")
            print(f"✅ 表 {table} 新增字段：{column}")
        else:
            print(f"ℹ️  表 {table} 已存在字段：{column}（跳过添加）")

    # 调用函数添加“平均分”和“最高分”字段（兼容MySQL 5.x）
    add_column_if_not_exists("score", "平均分", "FLOAT")
    add_column_if_not_exists("score", "最高分", "FLOAT")

    # ===================== 6. 将计算后的数据写入MySQL =====================
    cursor.execute("DELETE FROM score;")  # 清空原有数据（避免重复）
    insert_data = [tuple(row) for row in df.values]
    insert_sql = """
    INSERT INTO score (name, chinese, math, english, computer, 平均分, 最高分)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.executemany(insert_sql, insert_data)
    conn.commit()
    print(f"✅ 计算后的数据已更新到数据库")

    # ===================== 7. 最终读取并格式化输出 =====================
    final_df = pd.read_sql("SELECT * FROM score;", conn)
    print("\n🎯 最终数据库完整数据（含统计信息）：")
    print(final_df.to_string(index=False))  # 不显示索引

except pymysql.Error as e:
    print(f"❌ MySQL操作失败：{e}")
    conn.rollback()
except Exception as e:
    print(f"❌ 程序执行失败：{e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("\n🔌 MySQL连接已关闭")