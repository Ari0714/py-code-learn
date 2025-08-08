import time
import findspark

findspark.init()
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import requests


def readFromMysql(spark):
    return spark.read.format("jdbc") \
        .options(url='jdbc:mysql://8.148.227.29:3306/us-stock?characterEncoding=utf-8&useSSL=false',
                 driver="com.mysql.jdbc.Driver",
                 dbtable='drop_ratio_202507',
                 user="root",
                 password='cj111111', ) \
        .load()


def sendMsg(msg):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0c90c9da-8b10-40b1-9818-61d73758e683"
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    requests.post(webhook_url, json=data)


def get_daily_change_percent(symbol, apikey):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=2&apikey={apikey}"
    resp = requests.get(url).json()
    try:
        # print(resp['values'])
        latest = float(resp['values'][0]['close'])
        prev = float(resp['values'][1]['close'])
        change_pct = ((latest - prev) / prev) * 100
        return round(change_pct, 2)
    except Exception as e:
        print(f"⚠️ 解析失败: {e}")
        return None


def getAllSymbol():
    index_dict = dict()

    apikey = "9b0740741cc74bb2ab03dd90b74e8061"  # 替换为你的 Twelve Data Key

    # index
    for symbol in ["QQQ"]:
        pct = get_daily_change_percent(symbol, apikey)
        index_dict[symbol] = pct

    # m7
    avg_sum = 0
    for symbol in ["NVDA", "AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "META"]:
        pct = get_daily_change_percent(symbol, apikey)
        index_dict[symbol] = pct
        avg_sum += pct
        print(f"{symbol} 昨日涨跌幅：{pct}%")
        time.sleep(8)
    index_dict['M7'] = round(avg_sum / 7, 2)

    # medium
    # for symbol in ["PLTR", "TSM", "AVGO", "NFLX", "HOOD", "AMD"]:
    #     pct = get_daily_change_percent(symbol, apikey)
    #     index_dict[symbol] = pct
    #     print(f"{symbol} 昨日涨跌幅：{pct}%")
    #     time.sleep(8)

    # small and extra
    # for symbol in ["RGTI","IONQ","RKLB","ASTS","MP","OKLO","CRDO"]:
    #     pct = get_daily_change_percent(symbol, apikey)
    #     index_dict[symbol] = pct
    #     print(f"{symbol} 昨日涨跌幅：{pct}%")
    #     time.sleep(8)

    # for k, v in index_dict.items():
    #     print(k, v)

    return index_dict


# 示例调用
if __name__ == '__main__':

    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    allsymbol = getAllSymbol()
    schema = StructType([StructField('indexx', StringType()),
                         StructField('real_ratio', StringType())
                         ])
    df = spark.createDataFrame(sc.parallelize(allsymbol.items()), schema)
    df.show()
    df.createOrReplaceTempView("drop_ratio_realtime")

    drop_ratio_dt = readFromMysql(spark)
    drop_ratio_dt.show()
    drop_ratio_dt.createOrReplaceTempView("drop_ratio_dt")

    resDF = spark.sql("""
                        SELECT 
                            a.indexx, 
                            a.real_ratio, 
                            concat_ws('/', -b.x1,-b.x2,-b.x3) fix_ratio, sum(if(a.real_ratio <= -b.x1,1,0)) + sum(if(a.real_ratio <= -b.x2,1,0)) + sum(if(a.real_ratio <= -b.x3,1,0)) warn_type
                        from drop_ratio_realtime a
                        join drop_ratio_dt b
                        where a.indexx = b.indexx
                        group by a.indexx, a.real_ratio, fix_ratio
                        order by cast(a.real_ratio as float)
                """)
    resDF.show()

    sends = time.strftime('%Y-%m-%d %H:%M', time.localtime()) + "\n"
    cols = resDF.rdd.map(tuple).collect()
    for i in cols:
        if (str(i[0]) in ["NVDA", "AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "META"]):
            sends += "\n" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])
    for i in cols:
        if (str(i[0]) in ["M7"]):
            sends += "\n-" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])
    for i in cols:
        if (str(i[0]) in ["QQQ"]):
            sends += "\n\n-" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])
    # sends += "\n"

    # for i in cols:
    #     if (str(i[0]) in ["PLTR", "TSM", "AVGO", "NFLX", "AMD"]):
    #         sends += "\n" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])
    # sends += "\n"

    # for i in cols:
    #     if (str(i[0]) in ["MP","CRDO"]):
    #         sends += "\n" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])
    # sends += "\n"

    # for i in cols:
    #     if (str(i[0]) in ["HOOD"]):
    #         sends += "\n" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])
    # for i in cols:
    #     if (str(i[0]) in ["IBIT"]):
    #         sends += "\n-" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])
    # sends += "\n"

    # for i in cols:
    #     if (str(i[0]) in ["RGTI","IONQ"]):
    #         sends += "\n" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])
    # sends += "\n"

    # for i in cols:
    #     if (str(i[0]) in ["RKLB","ASTS"]):
    #         sends += "\n" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])
    # sends += "\n"

    # for i in cols:
    #     if (str(i[0]) in ["OKLO"]):
    #         sends += "\n" + str(i[0]) + ": " + str(i[1]) + " | " + str(i[2]) + " | " + str(i[3])

    sendMsg(sends)
