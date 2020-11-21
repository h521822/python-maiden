# 题目：使用lambda来创建匿名函数。

i = 2
functionName = lambda i:i+3     # 匿名函数lambda，方法名：functionName；传入参数：i；返回值：i+3
if __name__ == "__main__":
    print(functionName(i))