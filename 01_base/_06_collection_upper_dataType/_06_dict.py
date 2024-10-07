# 字典的创建
d = {
    'name':'mia',  # 键值对
    'gender':False,
    'name':'jack'  # 键重复的话，会覆盖掉之前的值
}
print(d)
print(type(d))
# d = {}
# print(d)
# print(type(d))
# d = dict()
# print(d,type(d))
# 新增键值对
d['height'] = 170
d['HEIGHT'] = 170
print(d)
# 获取键值对
print(d['name'])
# 修改键值对
d['gender'] = True
print(d)
# del d
# print(d)
# in
print('name' in d)

# 字典的遍历
print('\n'+'*'*20)
for i in d:
    print(i,d[i])
print('-'*30)
print(d.items())
for k,v in d.items():
    print(k,v)
for k in d.keys():
    print(k)
for v in d.values():
    print(v)

# 字典的常用方法
d.pop('name')
print(d)
a = d.copy()
print('a的键值对',a)
print(d.get('gender'))
d.popitem()
d.popitem()
print('pop',d)
d.update({'age':18})
print('update',d)
d.clear()
print(d)

# transform
print('\n'+'*'*20)
d3 = {'c':3,'a':1,'b':2}
print(list(d3))  # default only  key
print(list(d3.items()))  # default only  key


# sort
print('\n'+'*'*20)
d2 = {'c':3,'a':1,'b':2}
print(list(d2.items())[0][0])
d2_sort = sorted(d2.items(),key=lambda x:x[1],reverse=True)
print(type(d2_sort))
print(d2_sort)
print([[x[0],x[1]] for x in d2_sort])


# accumulate
print('\n'+'*'*20)
dict = {}
li2 = ['a','b','b','c']
for i in li2:
    dict[i] = dict.get(i,0) + 1
for item in dict.items():
    print(item)

