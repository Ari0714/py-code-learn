
# if
print(1==1)
print(1==1==1)


# 1、singe branch
print('singe branch', '*' * 20)
weather = '下雨'
if weather != '下雨':
    print('带伞出门')  # if语句的下级代码

# if的语法
print('\n'+'*'*20)
if False:
    print(111)


# 判断年龄age>18
print('\n'+'*'*20)
age = 19
if age >= 18:
    print('可以进网吧')
    print('hello')


# 2、double branch
print('double branch', '*' * 20)
weather = '晴天'
if weather == '下雨':
    print('出门要带伞') # 缩进
    print(111)
else:
    print('戴个帽子')

# 判断年龄
age = int(input('请输入你的年龄：'))
if age >= 18:
    print('可以去网吧')
else:
    print('在家写作业吧')


# 3、multiple 多分枝
print('multiple branch', '*' * 20)
# score = 94
# if score > 90:
#     print('A')
# elif score > 80:
#     print('B')
# elif score > 70:
#     print('C')
# else:
#     print('D')
#
#
# bmi计算
# bmi =w/(h*h)
w = float(input('请输入你的体重，单位kg：'))
h = float(input('请输入你的身高，单位米：'))
bmi = w / (h * h)
print(bmi)
if bmi < 18.5:
    print('多吃一点才健康')
elif bmi < 23.9:
    print('你的体型非常的标准')
else:
    print('适当的可以多运动一下')


# 4、match since3.10
x = 'heidsio'
# match x:
#     case 'hello':
#         print('正确')
#     case 'helo':
#         print('少写了一个l')
#     case 'heiio':
#         print('字母l拼错了')
#     case _:
#         print('拼写不正确，请仔细检查')


# 5、age judge
age = input('请输入你的年龄：')
if age.isdigit():
    age = int(age)
    if age>=0 and age<=120:
        print('输入正确')
    else:
        print('输入错误，请重新输入')
else:
    print('请输入阿拉伯数字！')


# 6、score judge
py_score = input('请输入你的python课程成绩：')
c_score = input('请输入你的C课程成绩：')

if py_score.isdigit() and c_score.isdigit():
    py_score = int(py_score)
    c_score = int(c_score)
    if py_score>=60 or c_score>=60:
        print('合格')
    else:
        print('重修')
else:
    if not py_score.isdigit():
        print('py的成绩必须输入数字！')
    if not c_score.isdigit():
        print('c的成绩必须输入数字！')