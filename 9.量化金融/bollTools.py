#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
from requests import get
import time
import os
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import random

def get_html(baseUrl):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    try:
        resp = get(baseUrl, headers=headers)
        print(resp.status_code)
        if resp.status_code == 200:
            # print(resp.content)
            return resp.text
        print("没有爬取到相应的内容")
        return None
    except RequestException:
        print("没有爬取到相应的内容")
        return None



# 2、数据存储
def save_data(dataInfo):
    # 1、打开txt文件     w:覆盖以前的内容；a:在最后追加
    file_handle = open('data.txt', mode='w',encoding="utf-8")
    # 2、向文件写入数据
    file_handle.write(dataInfo + ' \n')
    # 3、关闭文件
    file_handle.close()
    # pass

    

# 天天基金。更新快，并且有估值。但是数据量少
def get_ttjj_data(code):
    
    t = time.time()
    rt = int(round(t * 1000))

    # 获取最新的估值
    # rt(毫秒级时间撮)，不用也能访问。但是我们尽量默认真实访问
    baseUrl = "http://fundgz.1234567.com.cn/js/" + code + ".js?rt=" + str(rt)

    # 查询首页所有信息
    # url = "http://fund.eastmoney.com/" + code + ".html?spm=search"

    txt = get_html(baseUrl)
    # print(txt)
    jsonText = json.loads(txt[txt.find("{"):txt.find("}") + 1])
    # print(jsonText)
    name = jsonText['name']     # 基金名称
    jzrq = jsonText['jzrq']     # 上个交易日的日期
    dwjz = jsonText['dwjz']     # 上个交易日的单位净值
    gsz = jsonText['gsz']       # 最近一个交易日的单位净值估值
    gszzl = jsonText['gszzl']   # 最近一个交易日的日涨跌幅
    gztime = jsonText['gztime'][:10] # 最近一个交易日的日期
  
    # print(dataList[:1])
    hxDate = dataList[:1][0][0]

    # 如果和讯没有取到最近的一个交易日的数据。则从天天基金取
    if hxDate != gztime:
        # 如果和讯没有取到上一个交易日的数据。则从天天基金取
        # print(hxDate)
        # print(jzrq)
        if hxDate != jzrq:
            indexList.append(jzrq)
            list = []
            list.append(jzrq)
            list.append(float(dwjz))
            dataList.append(list)
        indexList.append(gztime)
        list = []
        list.append(gztime)
        list.append(float(gsz))
        dataList.append(list)
    return name



# 和讯。历史数据比较全，但是更新太慢
def get_hx_data(code):

    baseUrl = "http://jingzhi.funds.hexun.com/database/jzzs.aspx?fundcode=" + code + "&enddate=2025-05-15"

    soup = BeautifulSoup(get_html(baseUrl), 'lxml')
    # print(soup.prettify())

    # 2、数据格式化
    trs = soup.select('.m_table > tbody > tr')
    for tr in trs:
        tds = tr.select('td')
        # print(tds)
        tdInfo = [td.get_text() for td in tds]
        indexList.append(tdInfo[0])
        list = []
        list.append(tdInfo[0])
        list.append(float(tdInfo[1]))
        # list.append(float(tdInfo[3].strip('%'))/100)

        dataList.append(list)



# 获取数据
def get_data(code):
    if isNew:
        get_hx_data(code)
        stop = random.uniform(2, 5)
        time.sleep(stop)
        name = get_ttjj_data(code)
        df = pd.DataFrame(dataList, index=indexList, columns=titleList).sort_index()

        # print(df)
        df['name'] = name 

        # 保存数据
        df.to_csv(code + '.csv')
    else:
        # 读取数据
        df = pd.read_csv(code + '.csv',index_col='date')

    msg_text = doData(df)
    return msg_text


