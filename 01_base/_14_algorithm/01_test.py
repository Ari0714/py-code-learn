
# a = 'ad'
# a.strip()
#
# li = [1,2,3]
# print(li[-1])


# strs = 'Hello World'.split(' ')
# li = []
# for i in strs:
#     print(i)
#     if (len(i.strip()) > 0):
#         li.append(i)
# print(len(li[-1]))

# list1 = {'1':1,'2':2}
# list2 = list1 # link
# list1['1'] = 5
# sum = list1['1'] + list2['1']
# print(sum)


def maxNumberOfBalloons(text: str) -> int:
    dict = {}
    for i in text:
        if (i in 'balloon'):
            # if (i == 'l' or i == 'o'):
            if (i == ('l' or 'o')):
                if (dict.get(i) is not None):
                    dict[i] = dict.get(i) + 0.5
                else:
                    dict[i] = 0.5
            else:
                if (dict.get(i) is not None):
                    dict[i] = dict.get(i) + 1
                else:
                    dict[i] = 1
    print(dict)

    if (len(dict) > 4):
        sort_d = sorted(dict.items(), key=lambda x: x[1])
        # return int(sort_d[0][1])
        return sort_d
    else:
        return 0

# print(maxNumberOfBalloons('bballon'))


def uniqueOccurrences(self, arr: list) -> bool:
    dict = {}
    for i in arr:
        i2 = abs(i)
        if (dict.get(i2) is not None):
            dict[i2] = dict.get(i2) + 1
        else:
            dict[i2] = 1
    print(dict)

    dict2 = {}
    for i in dict.values():
        if (dict2.get(i) is not None):
            dict2[i] = dict2.get(i) + 1
        else:
            dict2[i] = 1
    print(dict2)

    for i in dict2.values():
        if i > 1:
            return False
    return True


print(uniqueOccurrences('1', [-17,-21,9,9,22,22,22,-21,-16,-21,-16,-9,-16,-21,22,-21,-17,-21,-16,-17,22]))