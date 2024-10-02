# 1、define variable
fruit_type = '苹果'
apple_num = 4
apple_price = 3
print('sum payment:', apple_num * apple_price)

# 2、update variable
apple_price = 3.5
print('update sum payment:', apple_num * apple_price)

# 3、type
a = '123abc'
print(type(a))
print(isinstance(a, str))

# int
print("int*" * 20)
t1 = 0.5
print(int(t1))
t2 = 1.5
print(int(t2))
print(10/3)
print(10//3)

print(11%3)  #get rest,opposite above #mod


# float
print('\n' + ("*" * 20))
print("float*" * 20)
t2 = 10.234
t3 = 14.56
t3 = t3 + 10
print(t3)
print(round(t2 * t3, 2))
import math

print(math.floor(t2 * t3))
print(math.ceil(t2 * t3))

# str
print('\n' + ("*" * 20))
s1 = '123456123456'
s2 = '123abc'
s3 = s2
print(s3)
print(s1.count('1'))
print('966999999999996'.replace('6', '9', 3))  # digital represent replace num, 1 -> replace_first
s3 = '''
123
abc
'''
print(s3)
print(s3.strip())
print(s1 + s2)
print('#$%' * 3)
# str index
print(s1[0])
print(s1[-1])
print(s1[1:3])  # contain head not tail [)
print(s1[1:6:2])
print(s1[::2])
print('reverse str:', s1[-1:-10:-1])  # str outrange not report error
print('reverse str:', s1[::-1])  # str outrange not report error





# == is: ==compare value, is compare disk position
print(65 == 65)   # 输出 True
print(65555 is 65555)   # 输出 True
print('65' == '65')   # 输出 True
print('65' is '65')   # 输出 True

print([1, 2, 3, 4] is [1, 2, 3, 4])  # 输出 False
print([1, 2, 3, 4] == [1, 2, 3, 4])  # 输出 True
