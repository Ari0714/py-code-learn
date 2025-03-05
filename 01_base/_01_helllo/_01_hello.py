import  datetime
import time

print("hello world")


'''time'''
print(time.time())
print(time.localtime())

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


# dt = time.strptime('%Y-%m-%d %H:%M:%S', time.time())
# print(dt)