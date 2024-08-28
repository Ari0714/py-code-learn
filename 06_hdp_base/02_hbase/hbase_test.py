import findspark
findspark.init()
from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame




if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext