import sys

max_value = sys.maxsize
min_value = -sys.maxsize - 1

print(max_value)
print(min_value)

# int
# sys.set_int_max_str_digits(0)
print("int*" * 20)
t1 = 0.5
print(int(t1))
t2 = 1.5
print(int(t2))
print(10/3)   # 3.33
print(10//-3)  # -4  #positive digit -1
print(10//3)  # 3
print(10%3)  # 1, get rest,opposite above #mod

print(sum([2,3,4]) / len([2,3,4]))