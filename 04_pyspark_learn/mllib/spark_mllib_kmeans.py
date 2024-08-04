import findspark
findspark.init()
from pyspark.mllib.linalg import Vectors
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.ml.clustering import KMeans
from pyspark.ml.linalg import Vectors

'''
需求： 使用KMeans寻找【SepalLengthCm,SepalWidthCm】的聚类中心
'''
def f(x):
    rel = {}
    rel['features'] = Vectors.dense(float(x[1]),float(x[2]))
    return rel

if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    df = sc.textFile("input/Iris.csv")\
        .filter(lambda x: not str(x).__contains__('Id'))\
        .map(lambda line: line.split(','))\
        .map(lambda p: Row(**f(p))).toDF()
    df.show()

    # 使用kmeans模型训练
    kmeansmodel = KMeans().setK(3).setFeaturesCol('features').setPredictionCol('prediction').fit(df)

    # 寻找聚类中心
    results2 = kmeansmodel.clusterCenters()
    for item in results2:
        print(item)

    # 保存模型
    # kmeansmodel.save('output/kmeansmodel.model')


