#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import datetime
import time
from requests import get
import json
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('bmh')


# user_agent列表
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]

# referer列表
referer_list = [
    'http://fund.eastmoney.com/110022.html',
    'http://fund.eastmoney.com/110023.html',
    'http://fund.eastmoney.com/',
    'http://fund.eastmoney.com/110025.html'
]


def get_html(baseUrl):
    # 获取一个随机user_agent和Referer
    headers = {'User-Agent': random.choice(user_agent_list), 'Referer': random.choice(referer_list)}
    try:
        resp = get(baseUrl, headers=headers)
        # print(resp.status_code)
        if resp.status_code == 200:
            # print(resp.content)
            return resp.text
        print("没有爬取到相应的内容")
        return None
    except RequestException:
        print("没有爬取到相应的内容")
        return None


if __name__ == "__main__":

    starttime = datetime.datetime.now()
    print(starttime)

    t = time.time()
    rt = int(round(t * 1000))
    code = "004070"
    baseUrl = "http://api.fund.eastmoney.com/f10/lsjz?fundCode=" + code + "&pageIndex=1&pageSize=200&startDate=&endDate=&_=" + str(rt)
    data = get_html(baseUrl)

    jsonText = json.loads(data)
    infos = jsonText['Data']['LSJZList']

    infosList = []
    indexList = []
    titleList = ['FSRQ', 'DWJZ', 'LJJZ', 'JZZZL']

    for info in infos:
        # print(info)
        FSRQ = info['FSRQ']     # 日期
        DWJZ = info['DWJZ']     # 单位净值
        LJJZ = info['LJJZ']     # 累计净值
        JZZZL = info['JZZZL']     # 增长率
        # print(FSRQ)
        # print(float(DWJZ))
        # print(float(LJJZ))
        # print(float(JZZZL))

        indexList.append(FSRQ)

        infoList = []
        infoList.append(FSRQ)
        infoList.append(float(DWJZ))
        infoList.append(float(LJJZ))
        infoList.append(float(JZZZL))
        infosList.append(infoList)

    df = pd.DataFrame(infosList, index=indexList, columns=titleList).sort_index()
    # print(df)

    df['ma'] = df['LJJZ'].rolling(5).mean()
    # 去除缺失行
    df = df.dropna()
    # print(df)

    df[['FSRQ', 'LJJZ', 'ma']].plot()

    plt.show()

    endtime = datetime.datetime.now()
    print(endtime)

    print('\n数据处理成功!所用时间为：' + str((endtime - starttime).seconds))
