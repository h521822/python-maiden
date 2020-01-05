# 题目：有一分数序列：2/1，3/2，5/3，8/5，13/8，21/13...求出这个数列的前20项之和。
a = 2
b = 1
c = 0
arr = []
for i in range(20):
    arr.append(a / b)
    c = a
    a += b
    b = c

print(arr)
print('前20项之和为{}：'.format(sum(arr)))
