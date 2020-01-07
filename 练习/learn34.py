# 题目：打印出杨辉三角形（要求打印出10行如下图）。　
# 1 
# 1 1 
# 1 2 1 
# 1 3 3 1 
# 1 4 6 4 1 
# 1 5 10 10 5 1 
# 1 6 15 20 15 6 1 
# 1 7 21 35 35 21 7 1 
# 1 8 28 56 70 56 28 8 1 
# 1 9 36 84 126 126 84 36 9 1


# PS 调整后
# 1 
# 1   1 
# 1   2   1 
# 1   3   3   1 
# 1   4   6   4   1 
# 1   5  10  10   5   1 
# 1   6  15  20  15   6   1 
# 1   7  21  35  35  21   7   1 
# 1   8  28  56  70  56  28   8  1 
# 1   9  36  84 126 126  84  36  9  1

# 程序分析：怎么说呢？其实这就是一个简单的递归，只是题例中由于各数字长度不一致，比较难发现规律
# 看本人调整后的题例，其实就是，除了边界以外的数据，s[i,j] = s[i-1,j-1] + s[i-1,j]


n = 10
def lst(i,j):
    if i==j or j==1:
        return 1
    else:
        return lst(i-1,j-1) + lst(i-1,j)

for i in range(1,n+1):
    for j in range(1,i+1):
        print (lst(i,j),end=' '),
    print()