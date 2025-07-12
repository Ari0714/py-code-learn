import findspark
findspark.init()
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession
import jieba

# 处理时间 2020/5/19 => 2020-05-19
def f0(x):
    return str(datetime.strptime(x, '%Y/%m/%d').date())

def f1(x):
    strings = x.split("\t")
    return (f0(strings[0]), strings[1], strings[2], strings[3], strings[4])

# 获取日期的前一天
def f2(x):
    return str(datetime.strptime(x, '%Y-%m-%d').date() + timedelta(days=-1))

# dataframe => rdd
def df2rdd(inputDF):
    inputDF.select("province","specialty").rdd.map(tuple).foreach(lambda x:print(x))

# 02_hbase => dataframe
def rdd2df(rdd):
    schema = StructType([StructField('day', StringType()),
                         StructField('county', StringType()),
                         StructField('state', StringType()),
                         StructField('confirm', StringType()),
                         StructField('death', StringType())
                         ])
    df = spark.createDataFrame(rdd, schema)

# jieba切词
def jiebe_cut(rdd):
    rdd.flatMap(lambda x:jieba.cut(x))


if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    # 读取数据: day	county	state	confirm	death
    inputRDD = sc.textFile("00_input/data.csv") \
        .filter(lambda x: "day" not in x) \
        .filter(lambda x: len(x) > 0)

    # 结构转换
    mapRDD = inputRDD.map(lambda x: f1(x))

    # 定义schema
    schema = StructType([StructField('day', StringType()),
                         StructField('county', StringType()),
                         StructField('state', StringType()),
                         StructField('confirm', StringType()),
                         StructField('death', StringType())
                         ])

    # 直接读取
    inputDF = spark.read \
        .format("csv") \
        .option("sep", ",") \
        .schema(schema) \
        .option("header", "false") \
        .load("00_input/doctors.txt")


    # 转化为dataFrame
    df = spark.createDataFrame(mapRDD, schema)
    df.show()
    # 创建临时表
    df.createOrReplaceTempView('info')

    # 1) 统计截止5月10日的累计确诊人数(*)
    resultult01 = spark.sql("""
            select sum(confirm) as totalconfirm
            from info
            where day = '2020-05-10'
             """)
    # resultult01.show()

    # 2) 统计截止3月28日的累计死亡人数(*)
    resultult02 = spark.sql("""
                select sum(death) as totaldeath
                from info
                where day = '2020-03-28' 
                 """)
    # result02.show()

    # 3) 统计3月10日的新增确诊人数和新增死亡人数(**)
    resultDF03 = spark.sql("""
            SELECT *,csm - lag(csm) over(order by day) case_up, dsm - lag(dsm) over(order by day) death_up from (
                SELECT day,SUM(confirm) csm, SUM(death) dsm
                from info
                GROUP by day
            ) where day = '2020-03-10' or day = '2020-03-09'
            """)
    # resultDF03.show()

    # 4) 统计截止2月10日，各州的累计确诊人数,只保留人数不为0的,结果存储在新表confirm_by_state_2_10中(**,在mysql中输入命令完成)
    result04 = spark.sql("""
                       select state, sum(confirm) as totalconfirm
                       from info
                       where day = '2020-02-10'
                       group by state
                       having totalconfirm > 0
                        """)
    # result04.show()
    # 写入mysql
    url = 'jdbc:mysql://hdp:3306/test?useSSL=false'
    auth_mysql = {"user": "root", "password": "111111"}
    # result04.write.jdbc(url, 'confirm_by_state_2_10', mode='overwrite', properties=auth_mysql)

    # 5) 统计截止3月10日，各州的累计死亡人数,只保留人数不为0的,结果存储在新表death_by_state_3_10中(**,在mysql中输入命令完成)
    result05 = spark.sql("""
                       select state, sum(death) as totaldeath
                       from info
                       where day = '2020-03-10'
                       group by state
                       having totaldeath > 0
                        """)
    # result05.show()
    # result05.write.jdbc(url, 'death_by_state_3_10', mode='overwrite', properties=auth_mysql)

    # 6) 统计截止3月5日，确诊人数最多的十个州(**)
    result06 = spark.sql("""
               select state, sum(confirm) as totalconfirm
               from info
               where day = '2020-03-05'
               group by state
               order by totalconfirm desc
               limit 10
                """)
    # result06.show()

    # 7) 统计截止4月30日，死亡人数最多的十个州,只保留人数不为0的(**)
    result07 = spark.sql("""
                   select state, sum(death) as totaldeath
                   from info
                   where day = '2020-04-30'
                   group by state
                   having totaldeath > 0
                   order by totaldeath desc
                   limit 10
                    """)
    # result07.show()

    # 8) 统计截止3月18日,确诊人数最少的十个州(**)
    result08 = spark.sql("""
                   select state, sum(confirm) as totalconfirm
                   from info
                   where day = '2020-03-18'
                   group by state
                   order by totalconfirm
                   limit 10
                    """)
    # result08.show()

    # 9) 统计截止3月25日，死亡人数最少的十个州,只保留人数不为0的(**)
    result09 = spark.sql("""
                       select state, sum(death) as totaldeath
                       from info
                       where day = '2020-03-25'
                       group by state
                       having totaldeath > 0
                       order by totaldeath
                       limit 10
                        """)
    # result09.show()

    # 10) 统计截止4月13日，全美的病死率。病死率 = 死亡数/确诊数(**)
    result10 = spark.sql("""
                select 'USA' as country, round(sum(death)/sum(confirm),4) as deathRate
                from info 
                where day = '2020-04-13'
                """)
    # result10.show()

    # 11) 统计截止4月13日，各州的病死率。病死率 = 死亡数/确诊数(**)
    result11 = spark.sql("""
                    select state, round(sum(death)/sum(confirm),4) as deathRate
                    from info 
                    where day = '2020-04-13'
                    group by state
                    """)
    # result11.show()

    # 12)统计每个月确诊总人数(**)
    result12 = spark.sql("""
                      select date_format(day,'yyyy-MM') monthh, sum(confirm) as totalconfirm
                      from info
                      group by date_format(day,'yyyy-MM')
                       """)
    # result12.show()

    # 13)统计每个月死亡总人数(**)
    result13 = spark.sql("""
                     select date_format(day,'yyyy-MM') monthh, sum(death) as totaldeath
                     from info
                     group by date_format(day,'yyyy-MM')
                      """)
    # result13.show()

    # 14)统计截止哪一天总确诊人数首次超过100万人(**)
    result14 = spark.sql("""
                      select day, sum(confirm) as totalconfirm
                      from info
                      group by day
                      having totalconfirm >= 1000000
                      order by day
                      limit 1
                    """)
    # result14.show()

    # 15)统计截止哪一天总死亡人数首次超过7万人(**)
    result15 = spark.sql("""
                      select day, sum(death) as totaldeath
                      from info
                      group by day
                      having totaldeath >= 70000
                      order by day
                      limit 1
                    """)
    # result15.show()



    '''新加入'''
    # 16)统计截止每个月底累计确诊人数最多的3个州(***)
    result16 = spark.sql("""
                     select monthh, state from (
                        select *, row_number() over(partition by monthh order by max_confirm desc) rk
                        from (
                            select state, date_format(day,'yyyy-MM') monthh, max(confirm) max_confirm
                            from info
                            group by state, date_format(day,'yyyy-MM')
                             )
                        ) t 
                    where rk <= 3
                           """)
    result16.show()

    # 17)统计截止4月30日每个州累计死亡人数最多的3个县(***)
    result17 = spark.sql("""
                    select state, county from (
                        select *, row_number() over(partition by state order by max_death desc) rk
                            from (
                                select state, county, max(death) max_death
                                from info
                                where day = '2020-04-30'
                                group by state, county
                                 )
                        ) t 
                    where rk <= 3
                               """)
    result17.show()

    # 18)统计每个月新增确诊人数最多的3个州(** **)
    result18 = spark.sql("""
                select monthh, state from (
                    select *, row_number() over(partition by monthh order by up_confirm desc) rk
                    from (
                        select state, date_format(day,'yyyy-MM') monthh, max(confirm) - min(confirm) up_confirm
                        from info
                        group by state, date_format(day,'yyyy-MM')
                         )
                    ) t 
                where rk <= 3
                                   """)
    result18.show()

    # 19)统计每个月新增死亡人数最多的3个州(** **)
    result19 = spark.sql("""
                    select monthh, state from (
                        select *, row_number() over(partition by monthh order by up_confirm desc) rk
                        from (
                            select state, date_format(day,'yyyy-MM') monthh, max(death) - min(death) up_confirm
                            from info
                            group by state, date_format(day,'yyyy-MM')
                             )
                        ) t 
                    where rk <= 3
                                       """)
    result19.show()

    # 20)统计California截止每个月底累计确诊人数最多的3个县(***)
    result20 = spark.sql("""
                 select monthh, county from (
                    select *, row_number() over(partition by monthh order by max_confirm desc) rk
                    from (
                        select county, date_format(day,'yyyy-MM') monthh, max(confirm) max_confirm
                        from info
                        where state = 'California'
                        group by county, date_format(day,'yyyy-MM')
                         )
                    ) t 
                where rk <= 3
                       """)
    result20.show()

    # 21)统计California每个月新增确诊人数最多的3个县(****)
    result21 = spark.sql("""
                select monthh, county from (
                    select *, row_number() over(partition by monthh order by up_confirm desc) rk
                    from (
                        select county, date_format(day,'yyyy-MM') monthh, max(confirm) - min(confirm) up_confirm
                        from info
                        where state = 'California'
                        group by county, date_format(day,'yyyy-MM')
                         )
                    ) t 
                where rk <= 3
                           """)
    result21.show()

    # 22)统计California每个月新增死亡人数最多的3个县(****)
    result22 = spark.sql("""
                select monthh, county from (
                    select *, row_number() over(partition by monthh order by up_death desc) rk
                    from (
                        select county, date_format(day,'yyyy-MM') monthh, max(death) - min(death) up_death
                        from info
                        where state = 'California'
                        group by county, date_format(day,'yyyy-MM')
                         )
                    ) t 
                where rk <= 3
                           """)
    result22.show()

    # 23)统计Indiana截止每个月底累计确诊人数最多的3个县(***)
    result23 = spark.sql("""
                select monthh, county from (
                    select *, row_number() over(partition by monthh order by max_confirm desc) rk
                    from (
                        select county, date_format(day,'yyyy-MM') monthh, max(confirm) max_confirm
                        from info
                        where state = 'Indiana'
                        group by county, date_format(day,'yyyy-MM')
                         )
                    ) t 
                where rk <= 3
                           """)
    result23.show()

    # 24)统计Indiana每个月新增确诊人数最多的3个县(****)
    result24 = spark.sql("""
                select monthh, county from (
                    select *, row_number() over(partition by monthh order by up_death desc) rk
                    from (
                        select county, date_format(day,'yyyy-MM') monthh, max(death) - min(death) up_death
                        from info
                        where state = 'Indiana'
                        group by county, date_format(day,'yyyy-MM')
                         )
                    ) t 
                where rk <= 3
                           """)
    result24.show()

    # 25)统计Indiana每个月新增死亡人数最多的3个县(****)
    result25 = spark.sql("""
                select monthh, county from (
                    select *, row_number() over(partition by monthh order by up_death desc) rk
                    from (
                        select county, date_format(day,'yyyy-MM') monthh, max(death) - min(death) up_death
                        from info
                        where state = 'Indiana'
                        group by county, date_format(day,'yyyy-MM')
                         )
                    ) t 
                where rk <= 3
                           """)
    result25.show()


    # 保存
    # resDF01.repartition(1).write.mode(saveMode="Overwrite").json("output/01")
    # resDF02.repartition(1).write.mode(saveMode="Overwrite").json("output/02")
    # resDF03.repartition(1).write.mode(saveMode="Overwrite").json("output/03")