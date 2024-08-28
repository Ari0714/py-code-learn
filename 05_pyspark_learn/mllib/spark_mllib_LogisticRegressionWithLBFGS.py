import findspark
findspark.init()
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.sql import SparkSession



def f1(x):
    strings = x.split("\t")
    point = LabeledPoint(float(strings[13]), [float(strings[1]), float(strings[2]), float(strings[5])])
    return point

'''
预测心脏病
算法：线性回归 （0，1）
'''

if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    inputRDD = sc.textFile("00_input/heart.txt") \
        .filter(lambda x: "age" not in x)

    parseData = inputRDD.map(lambda x: f1(x))

    parseData.cache()
    parseData.foreach(lambda x: print(x))

    # 70%的训练集和30%的测试集
    splits = parseData.randomSplit([0.7, 0.3], seed=9)
    training = splits[0]
    test = splits[1]

    # 训练模型
    model = LogisticRegressionWithLBFGS.train(training, numClasses=3)

    # 模型预测，打印
    predictionAndLabels = test.map(lambda p: (p.label, model.predict(p.features)))
    predictionAndLabels.foreach(lambda x: print(x))

    # 计算预测准确率，打印
    trainErr = predictionAndLabels.filter(lambda lp: lp[0] != lp[1]).count() / float(parseData.count())
    print("Precision = " + str(1 - trainErr))
