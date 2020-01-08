# 题目：输入一个奇数，然后判断最少几个 9 除于该数的结果为整数。


if __name__ == '__main__':
    c = int(input('输入一个数字:\n'))

    b = 9
    while True:
        if b % c == 0:
            break
        else:
            b = b * 10 + 9

    print('最少{}个 9 除于{}的结果为整数'.format(len(str(b)),c))

