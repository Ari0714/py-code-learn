from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame
import numpy as np
import pandas as pd

if __name__ == '__main__':

    se0 = pd.Series(['book','picture'])
    print(se0)

    se = pd.Series(np.arange(10))
    print(se)
    print(type(se))

    se2 = pd.Series([1,2,3,4],index=[4,3,2,1])
    print(se2)

    se3 = pd.Series({'a':1,'b':2,'c':2,'d':None})
    print(se3)
    print(se3[0])
    print(se3['b'])

    # series property：index、value、
    print(se3.index)
    print(se3.values)
    print(se3.size)

    # series method：head、tail（default 5 row）
    print('*' * 20)
    print(se3.head(1))
    print(se3.tail(1))

    # isnon、notnull
    print('*' * 20)
    print(se3.isnull())
    print(se3.notnull())