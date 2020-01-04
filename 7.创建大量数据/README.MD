

<!-- TOC -->

- [1. 短时间内做出大量一定规则的数据](#1-%E7%9F%AD%E6%97%B6%E9%97%B4%E5%86%85%E5%81%9A%E5%87%BA%E5%A4%A7%E9%87%8F%E4%B8%80%E5%AE%9A%E8%A7%84%E5%88%99%E7%9A%84%E6%95%B0%E6%8D%AE)
  - [1.1. 简介](#11-%E7%AE%80%E4%BB%8B)
  - [1.2. 编写思路](#12-%E7%BC%96%E5%86%99%E6%80%9D%E8%B7%AF)
  - [1.3. 完整源代码](#13-%E5%AE%8C%E6%95%B4%E6%BA%90%E4%BB%A3%E7%A0%81)

<!-- /TOC -->



# 1. 短时间内做出大量一定规则的数据

---
## 1.1. 简介

怎么说呢？这个东西看起来貌似没有什么用。当对于开发人员来说，还是有用到的时候的。

For example，前端时间我有个客户，要求对系统做压力测试，需要几万条，甚至几十万条数据。初期使用execl,但是execl处理少量的数据还是非常优秀的，大量的数据会卡成狗。

so，有了这个。

## 1.2. 编写思路
基本没有什么技术可言，就是把字符串拼接到一起，然后生成为.txt文件就可以了，这里就不做过多的描述。
```python
# 处理数据
def do_data():
    global saveDataNum
    global dataInfo
    while (saveDataNum < saveDataNumTotal):
        saveDataNum = saveDataNum + 1
        dataInfo = dataInfo + baseData1 + '\'' + baseData2 + str(saveDataNum) + '\'' + baseData3 + baseData4
        print('第'+str(saveDataNum)+'条数据保存成功')

# 将处理好的数据保存到txt文件中
def save_data(dataInfo):
    # if saveDataNum == 1:
    #     # 1、打开txt文件     w:覆盖以前的内容；a:在最后追加
    #     file_handle = open('data.txt', mode='w')
    # else:
    #     file_handle = open('data.txt', mode='a')
    # 1、打开txt文件     w:覆盖以前的内容；a:在最后追加
    file_handle = open('data.txt', mode='w')
    # 2、向文件写入数据
    file_handle.write(dataInfo + ' \n')
    # 3、关闭文件
    file_handle.close()
    # pass
```

## 1.3. 完整源代码
项目源代码在 [GitHub仓库](https://github.com/h521822/python-maiden)  
项目持续更新，欢迎您[star本项目](https://github.com/h521822/python-maiden)


