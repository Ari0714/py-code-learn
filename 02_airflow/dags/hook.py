
# from airflow.providers.kafka.hooks.kafka import KafkaHook
# from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.hooks.http import HttpHook

from airflow.providers.http.hooks.http import HttpHook
import json


def example_http_hook():
    """HTTP Hook 基本用法"""

    # 创建 Hook 实例
    http_hook = HttpHook(http_conn_id='http_default', method='GET')

    # 1. 发起 GET 请求
    response = http_hook.run(
        endpoint='/api/users',
        headers={'Content-Type': 'application/json'}
    )

    # 解析响应
    if response.status_code == 200:
        users = response.json()
        print(f"获取到 {len(users)} 个用户")

    # 2. 发起 POST 请求
    http_hook.method = 'POST'
    response = http_hook.run(
        endpoint='/api/users',
        data=json.dumps({
            'username': 'new_user',
            'email': 'new@example.com'
        }),
        headers={'Content-Type': 'application/json'}
    )

    # 3. 发起 PUT 请求
    http_hook.method = 'PUT'
    response = http_hook.run(
        endpoint='/api/users/123',
        data=json.dumps({'email': 'updated@example.com'})
    )

    # 4. 发起 DELETE 请求
    http_hook.method = 'DELETE'
    response = http_hook.run(endpoint='/api/users/123')

    # 5. 带参数和认证的请求
    response = http_hook.run(
        endpoint='/api/data',
        data={'param1': 'value1', 'param2': 'value2'},
        headers={'Authorization': 'Bearer token123'},
        extra_options={'timeout': 30, 'verify': False}  # SSL 验证
    )


if __name__ == '__main__':
    pass