
# import my_module
# from my_module import add, author
# from my_module import *
from my_package.my_math import add as f

'''module'''
result = f(3,4)
print(result)
# print(author)
# total(1,2,3)


'''package'''
from my_package import my_math, my_card
from my_package import *
result = my_math.total(1,2,3)
print(result)
my_card.menu()
