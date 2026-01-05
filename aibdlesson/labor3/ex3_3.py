import pymysql

# ===================== 1. 配置MySQL连接信息 =====================
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "port": 3306,
    "database": "test01",
    "charset": "utf8mb4"
}

# ===================== 2. 学生成绩数据（文档指定4名学生）=====================
score_data = [
    ("张三", 88, 90, 98, 95),
    ("李四", 85, 92, 95, 98),
    ("王五", 89, 89, 90, 92),
    ("丁六", 82, 86, 89, 90)
]

# ===================== 3. 连接数据库，创建成绩表并插入数据 =====================
try:
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()

    # 步骤1：创建成绩表 score（姓名+四门成绩）
    create_score_table = """
    CREATE TABLE IF NOT EXISTS score (
        name VARCHAR(20) PRIMARY KEY,  # 姓名（主键，唯一）
        chinese FLOAT NOT NULL,        # 语文成绩
        math FLOAT NOT NULL,           # 数学成绩
        english FLOAT NOT NULL,        # 英语成绩
        computer FLOAT NOT NULL        # 计算机成绩
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cursor.execute(create_score_table)
    print(f"✅ 成绩表 score 创建成功（若已存在则跳过）")

    # 步骤2：插入成绩数据（IGNORE避免重复插入）
    insert_score_sql = """
    INSERT IGNORE INTO score (name, chinese, math, english, computer)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.executemany(insert_score_sql, score_data)  # 批量插入
    conn.commit()
    print(f"✅ 共插入 {len(score_data)} 名学生的成绩")

    # 步骤3：读取并输出“姓名+语文成绩”
    query_chinese_sql = "SELECT name, chinese FROM score ORDER BY name;"
    cursor.execute(query_chinese_sql)
    chinese_results = cursor.fetchall()

    print("\n📊 学生姓名+语文成绩：")
    for name, chinese in chinese_results:
        print(f"{name:2s}：语文 {chinese} 分")

except pymysql.Error as e:
    print(f"❌ MySQL操作失败：{e}")
    conn.rollback()
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("\n🔌 MySQL连接已关闭")