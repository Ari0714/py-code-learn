
# 1、while
print('for', '*' * 20)
# # 初始条件
n = 0
while n<100:
    print('hello Python')
    n += 1 # 判断条件更新

# # 高斯求和
# n = 2
# result = 0
# while n<10001:
#     result += n
#     n += 2
# print(result)

# while '111':
#     print(1)


# 2、for
print('for', '*' * 20)
# for i in range(10):
#     print('hello')
#     print(i)

# 高斯求和
result = 0
for i in range(101): # condition【）
    result += i
print(result)

# 1!+2!+3!..+n!
# result2 = 0
# for n in range(20):
#     if n>0:
#         result = 1
#         for i in range(n+1):
#             if i>0:
#                 result *= i
#         print(result)
#         result2 += result
# print(result2)

# 1!+2!+3!..+n!
# result2 = 0
# n = 1
# while n<=4:
#     result = 1
#     m = 1
#     while m<=n:
#         result *= m
#         m += 1
#     result2 += result
#     n +=1
# print(result2)



# 3、break
print('break', '*' * 20)
# while True:
#     print(111)
#     name = 00_input('请输入你的名字：')
#     if name == 'mia':
#         print('mia欢迎回家')
#         break
#     else:
#         print('mia不在家，你一会儿再来吧')


for i in range(10):
    if i>0 and i%3==0:
        print(i)
        break     #skip circle，only take one

# 判断一个数字n是否是质数
n = 8
a = 2
flag = 0
while a<n:
    if n%a==0:
        print(n,'不是质数')
        flag = 1
        break
    a += 1
else:
    print(n,'是质数')

# n = 5
# for i in range(2,n):
#     if n%i==0:
#         print(n,'不是质数')
#         break
# else:
#     print(n,'是质数')



# 4、continue
print('continue', '*' * 20)
for i in range(5):
    if i==2:
        continue    #stop run after, start new circle
        # print(111)
    print(i)



# 5、index explosion
# # 纸的厚度
# n = 0.1
# w = n
# for i in range(50):
#     w *= 2
#     print(w)
#
# # 国王麦粒
# # 1:1 2:2 3:4 4:8
# g = 1   # 当前格子应该放的麦子粒
# total = 0   # 总麦粒数
# a = 1  # 棋盘的格子数量
# while a<=100:
#     total += g  #计算当前的总麦粒数
#     print('在放满了%d个格子以后，总的麦粒数是%d' % (a, total))
#     a +=1   #走到下一个格子
#     g *= 2  #当前格子应该放的麦粒数*2
#
# 人生的复利 (1+0.01)=1.01
day = 0
total = 1
while day<365:
    total = total*1.11
    print(total)
    day += 1