# 数据处理
def doData(df):
    # CCI指标
    # 获取5日均线
    df['ma5'] = df['unitNet'].rolling(5).mean()

    # 6、计算布林线指标
    # 中轨（20日均线）
    df['g1'] = df['unitNet'].rolling(20).mean()
    # 数据1     (净值-中轨)的平方
    # df['s1'] = (df['unitNet'] - df['g1']) * (df['unitNet'] - df['g1'])
    df['s1'] = (df['unitNet'] - df['g1']) ** 2
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
    df['lnz'] = (2*df['unitNet']-df['g2']-df['g3'])/df['unitNet']
    # [@中轨]+([@上轨]-[@中轨])*0.309
    # 高位止盈线
    df['gwvyx'] = df['g1']+(df['g2']-df['g1'])*0.309
    # =[@中轨]-([@中轨]-[@下轨])*0.309
    # 低位加仓线
    df['dwjcx'] = df['g1']-(df['g1']-df['g3'])*0.309

    # 去除缺失行
    df = df.dropna()
    for i in range(1,len(df)):
        # print(df[i:i+1])
        
        # 当天
        d = df[i:i+1]
        # d = df.iloc[i]
        # 昨天
        d1 = df[i-1:i]
        # d1 = df.iloc[i-1]

        # print(d)
        # print(d1)

        # IF(AND(E4>G4,[@单位净值2]<[@上轨]),"清仓"
        if float(d1['unitNet']) > float(d1['g2']) and float(d['unitNet']) < float(d['g2']):
            # print(d.index)
            # d['ypck'] = "清仓"
            df.loc[d.index,'ypck'] = "清仓"
            # print(d['unitNet'])
        # IF(AND(E4>M4,E4<G4,[@单位净值2]<[@高位止盈线]),"止盈赎回"
        elif float(d1['unitNet']) > float(d1['gwvyx']) and float(d1['unitNet']) < float(d1['g2']) and float(d['unitNet']) < float(d['gwvyx']):
            df.loc[d.index,'ypck'] = "止盈赎回"
        # IF([@单位净值2]>[@低位加仓线],"观望期",
        elif float(d['unitNet']) > float(d['dwjcx']):
            df.loc[d.index,'ypck'] = "观望期"
        # IF([@单位净值2]>[@下轨],"可加仓","探底加仓")
        elif float(d['unitNet']) > float(d['g3']):
            df.loc[d.index,'ypck'] = "可加仓"
        else:
            df.loc[d.index,'ypck'] = "探底加仓"

        if i > 30 :

            # 计算CCI值
            # =(B2-SUM(H2:H31)/30)/AVEDEV(H2:H31)/0.015
            # 平均值：mean()        平均绝对偏差：mad()         苦恼mad()不能和rolling()一同使用
            ddf = df[i-29:i+1]
            df.loc[d.index,'cci'] = (d['unitNet'] - ddf['ma5'].mean()) / ddf['ma5'].mad() / 0.015


    # print(df)
    # print(df.iloc[-1]['name'])
    # print(df.iloc[-1]['ypck'])
    return df.iloc[-1]['name'] + '   ' + df.iloc[-1]['ypck'] + '   ' + str(round(df.iloc[-1]['cci'],2)) + '\n'



# 发送消息到邮箱
def send_sms(msg_text):
    # 第三方 SMTP 服务
    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "he521822@126.com"  # 用户名
    # mail_pass = "hj123456"  # 口令（是授权码，不是登录密码）
    mail_pass = "ZTHDVBGWWTIGJJEW"  # 口令（是授权码，不是登录密码）

    sender = 'he521822@126.com'     # 发送人邮箱，必须与 mail_user 一致
    receivers = ['h521822@126.com','1665521822@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    subject = '大吉大利晚上吃鸡'    # 标题
    msg_from = 'hej<h22@126.com>'   # 发件人(Tim为发送人名称，可以为空；<>为发送人邮箱，可以为空，可任意伪装)
    msg_to = 'h521822@126.com,1665521822@qq.com'   # 收件人，必须与 receivers 一致
    # msg_text = '现在是' + now + '，明天记得下午五点开会！'     # 发送内容

    message = MIMEText(msg_text, 'plain', 'utf-8')  # 邮箱内容
    message['From'] = msg_from
    message['To'] = msg_to

    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())    # 发送人，收件人，内容
        print("邮件发送成功")

    except smtplib.SMTPException:
        print("Error: 无法发送邮件")



    


if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    isNew = True
    # isNew = False

    # 表头（日期、单位净值、日增长率）
    # titleList = ['date','unitNet','growth']
    titleList = ['date','unitNet']

    # 基金编号
    codeList = ['001548','000961','000962',         # 50/300/500
    '000071',       # 恒生

    '001508', '000727', '000751',     # 动力灵活、健康灵活、嘉实新兴产业

    '161721',       # 招商地产      （不打算持有了）

    '001631',       # 食品饮料
    '161725',       # 白酒
    '320007',       # 科技
    '001618',       # 电子
    '004070',       # 证券
    '001595',       # 银行
                
    '166002',       # 中欧蓝筹
    '163402',       # 兴全趋势
    '519697',       # 交银优势
                
    '005224']       # 基建工程
    # codeList = ['005827','163402','270002','166002','260108','161005']
    # codeList = ['005224']
    msg_text = ''

    for code in codeList:
        print("{}数据处理开始".format(code))
        # print(stop)
            # 数据
        dataList = []
        # index列
        indexList = []
        msg_text += get_data(code)
        print("{}数据处理完成".format(code))

    send_sms(msg_text)
    
    print("数据处理完成")
