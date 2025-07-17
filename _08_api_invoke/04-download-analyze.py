import time

import requests
import findspark

findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import json


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

    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    inputRDD = sc.parallelize(data)
    # inputRDD.foreach(lambda x:print(x))

    # targetRDD = inputRDD.map(lambda x: (json.loads(json.dumps(x))['datetime'],json.loads(json.dumps(x))['close']))

    schema = StructType([StructField('datetime', StringType()),
                         StructField('close', StringType())
                         ])

    df = spark.createDataFrame(inputRDD, schema)
    df.show()
    df.createOrReplaceTempView("history_data")

    spark.sql(f"select min(datetime) min, max(datetime) max, count(*) cnt from history_data").show()

    legDF = spark.sql(f"""
                select *, round(((close - last_close) / last_close) *100,2) as ratio from (  
                    select  '{indexx}' indexx, 
                            *,
                            LAG(close, 1) OVER (ORDER BY datetime) AS last_close
                    from history_data
                 ) t
                """)
    legDF.createOrReplaceTempView("middle_table")

    resDF = spark.sql("""
            select 
            indexx,
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
            from middle_table
            group by indexx
                """)
    resDF.show()

    # 保存到mysql
    resDF.repartition(1).write.format('jdbc').options(
        url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
        driver='com.mysql.jdbc.Driver',  # the driver for MySQL
        user='root',
        dbtable='analysis_tab_202507',
        password='cj111111',
    ).mode('append').save()

    # 保存到mysql
    # legDF.repartition(1).write.format('jdbc').options(
    #     url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
    #     driver='com.mysql.jdbc.Driver',  # the driver for MySQL
    #     user='root',
    #     dbtable=str(indexx).lower()+'-202507',
    #     password='cj111111',
    # ).mode('overwrite').save()


if __name__ == '__main__':

    # ["IBIT", "QQQ","NVDA", "AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "META"]:
    # for i in ["IBIT", "QQQ","NVDA", "AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "META"]:
    #     get_data_insert(i)
    #     time.sleep(20)

    # ["PLTR", "MSTR", "TSM", "AVGO", "NFLX", "SMCI", "HOOD", "COIN", "AMD","MU"]
    # for i in ["PLTR", "MSTR", "TSM", "AVGO", "NFLX", "SMCI", "HOOD", "COIN", "AMD","MU"]:
    #     get_data_insert(i)
    #     time.sleep(20)

    # ["CRCL", "RGTI","IONQ","RKLB","ASTS","MP","SMR","QS","ENVX","CRDO","ROKU","RBLX"]
    for i in ["IONQ","RKLB","ASTS","MP","SMR","QS","ENVX","CRDO","ROKU","RBLX"]:
        get_data_insert(i)
        time.sleep(20)


