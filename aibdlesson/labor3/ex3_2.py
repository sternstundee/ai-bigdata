import pymysql

# ===================== 1. 配置MySQL连接信息 =====================
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "port": 3306,
    "database": "test01",  # 直接指定数据库
    "charset": "utf8mb4"
}

# ===================== 2. 连接数据库并读取数据 =====================
try:
    # 连接数据库
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    print(f"✅ 成功连接数据库：student_136")

    # 执行查询：读取所有学生信息
    query_sql = "SELECT id, name FROM mingdan ORDER BY id;"
    cursor.execute(query_sql)
    results = cursor.fetchall()  # 获取所有查询结果

    # 转换为字典（key：学号，value：姓名）
    student_dict = {row[0]: row[1] for row in results}

    # 输出字典
    print("\n📋 从数据库读取的学生信息字典：")
    if student_dict:
        for sid, sname in student_dict.items():
            print(f"{sid:2d}: {sname}")
    else:
        print("❌ 数据库中未查询到学生信息！")

except pymysql.Error as e:
    print(f"❌ MySQL操作失败：{e}")
finally:
    # 关闭连接
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("\n🔌 MySQL连接已关闭")