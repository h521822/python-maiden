# -*- coding:utf-8 -*-

from requests import post
from requests import get
import random
import json
import time
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd
import math
import matplotlib.pyplot as plt
# matplotlib.use('agg')
plt.style.use('bmh') 

import numpy as np

#############################
# 
# 量化金融，用数据科学投资
# 
#############################



def get_html(baseUrl):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    try:
        resp = get(baseUrl, headers=headers)
        # resp = post(baseUrl, params=reqdata, headers=headers)
        print(resp.status_code)
        if resp.status_code == 200:
            # print(resp.content)
            return resp.text
        print("没有爬取到相应的内容")
        return None
    except RequestException:
        print("没有爬取到相应的内容")
        return None


def get_data(code):
    # 1、获取数据
    baseUrl = 'http://jingzhi.funds.hexun.com/database/jzzs.aspx?fundcode=' + code + '&startdate=&enddate=2022-05-08'
    soup = BeautifulSoup(get_html(baseUrl), 'lxml')
    # print(soup.prettify())

    # 2、数据格式化
    trs = soup.select('.m_table > tbody > tr')
    dataList = []
    titleList = ['date','unitNet','totalNet','growth']
    indexList = []
    for tr in trs:
        tds = tr.select('td')
        # print(tds)
        tdInfo = [td.get_text() for td in tds]
        indexList.append(tdInfo[0])
        list = []
        list.append(tdInfo[0])
        list.append(float(tdInfo[1]))
        list.append(float(tdInfo[2]))
        list.append(float(tdInfo[3].strip('%'))/100)

        dataList.append(list)
    # print(dataList)
    

    df = pd.DataFrame(dataList, index=indexList, columns=titleList).sort_index()

    # # print(df)
    # # print(df.sort_index())

    # # 保存数据
    # df.to_csv('.csv')

    # # 读取数据
    # df = pd.read_csv('4444444444444.csv',index_col='date')

    # 3、计算真是单位净值
    # print(df.iloc[0]['unitNet'])


    # 去除缺失行
    # df = df.dropna()
    # print(df.iloc[-1]['unitNet'])

    last = df.iloc[-1]
    # print(last['unitNet'])
    # print(last['totalNet'])
    # print(last)

    if last['unitNet'] == last['totalNet']:
        df['realNet'] = df['unitNet']
    else:
        # df = df[:8]
        # df.loc[0,'realNet'] = d['unitNet']


        for i in range(0,len(df)):
            # 今天
            d = df[i:i+1]
            if i == 0 :
                df.loc[d.index,'realNet'] = d['unitNet']
            else:
                # 昨天
                d1 = df[i-1:i]
                # print(d1)
                # print(d1['realNet'])
                # print(d['growth'])
                # print(float(d['growth']) * float(d1['realNet']))
                # print(d1['realNet'] * (1 + d['growth']))

                df.loc[d.index,'realNet'] =  float(d1['realNet']) * (1 + float(d['growth']))




        # df['unitNet1'] = df['unitNet'].shift(1)
        # # 将所有NaN转为0
        # # df.fillna(0, inplace=True)
        # # 将指定列NaN转为0
        # df['unitNet1'].fillna(df.iloc[0]['unitNet'], inplace=True)
        # # 真实净值
        # df['realNet'] = df['unitNet1'] * (1 + df['growth'])
        # print("realNet:{}unitNet1:{}growth:{}".format(df['realNet'],df['unitNet1'],df['growth']))
        # df.drop(['unitNet1'],axis=1,inplace=True)

    # print(df)


    # 5、计算5日均线和10日均线
    df['ma5'] = df['realNet'].rolling(5).mean()
    df['ma30'] = df['realNet'].rolling(30).mean()
    # 去除缺失行
    df = df.dropna()
    # print(df)

    # 6、计算布林线指标
    # 中轨（20日均线）
    df['g1'] = df['realNet'].rolling(20).mean()
    # 数据1     (净值-中轨)的平方
    # df['s1'] = (df['realNet'] - df['g1']) * (df['realNet'] - df['g1'])
    df['s1'] = (df['realNet'] - df['g1']) ** 2
    # 数据2     数据1的20日均线
    df['s2'] = df['s1'].rolling(20).mean()
    # 数据3     数据2的平方根
    df['s3'] = df['s2'] ** 0.5 
    # 上轨      中轨+2*数据3
    df['g2'] = df['g1'] + 2 * df['s3']
    # 下轨      中轨-2*数据3
    df['g3'] = df['g1'] - 2 * df['s3']
    # =(2*[@单位净值2]-[@上轨]-[@下轨])/[@单位净值2]
    # 量能柱
    df['lnz'] = (2*df['realNet']-df['g2']-df['g3'])/df['realNet']
    # [@中轨]+([@上轨]-[@中轨])*0.309
    # 高位止盈线
    df['gwvyx'] = df['g1']+(df['g2']-df['g1'])*0.309
    # =[@中轨]-([@中轨]-[@下轨])*0.309
    # 低位加仓线
    df['dwjcx'] = df['g1']-(df['g1']-df['g3'])*0.309
    # 研判参考
    # print((float(df[30:31]['realNet']) > float(df[30:31]['g2'])) and (float(df[29:30]['realNet']) < float(df[29:30]['g2'])))
    # print(df[30:31]['realNet'] > df[30:31]['g2'])
    # print(df[29:30]['realNet'] < df[29:30]['g2'])
    # print(df)


    # 去除缺失行
    df = df.dropna()
    # df['ypck'] = df['g1']-(df['g1']-df['g3'])*0.309
    for i in range(1,len(df)):
        # print(df[i:i+1])
        
        # 当天
        d = df[i:i+1]
        # 昨天
        d1 = df[i-1:i]
        # print(d)
        # print(d1)

        # IF(AND(E4>G4,[@单位净值2]<[@上轨]),"清仓"
        if float(d1['realNet']) > float(d1['g2']) and float(d['realNet']) < float(d['g2']):
            # print(d.index)
            # d['ypck'] = "清仓"
            df.loc[d.index,'ypck'] = "清仓"
            # print(d['realNet'])
        # IF(AND(E4>M4,E4<G4,[@单位净值2]<[@高位止盈线]),"止盈赎回"
        elif float(d1['realNet']) > float(d1['g2']) and float(d['realNet']) < float(d['gwvyx']):
            df.loc[d.index,'ypck'] = "止盈赎回"
        # IF([@单位净值2]>[@低位加仓线],"观望期",
        elif float(d['realNet']) > float(d['dwjcx']):
            df.loc[d.index,'ypck'] = "观望期"
        # IF([@单位净值2]>[@下轨],"可加仓","探底加仓")
        elif float(d['realNet']) > float(d['g3']):
            df.loc[d.index,'ypck'] = "可加仓"
        else:
            df.loc[d.index,'ypck'] = "探底加仓"

        
    df.drop(['totalNet'],axis=1,inplace=True)
    df.drop(['unitNet'],axis=1,inplace=True)
    df.drop(['s1'],axis=1,inplace=True)
    df.drop(['s2'],axis=1,inplace=True)
    df.drop(['s3'],axis=1,inplace=True)
    # print(df)
    # 保存数据
    # df.to_csv('4444444444444.csv')

    df = df[-50:]
    df[['realNet','g1','g2','g3','lnz','gwvyx','dwjcx']].plot()
    # matplotlib显示
    # plt.style.use('bmh')
    plt.show()

    df = df[-20:]
    print(df)

    




if __name__ == '__main__':

    # # 白酒
    # code = '161725'
    # # 50
    # code = '001548'
    # # 证券
    # code = '004070'
    # # 银行
    # code = '001594'
    # 恒生
    code = '000071'
    
    
    startdate = '2020-02-08'
    enddate = '2020-05-08'

    get_data(code)
    print('\n列表爬取成功!')


