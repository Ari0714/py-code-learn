import findspark
findspark.init()
from pyspark.sql import SparkSession, DataFrame
from pyspark import SparkConf

if __name__ == '__main__':
    conf = SparkConf()
    # conf.setMaster('spark://master:7077')
    spark = SparkSession.builder.getOrCreate()

    # 读取数据
    inputDF = spark.read \
        .format("csv") \
        .option("sep", "\t") \
        .option("header", "true") \
        .load("input/data.txt")
    inputDF.show()
    # 创建临时表
    inputDF.createTempView("employ_info")

    # 1.各学历平均工资(X轴学历、Y轴该学历的平均工资)
    resDF01 = spark.sql("""
            select education, round(avg(salary),2) avg_salary from employ_info
            group by education
             """)
    resDF01.show()

    # 2.各城市平均工资走势(X轴 10大城市、Y轴 该城市对应的平均工资)
    resDF02 = spark.sql("""
            select city, round(avg(salary),2) avg_salary from employ_info
            group by city
            """)
    resDF02.show()

    # 3.各岗位招聘数量占比分析(数据分析师、机器学习工程师、数据挖掘工程师等）
    resDF03 = spark.sql("""
            select position_name, count(*) cnt from employ_info
            group by position_name
            """)
    resDF03.show()


    # 结果保存
    # resDF01.repartition(1).write.mode(saveMode="Overwrite").json("output/01")
    # resDF02.repartition(1).write.mode(saveMode="Overwrite").json("output/02")
    # resDF03.repartition(1).write.mode(saveMode="Overwrite").json("output/03")

    # 保存到mysql
    # resDF01.repartition(1).write.format('jdbc').options(
    #     url='jdbc:mysql://hdp:3306/test?characterEncoding=utf-8&useSSL=false',
    #     driver='com.mysql.jdbc.Driver',  # the driver for MySQL
    #     user='root',
    #     dbtable='resDF01',
    #     password='111111',
    # ).mode('overwrite').save()
    # resDF02.repartition(1).write.format('jdbc').options(
    #     url='jdbc:mysql://hdp:3306/test?characterEncoding=utf-8&useSSL=false',
    #     driver='com.mysql.jdbc.Driver',  # the driver for MySQL
    #     user='root',
    #     dbtable='resDF02',
    #     password='111111',
    # ).mode('overwrite').save()
    # resDF03.repartition(1).write.format('jdbc').options(
    #     url='jdbc:mysql://hdp:3306/test?characterEncoding=utf-8&useSSL=false',
    #     driver='com.mysql.jdbc.Driver',  # the driver for MySQL
    #     user='root',
    #     dbtable='resDF03',
    #     password='111111',
    # ).mode('overwrite').save()


