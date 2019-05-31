# 微薄利爬虫

---
## 简介
其实这是刚学习python时帮朋友写的，已经很久了，可能并不完善。  
爬取符合一定条件的数据，并保存到`.text`文件中.

## 编写思路
1. 爬取一定条件的记录

```python
def get_html(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    reqdata = {
        'action': 0,
        'state': state,
        'sortTime': 2,
        'sortLook': 2,
        'sortMoney': 2,
        'sortNum': 2,
        'classid': 0,
        'classParentid': 0,
        'limit': 32,
        'pageNo': page
    }
    # print(url)
    try:
        # resp = get(url, headers=headers)
        resp = post(baseUrl, params=reqdata, headers=headers)
        print(resp.status_code)
        if resp.status_code == 200:
            # print(resp.content)
            return resp.text
        print("没有爬取到相应的内容")
        return None
    except RequestException:
        print("没有爬取到相应的内容")
        return None
```

2. 对爬取的记录进行处理
```python
def doData(page):
    stop = random.uniform(0.1, 0.5)
    time.sleep(stop)
    print(stop)

    txt = get_html(page)
    jsonText = json.loads(txt)
    infos = jsonText['rows']
    print('正在抓取第' + str(page) + '页')
    # print(infos[0]['price'])

    num = 0
    for info in infos:
        try:
            num += 1

            print('正在爬取第' + str(page) + '页,第' + str(num) + '条的数据')
            # 下单金额
            try:
                price = info['price']
            except:
                price = ""
            print(price)
            if price <= priceMax:
                continue
            # 花费金额
            try:
                costMoney = info['costMoney']
            except:
                costMoney = ""
            print(costMoney)
            if costMoney > 0:
                continue
            # 剩余数量
            try:
                lastNum = info['lastNum']
            except:
                lastNum = ""
            print(lastNum)
            if state == 1 and lastNum < 1:
                continue
            # 商品编号
            try:
                goodsId = info['goodsId']
            except:
                goodsId = ""
            print(goodsId)
            dataInfo = '下单金额：' + str(price) + '；花费金额：' + str(costMoney) + '；剩余数量：' + str(lastNum) + '；链接：' + 'http://ls.vboly.com/web/vblgoods/info/goodsid/' + str(goodsId) + '.htm'
            print(dataInfo)
            global dataMuster
            dataMuster += dataInfo + ' \n'
            # saveData(dataInfo)
        except:
            print('爬取第' + str(page) + '页,第' + str(num) + '条数据失败')
            pass
```

3. 将处理好的数据保存到`.text`文件中
```python
# 将处理好的数据保存到txt文件中
def saveData():
    # 1、打开txt文件     w:覆盖以前的内容；a:在最后追加
    file_handle = open('test.txt', mode='w')
    # 2、向文件写入数据
    file_handle.write(dataMuster + ' \n')
    # 3、关闭文件
    file_handle.close()
    # pass
```

## 完整源代码
项目源代码在 [GitHub仓库](https://github.com/h521822/python-maiden)  
项目持续更新，欢迎您[star本项目](https://github.com/h521822/python-maiden)


