
print('abc'[0:0])   # return ''

s0 = 'abc'
for i in range(len(s0)):
    print(s0[0:i+1])
print(s0[0:1])

# 序列的通用操作
s1 = 'hello world'
print(s1+' mia')
print(s1.split(' ')[1])
print(s1[1])
print(s1[::-1])
print(reversed(s1))   # return object, no use
print(''.join(reversed(s1)))  # list -> str
print(s1*3)
print(len(s1))
print(max(s1),min(s1))
print('a##'.isalpha())
print('1'.isdigit())
print('1234'.startswith('1'))

print('\n'+'*'*20)
# del s1
# print(s1)
print('s' in s1)
print('abcd'<'abce')
print('cd'<'abcd')
#
# # 字符串的遍历
# for i in s1:
#     print(i)
# for index,value in enumerate(s1):
#     print(index,value)
# for i in range(len(s1)):
#     print(i,s1[i])
#
# # 类型转换
# print(str(12),type(str(12)))  # int-->str
# print(str([1,2,3,4]), type(str([1,2,3,4]))) #list-->str
# print(str((1,)),type(str(1,)))  #tuple-->str
#
# # 常用方法
print(s1.title())  # first word upper(), -> Hello World
print(s1.lower())  # hello world
print(s1.upper())  # HELLO WORLD
print(s1.islower())
print(s1.isupper())
print(s1.count('o'))
print(s1.strip())
print(s1.split(' ')) # 分隔字符串
print(s1.find('a'))
print('#$'.join(['111','222','333']))

print('\n'+'*'*20)
s2 = '123456123456'
print(s2.find('12'))  # return first 1, no error and return -1 if not find
print(s2.find('12', 3))  # start index3 find
print(s2.rfind('12'))  #
# print(s2.index('125'))  # return first 1, error if not find
print(s2.index('12', 3))  # start index3 find
print(s2.rindex('12', 3))  #


# # 字符串的统计
print('\n'+'*'*20)
# s = 00_input('请输入一篇文章：')
# # 字母的个数、数字的个数、符号的个数
# a,b,c = 0,0,0
# for i in s:
#     if i.isdigit():
#         b+=1
#     elif i.isalpha():
#         a+=1
#     else:
#         c+=1
# print(a,b,c)

s = 'abcd'
print(s)
print(s[0])
s = 't' + s[1:]
print(s)
s = list(s)
print(s)
s[0] = 'a'
print(s)

# letter to digital, versa
print('\n' + ("*" * 20))
print(chr(65))   # A
print(chr(97))   # a
print(ord('A'))  # 65 - 90
print(ord('a'))  # 97 - 122

# print alpha char between a-x
res1 = []
for i in range(ord("A"),ord("Z")+1):
    res1.append(chr(i))
print(res1)

# remove & replace
print('\n' + ("*" * 20))
str_r1 = 'abca'
str_r2 = str_r1.replace('c','d')  # all
# print(str_r2)
str_r3 = str_r1.replace('a','r')
print(str_r3)
# str_r3 = str_r1.removeprefix('a')
# print(str_r3)
# str_r4 = str_r1.removesuffix('a')
# print(str_r4)
li_p1 = list('123')
li_p1.pop(2)   #print exact figure
print(li_p1)