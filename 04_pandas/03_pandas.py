from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    scores = np.random.randint(40, 100, (10, 5))
    print(scores)

    score_df = pd.DataFrame(scores)
    print(score_df)

    subject = ['chinese', 'math', 'music', 'pe', 'art']
    stu = ['stu' + str(i) for i in range(score_df.shape[0])]
    score_df2 = pd.DataFrame(scores, columns=subject, index=stu)
    print(score_df2)

    # property && method
    print("*" * 20)
    d = {'name': pd.Series(['p1', 'p2', "p3", 'p4', 'p5', 'p6', 'p7']),
         'age': pd.Series(['15', '16', "17", '18', '19', '20', '23']),
         'gender': pd.Series(['male', 'male', "male", 'female', 'female', 'female', 'female'])
         }
    p2 = pd.DataFrame(d)
    print(p2)
    print("*" * 20)
    print(p2.T)
    print("*" * 20)
    print(p2.values)
    print("*" * 20)
    print(p2.axes)
    print("*" * 20)
    print(p2.empty)
    print("*" * 20)
    print(p2.ndim)
    print("*" * 20)
    print(p2.shape)

    print("*" * 20)
    p2_s = p2.shift(1, freq=None, axis=0)  # 0 up-down shift，1 left-right shift
    print(p2_s)

    '''df operation'''
    print("*" * 20)
    print(p2['name'][0])
    print(p2['age'].sum)

    '''df visualization'''
    print("*" * 20)
    v1 = pd.DataFrame(np.random.randn(20,5),index=pd.date_range('5/20/2023',periods=20),columns=list('abcde'))
    print(v1)
    # v1.plot()
    # plt.show()

    v2 = pd.DataFrame(np.random.randn(20,5),columns=['a','b','c','d','e'])
    print(v2)
    # v2.plot.bar()
    # plt.show()

    v3 = pd.DataFrame(np.random.randn(30, 5), columns=['a', 'b', 'c', 'd', 'e'])
    print(v3)
    # v3.plot.scatter(x='a',y='e')
    # plt.show()

    v4 = pd.DataFrame(3 * np.random.rand(2), index=['boy', 'girl'], columns=['L'])
    print(v4)
    v4.plot.pie(subplots=True)
    plt.show()



