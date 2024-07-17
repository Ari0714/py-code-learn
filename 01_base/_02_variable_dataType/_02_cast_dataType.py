# 1、 -> int
s = '2024'
print(type(int(s)))
s2, s3 = True, False
print((int(s2), int(s3)))

# 2、 -> float
s = '324.6'  # 有没有小数点都可以
print(float(s))
n = 2024
print(float(n))
print(float(s2), float(s3))

# 3、 -> bool
print('bool', '*' * 20)
s = '0'
print(bool(s))
s1 = ''  # 空串
print(bool(s1))
n = 0
print(bool(n))
f = 0.0
print(bool(f))

# 4、 -> str
print('str', '*' * 20)
n = 5
print(str(n))
print(type(str(n)))
# float -->str
f = 5.3
print(str(f))
print(type(str(f)))
# bool --> str
a = True
print(type(a))
print(type(str(a)))
# 进制的转换
s = '1a'
print(int(s, 16))