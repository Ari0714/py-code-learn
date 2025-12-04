import time

import requests
import findspark

findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import json
from datetime import datetime, date, timedelta


def get_daily_change_percent(symbol, start_date, end_date):

    apikey = '9b0740741cc74bb2ab03dd90b74e8061'
    # url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=365&apikey={apikey}"
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&start_date={start_date}&end_date={end_date}&apikey={apikey}&outputsize=5000"

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


def get_data_insert(symbol, start_date, end_date):
    data = get_daily_change_percent(symbol, start_date, end_date)
    # print(data)

    if data != None:
        spark = SparkSession.builder.getOrCreate()
        sc = spark.sparkContext

        inputRDD = sc.parallelize(data)
        # inputRDD.foreach(lambda x:print(x))

        # targetRDD = inputRDD.map(lambda x: (json.loads(json.dumps(x))['datetime'],json.loads(json.dumps(x))['close']))

        schema = StructType([StructField('datetime', StringType()),
                             StructField('open', StringType()),
                             StructField('high', StringType()),
                             StructField('low', StringType()),
                             StructField('close', StringType()),
                             StructField('volume', StringType())
                             ])

        df = spark.createDataFrame(inputRDD, schema)
        df.show()
        df.createOrReplaceTempView("history_data")

        # 保存
        resDF = spark.sql("select datetime as date, open, high, low, close, volume from history_data")
        resDF.repartition(1).write.mode(saveMode="Overwrite").option("header","true").csv(f"output/price/{end_date.year}/{end_date}/{symbol}")
    else:
        print("没有获取到 rsi 数据。")


if __name__ == '__main__':

    end_date = datetime.strptime("2025-12-3", "%Y-%m-%d").date()
    # 获取今日日期, 计算去年今日
    # end_date = date.today()
    start_date = date(end_date.year - 10, end_date.month, end_date.day)

    # for i in [
    #           "voo", "qqq",
    #           "iren", "nbis", "crwv", "cifr", "wulf","clsk",
    #           "rklb", "asts", "onds",
    #           "nvda", "goog", "tsla", "aapl", "meta",
    #           "amd", "tsm", "avgo", "crdo", "sndk",
    #           "be", "eose", "oklo",
    #           "hood","pltr","app",
    #           "ibit"]:
    for i in [
              "qqq"]:
        print(f"\n==========={i}===========")
        try:
            get_data_insert(i,start_date,end_date)
        except:
            pass

        time.sleep(10)
