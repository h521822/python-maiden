# 题目：判断101-200之间有多少个素数，并输出所有素数。


for i in range(100,201):
    flag = True
    for j in range(2,i):
        if i % j == 0:
            flag = False
            break
    if flag:
        print(i)

