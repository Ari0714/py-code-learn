
# easy
# 移动0
# 双指针 0（n）
def move_zero(arr):
    left = 0
    for right in range(len(arr)):
        if (arr[right] != 0):
            arr[left],arr[right] = arr[right],arr[left]
            left += 1
    return arr


if __name__ == '__main__':
    print(move_zero([0, 1, 0, 3, 12]))

