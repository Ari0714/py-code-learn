# import yfinance
#
# data = yfinance.download('QQQ')
#
# print(data)
import time

import requests


def get_daily_change_percent(symbol, apikey='9b0740741cc74bb2ab03dd90b74e8061'):
    # url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=365&apikey={apikey}"
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&start_date=2024-07-05&end_date=2025-07-05&apikey={apikey}&outputsize=5000"

    resp = requests.get(url).json()
    try:
        # print(resp['values'])
        latest = resp['values']

        # for i in latest:
        #     # dt = resp['values'][1]['datetime']
        #     # latest = float(resp['values'][0]['close'])
        #     # prev = float(resp['values'][1]['close'])
        #     # change_pct = ((latest - prev) / prev) * 100
        #     # return round(change_pct, 2)
        return latest
    except Exception as e:
        print(f"⚠️ 解析失败: {e}")
        return None





def get_data_insert(indexx):
    data = get_daily_change_percent(indexx)
    print(data)

    import findspark
    findspark.init()
    from datetime import datetime, timedelta
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
    from pyspark.sql import SparkSession
    import json

    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    inputRDD = sc.parallelize(data)
    # inputRDD.foreach(lambda x:print(x))

    # targetRDD = inputRDD.map(lambda x: (json.loads(json.dumps(x))['datetime'],json.loads(json.dumps(x))['close']))

    schema = StructType([StructField('datetime', StringType()),
                         StructField('close', StringType())
                         ])

    df = spark.createDataFrame(inputRDD,schema)
    df.show()
    df.createOrReplaceTempView("history_data")

    spark.sql("""
                select min(datetime) min, max(datetime) max, count(*) cnt from history_data
                """).show()

    legDF = spark.sql("""
                select *, round(((close - last_close) / last_close) *100,2) as ratio from (  
                select *,
                    LAG(close, 1) OVER (ORDER BY datetime) AS last_close
                 from history_data
                 ) t
                """)
    legDF.createOrReplaceTempView("middle_table")


    resDF = spark.sql("""
            select 
            sum(if(ratio < -1.0,1,0)) as `1.0`,
            sum(if(ratio < -1.1,1,0)) as `1.1`,
            sum(if(ratio < -1.2,1,0)) as `1.2`,
            sum(if(ratio < -1.3,1,0)) as `1.3`,
            sum(if(ratio < -1.4,1,0)) as `1.4`,
            sum(if(ratio < -1.5,1,0)) as `1.5`,
            sum(if(ratio < -1.6,1,0)) as `1.6`,
            sum(if(ratio < -1.7,1,0)) as `1.7`,
            sum(if(ratio < -1.8,1,0)) as `1.8`,
            sum(if(ratio < -1.9,1,0)) as `1.9`,
            sum(if(ratio < -2.0,1,0)) as `2.0`,
            sum(if(ratio < -2.1,1,0)) as `2.1`,
            sum(if(ratio < -2.2,1,0)) as `2.2`,
            sum(if(ratio < -2.3,1,0)) as `2.3`,
            sum(if(ratio < -2.4,1,0)) as `2.4`,
            sum(if(ratio < -2.5,1,0)) as `2.5`,
            sum(if(ratio < -2.6,1,0)) as `2.6`,
            sum(if(ratio < -2.7,1,0)) as `2.7`,
            sum(if(ratio < -2.8,1,0)) as `2.8`,
            sum(if(ratio < -2.9,1,0)) as `2.9`,
            sum(if(ratio < -3.0,1,0)) as `3.0`
            from middle_table
                """)
    resDF.show()

    # 保存到mysql
    legDF.repartition(1).write.format('jdbc').options(
        url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
        driver='com.mysql.jdbc.Driver',  # the driver for MySQL
        user='root',
        dbtable=str(indexx).lower(),
        password='cj111111',
    ).mode('overwrite').save()

if __name__ == '__main__':

    # ["NVDA", "AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "META","QQQ"]:
    # for i in ["NVDA", "AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "META","QQQ"]:
    #     get_data_insert(i)

    # ["PLTR", "MSTR", "TSM", "AVGO", "NFLX", "SMCI", "HOOD","COIN"]:
    # for i in ["PLTR", "MSTR", "TSM", "AVGO", "NFLX", "SMCI", "HOOD","COIN"]:
    #     get_data_insert(i)
    #     time.sleep(20)

    # ["IBIT"]:
    for i in ["IBIT"]:
        get_data_insert(i)
        time.sleep(20)






