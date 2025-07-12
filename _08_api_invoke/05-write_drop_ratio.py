
import findspark
findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import json


spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

# 定义schema
schema = StructType([StructField('indexx', StringType()),
                     StructField('x1', StringType()),
                     StructField('x2', StringType()),
                     StructField('x3', StringType())
                     ])

# 直接读取
inputDF = spark.read \
    .format("csv") \
    .option("sep", "\t") \
    .schema(schema) \
    .option("header", "false") \
    .load("input/drop-ratio-202507.txt")

inputDF.show()
# 创建临时表
inputDF.createOrReplaceTempView('info')


# 保存到mysql
inputDF.repartition(1).write.format('jdbc').options(
    url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
    driver='com.mysql.jdbc.Driver',  # the driver for MySQL
    user='root',
    dbtable='drop_ratio_202507',
    password='cj111111',
).mode('overwrite').save()
