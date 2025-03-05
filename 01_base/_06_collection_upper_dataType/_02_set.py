
# 集合的创建
s = set()
print(s,type(s))
s = {1,2,3,4,1,2}
print(s,type(s))
s = set([1,2,3,1])  # list-->set
print(s)
s = set((1,2,3))  # tuple-->set
print(s)
s = set('123')  # str-->set
print(s)
s = set({'a':2,'b':3})  # dict-->set  only adopt key
print(s)
# in
print(1 in s)
# len
print(len(s))
print(min({1,2,3,4}))
# del s
# print(s)


# 集合的遍历
print('\n'+'*'*20)
for i in s:
    print(i)

# 常用的方法
print('\n'+'*'*20)
s.remove('a')
print(s)
s.update({2,3,4,5,6,7,6,5})
print(s)
s.add(9)
print(s)
s.add(1)
print(s)
s2 = set()
l1 = [1,2]
l2 = [3,4,5]
s2.update(l1,l2)
print(s2)

# intersection unall subtract
print('\n'+'*'*20)
s2 = {5,6,7,8,9}
print(s2)
print(s & s2)  # intersection
print(s | s2) # union   return is set, no replica
print(s - s2) # subtract

# 列表去重
print('\n'+'*'*20)
score = [80,70,60,80,70,60,40]
s = set(score)   # order has been destroy
print(s)
d = {}
# 统计各个分数都有几个学生
for i in s:
    t = score.count(i)
    d[i] = t
for k,v in d.items():
    print('得分为%d的学生有%d个人' % (k, v))
