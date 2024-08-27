from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    pd1 = pd.read_csv('00_input/data.csv', sep='\t', header=0)
    print(pd1)
    print(pd1['city'])
    print(pd1[0:1])
    print(pd1['city'][0:1])

    # loc
    print("*" * 20)
    print(pd1.loc[1])
    print(pd1.loc[:,'size'])
    print(pd1.loc[0:3, 'advantage':'education'])
    print(pd1.loc[0, 'city'])

    # iloc（similar to loc，column index -》 position index）
    print("*" * 20)
    print(pd1.iloc[0:1])
    print(pd1.iloc[:,0:2])
    print(pd1.iloc[0:2, 0:2])
    pd1.iloc[2, 2] = 'abc'

    # filter
    print("*" * 20)
    pd1_filter = pd1['salary'] > 20000
    print(pd1_filter)
    pd1_filter_data = pd1[pd1['salary'] > 20000]
    print(pd1_filter_data)
    pd1_query = pd1.query('salary>20000')
    print(pd1_query)

    # write
    print("*" * 20)
    pd1_query.to_csv('00_input/output.csv',sep=',',header=True,index=False)
