from pyhive import hive
import traceback


if __name__ == '__main__':
    try:
        print("Testing PyHive connection...")

        # 尝试不同的连接参数
        conn = hive.Connection(
            host='x1',
            port=10000,
            # username='',  # 通常可以为空
            # password='',
            # auth='NOSASL'  # 重要：尝试NOSASL认证
        )

        cursor = conn.cursor()
        cursor.execute('SELECT 1 as test_value')
        result = cursor.fetchall()

        print(f"✓ PyHive连接成功! 查询结果: {result}")
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"✗ PyHive连接失败: {e}")
        print("详细错误:")
        traceback.print_exc()
