from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    r_pd = pd.read_csv('00_input/data2.txt', sep=',', header=None, names=['id', 'name', 'profession'])
    print(r_pd)

    se1 = pd.Series([3,'fd','driver'],index=['id', 'name', 'profession'])
    se2 = pd.Series([4, 'dwf', 'engineer '], index=['id', 'name', 'profession'])
    r_pd2 = r_pd.append([se1,se2],ignore_index=True)
    print(r_pd2)

    # nlargest , nsmallest
    print(r_pd2.nlargest(3, 'id'))
    print(r_pd2.nsmallest(3, 'id'))

    # aggregate
    print('\n' + ('*' * 20))
    print(r_pd2.groupby('id').id.mean())   #avg
    print(r_pd2.groupby('id')['id'].max())
    print(r_pd2.groupby('id').agg({'id':'count','profession':'count'}))

    # filter query
    print('\n'+('*' * 20))
    r_pd2['salary'] = [200,500,145,787]
    print(r_pd2)
    pd1_filter = r_pd2['salary'] > 500
    print(pd1_filter)
    pd1_filter2 = r_pd2.loc[r_pd2['salary'] > 500]
    print(pd1_filter2)
    pd1_query = r_pd2.query('salary>200 & salary<600')
    print(pd1_query)
    pd1_filter_data = r_pd2[r_pd2['salary'] > 200]
    print(pd1_filter_data)

    # sort
    print('\n'+('*' * 20))
    print(r_pd2.sort_index(ascending=False))
    print(r_pd2.sort_values('id',ascending=False))

    # join, merge





