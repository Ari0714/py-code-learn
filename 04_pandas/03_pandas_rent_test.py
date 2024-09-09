from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    r_pd = pd.read_csv('00_input/rent.txt', sep=',', header=0)
    print(r_pd)

    # 1. rent highest/lowes/average/middle price
    print(r_pd.sort_values('price', ascending=False).iloc[0,2])
    print(r_pd.sort_values('price', ascending=True).iloc[0,2])
    # print(r_pd.groupby('price').mean())
    print(r_pd.loc[:,'price'].median())

    # 2. rent highest/lowes price all info
    print('\n'+('*'*20))
    print(r_pd.sort_values('price', ascending=False).iloc[0, :])
    print(r_pd.sort_values('price', ascending=True).iloc[0, :])

    # 3. see house maximum people
    print('\n' + ('*' * 20))
    print(r_pd.groupby('area').agg({'name':'count'}).sort_values('name',ascending=False).iloc[0,:])

    # 4. type statictis
    print('\n' + ('*' * 20))
    print(r_pd.groupby('type').agg({'name': 'count'}).sort_values('name', ascending=False))

    # 5. see house top 5 blocks
    print('\n' + ('*' * 20))
    print(r_pd.groupby('name').agg({'area': 'count'}).sort_values('area', ascending=False).iloc[0:5, :])

    # 6. 五华, price < 1000, order price
    print('\n' + ('*' * 20))
    print(r_pd.query('area=="五华" & price < 1000').sort_values('price',ascending=False))



