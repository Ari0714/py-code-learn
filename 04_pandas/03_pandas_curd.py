from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    r_pd = pd.read_csv('00_input/data2.txt', sep=',',header=None,names=['id','name','profession'])
    # print(r_pd)

    'row manipulate'
    # append
    ser = pd.Series([3, 'cad', 'driver'], index=['id', 'name', 'profession'])
    r_pd2 = r_pd.append(ser,ignore_index=True)
    # print(r_pd2)

    # modify
    r_pd2.loc[1,'id'] = 11
    # print(r_pd2)

    # drop
    # r_pd2.drop([1,2])
    # print(r_pd2)

    'column manipulate'
    # add
    r_pd2['country'] = ['China','Germen','France']
    # print(r_pd2)

    # drop: return new df
    r_pd3 = r_pd2.drop(['country'],axis=1)
    print(r_pd3)







