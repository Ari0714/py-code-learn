import os

# 打开文件
# f = open('test.txt')  # 相对路径
path = os.getcwd()
filename = path + '/test.txt'
f = open(filename, mode='r', encoding='utf-8')  # 绝对路径

# # 读取文件
# context = f.read()   #[) read all no line-break
# print(context)

context = f.read(6)   #[) read 5 index
print(context)

context = f.readline()  #[) read 1 line, above has read dont read anymore
print(context)

context = f.readlines()  #[) list，start over read anymore，built-in line-break
for i in context:
    print(i,end='')
print(context)

# # 关闭文件
f.close()