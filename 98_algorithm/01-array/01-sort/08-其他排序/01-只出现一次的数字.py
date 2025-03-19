
# easy
# 只出现一次的数字,

def only_exist_one(arr):
    res = []
    if(len(arr) == 1):
        return arr[0]
    else:
        print('input error')
    for i in arr:
        if(arr.count(i) == 1):
            res.append(i)
    return res


if __name__ == '__main__':
    # print(only_exist_one([]))
    # print(only_exist_one([1,2,2]))
    print(only_exist_one([1,2,2,3]))