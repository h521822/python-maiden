
# 工作中的小应用
# 获取文件中所有行的前两个字段

import os

# 不懂为什么VS code 不能使用相对路径
os.chdir(os.path.abspath(os.path.dirname(__file__)))

with open(r"./store.txt") as f:
    for i in f.readlines():
        list = i.split()        # split() 通过指定分隔符对字符串进行切片，返回列表      与.split(' ') 效果一样
        # print(list)
        if list:                # list有可能不存在
            tenant = list[0]
            store = list[1]
    
            print("tenant_id={0} and store_id={1};".format(tenant,store))