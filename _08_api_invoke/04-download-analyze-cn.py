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


def get_insert(input_data, tab):
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(input_data)

    # targetRDD = inputRDD.map(lambda x: (json.loads(json.dumps(x))['datetime'],json.loads(json.dumps(x))['close']))

    inputDF.show()
    inputDF.createOrReplaceTempView("history_data")

    spark.sql("select min(dt) min, max(dt) max, count(*) cnt from history_data").show()

    # legDF = spark.sql(f"""
    #             select *, round(((close - last_close) / last_close) *100,2) as ratio from (
    #                 select
    #                    '{tab}' indexx,
    #                     *,
    #                     LAG(close, 1) OVER (ORDER BY dt) AS last_close
    #                 from history_data
    #              ) t
    #             """)
    # legDF.createOrReplaceTempView("middle_table")


    resDF = spark.sql(f"""
            select 
            '{tab}' indexx,
            sum(if(ratio <= -0.5,1,0)) as `-0.5`,
            sum(if(ratio <= -0.6,1,0)) as `-0.6`,
            sum(if(ratio <= -0.7,1,0)) as `-0.7`,
            sum(if(ratio <= -0.8,1,0)) as `-0.8`,
            sum(if(ratio <= -0.9,1,0)) as `-0.9`,
            sum(if(ratio <= -1.0,1,0)) as `-1.0`,
            sum(if(ratio <= -1.1,1,0)) as `-1.1`,
            sum(if(ratio <= -1.2,1,0)) as `-1.2`,
            sum(if(ratio <= -1.3,1,0)) as `-1.3`,
            sum(if(ratio <= -1.4,1,0)) as `-1.4`,
            sum(if(ratio <= -1.5,1,0)) as `-1.5`,
            sum(if(ratio <= -1.6,1,0)) as `-1.6`,
            sum(if(ratio <= -1.7,1,0)) as `-1.7`,
            sum(if(ratio <= -1.8,1,0)) as `-1.8`,
            sum(if(ratio <= -1.9,1,0)) as `-1.9`,
            sum(if(ratio <= -2.0,1,0)) as `-2.0`,
            sum(if(ratio <= -2.1,1,0)) as `-2.1`,
            sum(if(ratio <= -2.2,1,0)) as `-2.2`,
            sum(if(ratio <= -2.3,1,0)) as `-2.3`,
            sum(if(ratio <= -2.4,1,0)) as `-2.4`,
            sum(if(ratio <= -2.5,1,0)) as `-2.5`,
            sum(if(ratio <= -2.6,1,0)) as `-2.6`,
            sum(if(ratio <= -2.7,1,0)) as `-2.7`,
            sum(if(ratio <= -2.8,1,0)) as `-2.8`,
            sum(if(ratio <= -2.9,1,0)) as `-2.9`,
            sum(if(ratio <= -3.0,1,0)) as `-3.0`,
            sum(if(ratio <= -3.1,1,0)) as `-3.1`,
            sum(if(ratio <= -3.2,1,0)) as `-3.2`,
            sum(if(ratio <= -3.3,1,0)) as `-3.3`,
            sum(if(ratio <= -3.4,1,0)) as `-3.4`,
            sum(if(ratio <= -3.5,1,0)) as `-3.5`,
            sum(if(ratio <= -3.6,1,0)) as `-3.6`,
            sum(if(ratio <= -3.7,1,0)) as `-3.7`,
            sum(if(ratio <= -3.8,1,0)) as `-3.8`,
            sum(if(ratio <= -3.9,1,0)) as `-3.9`,
            sum(if(ratio <= -4.0,1,0)) as `-4.0`,
            sum(if(ratio <= -4.1,1,0)) as `-4.1`,
            sum(if(ratio <= -4.2,1,0)) as `-4.2`,
            sum(if(ratio <= -4.3,1,0)) as `-4.3`,
            sum(if(ratio <= -4.4,1,0)) as `-4.4`,
            sum(if(ratio <= -4.5,1,0)) as `-4.5`,
            sum(if(ratio <= -4.6,1,0)) as `-4.6`,
            sum(if(ratio <= -4.7,1,0)) as `-4.7`,
            sum(if(ratio <= -4.8,1,0)) as `-4.8`,
            sum(if(ratio <= -4.9,1,0)) as `-4.9`,
            sum(if(ratio <= -5.0,1,0)) as `-5.0`,
            sum(if(ratio <= -5.1,1,0)) as `-5.1`,
            sum(if(ratio <= -5.2,1,0)) as `-5.2`,
            sum(if(ratio <= -5.3,1,0)) as `-5.3`,
            sum(if(ratio <= -5.4,1,0)) as `-5.4`,
            sum(if(ratio <= -5.5,1,0)) as `-5.5`,
            sum(if(ratio <= -5.6,1,0)) as `-5.6`,
            sum(if(ratio <= -5.7,1,0)) as `-5.7`,
            sum(if(ratio <= -5.8,1,0)) as `-5.8`,
            sum(if(ratio <= -5.9,1,0)) as `-5.9`,
            sum(if(ratio <= -6.0,1,0)) as `-6.0`,
            sum(if(ratio <= -6.1,1,0)) as `-6.1`,
            sum(if(ratio <= -6.2,1,0)) as `-6.2`,
            sum(if(ratio <= -6.3,1,0)) as `-6.3`,
            sum(if(ratio <= -6.4,1,0)) as `-6.4`,
            sum(if(ratio <= -6.5,1,0)) as `-6.5`,
            sum(if(ratio <= -6.6,1,0)) as `-6.6`,
            sum(if(ratio <= -6.7,1,0)) as `-6.7`,
            sum(if(ratio <= -6.8,1,0)) as `-6.8`,
            sum(if(ratio <= -6.9,1,0)) as `-6.9`,
            sum(if(ratio <= -7.0,1,0)) as `-7.0`,
            sum(if(ratio <= -7.1,1,0)) as `-7.1`,
            sum(if(ratio <= -7.2,1,0)) as `-7.2`,
            sum(if(ratio <= -7.3,1,0)) as `-7.3`,
            sum(if(ratio <= -7.4,1,0)) as `-7.4`,
            sum(if(ratio <= -7.5,1,0)) as `-7.5`,
            sum(if(ratio <= -7.6,1,0)) as `-7.6`,
            sum(if(ratio <= -7.7,1,0)) as `-7.7`,
            sum(if(ratio <= -7.8,1,0)) as `-7.8`,
            sum(if(ratio <= -7.9,1,0)) as `-7.9`,
            sum(if(ratio <= -8.0,1,0)) as `-8.0`,
            sum(if(ratio <= -8.1,1,0)) as `-8.1`,
            sum(if(ratio <= -8.2,1,0)) as `-8.2`,
            sum(if(ratio <= -8.3,1,0)) as `-8.3`,
            sum(if(ratio <= -8.4,1,0)) as `-8.4`,
            sum(if(ratio <= -8.5,1,0)) as `-8.5`,
            sum(if(ratio <= -8.6,1,0)) as `-8.6`,
            sum(if(ratio <= -8.7,1,0)) as `-8.7`,
            sum(if(ratio <= -8.8,1,0)) as `-8.8`,
            sum(if(ratio <= -8.9,1,0)) as `-8.9`,
            sum(if(ratio <= -9.0,1,0)) as `-9.0`,
            sum(if(ratio <= -9.1,1,0)) as `-9.1`,
            sum(if(ratio <= -9.2,1,0)) as `-9.2`,
            sum(if(ratio <= -9.3,1,0)) as `-9.3`,
            sum(if(ratio <= -9.4,1,0)) as `-9.4`,
            sum(if(ratio <= -9.5,1,0)) as `-9.5`,
            sum(if(ratio <= -9.6,1,0)) as `-9.6`,
            sum(if(ratio <= -9.7,1,0)) as `-9.7`,
            sum(if(ratio <= -9.8,1,0)) as `-9.8`,
            sum(if(ratio <= -9.9,1,0)) as `-9.9`,
            sum(if(ratio <= -10.0,1,0)) as `-10.0`,
            sum(if(ratio <= -10.1,1,0)) as `-10.1`,
            sum(if(ratio <= -10.2,1,0)) as `-10.2`,
            sum(if(ratio <= -10.3,1,0)) as `-10.3`,
            sum(if(ratio <= -10.4,1,0)) as `-10.4`,
            sum(if(ratio <= -10.5,1,0)) as `-10.5`,
            sum(if(ratio <= -10.6,1,0)) as `-10.6`,
            sum(if(ratio <= -10.7,1,0)) as `-10.7`,
            sum(if(ratio <= -10.8,1,0)) as `-10.8`,
            sum(if(ratio <= -10.9,1,0)) as `-10.9`,
            sum(if(ratio <= -11.0,1,0)) as `-11.0`,
            sum(if(ratio <= -11.1,1,0)) as `-11.1`,
            sum(if(ratio <= -11.2,1,0)) as `-11.2`,
            sum(if(ratio <= -11.3,1,0)) as `-11.3`,
            sum(if(ratio <= -11.4,1,0)) as `-11.4`,
            sum(if(ratio <= -11.5,1,0)) as `-11.5`,
            sum(if(ratio <= -11.6,1,0)) as `-11.6`,
            sum(if(ratio <= -11.7,1,0)) as `-11.7`,
            sum(if(ratio <= -11.8,1,0)) as `-11.8`,
            sum(if(ratio <= -11.9,1,0)) as `-11.9`,
            sum(if(ratio <= -12.0,1,0)) as `-12.0`
            from history_data
            group by indexx
                """)
    resDF.show()

    # 保存到mysqlrea
    resDF.repartition(1).write.format('jdbc').options(
        url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
        driver='com.mysql.jdbc.Driver',  # the driver for MySQL
        user='root',
        dbtable='analysis_tab_cn_202508',
        password='cj111111',
    ).mode('append').save()

    # 保存到mysql
    # inputDF.repartition(1).write.format('jdbc').options(
    #     url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
    #     driver='com.mysql.jdbc.Driver',  # the driver for MySQL
    #     user='root',
    #     dbtable=tab,
    #     password='cj111111',
    # ).mode('overwrite').save()


if __name__ == '__main__':
    get_insert("input/159941历史数据.csv", 'inner159941')
    get_insert("input/518880历史数据.csv", 'inner518880')
