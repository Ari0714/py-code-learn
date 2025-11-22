# 示例：通过Python发送机器人消息
import findspark
findspark.init()
import requests
import pandas as pd
import time
from fear_and_greed import get
import datetime
import requests
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession

def sendMsg(msg):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0c90c9da-8b10-40b1-9818-61d73758e683"
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    requests.post(webhook_url, json=data)


if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    # 填写你的API密钥
    api_key = "9b0740741cc74bb2ab03dd90b74e8061"
    # symbol = "TSLA"
    interval = "1day"  # 或者 "5min", "1h", "1wk" 等
    time_period = 14  # RSI的时间周期
    start_date = "2024-11-22"
    end_date = "2025-11-22"

    for symbol in ["QQQ", "NBIS", "IREN", "CIFR", "WULF",
                   "NVDA", "TSLA", "GOOG",
                   "PLTR", "TSM", "AVGO", "HOOD", "AMD",
                   "RKLB","ASTS","OMDS",
                   "BE","EOSE"]:
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
            rsi_data = pd.DataFrame(data['values'])

            schema = StructType([StructField('datetime', StringType()),
                                 StructField('rsi', StringType())
                                 ])
            df = spark.createDataFrame(sc.parallelize(data['values']), schema)
            df.show()
            df.createOrReplaceTempView("rsi_realtime")
            resDF = spark.sql(f"""
                        select '{symbol}' symbol,
                                max(rsi) max_rsi, 
                                min(rsi) min_rsi, 
                                avg(rsi) avg_rsi, 
                                sum(if(`datetime`='2025-11-21',rsi,0)) cur_value, 
                                percentile_approx(rsi, 0.85) rsi_p8,
                                percentile_approx(rsi, 0.2) rsi_p2
                        from rsi_realtime
                        """)
            resDF.show()

            # 保存到mysql
            resDF.repartition(1).write.format('jdbc').options(
                url='jdbc:mysql://hdp:3306/us-stock?characterEncoding=utf-8&useSSL=false',
                driver='com.mysql.jdbc.Driver',  # the driver for MySQL
                user='root',
                dbtable=f'rsi_20251122_85',
                password='111111',
            ).mode('append').save()

            # data = response.json()
            # rsi_data = pd.DataFrame(data['values'])
            # rsi_data['datetime'] = pd.to_datetime(rsi_data['datetime'])
            # print(rsi_data[['datetime', 'rsi']])
            # rsi_data[['datetime', 'rsi']].to_csv(f"output/rsi-{symbol}.csv")
        else:
            print(f"Error: {response.status_code} - {response.text}")

        time.sleep(10)



