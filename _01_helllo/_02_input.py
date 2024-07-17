
# name = input("请输入您的姓名：")
# print("name:", name)

# 2、advanced usage
year = 2024  # 年份
month = 2
day = 20
week = "一"
weather = "晴"
temp = 19.5
print(year, "年，我要去10个城市旅游", sep="", end="\n\n")
print("今天是 %d 年 %02d 月 %d 日,星期%s,天气%s，温度%.1f" % (year, month, day, week, weather, temp))

# 3、next row
print(year, "xxx123", end="\n")  #print default \n