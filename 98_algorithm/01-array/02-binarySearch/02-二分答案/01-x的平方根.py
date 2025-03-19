

# 简单
# x 的平方根
# 由于返回类型是整数，结果只保留 整数部分 ，小数部分将被 舍去 。 4 => 2 8 => 2

def x_sqrt(target):
    if(target < 1):
        print('input value must > 0')
    for i in range(0,int(target/2)):
        if(i**2 == target):
            return i
    for i in range(0,int(target/2)):
        if(i**2 <= target and (i+1)**2 >= target):
            return i

if __name__ == '__main__':
    print(x_sqrt(8))
    # print(x_sqrt(9))
    print(x_sqrt(64))

