import findspark

findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import jieba

'''read csv file'''


def read_csv():
    spark = SparkSession.builder.getOrCreate()

    # 定义schema
    schema = StructType([StructField('id', StringType()),
                         StructField('product', StringType()),
                         StructField('comment', StringType()),
                         ])

    # read file
    inputDF = spark.read \
        .format("csv") \
        .option("sep", "\t") \
        .schema(schema) \
        .option("header", "false") \
        .load("../../file_input/aa.txt")
    inputDF.show()
    inputDF.createOrReplaceTempView("product_info")

    # analysis
    res01 = spark.sql("""
                    select product, count(*) cnt
                    from product_info
                    group by product
                    order by cnt desc
                    """)
    res01.show()


if __name__ == '__main__':
    read_csv()
    MySparkUtil.readFromMysql()
