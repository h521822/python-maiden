# 求1+2!+3!+...+20!的和。

ijArr = []
for i in range(1,21):
    ij = 1
    for j in range(1,i + 1):
        ij = ij * j

    ijArr.append(ij)

print('前20项之和为{}'.format(sum(ijArr))) 


s = 0
t = 1
for n in range(1,21):
    t *= n
    s += t

print('前20项之和为{}'.format(s)) 
