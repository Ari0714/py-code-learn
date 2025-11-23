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
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&start_date=2024-11-22&end_date=2025-11-22&apikey={apikey}&outputsize=5000"

    resp = requests.get(url).json()
    try:
        print(resp['values'])
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
    # print(data)

    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    inputRDD = sc.parallelize(data)
    # inputRDD.foreach(lambda x:print(x))

    # targetRDD = inputRDD.map(lambda x: (json.loads(json.dumps(x))['datetime'],json.loads(json.dumps(x))['close']))

    schema = StructType([StructField('datetime', StringType()),
                         StructField('open', StringType()),
                         StructField('close', StringType()),
                         StructField('volume', StringType())
                         ])

    df = spark.createDataFrame(inputRDD, schema)
    df.show()
    df.createOrReplaceTempView("history_data")

    # spark.sql(f"select min(datetime) min, max(datetime) max, count(*) cnt from history_data").show()

    # legDF = spark.sql(f"""
    #             select *, round((close - open) * volume) / 10000 as liquity from (
    #                 select  '{indexx}' indexx,
    #                         *
    #                 from history_data
    #              ) t
    #             order by datetime
    #             """)
    # legDF.show()
    # legDF.createOrReplaceTempView("middle_table")

    # 保存
    resDF = spark.sql("select datetime as date, open, close, volume from history_data")
    resDF.repartition(1).write.mode(saveMode="Overwrite").option("header","true").csv(f"output/price/2025/{indexx}")


    # 保存到mysql
    # resDF.repartition(1).write.format('jdbc').options(
    #     url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
    #     driver='com.mysql.jdbc.Driver',  # the driver for MySQL
    #     user='root',
    #     dbtable='analysis_tab_202509',
    #     password='cj111111',
    # ).mode('append').save()


if __name__ == '__main__':

    # for i in ["VOO", "QQQ",
    #           "IREN", "NBIS", "CRWV", "CIFR", "WULF",
    #           "RKLB", "ONDS",
    #           "NVDA", "GOOG", "TSLA",
    #           "AMD", "TSM", "AVGO",
    #           "BE", "EOSE",
    #           "HOOD","PLTR",
    #           "IBIT"]:

    for i in [
              "mp"]:
        print(f"==========={i}===========")
        try:
            get_data_insert(i)
        except:
            pass

        time.sleep(15)

    # index & m7
    # for i in ["QQQ","NVDA","META","MSFT","GOOG","AMZN","AAPL","TSLA"]:
    #     get_data_insert(i)
    #     time.sleep(15)
    #
    # # coin
    # for i in ["HOOD","COIN","CRCL","BMNR","MSTR"]:
    #     get_data_insert(i)
    #     time.sleep(15)
    #
    # # semi
    # for i in ["AVGO","ORCL","AMD","CRDO","CLS","ALAB","TSM","MRVL"]:
    #     get_data_insert(i)
    #     time.sleep(15)
    #
    # # aa
    # for i in ["META","PLTR","APP"]:
    #     get_data_insert(i)
    #     time.sleep(15)
    #
    # # af
    # for i in ["APLD","IREN","CORZ","CRWV","NBIS"]:
    #     get_data_insert(i)
    #     time.sleep(15)
    #
    # # electricity & nuclear
    # for i in ["GEV","CEG","CCJ","BWXT","LEU","OKLO","VST","VRT","TGEN","FIX","AGX","BE"]:
    #     get_data_insert(i)
    #     time.sleep(15)
    #
    # # space
    # for i in ["RKLB","ASTS","JOBY","RCAT"]:
    #     get_data_insert(i)
    #     time.sleep(15)
    #
    # # finance
    # for i in ["SOFI","SEZL","PGY","OPFI","UPST","AFRM"]:
    #     get_data_insert(i)
    #     time.sleep(15)
    #
    # # medical
    # for i in ["HIMS","CRSP","TEM","UNH"]:
    #     get_data_insert(i)
    #     time.sleep(15)
    #
    # # quantum
    # for i in ["RGTI","IONQ"]:
    #     get_data_insert(i)
    #     time.sleep(15)

    # s
    # for i in ["RDDT","SERV","RBLX","SOUN","RBRK","SMCI","MP"]:
    #     get_data_insert(i)
    #     time.sleep(15)


    # for i in ["BE"]:
    #     get_data_insert(i)
    #     time.sleep(15)
