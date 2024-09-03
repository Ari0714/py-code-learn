
# a = 'ad'
# a.strip()
#
# li = [1,2,3]
# print(li[-1])


strs = 'Hello World'.split(' ')
li = []
for i in strs:
    print(i)
    if (len(i.strip()) > 0):
        li.append(i)
print(len(li[-1]))

# list1 = {'1':1,'2':2}
# list2 = list1 # link
# list1['1'] = 5
# sum = list1['1'] + list2['1']
# print(sum)