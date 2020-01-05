# 题目：打印出如下图案（菱形）:

h = int(input('请输入一个奇数：'))
for i in range(1,h + 1):
    print()
    if i <= h // 2 + 1:
        for j in range(h-i-(h // 2)):
            print(' ',end='')
        for j in range(2 * i - 1):
            print('*',end='')
    else:
        for j in range(i-(h // 2) - 1):
            print(' ',end='')
        for j in range(2*(h-i) + 1):
            print('*',end='')


