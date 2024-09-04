
import jieba
# import pyhdfs
from hdfs3 import HDFileSystem
import sys

if __name__ == '__main__':

    hdfs = HDFileSystem(host='dmp-64', port=8020)
    hdfs.ls('/user/data')
    # # hdfs.put('local-file.txt', '/user/data/remote-file.txt')
    # # hdfs.cp('/user/data/file.txt', '/user2/data')

