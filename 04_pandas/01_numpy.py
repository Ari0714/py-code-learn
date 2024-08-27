from datetime import datetime, timedelta
from pyspark.sql import SparkSession, DataFrame
import numpy as np
import pandas as pd

if __name__ == '__main__':
    a1 = np.arange(10)
    print(a1)
    print(type(a1))