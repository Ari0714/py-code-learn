#!/usr/bin/python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    # 用户 test_owner DAG下的所有者
    'owner': 'luanhao',
    # 是否开启任务依赖
    'depends_on_past': True,
    # 邮箱
    'email': ['1127914080@qq.com'],
    # 启动时间
    'start_date': datetime(2023, 1, 19),
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
# test代表任务名称（可以修改其他名称,这里我们用wordcount）
dag = DAG('wordcount', default_args=default_args, schedule_interval=timedelta(days=1))
# 创建单个任务
t1 = BashOperator(
    # 任务 id
    task_id='dwd',
    # 任务命令 使用Spark的wordcount
    bash_command='ssh hadoop102 "/opt/module/spark-3.2-yarn/bin/spark-submit --class org.apache.spark.examples.SparkPi --master yarn /opt/module/spark-3.2-yarn/examples/jars/spark-examples*.jar 10 "',
    # 重试次数
    retries=1,
    # 把任务添加进图中
    dag=dag)

t2 = BashOperator(
    task_id='dws',
    bash_command='ssh hadoop102 "/opt/module/spark-3.2-yarn/bin/spark-submit --class org.apache.spark.examples.SparkPi --master yarn /opt/module/spark-3.2-yarn/examples/jars/spark-examples*.jar 10 "',
    retries=1,
    dag=dag)

t3 = BashOperator(
    task_id='ads',
    bash_command='ssh hadoop102 "/opt/module/spark-3.2-yarn/bin/spark-submit --class org.apache.spark.examples.SparkPi --master yarn /opt/module/spark-3.2-yarn/examples/jars/spark-examples*.jar 10 "',
    retries=1,
    dag=dag)

# 设置任务依赖
t2.set_upstream(t1)
t3.set_upstream(t2)
