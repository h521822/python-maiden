# 利用递归方法求5!。



def fa(n):
    sum = 1
    if n == 1:
        sum = 1
    else:
        sum = n * fa(n -1)
    return sum

print(fa(5))