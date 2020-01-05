# 题目：两个乒乓球队进行比赛，各出三人。甲队为a,b,c三人，乙队为x,y,z三人。
# 已抽签决定比赛名单。有人向队员打听比赛的名单。a说他不和x比，c说他不和x,z比，请编程序找出三队赛手的名单。

yArr = ['x','y','z']

for a in yArr:
    for b in yArr:
        for c in yArr:
            if a!=b and a!=c and b!=c and a!='x' and c!='x' and c!='z':
                print('a-%s;b-%s;c-%s'%(a,b,c))
