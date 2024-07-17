# 1、calculate、算数
print('calculate', '*' * 20)
print(4 + 1)
print(4 + 1)
a = 10
b = 3
print(a - b)
print(a * 4)
print(a / b)
print(a // b)  # 整除，取整
print(a % b)  # 获取余数，求模
print(a ** 3)  # 幂运算
print(3 + 2 * (4 ** 2))

# 2、assign、赋值
print('assign', '*' * 20)
a = 2
print(a)
a += 2  # 自增
print(a)
a = a + 2
print(a)

# 3、compare、比较
print('compare', '*' * 20)
print(3 != 3)  # 判断不相等
print(3 == 2)  # 判断相等
print(3 >= 2)
print(3 <= 3)
print(3.0 == 3)
print(True == False)
print('hello' < 'hell')  # 字符串的比较运算：每个字符的ascii码值
print(1<2<3)
print(1<2 and 2<3)
print('y'<'x'==False)
print('y'<'x' and 'x'==False)


# 4、logic、逻辑
print('logic', '*' * 20)
# 与，并且 and
print(True and False)
print(True and True)
print(True and False and True)
print(1==1 and True and 2<3)
print('hello' and 'hi') # 短路运算
print('' and 'hi')
print(False and 'hi')
print(0 and 1)
# 或者or
print(True or False)
print(False or False or True)
print(1 or 0)
print(2024 or 2025 or 0)
print(0 or '' or 888)
# 非not
print(not True)
print(not 1)
print(not '')
# 优先级 not>and>or
print(True and False and not False)
print(True or False and True or False)


# 5、position、位
print('position', '*' * 20)
# 按位与&
'''
101
111
----
101
'''
print(5 & 7)
# 按位或 |
'''
011
100
----
111
'''
print(3 | 4)

# 按位异或
'''
010
100
----
110
'''
print(2 ^ 4)
# 按位取反~
'''
01
---
10
110
'''
print(~1)
# 左移 右移
'''
101
----
10100
'''
print(5<<2)


# 6、member、成员
print('member', '*' * 20)
print('12' in '123')
print('hi' not in 'hello')
a = 1
b = 2
print(a is b)
print(a is not b)

