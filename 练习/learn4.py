# 题目：斐波那契数列。

# 程序分析：斐波那契数列（Fibonacci sequence），又称黄金分割数列，指的是这样一个数列：0、1、1、2、3、5、8、13、21、34、……。

# 在数学上，费波那契数列是以递归的方法来定义：

# F0 = 0     (n=0)
# F1 = 1    (n=1)
# Fn = F[n-1]+ F[n-2](n=>2)

f1 = 0
f2 = 1

num = int(input('int:'))

fn = 0
for id in range(num):
    if id == 0: 
        fn = f1
    elif id == 1:
        fn = f2
    else:
        fn = f1 + f2
        f1 = f2
        f2 = fn

print('fn:' + str(fn))