import findspark
import pandas as pd

findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import jieba
import pyhdfs
from hdfs3 import HDFileSystem

if __name__ == '__main__':
    client = pyhdfs.HdfsClient(hosts='hdp:9870',user_name='hdfs')
    dir = client.listdir('/')
    print(client.copy_from_local('../00_input/data.csv', '/input'))
    for i in dir:
        print(i)
    # print(dir)

    print(pd.DataFrame(dir,columns=['name']))

