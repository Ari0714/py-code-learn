# 列表的创建
print(list(range(3)))
print(list(range(1,3)))
list1 = []  # 空列表
print(list1)
print(type(list1))
list2 = [1, 2, 3, True, False, 'hello']
print(list2)
list3 = list() # 类型转换：把参数转换为列表
print(list3)
list3 = list('12345678') # 类型转换：str-->list
# print(list3)
print(list3[::-1])
print(list3)
print(list3.count('1'))
print(1 not in [1,2,3])
print(['2','2','4'].index('2'))     #no value report error; only str has find func, no value return -1


print('\n'+'*'*20)
# 列表的索引
print(list3[5])

# 列表的切片
print('\n'+'*'*20)
print(list3[0:5:1])
print(list3[2:6:2])

# 列表的加法和乘法
print(list3 + list2)
print(list3 * 3)

# 列表的成员运算
print('1' not in list3)
print('1' in [1, 2, 3, 4])
print([3,2,3,4]<[2,1])

# 内置函数  函数名()
print('\n'+'*'*20)
list4 = [1,2,3,4]
print(([][0:0]))  # sum(empty []) -> return 0
print(len(list4))  # 求元素个数
print(max(list4))  # 求元素的最大值
print(min(list4))  # 求元素的最小值
print(sum(list4) / len(list4))  # mean
# del list3   # 删除变量
# print(list3)
print('-'*30)
# 列表的遍历
for i in list2:
    print(i)

for i,j in enumerate(list2):  # 枚举
    print(i,j)

for i in range(len(list2)):
    print(i,list2[i])

print('-'*30)
# 列表的常用方法method  变量.方法名()
# 添加元素
list3.append('666')  # error, li2 retuen None: li2 = li.append('123')
print(list3)
# 添加列表
list3.extend([1, 2, 3])
print(list3)
# 插入元素
list3.insert(2,'hello')
print(list3)
# 根据索引删除元素
list3.pop(3)
print(list3)
# 根据元素删除
list3.remove('7')
list3.pop(0)
print(list3)
list3.append('hello')
print(list3)
# 清空列表
list3.clear()
print(list3)

# 计算若干个人的平均年龄
age = [10,20,30,40,23,45,78,43]
print(sum(age) / len(age))

# sort
print('\n'+'*'*20)
sort_li1 = [6, 2, 3, 4, 5]
sort_li1.sort()
print(sort_li1)
sort_li2 = sorted(sort_li1)
print(sort_li2)

# get common have
print('\n'+'*'*20)
set1 = set()
A = [1, 2, 3, 4, 5]
B = [4, 5, 6, 7, 8]
print(set(A).intersection(set(B))) # {4, 5}
print([x for x in A if x in B])

# enumerate
print('\n'+'*'*20)
aa = list(enumerate([1,2,3]))
print(aa)  #[(0, 1), (1, 2), (2, 3)]

# 2w list distinct
print('\n'+'*'*20)
li2 = [[1,2],[3,4],[1,2]]
# print([x for x in li2 if ])