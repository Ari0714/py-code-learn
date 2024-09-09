from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba


def cut_words(word):
    return list(jieba.cut(word))

if __name__ == '__main__':
    pd1 = pd.read_csv('00_input/data.csv', sep='\t', header=0)
    print(pd1)
    print(pd1.info())
    print(pd1.city)
    print("*" * 20)
    print(pd1['city'])
    print(pd1[0:1])
    print(pd1['city'][0:1])

    # loc
    print("loc"+("*" * 20))
    print(pd1.loc[2])  # 1 row easy to see
    print(pd1.loc[:,'size'])
    print(pd1.loc[0:3, 'advantage':'education'])
    print(pd1.loc[[0,1,2,3], ['advantage','city','education']])
    print(pd1.loc[0, 'city'])

    # iloc（similar to loc，column index -》 position index）
    print("*" * 20)
    print(pd1.iloc[0:1])
    print(pd1.iloc[:,0:2])
    print(pd1.iloc[0:2, 0:2])
    pd1.iloc[2, 2] = 'abc'



    # write
    # print("*" * 20)
    # pd1_query.to_csv('00_input/output.csv',sep=',',header=True,index=False)

    # drop duplicate
    print("*" * 20)
    pd1_unique = pd1.id.unique()
    print(len(pd1_unique))
    drop_duplicate = pd1.duplicated(subset='id',keep='first')

    # apply
    pd1_apply = pd1.advantage.apply(cut_words)
    print(pd1_apply)



