#题目： 输入三个整数x,y,z，请把这三个数由小到大输出。

# 分析：数组.sort()方法可排序
inputArr = []
for id in range(3):
    i = int(input('int:'))
    inputArr.append(i)

inputArr.sort()         # 升序输出
# inputArr.sort(reverse=True)               # 降序顺出

print(inputArr)