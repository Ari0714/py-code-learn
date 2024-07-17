import argparse
import findspark
findspark.init()
from pyspark import SparkConf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DecimalType, FloatType
from pyspark.sql import SparkSession, DataFrame
from CollaborativeFiltering import CollaborativeFiltering

if __name__ == '__main__':

    conf = SparkConf().setAppName('collaborativeFiltering').setMaster("local[*]")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    data_path = "input/ratings.csv"
    model_path = "output/model_param"
    train_flag = True
    epoch = 10

    # 读取ratings
    ratingsInputDF = spark.read \
        .format("csv") \
        .option("header", "true") \
        .load("input/ratings.csv")
    ratingsInputDF.show()
    # 创建临时表
    ratingsInputDF.createTempView("ratings_info")

    # 数据清洗，类型转换
    ratingSamples = spark.sql("""
                                select cast(userId as int) as userIdInt,
                                       cast(productId as int) as productId,
                                       cast(rating as float) as ratingFloat
                                from ratings_info
                                where userId is not null
                            """)

    # 训练集、测试集数据划分
    training, test = ratingSamples.randomSplit((0.8, 0.2), seed=2022)

    # ALS开始训练
    cf = CollaborativeFiltering(spark_session=spark)

    if train_flag is True:
        cf.train(train_set=training,
                 user_col='userIdInt',
                 item_col='productId',
                 rating_col='ratingFloat',
                 epoch=epoch)

        cf.save(model_dir=model_path)
    else:
        cf.load(model_dir=model_path)

    # 训练损失值
    loss = cf.eval(test_set=test, label_col='ratingFloat', metric='rmse')
    print("[Root-mean-square error] {}".format(loss))

    # 为每个用户生成前3个金融产品推荐
    user_recs = cf.recommend_for_all_users(num_items=3)
    user_recs.show(10, False)

    # 为每个金融产品生成前3名用户推荐
    movie_recs = cf.recommend_for_all_items(num_users=3)
    movie_recs.show(10, False)

    # 为指定的一组用户生成前3个金融产品推荐
    user_data = ratingSamples.select("userIdInt").distinct().limit(10)
    user_sub_recs = cf.recommend_for_user_subset(dataset=user_data, num_items=3)
    user_sub_recs.show(10, False)

    # 为一组指定的金融产品生成前3名用户推荐
    movie_data = ratingSamples.select("productId").distinct().limit(10)
    movie_sub_recs = cf.recommend_for_item_subset(dataset=movie_data, num_users=3)
    movie_sub_recs.show(10, False)

    spark.stop()
