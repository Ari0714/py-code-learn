
import findspark
findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import json


spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

# 直接读取
inputDF = spark.read \
    .format("csv") \
    .option("sep", ",") \
    .option("header", "true") \
    .load("input/VIX_History.csv")

inputDF.show()
# 创建临时表
inputDF.createOrReplaceTempView('info')

resDF = spark.sql("""
            select date_format(to_date(DATE, 'MM/dd/yyyy'),'yyyy-MM-dd') DATE2, OPEN, CLOSE, round((CLOSE - OPEN) / OPEN * 100,2) ratio
            from info
            order by DATE2 DESC
            """)
resDF.show()


# 保存到mysql
resDF.repartition(1).write.format('jdbc').options(
    url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
    driver='com.mysql.jdbc.Driver',  # the driver for MySQL
    user='root',
    dbtable='vix_history',
    password='cj111111',
).mode('overwrite').save()
