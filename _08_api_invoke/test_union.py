
import findspark
findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import json
import glob

def union_rsi(stock):
    # 直接读取
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(glob.glob(f"output/price/2025/{stock}/part-00000-*-c000.csv")[0])
    inputDF.show()
    inputDF.createOrReplaceTempView('price')

    # 读取rsi
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(f"output/rsi/rsi-{stock}.csv")
    inputDF.show()
    inputDF.createOrReplaceTempView('rsi')

    # 读取macd
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .option("header", "true") \
        .load(f"output/macd/macd-{stock}.csv")
    inputDF.show()
    inputDF.createOrReplaceTempView('macd')

    # union
    resDF = spark.sql("""
        select a.date, a.open, a.high, a.low, a.close, a.volume, 
               b.rsi,
               c.macd, c.macd_signal, c.macd_hist
        from price a join rsi b join macd c
        where (a.date = b.datetime and a.date = c.datetime)
        order by a.date
        """)
    resDF.show()
    resDF.repartition(1).write.mode(saveMode="Overwrite").option("header", "true").csv(f"output/rsi_union/{stock}")


if __name__ == '__main__':
    for i in [
              "voo", "qqq",
              "iren", "nbis", "crwv", "cifr", "wulf",
              "rklb", "asts", "onds",
              "nvda", "goog", "tsla", "aapl", "meta",
              "amd", "tsm", "avgo", "crdo", "sndk",
              "be", "eose", "oklo",
              "hood","pltr","app",
              "ibit"]:
        print(f"==========={i}===========")
        union_rsi(i)



