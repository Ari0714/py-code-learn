import findspark
findspark.init()
from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame


# 处理时间 2020/5/19 => 2020-05-19
def f0(x):
    return str(datetime.strptime(x, '%Y/%m/%d').date())

def f1(x):
    strings = x.split("\t")
    return (f0(strings[0]), strings[1], strings[2], strings[3], strings[4])

# 获取日期的前一天
def f2(x):
    return str(datetime.strptime(x, '%Y-%m-%d').date() + timedelta(days=-1))


if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    # 读取数据: day	county	state	confirm	death
    inputRDD = sc.textFile("input/data.txt") \
        .filter(lambda x: "day" not in x) \
        .filter(lambda x: len(x) > 0)

    mapRDD = inputRDD.map(lambda x: f1(x))

    # 1) 统计截止每日的累计确诊人数
    result01 = mapRDD.map(lambda x: (x[0], int(x[3]))).reduceByKey(lambda x, y: x + y)
    # result01.foreach(lambda x: print(x))

    # 2) 统计截止每日的累计死亡人数
    result02 = mapRDD.map(lambda x: (x[0], int(x[4]))).reduceByKey(lambda x, y: x + y)
    # result02.foreach(lambda x: print(x))

    # 3) 统计每日的新增确诊人数
    yesterday_confirm = result01.map(lambda x: (f2(x[0]), x[1]))
    result03 = result01.join(yesterday_confirm).map(lambda x: (x[0], x[1][1] - x[1][0]))
    # result03.foreach(lambda x: print(x))

    # 4) 统计每日的新增死亡人数
    yesterday_death = result02.map(lambda x: (f2(x[0]), x[1]))
    result04 = result02.join(yesterday_death).map(lambda x: (x[0], x[1][1] - x[1][0]))
    # result04.foreach(lambda x: print(x))

    # 5) 统计截止5月19日，各州的累计确诊人数
    filterRDD = mapRDD.filter(lambda x: x[0] == '2020-05-19')
    result05 = filterRDD.map(lambda x: (x[2], int(x[3]))).reduceByKey(lambda x, y: x + y)
    # result05.foreach(lambda x: print(x))

    # 6) 统计截止5月19日，各州的累计死亡人数
    result06 = filterRDD.map(lambda x: (x[2], int(x[4]))).reduceByKey(lambda x, y: x + y)
    # result06.foreach(lambda x: print(x))

    # 7) 统计截止5月19日，累计确诊人数最多的十个州
    result07 = filterRDD.map(lambda x: (x[2], int(x[3]))).reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], False).take(10)
    # for i in result07:
    #     print(i)

    # 8) 统计截止5月19日，累计死亡人数最多的十个州
    result08 = filterRDD.map(lambda x: (x[2], int(x[4]))).reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], False).take(10)
    # for i in result08:
    #     print(i)

    # 9) 统计截止5月19日，累计确诊人数最少的十个州
    result09 = filterRDD.map(lambda x: (x[2], int(x[3]))).reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], True).take(10)
    # for i in result09:
    #     print(i)

    # 10) 统计截止5月19日，累计死亡人数最少的十个州
    result10 = filterRDD.map(lambda x: (x[2], int(x[4]))).reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], True).take(10)
    # for i in result10:
    #     print(i)

    # 11) 统计截止5月19日，全美的病死率。病死率 = 死亡数/确诊数
    confirm_num = filterRDD.map(lambda x: int(x[3])).sum()
    death_num = filterRDD.map(lambda x: int(x[4])).sum()
    # print("death_ratio: " + str(death_num / confirm_num))

    # 12) 统计截止5月19日，各州的病死率。
    state_confirm_num = filterRDD.map(lambda x: (x[2], int(x[3]))).reduceByKey(lambda x, y: x + y)
    state_death_num = filterRDD.map(lambda x: (x[2], int(x[4]))).reduceByKey(lambda x, y: x + y)
    state_death_ratio = state_confirm_num.join(state_death_num).map(lambda x: (x[0], x[1][1] / x[1][0]))
    # state_death_ratio.foreach(lambda x: print(x))

    # 13) 统计截止5月19日，病死率最高的十个州。
    result13 = state_death_ratio.sortBy(lambda x: x[1], False).take(10)
    # for i in result13:
    #     print(i)

    '''新加'''
    # 14) 统计截止5月19日，Florida确诊人数最多的五个country。
    result14 = filterRDD.filter(lambda x:x[2]=='Florida').map(lambda x: (x[1], int(x[3])))\
        .reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], False).take(5)
    for i in result14:
        print(i)

    # 15) 统计截止5月19日，New York确诊人数最多的五个country。
    result15 = filterRDD.filter(lambda x: x[2] == 'New York').map(lambda x: (x[1], int(x[3]))) \
        .reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], False).take(5)
    for i in result15:
        print(i)

    # 16) 统计截止5月19日，California确诊人数最多的五个country。
    result16 = filterRDD.filter(lambda x: x[2] == 'California').map(lambda x: (x[1], int(x[3]))) \
        .reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], False).take(5)
    for i in result16:
        print(i)

    # 17) 统计截止5月19日，Florida死亡人数最多的五个country。
    result17 = filterRDD.filter(lambda x: x[2] == 'Florida').map(lambda x: (x[1], int(x[4]))) \
        .reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], False).take(5)
    for i in result17:
        print(i)

    # 18) 统计截止5月19日，New York死亡人数最多的五个country。
    result18 = filterRDD.filter(lambda x: x[2] == 'New York').map(lambda x: (x[1], int(x[4]))) \
        .reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], False).take(5)
    for i in result18:
        print(i)

    # 19) 统计截止5月19日，California死亡人数最多的五个country。
    result19 = filterRDD.filter(lambda x: x[2] == 'California').map(lambda x: (x[1], int(x[4]))) \
        .reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda x: x[1], False).take(5)
    for i in result19:
        print(i)