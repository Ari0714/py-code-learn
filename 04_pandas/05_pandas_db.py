from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql

if __name__ == '__main__':
    db_conn = pymysql.connect(
        host='hwhdp',
        port=3306,
        user='root',
        password='cj111111',
        database='test',
        charset='utf8'
    )

    query_sql = 'SELECT * from resDF01'

    pd_mysql = pd.read_sql(sql=query_sql,con=db_conn)
    print(pd_mysql)

    # calculate avg_salary
    avg_salary = pd_mysql.loc[:,'avg_salary']
    print(avg_salary.mean())
