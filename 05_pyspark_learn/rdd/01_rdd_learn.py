import findspark
from pyspark.sql.types import DataType

findspark.init()
from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame


if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    # read data
    rdd1 = sc.parallelize([1,2,3,4])
    rdd1.foreach(lambda x:print(x))

    inputRDD = sc.textFile("00_input/data.csv") \
        .filter(lambda x: "day" not in x) \
        .filter(lambda x: len(x) > 0)
    inputRDD.foreach(lambda x:print(x))