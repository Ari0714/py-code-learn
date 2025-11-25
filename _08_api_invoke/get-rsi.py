import findspark

from _08_api_invoke.utils.util import createFilePath

findspark.init()
import pandas as pd
import time
from fear_and_greed import get
import datetime
import requests
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
from datetime import datetime, date, timedelta


def get_rsi(symbol, start_date, end_date):
    # spark = SparkSession.builder.getOrCreate()
    # sc = spark.sparkContext

    # 填写你的API密钥
    api_key = "9b0740741cc74bb2ab03dd90b74e8061"
    # symbol = "TSLA"
    interval = "1day"  # 或者 "5min", "1h", "1wk" 等
    time_period = 14  # RSI的时间周期

    # API请求URL
    url = f"https://api.twelvedata.com/rsi"
    params = {
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "apikey": api_key,
        "start_date": start_date,
        "end_date": end_date
    }
    # 发起请求
    response = requests.get(url, params=params)

    # 检查响应
    if response.status_code == 200:
        data = response.json()

        if "values" in data:
            rsi_data = pd.DataFrame(data['values'])
            return rsi_data
        else:
            print("没有获取到 MACD 数据。")
            return None

        # schema = StructType([StructField('datetime', StringType()),
        #                      StructField('rsi', StringType())
        #                      ])
        # df = spark.createDataFrame(sc.parallelize(data['values']), schema)
        # df.show()
        # df.createOrReplaceTempView("rsi_realtime")
        # resDF = spark.sql(f"""
        #             select '{symbol}' symbol,
        #                     max(rsi) max_rsi,
        #                     min(rsi) min_rsi,
        #                     avg(rsi) avg_rsi,
        #                     sum(if(`datetime`='2024-11-22',rsi,0)) cur_value,
        #                     percentile_approx(rsi, 0.85) rsi_p8,
        #                     percentile_approx(rsi, 0.2) rsi_p2
        #             from rsi_realtime
        #             """)
        # resDF.show()

        # 保存到mysql
        # resDF.repartition(1).write.format('jdbc').options(
        #     url='jdbc:mysql://hdp:3306/us-stock?characterEncoding=utf-8&useSSL=false',
        #     driver='com.mysql.jdbc.Driver',  # the driver for MySQL
        #     user='root',
        #     dbtable=f'rsi_20251122_85',
        #     password='111111',
        # ).mode('append').save()

        # data = response.json()
        # rsi_data = pd.DataFrame(data['values'])
        # rsi_data['datetime'] = pd.to_datetime(rsi_data['datetime'])
        # print(rsi_data[['datetime', 'rsi']])
    else:
        print(f"Error: {response.status_code} - {response.text}")

    time.sleep(10)

if __name__ == '__main__':

    start_date = "2023-11-22"
    end_date = "2024-11-22"
    # 获取今日日期, 计算去年今日
    # end_date = date.today()
    # start_date = date(end_date.year - 1, end_date.month, end_date.day)

    for i in [
        "voo", "qqq",
        "iren", "nbis", "crwv", "cifr", "wulf",
        "rklb", "asts", "onds",
        "nvda", "goog", "tsla", "aapl", "meta",
        "amd", "tsm", "avgo", "crdo", "sndk",
        "be", "eose", "oklo",
        "hood", "pltr", "app",
        "ibit"]:

    # for i in [
    #         "voo"]:
        print(f"\n==========={i}===========")
        rsi_data = get_rsi(i,start_date,end_date)

        # 如果获取到数据，展示结果
        if rsi_data is not None:
            print(rsi_data.tail())  # 打印最后几行数据

        createFilePath(f"output/rsi/2024/{end_date}/")
        try:
            rsi_data[['datetime', 'rsi']].to_csv(f"output/rsi/2024/{end_date}/rsi-{i}.csv")
        except:
            pass

        time.sleep(10)




