
# medium
# 三数之和
def three_sum(arr, target):
    for i in arr:
        for j in arr:
            for k in arr:
                if(i+j+k == target):
                    return (i,j,k)


if __name__ == '__main__':
    print(three_sum([1,2,3,4,5,6,9],12))

