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
t1 = 10
# float
t2 = 10.234
t3 = 14.56
print(round(t2 * t3, 2))
import math
print(math.floor(t2 * t3))
print(math.ceil(t2 * t3))
# str
s1 = '123456'
s2 = '123abc'
s3 = '''
123
abc
'''
print(s3)
print(s1 + s2)
print('#$%' * 3)
# str index
print(s1[0])
print(s1[-1])
print(s1[1:3]) #contain head not tail [)
print(s1[1:6:2])
print(s1[::2])
print('reverse str:', s1[-1:-10:-1]) #str outrange not report error
print('reverse str:', s1[::-1]) #str outrange not report error
