import findspark

findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import json
import glob
from datetime import datetime, date, timedelta
from utils.util import createFilePath
import time
import pandas as pd

from get_bollinger import get_bollinger
from get_cci import get_cci
from get_kd import get_kd
from get_macd import get_macd
from get_mfi import get_mfi
from get_rsi import get_rsi
from get_stocksPrices import get_data_insert


def get_all_data(stock_name, start_date, end_date, typee):
    print(f"\n==========={typee} - {stock_name}===========")
    get_data = pd.DataFrame([])
    if typee == 'bollinger':
        get_data = get_bollinger(stock_name, start_date, end_date)
    elif typee == 'cci':
        get_data = get_cci(stock_name, start_date, end_date)
    elif typee == 'kd':
        get_data = get_kd(stock_name, start_date, end_date)
    elif typee == 'macd':
        get_data = get_macd(stock_name, start_date, end_date)
    elif typee == 'mfi':
        get_data = get_mfi(stock_name, start_date, end_date)
    elif typee == 'price':
        get_data = get_data_insert(stock_name, start_date, end_date)
    elif typee == 'rsi':
        get_data = get_rsi(stock_name, start_date, end_date)

    if get_data is not None:
        print(get_data.tail())  # 打印最后几行数据
    createFilePath(f"output/{typee}/{end_date.year}/{end_date}/")
    try:
        get_data.to_csv(f"output/{typee}/{end_date.year}/{end_date}/{typee}-{stock_name}.csv")
    except:
        pass


def union_rsi(stock, end_date, year):
    # 直接读取
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(glob.glob(f"output/price/{year}/{end_date}/{stock}/part-00000-*-c000.csv")[0])
    inputDF.show()
    inputDF.createOrReplaceTempView('price')

    # 读取rsi
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(f"output/rsi/{year}/{end_date}/rsi-{stock}.csv")
    # inputDF.show()
    inputDF.createOrReplaceTempView('rsi')

    # 读取macd
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(f"output/macd/{year}/{end_date}/macd-{stock}.csv")
    # inputDF.show()
    inputDF.createOrReplaceTempView('macd')

    # 读取mfi
    # inputDF = spark.read \
    #     .format("csv") \
    #     .option("sep", ",") \
    #     .option("header", "true") \
    #     .load(f"output/mfi/{year}/{end_date}/mfi-{stock}.csv")
    # # inputDF.show()
    # inputDF.createOrReplaceTempView('mfi')

    # 读取kd
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(f"output/kd/{year}/{end_date}/kd-{stock}.csv")
    # inputDF.show()
    inputDF.createOrReplaceTempView('kd')

    # 读取cci
    # inputDF = spark.read \
    #     .format("csv") \
    #     .option("sep", ",") \
    #     .option("header", "true") \
    #     .load(f"output/cci/{year}/{end_date}/cci-{stock}.csv")
    # # inputDF.show()
    # inputDF.createOrReplaceTempView('cci')

    # 读取bollinger
    # inputDF = spark.read \
    #     .format("csv") \
    #     .option("sep", ",") \
    #     .option("header", "true") \
    #     .load(f"output/bollinger/{year}/{end_date}/bollinger-{stock}.csv")
    # # inputDF.show()
    # inputDF.createOrReplaceTempView('bollinger')

    # union
    #      select a.date, a.open, a.high, a.low, a.close, a.volume,
    #            b.rsi,
    #            c.macd, c.macd_signal, c.macd_hist,
    #            d.mfi,
    #            e.fast_k, e.fast_d,
    #            f.cci,
    #            g.upper_band, g.middle_band, g.lower_band
    #     from price a join rsi b join macd c join mfi d join kd e join cci f join bollinger g
    #     where (a.date = b.datetime and a.date = c.datetime and a.date = d.datetime
    #            and a.date = e.datetime and a.date = f.datetime and a.date = g.datetime)
    #     order by a.date
    resDF = spark.sql("""
        select a.date, a.open, a.high, a.low, a.close, a.volume,
               b.rsi,
               c.macd, c.macd_signal, c.macd_hist,
               e.fast_k, e.fast_d
        from price a join rsi b join macd c join kd e
        where (a.date = b.datetime and a.date = c.datetime
               and a.date = e.datetime)
        order by a.date
        """)
    resDF.show()
    resDF.repartition(1).write.mode(saveMode="Overwrite").option("header", "true").csv(
        f"output/rsi_union/{year}/{end_date}/{stock}")


if __name__ == '__main__':

    # 29 stocks
    stock_list = [
        "voo", "qqq", "smh",
        "nvda", "goog", "tsla", "aapl", "meta",
        "amd", "tsm", "avgo", "crdo", "mu",
        "iren", "cifr", "nbis", "wulf", "crwv", "clsk",
        "rklb", "asts", "onds",
        "be", "eose", "oklo", "te",
        "hood", "pltr", "app"]
    # stock_list = [
    #     "te"]

    # end_date = datetime.strptime("2021-12-31", "%Y-%m-%d").date()
    # 获取今日日期, 计算去年今日
    end_date = date.today()
    start_date = date(end_date.year - 1, end_date.month, end_date.day)

    for stock_name in stock_list:
        # 获取所有数据 # for typee in ['bollinger', 'cci', 'kd', 'macd', 'mfi', 'rsi', 'price']:
        for typee in ['kd', 'macd', 'rsi', 'price']:
            get_all_data(stock_name, start_date, end_date, typee)
            time.sleep(9)


    for stock_name2 in stock_list:
        try:
            union_rsi(stock_name2, end_date, end_date.year)
        except:
            pass
