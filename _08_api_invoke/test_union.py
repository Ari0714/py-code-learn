
import findspark
findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import json
import glob
from datetime import datetime, date, timedelta

def union_rsi(stock,end_date, year):

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
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(f"output/mfi/{year}/{end_date}/mfi-{stock}.csv")
    # inputDF.show()
    inputDF.createOrReplaceTempView('mfi')

    # 读取kd
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(f"output/kd/{year}/{end_date}/kd-{stock}.csv")
    # inputDF.show()
    inputDF.createOrReplaceTempView('kd')

    # 读取cci
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(f"output/cci/{year}/{end_date}/cci-{stock}.csv")
    # inputDF.show()
    inputDF.createOrReplaceTempView('cci')

    # union
    resDF = spark.sql("""
        select a.date, a.open, a.high, a.low, a.close, a.volume,
               b.rsi,
               c.macd, c.macd_signal, c.macd_hist,
               d.mfi,
               e.fast_k, e.fast_d,
               f.cci
        from price a join rsi b join macd c join mfi d join kd e join cci f
        where (a.date = b.datetime and a.date = c.datetime and a.date = d.datetime 
               and a.date = e.datetime and a.date = f.datetime)
        order by a.date
        """)
    resDF.show()
    resDF.repartition(1).write.mode(saveMode="Overwrite").option("header", "true").csv(f"output/rsi_union/{year}/{end_date}/{stock}")


if __name__ == '__main__':

    # end_date = "2024-11-22"
    # 获取今日日期, 计算去年今日
    end_date = date.today()

    for i in [
              "voo", "qqq",
              "iren", "nbis", "crwv", "cifr", "wulf",
              "rklb", "asts", "onds",
              "nvda", "goog", "tsla", "aapl", "meta",
              "amd", "tsm", "avgo", "crdo", "sndk",
              "be", "eose", "oklo",
              "hood","pltr","app",
              "ibit"]:
        print(f"\n==========={i}===========")
        try:
            union_rsi(i,end_date,2025)
        except:
            pass



