# 题目：输出 9*9 乘法口诀表。

for i in range(1,10):
    print()             # 换行
    for j in range(1,10):
        if i >= j:
            print("%d*%d=%d" % (i, j, i*j), end='  ')       # , end='  '  不换行

