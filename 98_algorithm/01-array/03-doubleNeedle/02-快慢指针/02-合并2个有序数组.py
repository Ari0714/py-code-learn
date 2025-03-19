# easy
# 合并2个有序数组
# 双指针后向前，0（m+n）
def merge(arr1, m, arr2, n):
    p1, p2, p = m - 1, n - 1, m + n - 1
    while (p1 >= 0 and p2 >= 0):
        if (arr1[p1] > arr2[p2]):
            arr1[p] = arr1[p1]
            p1 -= 1
        else:
            arr1[p] = arr2[p2]
            p2 -= 1
        p -= 1

    while (p2 >= 0):
        arr1[p] = arr2[p2]
        p2 -= 1
        p -= 1
    return arr1


if __name__ == '__main__':
    print(merge([1, 7, 8, 0, 0, 0], 3, [1, 2, 3], 3))
