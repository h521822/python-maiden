# 题目：输入数组，最大的与第一个元素交换，最小的与最后一个元素交换，输出数组。

arr = [2,4,5,2,6,2,1,7,4,3,8,6,3]   

print(arr.index(2,4))       # .index(i,j)：i元素,从j开始第一次出现的位置

min = min(arr)      # 最大值
max = max(arr)      # 最小值
arr.remove(min)     # 移除某个元素(存在多个相同的元素，只会移除第一个)
arr.remove(max)

# arr[0] = max      # 替换某个元素
arr.insert(0,max)   # 插入一个元素
# arr[-1] = min
arr.append(min)     # 追加一个元素
print(arr)