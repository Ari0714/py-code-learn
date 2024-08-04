import findspark
findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import jieba


class MySparkUtil:

    # read mysql
    def readFromMysql(self,spark):
        spark.read.format("jdbc")\
            .options(url="jdbc:mysql://192.168.112.10:3306/test", driver="com.mysql.jdbc.Driver",dbtable="test_spark", user="root", password="xxxxxx")\
            .load()
