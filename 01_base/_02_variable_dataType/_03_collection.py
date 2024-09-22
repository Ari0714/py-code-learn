# 1、 range
for i in range(2,0,-1):
    print(i)

# 2、list
print('\n'+"*"*20)
li1 = [0,3,6,4,5]
print(max(li1))
# remove
li1.pop(0)
li1.remove(5)
li1.clear()
# li1.append(6)
# li1.append(5)
# print(li1)
# print(sorted(li1,reverse=False))
# li1.sort(key=lambda x:x == 0,reverse=False)    # not sort put last position, bool sort base on [1,0]
# print(li1)
sorted(li1)  # sorted need return new. sort not
print(li1)
li1.sort()
print(li1)

# 3、map
print("*"*20)
dict = {'a':1,'b':2}
dict['c'] = 3
print(dict)
print(dict.get('c') is not None)
for key,value in dict.items():
    print(key,value)

dict = {'b':2,'a':1,}
print(dict)
print(type(list(dict.items())[0]))
dict_sort = sorted(dict.items(),key=lambda i:i[1])
print(dict_sort[0][0])
print(len(dict))

# 4、set
print('\n'+"*"*20)
ss = {}
s = set()
s.add(1)
s.add(2)
s.add(3)
s2 = set()
s2.add(1)
s2.add(2)
s2.add(3)
s2.add(4)
print(s2 >= s)

# 2、 -> float
# s = '324.6'  # 有没有小数点都可以
# print(float(s))
# n = 2024
# print(float(n))
# print(float(s2), float(s3))
#
# # 3、 -> bool
# print('bool', '*' * 20)
# s = '0'
# print(bool(s))
# s1 = ''  # 空串
# print(bool(s1))
# n = 0
# print(bool(n))
# f = 0.0
# print(bool(f))
#
# # 4、 -> str
# print('str', '*' * 20)
# n = 5
# print(str(n))
# print(type(str(n)))
# # float -->str
# f = 5.3
# print(str(f))
# print(type(str(f)))
# # bool --> str
# a = True
# print(type(a))
# print(type(str(a)))
# # 进制的转换
# s = '1a'
# print(int(s, 16))