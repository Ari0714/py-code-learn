import findspark
findspark.init()
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession, DataFrame
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from pyspark.sql import *
import numpy

'''
预测2018年全年房价走势
算法：线性回归
'''

if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    '''数据读取'''
    inputDF = spark.read \
        .format("csv") \
        .option("sep", "\t") \
        .option("header", "true") \
        .load("hdfs://hdp:8020/input/part-00000")
    inputDF.createOrReplaceTempView("house_info")
    inputDF.show()

    '''数据分析'''
    # 计算截至2017年的每月房价走势
    resDF01 = spark.sql("""
                select *, rank() over(order by dt) rk from(
                    select date_format(tradeTime,'yyyy-MM') dt, round(avg(totalPrice),2) avg_price
                    from house_info
                    where date_format(tradeTime,'yyyy') < '2018'
                    group by date_format(tradeTime,'yyyy-MM')
                ) t
                """)
    resDF01.show()

    '''算法预测'''
    resRDD = resDF01.select("rk", "dt", "avg_price").rdd.map(tuple)
    # resRDD.foreach(lambda x: print(x))

    # 模型封装
    parseData = resRDD.map(lambda x: LabeledPoint(float(x[2]), [float(x[0])]))

    # 模型训练
    model = LinearRegressionWithSGD.train(parseData, 1, 0.000258)

    # 测试数据预测
    preRDD = sc.parallelize([102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113])
    preResRDD = preRDD.map(lambda x: ('2018', round(numpy.float(model.predict(Vectors.dense(x))),2)))
    preResRDD.repartition(1).foreach(lambda x: print(x))

    # 转换结构，调整输出格式
    schema = StructType([StructField('dt', StringType()), StructField('pre_price', StringType())])
    preResDF = spark.createDataFrame(preResRDD, schema)
    preResDF.createOrReplaceTempView("pre_price_info")
    preResFormatDF = spark.sql("""
                            select concat('2018-',row_number() over(order by 1)) dt, pre_price
                            from pre_price_info
                            """)
    preResFormatDF.show()

    # 保存到mysql
    preResFormatDF.repartition(1).write.format('jdbc').options(
        url='jdbc:mysql://hdp:3306/test?characterEncoding=utf-8&useSSL=false',
        driver='com.mysql.jdbc.Driver',  # the driver for MySQL
        user='root',
        dbtable='preResFormatDF',
        password='111111',
    ).mode('overwrite').save()