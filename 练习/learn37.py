# 题目：有 n 个整数，使其前面各数顺序向后移 m 个位置，最后 m 个数变成最前面的 m 个数

# 参考：https://www.cnblogs.com/zhenwei66/p/6598996.html

from collections import deque

m = 3
a = [1,2,3,4,5,6,7]   # 7 个数
f = deque(a)
f.rotate(m)         # rotate（把右边元素放到左边）  #指定次数，默认1次
print (list(f))