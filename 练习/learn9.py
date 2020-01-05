
# 题目：将一个正整数分解质因数。例如：输入90,打印出90=2*3*3*5。

def reduceNum(num):
    print ('{} = '.format(num),end=''),
    n = num
    m = 0
    while n != 1:           # 递归，直到剩余一个素数
        for i in range(2,n + 1):
            if n % i == 0:
                m = i
                break
        n = n // m
        if n == 1:
            print ('{}'.format(m)),  
        else:
            print ('{} * '.format(m),end=''),  
        
reduceNum(int(input('int:')))