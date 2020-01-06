# 题目：按逗号分隔列表。
# 分析：转成字符串，去掉首位

L = [1,2,3,4,5]
print(str(L)[1:-1])
print(repr(L)[1:-1])    # repr() 函数将对象转化为供解释器读取的形式。   我理解为object转为string，类似str()
print(','.join(str(n) for n in L))      # 返回通过指定字符连接序列中元素后生成的新字符串。