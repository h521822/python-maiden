# 题目：有n个人围成一圈，顺序排号。从第一个人开始报数（从1到3报数），凡报到3的人退出圈子，问最后留下的是原来第几号的那位。

p = 100

arr = [i for i in range(1,p + 1)]
print(arr)

i = 1
while len(arr) > 1:
    if i % 3 == 0:
        arr.pop(0)
    else:
        arr.insert(len(arr),arr.pop(0))
    i += 1
print(arr[0])




# while len(arr) >= 3:
#     arr.append(arr[0])
#     arr.append(arr[1])
#     arr.pop(2)
#     arr.pop(1)
#     arr.pop(0)

# print(arr[1])


