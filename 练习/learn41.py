# 题目：八进制转换为十进制

s = 123
r = 0
for i in range(len(str(s))):
    r = r + s // (10 ** i) % 10 * (8 ** i)
    

print(r)


