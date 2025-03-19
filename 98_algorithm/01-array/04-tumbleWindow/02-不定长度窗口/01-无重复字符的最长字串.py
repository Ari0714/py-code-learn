# medium
# 无重复字符的最长字串


def unique_str_violence(s):
    max_res = 0
    for i in range(len(s)):
        # use set to eliminate duplicate element
        seen = set()
        for j in range(i, len(s)):
            if (s[j] in seen):
                break
            seen.add(s[j])
            max_res = max(max_res, j - i + 1)
    return max_res


if __name__ == '__main__':
    print(unique_str_violence('aaaaabc'))
