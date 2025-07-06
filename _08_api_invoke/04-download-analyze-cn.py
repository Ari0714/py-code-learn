# import yfinance
#
# data = yfinance.download('QQQ')
#
# print(data)

import findspark
findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import json

spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

inputDF = spark.read \
    .format("csv") \
    .option("sep", ",") \
    .option("header", "true") \
    .load("input/518880-history.csv")

# targetRDD = inputRDD.map(lambda x: (json.loads(json.dumps(x))['datetime'],json.loads(json.dumps(x))['close']))

inputDF.show()
inputDF.createOrReplaceTempView("history_data")

# spark.sql("""
#             select min(datetime) min, max(datetime) max, count(*) cnt from history_data
#             """).show()
#
# legDF = spark.sql("""
#             select *, round(((close - last_close) / last_close) *100,2) as ratio from (
#             select *,
#                 LAG(close, 1) OVER (ORDER BY datetime) AS last_close
#              from history_data
#              ) t
#             """)
# legDF.createOrReplaceTempView("middle_table")
#
#
# resDF = spark.sql("""
#         select
#         sum(if(ratio < -1.0,1,0)) as `1.0`,
#         sum(if(ratio < -1.1,1,0)) as `1.1`,
#         sum(if(ratio < -1.2,1,0)) as `1.2`,
#         sum(if(ratio < -1.3,1,0)) as `1.3`,
#         sum(if(ratio < -1.4,1,0)) as `1.4`,
#         sum(if(ratio < -1.5,1,0)) as `1.5`,
#         sum(if(ratio < -1.6,1,0)) as `1.6`,
#         sum(if(ratio < -1.7,1,0)) as `1.7`,
#         sum(if(ratio < -1.8,1,0)) as `1.8`,
#         sum(if(ratio < -1.9,1,0)) as `1.9`,
#         sum(if(ratio < -2.0,1,0)) as `2.0`,
#         sum(if(ratio < -2.1,1,0)) as `2.1`,
#         sum(if(ratio < -2.2,1,0)) as `2.2`,
#         sum(if(ratio < -2.3,1,0)) as `2.3`,
#         sum(if(ratio < -2.4,1,0)) as `2.4`,
#         sum(if(ratio < -2.5,1,0)) as `2.5`,
#         sum(if(ratio < -2.6,1,0)) as `2.6`,
#         sum(if(ratio < -2.7,1,0)) as `2.7`,
#         sum(if(ratio < -2.8,1,0)) as `2.8`,
#         sum(if(ratio < -2.9,1,0)) as `2.9`,
#         sum(if(ratio < -3.0,1,0)) as `3.0`
#         from middle_table
#             """)
# resDF.show()
#
# 保存到mysql
inputDF.repartition(1).write.format('jdbc').options(
    url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
    driver='com.mysql.jdbc.Driver',  # the driver for MySQL
    user='root',
    dbtable='inner518880',
    password='cj111111',
).mode('overwrite').save()
