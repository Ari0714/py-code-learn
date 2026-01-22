#!/usr/bin/python

import sys
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago


sys.path.append('/root/airflow2.2.5/abcc')
from plugins.metadata_plugin import pre_execute, post_execute

default_args = {
    # 用户
    'owner': 'Ari',
    # 是否开启任务依赖
    'depends_on_past': True,
    # 邮箱
    'email': ['1187334030@qq.com'],
    # 启动时间
    'start_date': days_ago(0),
    # 出错是否发邮件报警
    'email_on_failure': False,
    # 重试是否发邮件报警
    'email_on_retry': False,
    # 重试次数
    'retries': 1,
    # 重试时间间隔
    'retry_delay': timedelta(minutes=5),
}

# 声明任务图
dag = DAG('test_hook', default_args=default_args, schedule_interval=timedelta(days=1))

# 创建单个任务
t1 = BashOperator(
    # 任务id
    task_id='dwd',
    # 任务命令
    bash_command='echo "hello Ari"',
    pre_execute=pre_execute,
    post_execute=post_execute,
    # 重试次数
    retries=1,
    # 把任务添加进图中
    dag=dag)

t2 = BashOperator(
    task_id='dws',
    bash_command='echo "hello Ari"',
    retries=1,
    dag=dag)

t3 = BashOperator(
    task_id='ads',
    bash_command='echo "hello Ari"',
    retries=1,
    dag=dag)

# 设置任务依赖
t1 >> t2 >> t3
# t2.set_upstream(t1)
# t3.set_upstream(t2)