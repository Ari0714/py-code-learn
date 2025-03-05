import random

# random
print('\n'+'*'*20)
print(random.choice('abc'))

s2 = set()
l1 = [1,2]
l2 = [3,4,5]
s2.update(l1,l2)
print(s2)